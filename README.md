---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# Interceptor_M — Autonomous Swarm Counter-UAS

**Interceptor_M** is a high-performance, swarm-capable drone interception system designed to neutralize Group 1 and 2 UAS threats. The project utilizes multi-agent reinforcement learning (MAPPO) and high-fidelity 6-DOF physics to achieve autonomous intercepts.

---

## 🚀 Performance Baseline (DD-400)

| Metric | Value | Condition |
|---|---|---|
| **Intercept Speed** | 300 m/s (Mach 0.88) | Full Thrust |
| **MTOW** | 400 g | Defense (DD) Line |
| **Max Load Factor** | 5.9 g | Aero-limited @ 12° AoA |
| **Turn Radius** | 1,559 m | @ 300 m/s |
| **Unified Physics** | 6-DOF Rigid Body | Euler/RK4 Integration |

---

## 🧱 Hardware & CAD

Interceptor_M supports **procedural CAD generation**. STL files for the launcher and airframe can be generated directly from Python scripts using `numpy-stl`.

- **Launcher Parts**: Chassis, Rails, and Locking Mechanisms.
- **Airframe**: Parametric scaling based on product line specs.

See [`docs/CAD_GENERATION.md`](./docs/CAD_GENERATION.md) for generation instructions.

## 🛠️ Product Family

The platform follows a **common-core strategy** across three market lines:
- **DD (Defense)**: 400g MTOW, 380mm Length, tube-launched.
- **DI (Industrial)**: 300g MTOW, optimized for reusability.
- **DC (Civil)**: 250g MTOW, lightweight compact frame.

Detailed Specs: [`PARAMETERS.json`](./PARAMETERS.json) | [`PRODUCT-FAMILY.md`](./PRODUCT-FAMILY.md)

---

## 🧠 AI & Simulation

The interception logic is trained in a customized **Isaac Gym** environment using **MAPPO** (Multi-Agent Proximal Policy Optimization).

- **Physics**: Real-world aerodynamic modeling ($C_x$, $C_{L\alpha}$) and atmospheric density.
- **Training**: Centralized learning with decentralized execution for swarm coordination.
- **Verification**: Cross-verified via MATLAB analytical models.

---

## ⚖️ Governance & Compliance

Operated by a team of parallel AI agents (D1-D3, E1-E3) under a strict 11-gate approval process.
- **Auto-Approval**: Minor gates (G1, G3, G5, G6, G8) are managed autonomously based on performance KPIs.
- **Auditing**: All decisions are logged in the [`GATE_AUDIT_LOG.md`](./agents/agent_manager/gate_packages/GATE_AUDIT_LOG.md).

---

## 🏁 Getting Started

```bash
# Clone the repository
git clone https://github.com/Commonfields25/Interceptor_M.git

# Run Physics Smoke Test
python3 engineering/ML/isaac_gym/swarm_env.py

# Run MAPPO Baseline Training (Burst)
python3 engineering/ML/mappo_baseline/train_ppo.py --updates 10
```

---
*Interceptor_M Engineering Group | Proprietary & Confidential*
