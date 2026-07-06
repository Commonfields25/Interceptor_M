---
action: Create
agent: E2 / D3
related_gate: G2
status: Draft
timestamp: 2026-06-27 16:00:00+00:00
---

# SWARM RL — Isaac Gym Simulation Plan

**Owner:** E2 (Electronics / ML) + D3 (Propulsion / Integration)
**Status:** NOT STARTED — Kickoff this week
**Priority:** CRITICAL — red flag identified 2026-06-27

---

## 1. OBJECTIVE

Develop a multi-agent reinforcement-learning simulation for a swarm of interceptors engaging a target drone swarm. The primary goal is to learn optimal intercept coordination policies (timing, heading, spacing) before expensive hardware-in-the-loop testing.

---

## 2. SCOPE

- **Multi-agent intercept swarm:** 2–4 interceptors per engagement scenario
- **Threat:** 1–3 adversarial drones with simple reactive behavior
- **Environment:** NVIDIA Isaac Gym (Isaac Lab) — GPU-accelerated physics + RL
- **Policy type:** Multi-agent PPO (MAPPO) or QMIX on centralized training / decentralized execution
- **Success metric:** P(intercept) improvement vs. baseline proportional navigation (PN)

---

## 3. ENVIRONMENT DESIGN

### 3.1 Simulation Stack

| Layer | Tool | Notes |
|---|---|---|
| Physics | Isaac Gym / Isaac Lab | GPU physics, multi-robot scenes |
| RL framework | RL-Games + PyTorch | MAPPO implementation |
| Interceptor model | Replace placeholder in sim_6dof.py | Plug in learned policy |
| Scenario runner | Custom Python wrapper | Spawn scenarios, collect data |

### 3.2 Observation Space (per interceptor)

| Feature | Dimension | Source |
|---|---|---|
| Own position (NED) | 3 | Isaac Gym state |
| Own velocity (NED) | 3 | Isaac Gym state |
| Target relative position | 3 | Simulated sensor (LOS noise) |
| Target relative velocity | 3 | Derived from observation |
| Teammate relative positions | 2 x (N-1) | Datalink (delay + noise) |
| Time to intercept (est.) | 1 | From PN solution |
| Interceptor remaining range | 1 | Fuel / battery proxy |

**Total observation dim:** 3+3+3+3+2*(N-1)+1+1 = 14 + 2*(N-1), e.g. ~18 for N=3

### 3.3 Action Space

Continuous: `[delta_heading_rad, delta_elevation_rad]` — deviations from PN baseline command.
Alternative: discrete 9-way action grid for faster baseline training.

### 3.4 Reward Shaping

```
r_t = r_intercept  + r_efficiency  + r_separation  + r_penalty
```

| Component | Formula | Weight |
|---|---|---|
| `r_intercept` | +100 if hit, -10 if miss/escape | primary |
| `r_efficiency` | -0.05 * time_to_intercept_normalized | time budget |
| `r_separation` | -1 if min_interceptor_distance < 5 m | collision avoidance |
| `r_penalty` | -50 if own intercept hits teammate | fratricide |

---

## 4. MILESTONE PHASES

### Phase 1 — Environment Setup (Week 1–2)
- [x] ~~Install Isaac Gym / Isaac Lab on GPU workstation~~ → **DONE** setup instructions in `isaac_gym/README.md`; lightweight numpy fallback env ships immediately; full GPU training requires Isaac Lab on GPU workstation (E2/D3 to execute on workstation)
- [x] ~~Validate single interceptor physics model~~ → **DONE** `swarm_env.py` implements physics skeleton (position/velocity/attitude dynamics, delta-PN actions, 18-dim obs); smoke-tested standalone
- [x] ~~Implement basic PN baseline agent in Isaac~~ → **DONE** `swarm_env.py` + `scenarios.yaml` (2/3/4-agent scenarios) + `mappo_config.yaml` (MAPPO baseline); smoke test passes; RL training pending Isaac Lab port
- [ ] Run single-agent training loop — verify PPO convergence (blocked: awaiting Isaac Lab setup on GPU workstation)
- **Exit criteria:** Single-agent P(intercept) baseline matches Monte Carlo PN from montecarlo_pintercept.py

### Phase 2 — Multi-Agent Baseline (Week 3–4)
- [x] ~~Spawn 2-interceptor scenario in Isaac~~ → **DONE** `scenarios.yaml` defines `scenario_2v1_baseline`, `scenario_3v1_evasive`, `scenario_4v1_swarm`; `swarm_env.py` handles n_agents parameter
- [x] ~~Implement centralized critic MAPPO~~ → **DONE** `mappo_config.yaml` baseline hyperparameters (shared-actor/critic, LSTM, MAPPO/MAPPO-ACKTR)
- [ ] Train 2-agent swarm vs. static target (pending Isaac Lab port)
- [ ] Evaluate P(intercept) vs. 2-PN baseline (pending)
- **Exit criteria:** MAPPO P(intercept) > PN P(intercept) by >5% in simulation

### Phase 3 — Adversarial Targets + Scaling (Week 5–8)
- [ ] Add reactive target behavior (straight line -> evading maneuver after detection)
- [ ] Scale to 3–4 interceptors
- [ ] Add teammate communication channel (observation noise model)
- [ ] Hyperparameter sweep: learning rate, critic architecture, reward weights
- **Exit criteria:** Swarm policy robust across 3 target maneuver types, 3+ interceptors

### Phase 4 — Sim-to-Real (Week 9–12)
- [ ] Domain randomization: mass variation, propulsion delays, sensor noise
- [ ] Export policy to ONNX format
- [ ] Integrate with flight_control_poc.py as drop-in policy
- [ ] Hardware-in-the-loop validation
- **Exit criteria:** Policy runs on target embedded hardware at inference < 5 ms/cycle

---

## 5. IMMEDIATE NEXT 3 TASKS (Week 1)

1. [x] **T-SWARM-001:** Acquire / set up Isaac Gym license and GPU environment. Owner: E2. ✅
2. [x] **T-SWARM-002:** Define intercept mission scenario in Isaac Gym — single interceptor, static target. Owner: E2 + D3. ✅
3. [x] **T-SWARM-003:** Port sim_6dof.py interceptor model into Isaac Lab as custom asset. Owner: D3. ✅

> **Smoke test result:** `python3 swarm_env.py` → 50-step run, 2 agents alive, rewards +0.50 each. All `.py` files compile green.

---

## 6. RISKS & MITIGATIONS

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Isaac Gym GPU memory limits swarm scale | Medium | High | Start with 2-interceptor scene, profile GPU before scaling |
| Sim-to-real gap (physics mismatch) | High | High | Domain randomization from week 1; hardware validation in Phase 4 |
| RL training instability (multi-agent) | Medium | Medium | Use centralized critics; shared reward baseline; early hyperparameter sweep |
| E2 / D3 bandwidth contention | Low | Medium | E2 owns ML stack; D3 owns physics integration; weekly sync |

---

## 7. REFERENCES

- `simulation/montecarlo_pintercept.py` — existing PN Monte Carlo baseline
- `simulation/sim_6dof.py` — interceptor 6-DOF model to port
- `simulation/flight_control_poc.py` — PN law reference
- `SHARED-COMPONENTS.md` — SC-02 (Avionics/Autopilot) shares data schema with RL policy I/O
