"""
swarm_env.py — Multi-Agent Intercept Gym Environment (Swarm RL Bootstrap)

Skeleton stub implementation:
  - Self-contained spaces API (no external gym/gymnasium dependency)
  - 18-dim continuous observation space (relative state vector)
  - 3-dim continuous action space (delta pitch / yaw / thrust)
  - 4-component reward: intercept, efficiency, separation, anti-fratricide
  - Lightweight numpy dynamics — runs standalone (no Isaac Gym needed)
  - Includes random-rollout smoke test in __main__

Author: E2 + D3 (Swarm RL team)
Reference: ../SWARM-RL-PLAN.md §Week-1
"""

from __future__ import annotations

import numpy as np
from typing import Dict, Tuple, Optional, List

# ---------------------------------------------------------------------------
# Minimal gym-like spaces (no external dependency required)
# ---------------------------------------------------------------------------
class Space:
    """Base class for a gym-compatible space."""
    def sample(self, rng: Optional[np.random.Generator] = None) -> np.ndarray:
        raise NotImplementedError
    def contains(self, x: np.ndarray) -> bool:
        raise NotImplementedError

class Box(Space):
    """
    A (possibly unbounded) box in R^n.
    Each dimension is independent and bounded by [low, high].
    """
    def __init__(self, low, high, shape: Tuple[int, ...], dtype=np.float32):
        self.low = np.array(low, dtype=dtype)
        self.high = np.array(high, dtype=dtype)
        self.shape = shape
        self.dtype = dtype
        assert self.low.shape == () or self.low.shape == self.shape
        assert self.high.shape == () or self.high.shape == self.shape

    def sample(self, rng: Optional[np.random.Generator] = None) -> np.ndarray:
        rng = rng or np.random.default_rng()
        # Uniform sample scaled to [low, high]
        return rng.uniform(self.low, self.high, size=self.shape).astype(self.dtype)

    def contains(self, x: np.ndarray) -> bool:
        return (x >= self.low).all() and (x <= self.high).all()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
N_AGENTS_MAX = 4
STATE_DIM = 18          # relative state vector dimension per agent
ACTION_DIM = 3          # delta-PN: [delta_pitch, delta_yaw, delta_thrust]
DT = 0.05               # simulation timestep [s]
MAX_STEPS = 200         # max episode length

# Reward component weights (from SWARM-RL-PLAN.md)
_R_INTERCEPT_SUCCESS = 100.0
_R_INTERCEPT_FAIL    = -10.0
_R_EFFICIENCY        = 0.01
_R_SEPARATION        = 0.1
_R_FRATRICIDE        = -50.0

# Thresholds
_SEPARATION_THRESHOLD = 5.0
_FRATRICIDE_THRESHOLD = 1.0
_INTERCEPT_DISTANCE   = 2.0


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
class SwarmInterceptEnv:
    """
    Multi-agent Gym environment for interceptor swarm control (standalone, no gym dependency).

    Dynamics (numpy fallback — no Isaac Gym required):
      - Each interceptor: position (x,y,z), velocity (vx,vy,vz), attitude (pitch,yaw,roll).
      - Action = [delta_pitch, delta_yaw, delta_thrust] (clipped to [-1, 1]).
      - Velocity updated from attitude + thrust; position from velocity.

    Observation per agent (18 dims):
      [0:3]   relative target position (x,y,z) in world frame
      [3:6]   relative target velocity (stubbed at 0)
      [6:9]   interceptor position (world)
      [9:12]  interceptor velocity (world)
      [12:15] interceptor attitude (pitch, yaw, roll)
      [15]    time-alive normalised
      [16]    fraction of swarm still alive
      [17]    nearest neighbour distance
    """

    metadata = {"render_modes": [], "name": "SwarmIntercept-v0"}

    def __init__(self, n_agents: int = 2, max_steps: int = MAX_STEPS,
                 seed: Optional[int] = None):
        self.n_agents = n_agents
        self.max_steps = max_steps

        self.observation_space = Box(
            low=-np.inf, high=np.inf, shape=(STATE_DIM,), dtype=np.float32)
        self.action_space = Box(
            low=-1.0, high=1.0, shape=(ACTION_DIM,), dtype=np.float32)

        self._rng: Optional[np.random.Generator] = None
        self._step_count = 0

        # State tensors
        self._positions: Optional[np.ndarray] = None
        self._velocities: Optional[np.ndarray] = None
        self._attitudes: Optional[np.ndarray] = None
        self._thrust: Optional[np.ndarray] = None
        self._alive: Optional[np.ndarray] = None
        self._target_pos: Optional[np.ndarray] = None

        if seed is not None:
            self.reset(seed=seed)

    # -------------------------------------------------------------------------
    # gym-compatible API
    # -------------------------------------------------------------------------
    def reset(self, seed: Optional[int] = None,
              options: Optional[Dict] = None) -> Tuple[Dict, Dict]:
        """
        Reset all agents and target.
        Returns (observations, info) — gym-style tuple.
        """
        if seed is not None:
            self._rng = np.random.default_rng(seed)
        elif self._rng is None:
            self._rng = np.random.default_rng()

        self._step_count = 0

        # --- Initialise interceptor states -----------------------------------
        spread = 15.0
        self._positions = np.zeros((self.n_agents, 3), dtype=np.float32)
        for i in range(self.n_agents):
            angle = 2 * np.pi * i / max(self.n_agents, 1)
            self._positions[i] = np.array(
                [spread * np.cos(angle),
                 spread * np.sin(angle),
                 self._rng.uniform(-2.0, 5.0)],
                dtype=np.float32)

        self._velocities = np.zeros((self.n_agents, 3), dtype=np.float32)
        for i in range(self.n_agents):
            speed = self._rng.uniform(20.0, 40.0)
            heading = self._rng.uniform(0, 2 * np.pi)
            self._velocities[i] = np.array(
                [speed * np.cos(heading),
                 speed * np.sin(heading),
                 self._rng.uniform(-5.0, 10.0)],
                dtype=np.float32)

        self._attitudes = np.zeros((self.n_agents, 3), dtype=np.float32)
        self._thrust = np.full(self.n_agents, 0.8, dtype=np.float32)
        self._alive = np.ones(self.n_agents, dtype=np.float32)

        # --- Initialise target ----------------------------------------------
        centroid = np.mean(self._positions, axis=0)
        self._target_pos = centroid + np.array(
            [0.0, 0.0, self._rng.uniform(40.0, 60.0)], dtype=np.float32)

        obs = self._get_observations()
        info = {}
        return obs, info

    def step(self, actions: Dict[int, np.ndarray]
             ) -> Tuple[Dict, np.ndarray, Dict, Dict, Dict]:
        """
        Apply actions, advance simulation by DT seconds.

        actions  : dict {agent_id: np.array(shape=(3,))} — each = [dp, dy, dt]
        Returns  : (observations, rewards, terminations, truncations, info)
        """
        self._step_count += 1

        # --- Apply actions ---------------------------------------------------
        for i in range(self.n_agents):
            if self._alive[i] < 0.5:
                continue

            action = actions.get(i, np.zeros(ACTION_DIM, dtype=np.float32))
            action = np.clip(action, -1.0, 1.0)
            d_pitch, d_yaw, d_thrust = action

            self._attitudes[i, 0] = np.clip(
                self._attitudes[i, 0] + d_pitch * DT, -np.pi / 3, np.pi / 3)
            self._attitudes[i, 1] = np.clip(
                self._attitudes[i, 1] + d_yaw * DT, -np.pi / 2, np.pi / 2)
            self._thrust[i] = np.clip(self._thrust[i] + d_thrust * DT, 0.0, 1.0)

            pitch, yaw = self._attitudes[i, 0], self._attitudes[i, 1]
            speed = 30.0 * self._thrust[i]
            body_vel = np.array([
                speed * np.cos(pitch) * np.cos(yaw),
                speed * np.cos(pitch) * np.sin(yaw),
                -speed * np.sin(pitch)
            ], dtype=np.float32)
            self._velocities[i] = body_vel
            self._positions[i] += self._velocities[i] * DT

        # --- Target drift ---------------------------------------------------
        self._target_pos[0] += 2.0 * DT

        # --- Compute rewards ------------------------------------------------
        rewards = np.zeros(self.n_agents, dtype=np.float32)
        terminations: Dict[int, bool] = {i: False for i in range(self.n_agents)}
        truncations: Dict[int, bool] = {i: False for i in range(self.n_agents)}

        for i in range(self.n_agents):
            if self._alive[i] < 0.5:
                rewards[i] = 0.0
                terminations[i] = True
                continue

            # 1. Intercept reward
            dist_to_target = np.linalg.norm(self._positions[i] - self._target_pos)
            if dist_to_target < _INTERCEPT_DISTANCE:
                rewards[i] += _R_INTERCEPT_SUCCESS
                self._alive[i] = 0.0
                terminations[i] = True
                continue

            # 2. Efficiency reward
            rewards[i] += _R_EFFICIENCY

            # 3. Separation / fratricide check
            for j in range(i + 1, self.n_agents):
                if self._alive[j] < 0.5:
                    continue
                d = np.linalg.norm(self._positions[i] - self._positions[j])
                if d < _FRATRICIDE_THRESHOLD:
                    rewards[i] += _R_FRATRICIDE
                    rewards[j] += _R_FRATRICIDE
                    self._alive[i] = 0.0
                    self._alive[j] = 0.0
                    terminations[i] = True
                    terminations[j] = True
                elif d < _SEPARATION_THRESHOLD:
                    penalty = -_R_SEPARATION * (_SEPARATION_THRESHOLD - d) / _SEPARATION_THRESHOLD
                    rewards[i] += penalty
                    rewards[j] += penalty

        # --- Truncation (episode length limit) -----------------------------
        if self._step_count >= self.max_steps:
            for i in range(self.n_agents):
                truncations[i] = True

        obs = self._get_observations()
        info = {
            "step": self._step_count,
            "n_alive": int(np.sum(self._alive)),
            "global_done": bool(
                np.all(~self._alive.astype(bool)) or any(truncations.values())),
        }
        return obs, rewards, terminations, truncations, info

    # -------------------------------------------------------------------------
    # Observation helper
    # -------------------------------------------------------------------------
    def _get_observations(self) -> Dict[int, np.ndarray]:
        """Return dict of 18-dim observation vectors, one per agent."""
        obs = {}
        for i in range(self.n_agents):
            pos = self._positions[i]
            vel = self._velocities[i]
            att = self._attitudes[i]
            tgt = self._target_pos

            dx, dy, dz = tgt[0] - pos[0], tgt[1] - pos[1], tgt[2] - pos[2]

            nn_dist = 0.0
            nn_val = float('inf')
            for j in range(self.n_agents):
                if i != j and self._alive[j] > 0.5:
                    d = np.linalg.norm(self._positions[i] - self._positions[j])
                    if d < nn_val:
                        nn_val = d
            nn_dist = nn_val if nn_val != float('inf') else 0.0

            vec = np.array([
                dx, dy, dz,                    # [0:3]   relative target pos
                0.0, 0.0, 0.0,                # [3:6]   relative target vel (stub)
                pos[0], pos[1], pos[2],        # [6:9]   interceptor pos
                vel[0], vel[1], vel[2],        # [9:12]  interceptor vel
                att[0], att[1], att[2],        # [12:15] interceptor attitude
                self._step_count / max(self.max_steps, 1),  # [15] time-normalised
                np.sum(self._alive) / max(self.n_agents, 1),  # [16] fraction alive
                nn_dist,                       # [17]    nearest neighbour
            ], dtype=np.float32)
            obs[i] = vec
        return obs

    def render(self):
        """Stub — no rendering in fallback mode."""
        pass


# ---------------------------------------------------------------------------
# Smoke test — random rollout (runs standalone, no gym/gymnasium/isaac required)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Swarm RL env smoke test")
    parser.add_argument("--n-agents", type=int, default=2,
                        help="Number of interceptors (2-4)")
    parser.add_argument("--steps", type=int, default=50,
                        help="Rollout steps")
    parser.add_argument("--seed", type=int, default=42,
                        help="RNG seed")
    args = parser.parse_args()

    n = max(2, min(4, args.n_agents))
    print(f"[SwarmInterceptEnv] Initialising {n}-agent smoke test "
          f"(seed={args.seed}, {args.steps} steps)")
    print("─" * 60)

    env = SwarmInterceptEnv(n_agents=n, max_steps=200, seed=args.seed)
    obs, _ = env.reset(seed=args.seed)

    total_rewards = {i: 0.0 for i in range(n)}
    for step in range(args.steps):
        # Random actions in [-0.5, 0.5]
        actions = {i: (np.random.rand(3) - 0.5) * 1.0 for i in range(n)}
        obs, rewards, terms, truncs, info = env.step(actions)

        for i in range(n):
            total_rewards[i] += rewards[i]

        if step < 5 or step % 10 == 0 or info["global_done"]:
            alive = info["n_alive"]
            r_str = " | ".join([f"a{i}={rewards[i]:+.1f}" for i in range(n)])
            print(f"  step {step:3d} | alive={alive}/{n} | {r_str}")

        if info["global_done"]:
            print(f"\n  [DONE] Episode ended at step {step}")
            break

    print("─" * 60)
    print(f"[Summary] Total rewards over {args.steps} steps:")
    for i in range(n):
        print(f"  agent {i}: {total_rewards[i]:+.2f}")
    print("[OK] Smoke test completed — swarm_env.py executes standalone.")