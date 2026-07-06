---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# MAPPO Single-Agent Baseline

**Issue:** #16
**Branch:** `feat/E2/mappo-baseline`
**Status:** In Progress → needs-review

## Overview

Pure-PyTorch single-agent PPO trained against `SwarmInterceptEnv` (n_agents=1).
The interceptor learns to close on and intercept a weaving target using only
body-frame observations.

---

## Environment Spec

### Source
`engineering/ML/isaac_gym/swarm_env.py` → `SwarmInterceptEnv`

### Wrapper
`train_ppo.py` wraps `SwarmInterceptEnv(n_agents=1)` to present a
single-agent `(obs, reward, done)` interface.

### Observation (18 dims, float32, body frame)
| Range | Description |
|-------|-------------|
| [0:3]  | Relative target position (m) — body frame |
| [3:6]  | Relative target velocity (m/s) — body frame |
| [6:9]  | Interceptor position (m) — world frame |
| [9:12] | Interceptor velocity (m/s) — world frame |
| [12:15]| Interceptor Euler angles (roll,pitch,yaw) — rad |
| [15]   | Time-alive normalised [0,1] |
| [16]   | Swarm fraction alive [0,1] |
| [17]   | Nearest-neighbour distance (m) |

### Action (3 dims, continuous, per agent)
| Dim | Description | Range |
|-----|-------------|-------|
| [0] | Thrust fraction | [0, 1] |
| [1] | Body-rate pitch command | [-3, +3] rad/s |
| [2] | Body-rate yaw command   | [-3, +3] rad/s |

### Reward
| Event | Reward |
|-------|--------|
| Intercept (distance < 2 m) | +100 |
| Alive per step | +0.01 |
| Separation penalty (< 5 m) | -0.01×step |
| Fratricide (< 1 m) | -50 |
| Ground hit (z < 0) | -20 |

### Episode
- Max steps: 200 (10 s at dt=0.05)
- Terminates on: intercept, fratricide, or ground hit

---

## Algorithm

| Component | Value |
|-----------|-------|
| Policy | MLP Actor-Critic, shared 64-unit trunk, Gaussian |
| Log-std | Learnable per action dim |
| Rollout length | 128 steps |
| Minibatch size | 32 |
| PPO epochs per update | 4 |
| PPO clip ε | 0.2 |
| GAE λ | 0.95 |
| Discount γ | 0.99 |
| Value loss coefficient | 0.5 |
| Entropy coefficient | 0.01 |
| Optimizer | Adam(lr=3e-4, weight_decay=1e-5) |
| Gradient clip | max norm 0.5 |

---

## Running

```bash
# Default: 100 updates, seed 42
python engineering/ML/mappo_baseline/train_ppo.py --updates 100 --seed 42

# Quick smoke test (20 updates)
python engineering/ML/mappo_baseline/train_ppo.py --updates 20 --seed 42

# Custom save frequency
python engineering/ML/mappo_baseline/train_ppo.py --updates 100 --save_freq 10
```

**Output directory structure:**
```
engineering/ML/mappo_baseline/
├── logs/
│   └── rewards.csv          ← training metrics
├── checkpoints/
│   ├── ppo_updateN.pt       ← periodic checkpoint
│   └── ppo_final.pt         ← final model
└── train_ppo.py
```

---

## CSV Log Fields

| Column | Description |
|--------|-------------|
| `update` | PPO update number |
| `global_step` | Total environment steps |
| `episodes` | Total episodes completed |
| `mean_reward_50ep` | Rolling mean reward over last 50 episodes |
| `policy_loss` | PPO surrogate loss (negative, maximise) |
| `value_loss` | Value function MSE |
| `entropy` | Action distribution entropy |
| `sps` | Steps per second |
| `walltime_s` | Elapsed wall time (s) |

---

## Expected behaviour

- **First few updates:** reward ~0 (random policy, mostly ground hits or timeout)
- **~20–50 updates:** policy learns to thrust and steer toward target; reward climbs to ~10–30
- **~80–100 updates:** reward stabilises; mean rolling reward is the key indicator

---

## Hardware

- **CPU only** (no GPU required)
- RAM: ~100 MB
- Expected wall time for 100 updates: ~3–8 min depending on hardware