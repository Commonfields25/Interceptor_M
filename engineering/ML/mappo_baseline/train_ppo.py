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
OBS_DIM  = 13
ACT_DIM  = 3

LOG_DIR    = os.path.join(_SCRIPT_DIR, "logs")
CKPT_DIR   = os.path.join(_SCRIPT_DIR, "checkpoints")
os.makedirs(LOG_DIR,    exist_ok=True)
os.makedirs(CKPT_DIR,   exist_ok=True)


# ── Environment wrapper (dict → flat arrays for single-agent) ──────────────────
class SingleAgentEnv:
    def __init__(self, seed: int | None = None):
        self._env = SwarmInterceptEnv(n_agents=1, max_steps=200)
        self.observation_space = self._env.observation_space
        self.action_space      = self._env.action_space
        self._flat_obs: np.ndarray | None = None

    def reset(self, seed: int | None = None):
        obs_dict, info = self._env.reset(seed=seed)
        self._flat_obs = obs_dict[0].astype(np.float32)
        return self._flat_obs, info

    def step(self, action: np.ndarray):
        action_dict = {0: action.astype(np.float32)}
        obs_dict, rewards, terminated, truncated, info = self._env.step(action_dict)
        self._flat_obs = obs_dict[0].astype(np.float32)
        return self._flat_obs, float(rewards[0]), bool(terminated[0]), bool(truncated[0]), info

    @property
    def sim_time(self):
        return self._env._sim_time


# ── MLP Actor-Critic ───────────────────────────────────────────────────────────
class ActorCritic(nn.Module):
    def __init__(self, obs_dim: int, act_dim: int, hidden: int = 64):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.Tanh(),
            nn.Linear(hidden,         hidden), nn.Tanh(),
        )
        self.actor  = nn.Linear(hidden, act_dim)
        self.value  = nn.Linear(hidden, 1)
        self.log_std = nn.Parameter(torch.zeros(act_dim))

    def forward(self, x):
        h = self.shared(x)
        mu = self.actor(h)
        val = self.value(h).squeeze(-1)
        std = torch.exp(self.log_std).expand_as(mu)
        return mu, std, val

    def act(self, x):
        mu, std, _ = self.forward(x)
        dist = torch.distributions.Normal(mu, std)
        return dist.sample()

class RolloutStorage:
    def __init__(self, capacity, obs_dim, act_dim):
        self.capacity = capacity
        self.obs_buf = torch.zeros(capacity, obs_dim)
        self.act_buf = torch.zeros(capacity, act_dim)
        self.reward_buf = torch.zeros(capacity)
        self.done_buf = torch.zeros(capacity, dtype=torch.bool)
        self.logp_buf = torch.zeros(capacity)
        self.value_buf = torch.zeros(capacity)
        self.returns_buf = torch.zeros(capacity)
        self.adv_buf = torch.zeros(capacity)
        self._pos = 0
        self.full = False

    def add(self, obs, act, reward, done, logp, value):
        self.obs_buf[self._pos] = obs
        self.act_buf[self._pos] = act
        self.reward_buf[self._pos] = reward
        self.done_buf[self._pos] = done
        self.logp_buf[self._pos] = logp
        self.value_buf[self._pos] = value
        self._pos = (self._pos + 1) % self.capacity
        if self._pos == 0: self.full = True

    def compute_returns(self, last_value, gamma, gae_lambda):
        adv = 0.0
        T = self.capacity if self.full else self._pos
        for t in reversed(range(T)):
            mask = 0.0 if self.done_buf[t] else 1.0
            delta = self.reward_buf[t] + gamma * (self.value_buf[t + 1] if t + 1 < T else last_value) * mask - self.value_buf[t]
            adv = delta + gamma * gae_lambda * mask * adv
            self.adv_buf[t] = adv
            self.returns_buf[t] = adv + self.value_buf[t]

    def feed_forward_generator(self, mini_batch_size):
        size = self.capacity if self.full else self._pos
        indices = torch.randperm(size)
        for start in range(0, size, mini_batch_size):
            idx = indices[start:start+mini_batch_size]
            yield (self.obs_buf[idx], self.act_buf[idx], self.logp_buf[idx], self.adv_buf[idx], self.returns_buf[idx], self.value_buf[idx])

def ppo_update(storage, policy, optimizer, ppo_epochs, ppo_clip, value_coef, entropy_coef, max_grad_norm, mini_batch_size):
    policy.train()
    for _ in range(ppo_epochs):
        for obs_b, act_b, logp_old_b, adv_b, ret_b, val_b in storage.feed_forward_generator(mini_batch_size):
            mu, std, val_pred = policy(obs_b)
            dist = torch.distributions.Normal(mu, std)
            logp_new = dist.log_prob(act_b).sum(dim=-1)
            ratio = torch.exp(logp_new - logp_old_b)
            surr1 = ratio * adv_b
            surr2 = ratio.clamp(1-ppo_clip, 1+ppo_clip) * adv_b
            policy_loss = -torch.min(surr1, surr2).mean()
            value_loss = torch.nn.functional.mse_loss(val_pred, ret_b)
            entropy = dist.entropy().sum(dim=-1).mean()
            loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(policy.parameters(), max_grad_norm)
            optimizer.step()
    return {"policy_loss": 0, "value_loss": 0, "entropy": 0}

def train(env, policy, args):
    optimizer = optim.Adam(policy.parameters(), lr=LEARNING_RATE)
    storage = RolloutStorage(ROLLOUT_STEPS, OBS_DIM, ACT_DIM)
    obs, _ = env.reset()
    for update in range(1, args.updates + 1):
        for step in range(ROLLOUT_STEPS):
            with torch.no_grad():
                obs_t = torch.from_numpy(obs).float()
                mu, std, val = policy(obs_t.unsqueeze(0))
                dist = torch.distributions.Normal(mu, std)
                action = dist.sample()
                logp = dist.log_prob(action).sum(dim=-1)
            obs_next, reward, term, trunc, info = env.step(action.squeeze(0).numpy())
            storage.add(obs_t, action.squeeze(0), reward, term or trunc, logp.item(), val.item())
            obs = obs_next
            if term or trunc: obs, _ = env.reset()
        with torch.no_grad():
            _, _, last_val = policy(torch.from_numpy(obs).float().unsqueeze(0))
        storage.compute_returns(last_val.item(), GAMMA, GAE_LAMBDA)
        ppo_update(storage, policy, optimizer, PPO_EPOCHS, PPO_CLIP, VALUE_COEF, ENTROPY_COEF, MAX_GRAD_NORM, MINI_BATCH_SIZE)
        print(f"Update {update} complete")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--updates", type=int, default=10)
    args = ap.parse_args()
    env = SingleAgentEnv()
    policy = ActorCritic(OBS_DIM, ACT_DIM, HIDDEN_DIM)
    train(env, policy, args)
