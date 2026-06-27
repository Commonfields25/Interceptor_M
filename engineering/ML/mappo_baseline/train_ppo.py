"""
MAPPO single-agent baseline — pure-PyTorch PPO + SwarmInterceptEnv.

Issue  : #16
Branch : feat/E2/mappo-baseline
"""

from __future__ import annotations
import os, sys, time, csv, argparse
from datetime import datetime

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# ── Robust import of the real swarm_env ──────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_ENGINEERING_ROOT = os.path.join(_SCRIPT_DIR, "..")
_ISAAC_GYM_ROOT = os.path.join(_ENGINEERING_ROOT, "isaac_gym")

if _ISAAC_GYM_ROOT not in sys.path:
    sys.path.insert(0, _ISAAC_GYM_ROOT)

from swarm_env import SwarmInterceptEnv

# ── Hyperparameters ────────────────────────────────────────────────────────────
ROLLOUT_STEPS   = 128     # steps per batch before PPO update
MINI_BATCH_SIZE = 32
PPO_CLIP        = 0.2
PPO_EPOCHS      = 4
GAE_LAMBDA      = 0.95
GAMMA           = 0.99
VALUE_COEF      = 0.5
ENTROPY_COEF    = 0.01
CLIP_VALUE_LOSS = True
LEARNING_RATE   = 3e-4
WEIGHT_DECAY    = 1e-5

HIDDEN_DIM      = 64
MAX_GRAD_NORM   = 0.5

DEVICE = torch.device("cpu")
OBS_DIM  = 18
ACT_DIM  = 3

LOG_DIR    = os.path.join(_SCRIPT_DIR, "logs")
CKPT_DIR   = os.path.join(_SCRIPT_DIR, "checkpoints")
os.makedirs(LOG_DIR,    exist_ok=True)
os.makedirs(CKPT_DIR,   exist_ok=True)


# ── Environment wrapper (dict → flat arrays for single-agent) ──────────────────
class SingleAgentEnv:
    """Wraps SwarmInterceptEnv(n_agents=1) so it presents a simple
    (obs : np.ndarray, reward : float, done : bool) interface."""

    def __init__(self, seed: int | None = None):
        # Multi-agent env internally; we use only agent 0
        self._env = SwarmInterceptEnv(n_agents=1, max_steps=200, seed=seed)
        self.observation_space = self._env.observation_space
        self.action_space      = self._env.action_space
        self._flat_obs: np.ndarray | None = None

    # ------------------------------------------------------------------ reset --
    def reset(self, seed: int | None = None):
        """Returns (obs, info)."""
        obs_dict, info = self._env.reset(seed=seed)
        self._flat_obs = obs_dict[0].astype(np.float32)
        return self._flat_obs, info

    # ------------------------------------------------------------------ step --
    def step(self, action: np.ndarray):
        """Returns (obs, reward, terminated, truncated, info)."""
        action_dict = {0: action.astype(np.float32)}
        obs_dict, rewards, terminated, truncated, info = self._env.step(action_dict)
        self._flat_obs = obs_dict[0].astype(np.float32)
        done = bool(terminated[0] or truncated[0])
        return self._flat_obs, float(rewards[0]), bool(terminated[0]), bool(truncated[0]), info

    @property
    def sim_time(self):
        return self._env._sim_time


# ── MLP Actor-Critic ───────────────────────────────────────────────────────────
class ActorCritic(nn.Module):
    """Shared-trunk MLP with:
    - Gaussian policy  (mean MLP + learnable log_std)
    - Value head
    """

    def __init__(self, obs_dim: int, act_dim: int, hidden: int = 64):
        super().__init__()
        self.act_dim = act_dim

        self.shared = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.Tanh(),
            nn.Linear(hidden,         hidden), nn.Tanh(),
        )
        self.mean_head = nn.Linear(hidden, act_dim)
        # Learnable log_std, one per action dimension
        self.log_std = nn.Parameter(torch.zeros(act_dim))

        self.value_head = nn.Sequential(
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, 1),
        )

    def forward(self, x: torch.Tensor):
        h = self.shared(x)
        mu  = torch.tanh(self.mean_head(h))          # bounded mean
        std = torch.exp(self.log_std).clamp(1e-4)     # positive std
        val = self.value_head(h).squeeze(-1)         # (B,)
        return mu, std, val

    def act(self, x: torch.Tensor):
        """Sample action under current policy (deterministic for eval)."""
        with torch.no_grad():
            mu, std, _ = self.forward(x)
            dist = torch.distributions.Normal(mu, std)
            return dist.sample()


# ── Storage ─────────────────────────────────────────────────────────────────────
class RolloutStorage:
    """Ring-buffer storage for a single agent."""

    def __init__(self, capacity: int, obs_dim: int, act_dim: int):
        self.capacity = capacity
        self._pos = 0
        self.full = False

        self.obs_buf     = torch.zeros(capacity, obs_dim)
        self.act_buf     = torch.zeros(capacity, act_dim)
        self.reward_buf  = torch.zeros(capacity)
        self.done_buf    = torch.zeros(capacity, dtype=torch.bool)
        self.logp_buf    = torch.zeros(capacity)
        self.value_buf   = torch.zeros(capacity)
        self.returns_buf = torch.zeros(capacity)
        self.adv_buf     = torch.zeros(capacity)

    def add(self, obs, act, reward, done, logp, value):
        self.obs_buf    [self._pos] = obs
        self.act_buf    [self._pos] = act
        self.reward_buf [self._pos] = reward
        self.done_buf   [self._pos] = done
        self.logp_buf   [self._pos] = logp
        self.value_buf  [self._pos] = value
        self._pos = (self._pos + 1) % self.capacity
        if self._pos == 0:
            self.full = True

    def compute_returns(self, last_value: float, gamma: float, gae_lambda: float):
        """GAE + discounted returns."""
        adv = 0.0
        returns = []
        T = self.capacity if self.full else self._pos

        for t in reversed(range(T)):
            mask = 0.0 if self.done_buf[t] else 1.0
            delta = self.reward_buf[t] + gamma * (self.value_buf[t + 1] if t + 1 < T else last_value) * mask - self.value_buf[t]
            adv = delta + gamma * gae_lambda * mask * adv
            self.adv_buf[t] = adv
            returns.insert(0, adv + self.value_buf[t])

        for t in range(T):
            self.returns_buf[t] = returns[t % len(returns)]

    def feed_forward_generator(self, mini_batch_size: int):
        """Yields shuffled mini-batches."""
        size = self.capacity if self.full else self._pos
        indices = torch.randperm(size)
        for start in range(0, size, mini_batch_size):
            end   = min(start + mini_batch_size, size)
            idx   = indices[start:end]
            yield (self.obs_buf[idx], self.act_buf[idx],
                   self.logp_buf[idx], self.adv_buf[idx],
                   self.returns_buf[idx], self.value_buf[idx])


# ── PPO update ─────────────────────────────────────────────────────────────────
def ppo_update(storage: RolloutStorage, policy: ActorCritic, optimizer: optim.Adam,
               ppo_epochs: int, ppo_clip: float, value_coef: float,
               entropy_coef: float, max_grad_norm: float, mini_batch_size: int):
    """Clipped PPO surrogate loss + value loss + entropy bonus."""
    policy.train()
    loss_sum = value_sum = entropy_sum = 0.0

    for _ in range(ppo_epochs):
        for obs_b, act_b, logp_old_b, adv_b, ret_b, val_b in \
                storage.feed_forward_generator(mini_batch_size):

            obs_b   = obs_b.to(DEVICE)
            act_b   = act_b.to(DEVICE)
            logp_old_b = logp_old_b.to(DEVICE)
            adv_b   = (adv_b - adv_b.mean()) / (adv_b.std() + 1e-8)
            adv_b   = adv_b.to(DEVICE)
            ret_b   = ret_b.to(DEVICE)
            val_b   = val_b.to(DEVICE)

            mu, std, val_pred = policy(obs_b)

            # Log-prob of action under current policy
            dist = torch.distributions.Normal(mu, std)
            logp_new = dist.log_prob(act_b).sum(dim=-1)

            # Clipped surrogate ratio
            ratio = torch.exp(logp_new - logp_old_b)
            surr1 = ratio * adv_b
            surr2 = ratio.clamp(1 - ppo_clip, 1 + ppo_clip) * adv_b
            policy_loss = -torch.min(surr1, surr2).mean()

            # Value loss
            clipped_val = val_b + (val_pred - val_b).clamp(-ppo_clip, ppo_clip)
            if CLIP_VALUE_LOSS:
                value_loss = torch.nn.functional.mse_loss(val_pred, ret_b)
            else:
                value_loss = torch.nn.functional.mse_loss(val_pred, ret_b)

            # Entropy bonus
            entropy = dist.entropy().sum(dim=-1).mean()

            loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(policy.parameters(), max_grad_norm)
            optimizer.step()

            loss_sum     += float(policy_loss)
            value_sum    += float(value_loss)
            entropy_sum  += float(entropy)

    n = ppo_epochs
    return {
        "policy_loss":  loss_sum / n,
        "value_loss":   value_sum / n,
        "entropy":      entropy_sum / n,
    }


# ── Training loop ───────────────────────────────────────────────────────────────
def train(env: SingleAgentEnv, policy: ActorCritic, args):
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    optimizer   = optim.Adam(policy.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    storage     = RolloutStorage(ROLLOUT_STEPS, OBS_DIM, ACT_DIM)
    csv_path    = os.path.join(LOG_DIR, "rewards.csv")
    writer      = None

    obs, _ = env.reset(seed=args.seed)

    episode_reward = 0.0
    episode_count  = 0
    ep_rewards_buf = []
    global_step    = 0
    t0             = time.time()

    for update in range(1, args.updates + 1):
        for step in range(ROLLOUT_STEPS):
            with torch.no_grad():
                obs_t   = torch.from_numpy(obs).float().to(DEVICE)
                action  = policy.act(obs_t.unsqueeze(0)).squeeze(0).cpu().numpy()

            obs_next, reward, terminated, truncated, info = env.step(action)

            with torch.no_grad():
                _, _, value = policy(obs_t.unsqueeze(0))
                value = float(value.squeeze(0).cpu())

            storage.add(
                obs     = torch.from_numpy(obs).float(),
                act     = torch.from_numpy(action).float(),
                reward  = float(reward),
                done    = terminated or truncated,
                logp    = 0.0,          # filled in after the fact
                value   = value,
            )

            obs         = obs_next
            episode_reward += reward
            global_step += 1

            if terminated or truncated:
                ep_rewards_buf.append(episode_reward)
                episode_reward = 0.0
                episode_count += 1
                obs, _ = env.reset()

        # ── PPO update ──────────────────────────────────────────────────────────
        last_obs_t  = torch.from_numpy(obs).float().to(DEVICE)
        with torch.no_grad():
            _, _, last_val = policy(last_obs_t.unsqueeze(0))
            last_val = float(last_val.squeeze(0).cpu())

        storage.compute_returns(last_val, GAMMA, GAE_LAMBDA)

        # Re-fill log-prob under current (trained) policy
        obs_b  = storage.obs_buf[:storage.capacity if storage.full else storage._pos].to(DEVICE)
        act_b  = storage.act_buf[:storage.capacity if storage.full else storage._pos].to(DEVICE)
        with torch.no_grad():
            mu_p, std_p, _ = policy(obs_b)
            dist_p = torch.distributions.Normal(mu_p, std_p)
            logp_new = dist_p.log_prob(act_b).sum(dim=-1)
        storage.logp_buf[:storage.capacity if storage.full else storage._pos] = logp_new.cpu()

        stats = ppo_update(storage, policy, optimizer,
                           PPO_EPOCHS, PPO_CLIP, VALUE_COEF, ENTROPY_COEF,
                           MAX_GRAD_NORM, MINI_BATCH_SIZE)

        mean_ep_reward = float(np.mean(ep_rewards_buf[-50:])) if ep_rewards_buf else 0.0
        elapsed = time.time() - t0
        sps     = global_step / elapsed if elapsed > 0 else 0

        # ── CSV logging ─────────────────────────────────────────────────────────
        row = {
            "update":           update,
            "global_step":      global_step,
            "episodes":          episode_count,
            "mean_reward_50ep": round(mean_ep_reward, 4),
            "policy_loss":      round(stats["policy_loss"], 6),
            "value_loss":       round(stats["value_loss"],  6),
            "entropy":          round(stats["entropy"],     6),
            "sps":              round(sps, 1),
            "walltime_s":       round(elapsed, 1),
        }
        f = open(csv_path, "a", newline="")
        w = csv.DictWriter(f, fieldnames=row.keys())
        if writer is None:
            w.writeheader()
            writer = w
        w.writerow(row)
        f.close()

        print(f"[Update {update:4d}] step={global_step:6d}  "
              f"ep={episode_count:3d}  mean_rwd={mean_ep_reward:8.3f}  "
              f"pl={stats['policy_loss']:+.4f}  vl={stats['value_loss']:.4f}  "
              f"H={stats['entropy']:.4f}  sps={sps:.0f}")

        # ── Checkpoint ────────────────────────────────────────────────────────────
        if update % args.save_freq == 0:
            ckpt_path = os.path.join(CKPT_DIR, f"ppo_update{update}.pt")
            torch.save({
                "update":        update,
                "global_step":   global_step,
                "policy_state":  policy.state_dict(),
                "optimizer_state": optimizer.state_dict(),
            }, ckpt_path)

        # Reset storage for next rollout
        storage     = RolloutStorage(ROLLOUT_STEPS, OBS_DIM, ACT_DIM)

    print(f"\n✓ Training done. CSV: {csv_path}")
    return csv_path


# ── Entry point ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--updates",   type=int, default=100,   help="PPO update batches")
    ap.add_argument("--seed",      type=int, default=42)
    ap.add_argument("--save_freq", type=int, default=20)
    args = ap.parse_args()

    env    = SingleAgentEnv(seed=args.seed)
    policy = ActorCritic(OBS_DIM, ACT_DIM, HIDDEN_DIM).to(DEVICE)
    print(f"Device : {DEVICE}")
    print(f"Policy params : {sum(p.numel() for p in policy.parameters()):,}")

    csv_path = train(env, policy, args)

    # Save final checkpoint
    final_ckpt = os.path.join(CKPT_DIR, "ppo_final.pt")
    torch.save({
        "update":       args.updates,
        "policy_state": policy.state_dict(),
    }, final_ckpt)
    print(f"Final checkpoint: {final_ckpt}")
