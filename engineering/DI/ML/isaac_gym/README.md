---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# Swarm RL — Isaac Gym / Isaac Lab Setup

## Overview

This directory contains the multi-agent intercept environment for the Interceptor-M Swarm RL project.
The environment is built on **Isaac Gym** (preview release or newer) or **Isaac Lab** (preferred for RL research)
and uses **PyTorch MAPPO** (Multi-Agent Proximal Policy Optimization) as the baseline RL algorithm.

---

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU       | NVIDIA RTX 3080 (10 GB VRAM) | NVIDIA RTX 4090 / A100 (24 GB) |
| CPU       | 8 cores                      | 16+ cores                      |
| RAM       | 32 GB                         | 64 GB                          |
| OS        | Ubuntu 20.04 / 22.04         | Ubuntu 22.04                   |

---

## Software Dependencies

### Core
- **Python 3.8–3.10**
- **PyTorch 1.12+** — `pip install torch torchvision torchaudio`
- **NVIDIA GPU driver** 525+ with CUDA 11.7+

### Isaac Gym / Isaac Lab (choose one)

#### Option A — Isaac Lab (recommended, Isaac Gym preview release)
```bash
# 1. Clone Isaac Lab
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab

# 2. Install dependencies
./scripts/setup/deps.sh

# 3. Install Isaac Lab (editable)
pip install -e .

# 4. Verify installation
python scripts/rl_games/play.py --task Isaac_Reach_Joint --num_envs 32
```

#### Option B — Isaac Gym Preview 3 (legacy)
```bash
# 1. Download Isaac Gym from NVIDIA's website (requires login)
#    https://developer.nvidia.com/isaac-gym

# 2. Extract and install
tar -xzf isaacgympython3.tar.gz
cd isaacgym/python
pip install -e .

# 3. Test
python examples/1080_balls.py
```

### MAPPO Implementation
```bash
# 1. Install MAPPO dependencies
pip install git+https://github.com/marlbenchmark/pymarl.git
# Or use the standalone implementation:
git clone https://github.com/oxwhirl/pymarl.git && cd pymarl && pip install -e .
```

### Project-specific dependencies
```bash
pip install numpy pyyaml gym matplotlib scipy
```

---

## Directory Structure

```
isaac_gym/
├── README.md             ← this file
├── swarm_env.py          ← multi-agent intercept Gym environment
├── scenarios.yaml        ← scenario definitions (2-4 interceptors)
├── mappo_config.yaml     ← MAPPO hyperparameter baseline
└── training/             ← (future) training scripts
    └── train_mappo.py
```

---

## Quick Start — Smoke Test (no Isaac Gym required)

The `swarm_env.py` environment includes a lightweight numpy fallback so it can be tested
without Isaac Gym installed:

```bash
cd engineering/ML/isaac_gym
python swarm_env.py

# Expected output: random rollout of 50 steps with per-step reward print
```

---

## Full Training Run (requires Isaac Gym / Isaac Lab)

```bash
# 1. Set environment variables
export ISAAC_GYM_PATH=/path/to/isaacgym
export MPLBACKEND= Agg   # headless rendering

# 2. Run training
python training/train_mappo.py --config mappo_config.yaml --scenario scenarios.yaml
```

---

## Environment API Summary

| Method | Description |
|--------|-------------|
| `reset()` | Reset all agents; returns dict of observations |
| `step(actions)` | Apply actions; returns observations, rewards, done, info |
| `observation_space` | `gym.spaces.Box(low=-inf, high=inf, shape=(18,))` per agent |
| `action_space` | `gym.spaces.Box(low=-1, high=1, shape=(3,))` per agent (delta-PN) |
| `render()` | (stub) Visualize current state |

---

## Key Reference Docs

- Isaac Lab Docs: https://isaac-sim.github.io/IsaacLab/main/
- MAPPO Paper: Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments (NeurIPS 2020)
- SWARM-RL-PLAN.md: parent plan for this bootstrap (../SWARM-RL-PLAN.md)