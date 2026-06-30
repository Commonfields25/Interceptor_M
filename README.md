---
project: Interceptor_M
description: Modular Swarm Drone Interceptor System
version: 1.1
status: Active
date: 2026-06-28
---

# Interceptor_M

**Modular Swarm Drone Interceptor System**

[![Pylint](https://github.com/Commonfields25/Interceptor_M/actions/workflows/pylint.yml/badge.svg)](https://github.com/Commonfields25/Interceptor_M/actions/workflows/pylint.yml)
[![Python CI](https://github.com/Commonfields25/Interceptor_M/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Commonfields25/Interceptor_M/actions/workflows/python-ci.yml)
[![Node 24 Validation](https://github.com/Commonfields25/Interceptor_M/actions/workflows/node24-validation.yml/badge.svg)](https://github.com/Commonfields25/Interceptor_M/actions/workflows/node24-validation.yml)

A three-line family of tube-launched interceptor drones (DD / DI / DC) sharing a common platform. Designed for autonomous and semi-autonomous point-defense, infrastructure protection, and civil drone management.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Project Status: Active](https://img.shields.io/badge/Status-Active-green.svg)](#)
[![Gate: G1 RATIFIED](https://img.shields.io/badge/Gate-G1%20RATIFIED-blue.svg)](#)

---

## Overview

### What is Interceptor_M?

Interceptor_M is a modular, multi-role drone interceptor platform targeting three distinct market segments. Its primary mission is autonomous or human-in-the-loop neutralisation of adversarial unmanned aerial systems (UAS) in contested, GPS-denied environments.

**The problem solved:** Counter-UAS / C-UAS systems must be fast-deployable, cost-effective per engagement, and scalable from infantry-portable (DD) to fixed-infrastructure (DI) to civil airworthiness (DC). Interceptor_M addresses this with a common platform strategy that shares avionics, propulsion, datalink, and software across all three lines.

### Product Lines

| Line | Market | MTOW | Length | Payload | Status |
|------|--------|------|--------|---------|--------|
| **DD** | Defense / NATO C-UAS / SHORAD | 400 g | 380 mm | Warhead + multi-mode seeker | G2 in progress |
| **DI** | Industrial / critical infrastructure | TBD | TBD | Neutralisation payload (TBD) | Concept |
| **DC** | Civil / photography, delivery, agriculture | 250 g | TBD | RGB / multispectral camera | Concept |

*DD specs locked per DEC-007. DI/DC specs pending market study and NDC development.*

---

## Architecture

Interceptor_M uses a **common-platform modular architecture**. All three lines share the same core building blocks, differentiating only at the airframe scale and payload level.

### Shared Platform Components (SC-01 to SC-06)

| ID | Component | Owner | TRL | Lines |
|----|-----------|-------|-----|-------|
| SC-01 | Autopilot / Flight Controller Board (IMU + baro + MCU) | E3 | 4-5 | DD, DI, DC |
| SC-02 | Propulsion Brick (Motor + ESC assembly) | E1 / D1 | 4 | DD, DI, DC |
| SC-03 | Datalink / RF Modem (UHF or S-band) | E2 | 4 | DD, DI, DC |
| SC-04 | Mission Software Stack (flight control + GCS + nav) | E3 | 4-5 | DD, DI, DC |
| SC-05 | Ground Control Station (GCS) | E3 | 3 | DD, DI, DC |
| SC-06 | Launcher Interface (Sabot + Ring Set, 40 mm tube) | D3 | 4 | DD, DI |

Full registry: [`SHARED-COMPONENTS.md`](./SHARED-COMPONENTS.md)

**Line-specific modules:**
- **DD airframe:** 35 mm OD x 380 mm L, delta wings + cruciform fins, tube-launched
- **DI airframe:** Derived from DD, enlarged volume, industrial temp range (-40 to +85 degC)
- **DC airframe:** Lighter/smaller, simplified folding wing, civil airworthiness target

Full architecture: [`PRODUCT-FAMILY.md`](./PRODUCT-FAMILY.md)

---

## ML / Swarm RL

Multi-agent reinforcement learning for swarm coordination in intercept scenarios.

**Stack:** NVIDIA Isaac Gym / Isaac Lab + PyTorch MAPPO

| Phase | Description | Timeline |
|-------|-------------|----------|
| Phase 1 | Environment setup + single-agent PN baseline | Week 1-2 |
| Phase 2 | Multi-agent MAPPO vs. static target | Week 3-4 |
| Phase 3 | Adversarial targets + scaling to 3-4 interceptors | Week 5-8 |
| Phase 4 | Sim-to-real, ONNX export, hardware-in-the-loop | Week 9-12 |

**Owner:** E2 (Electronics / ML) + D3 (Propulsion / Integration)

Reference: [`engineering/ML/SWARM-RL-PLAN.md`](./engineering/ML/SWARM-RL-PLAN.md)

Smoke test: `python simulation/sim_6dof.py` (standalone 6-DOF model)
Isaac Gym env: `isaac_gym/swarm_env.py` (multi-agent intercept, gym API)

---

## Repository Structure

```
Interceptor_M/
|-- BOT_GUIDELINES.md            # AI agent interaction rules + namespace isolation
|-- PARAMETERS.json              # Shared + per-line parameters (DD, DI, DC)
|-- PRODUCT-FAMILY.md            # Product line matrix
|-- SHARED-COMPONENTS.md         # Shared component registry (SC-01 à SC-06)
|--
|-- agents/                      # Per-agent workspaces (D1/D2/D3, E1/E2/E3, AM)
|    |-- agent_manager/          # AM workspace: DECISION_LOG, TEAM_UPDATE
|    |-- D1/, D2/, D3/           # Design engineers
|    |-- E1/, E2/, E3/           # Systems / Electronics / Integration
|--
|-- Base_Launcher_Pieces/        # CAD base launcher parts
|--
|-- ci-templates/                # Canonical workflow templates
|    |-- workflows/             # CI templates (replicated in .github/workflows/)
|         |-- governance.yml    # Governance check workflow
|         |-- metrics.yml       # Project metrics
|         |-- pr-triage.yml     # PR triage automation
|         |-- python-ci.yml     # Python CI template
|         |-- docs-lint.yml     # Documentation lint
|         |-- node24-validation.yml  # Node 24 validation
|--
|-- .github/workflows/          # Active CI/CD workflows (live copies)
|    |-- pylint.yml             # Linting (specific files, multi-version)
|    |-- python-ci.yml          # Python CI
|    |-- node24-validation.yml  # Node 24 validation
|    |-- docs-lint.yml          # Docs lint
|    |-- build-provenance.yml   # Build provenance attestation
|    |-- ci-cd-secrets-demo.yml # Secrets management demo
|--
|-- docs/                        # Design documentation
|    |-- D2_aerodynamics.md
|    |-- D3_structure.md
|    |-- E2_electronics.md
|    |-- E3_integration.md
|    |-- consolidated_definition.md
|    |-- governance/            # Governance docs (cf. governance/ )
|    |    |-- MECHANICAL_DEV_APPROVAL.md  # Mechanical dev approval chain
|    |-- manufacturing/        # Manufacturing docs
|--
|-- engineering/                 # Engineering deliverables
|    |-- CFD/                   # Aerodynamics (CFD-PLAN.md)
|    |-- DC/                    # DC line deliverables
|    |-- DI/                    # DI line deliverables
|    |-- FEA/                   # Structural analysis (FEA-PLAN.md)
|    |-- ML/                    # ML / Swarm RL (SWARM-RL-PLAN.md)
|    |-- simulation/            # Simulation: 6-DOF, PN baseline, flight control
|         |-- sim_6dof.py       # Interceptor 6-DOF model
|         |-- montecarlo_pintercept.py  # PN Monte Carlo
|         |-- flight_control_poc.py     # PN law reference
|         |-- constants.py
|         |-- README.md
|         |-- swarm_env.py      # Isaac Gym multi-agent env
|         |-- scenarios.yaml    # Isaac Gym scenarios
|         |-- mappo_config.yaml # MAPPO hyperparameters
|--
|-- governance/                  # Project governance
|    |-- BOT_GUIDELINES.md      # Namespace isolation rules
|    |-- AUTO-APPROVAL-POLICY.md # Threshold-based auto-approval
|    |-- AGENT_MANAGER_RULES.md
|    |-- guidelines.md / rules.md
|    |-- ci_checks/            # CI governance checks
|--
|-- hardware/                    # Hardware / prototypes
|    |-- prototypes/
|--
|-- manufacturing/              # Manufacturing process docs
|--
|-- models/                     # CAD models by product line
|    |-- DD/
|         |-- DD-CONCEPT.md     # DD design concept + mass budget
|         |-- DD-PARAMETERS.md  # DD locked specs (400 g / 380 mm)
|--
|-- scripts/                    # Utility scripts
|--
|-- simulation/                 # Numerical simulation (legacy, same as engineering/simulation/)
|    |-- sim_6dof.py
|    |-- montecarlo_pintercept.py
|    |-- flight_control_poc.py
|    |-- constants.py
|    |-- README.md
|--
|-- LICENSE
```

---

## Governance

Interceptor_M uses a multi-agent governance model with 11 gates (G0-G11). See [`governance/AUTO-APPROVAL-POLICY.md`](./governance/AUTO-APPROVAL-POLICY.md) for details.

### Agent Roles

| Agent | Role |
|-------|------|
| DG | Director General — sole MAJOR gate authority |
| Agent Manager | Day-to-day coordination, MINOR gate auto-approval |
| D1 / D2 / D3 | Design engineers (platform, aerodynamics, propulsion) |
| E1 / E2 / E3 | Systems, Electronics, Integration engineers |
| AC | Amelioration Continue — continuous improvement |

### Gate System

- **MAJOR gates (always DG):** G0, G2, G4, G7, G9, G10, G11
- **MINOR gates (AM auto-approval eligible when KPIs > 90%):** G1, G3, G5, G6, G8

KPI thresholds for auto-approval:
- On-time delivery ≥ 90%
- Peer review coverage ≥ 80%
- Blocker resolution time ≤ 24 h
- Agent utilization ≥ 70%

### Namespace Isolation

Each agent operates within a defined scope. No two agents co-edit the same file in the same cycle. See [`governance/BOT_GUIDELINES.md`](./governance/BOT_GUIDELINES.md) Section 2.1.

### Mechanical Dev Approval

All mechanical D1/D2/D3 deliverables require DG approval. See [`docs/governance/MECHANICAL_DEV_APPROVAL.md`](./docs/governance/MECHANICAL_DEV_APPROVAL.md).

---

## Roadmap / État du projet

### 🔢 Milestones actifs (M5 → M9)

| Milestone | Échéance | Description |
|-----------|----------|-------------|
| **[M5] Branch Cleanup** | 10/07/2026 | Nettoyage branches inactives, politique de gestion des branches |
| **[M6] CI Node24** | 17/07/2026 | Migration CI → Node24, activation workflows |
| **[M7] Product Specs Lock DI** | 24/07/2026 | Finalisation specs DI, verrouillage BOM |
| **[M8] RL Env Hardening** | 14/08/2026 | Renforcement RL env, rebalancing agents |
| **[M9] Recrutement Ing. Conception** | 30/07/2026 | Recrutement ingénieur conception & design industriel |
| **[M1] Swarm RL Foundations** | 31/07/2026 | Physique 6-DOF, MAPPO baseline, 3 scénarios |
| **[M3] Governance & CI** | 15/08/2026 | Namespace isolation, auto-approval audit, CI pipeline |
| **[M2] Product Specs Locked** | 31/08/2026 | Toutes specs DI/DC/DD validées |
| **[M4] First Training Runs** | 30/09/2026 | Entraînement MAPPO GPU, courbes, métriques |

*Voir [`BRANCH_REVIEW.md`](./BRANCH_REVIEW.md) pour l'état détaillé des branches actives.*

### Product Line Roadmap

| Line | Next Milestone | Owner | Gate |
|------|---------------|-------|------|
| DD | NDC CdCF baselined, CFD initiated | E1 / E2 | G2 (target 2026-07-09) |
| DI | Market study + spec definition | E1 + Marketing | DI-NDC |
| DC | Airframe scaling from DD platform | D2 + D3 | DC-spec |

### ML / Swarm RL Roadmap

- **Now:** Environment bootstrap (swarm_env.py running), real 6-DOF dynamics porting (issue #15)
- **Week 2:** MAPPO single-agent training kickoff (issue #16)
- **Week 3-4:** Multi-agent adversarial training
- **Week 9-12:** Sim-to-real + hardware-in-the-loop

Full plan: [`engineering/ML/SWARM-RL-PLAN.md`](./engineering/ML/SWARM-RL-PLAN.md)

---

## Getting Started

### Prerequisites

- Python 3.9+
- NVIDIA Isaac Gym or Isaac Lab (for RL training; see [`engineering/ML/SWARM-RL-PLAN.md`](./engineering/ML/SWARM-RL-PLAN.md))
- PyTorch 2.0+
- git

### Clone

```bash
git clone https://github.com/Commonfields25/Interceptor_M.git
cd Interceptor_M
```

### Quickstart

```bash
# Install core simulation dependencies
pip install numpy scipy matplotlib

# Run the 6-DOF interceptor simulation (proportional navigation, standalone)
python simulation/sim_6dof.py

# Run Monte Carlo PN intercept study
python simulation/montecarlo_pintercept.py

# Run the PN flight-control proof-of-concept
python flight_control_poc.py
```

> **Expected:** `sim_6dof.py` produces a single-intercept run with proportional navigation. `montecarlo_pintercept.py` runs 100+ trials and prints P_k statistics. `flight_control_poc.py` validates the PN law against a head-on target.

**Optional — ML / RL training stack:**

```bash
pip install torch gymnasium PyYAML
# Isaac Gym: follow instructions at isaac sim.nvidia.com
# export ISAAC_GYM_PATH=/path/to/isaac_gym
# python isaac_gym/swarm_env.py
```

### Dependencies

```bash
# Core simulation
pip install numpy scipy matplotlib

# ML / RL training (optional)
pip install torch gymnasium PyYAML

# Isaac Gym (follow NVIDIA instructions at isaac sim.nvidia.com)
# Then:
# export ISAAC_GYM_PATH=/path/to/isaac_gym
```

---

## License

This project is proprietary and confidential. All rights reserved.
See [`LICENSE`](./LICENSE) for licensing terms.

---
## CI Status
- Python CI: active (python-ci.yml, push+PR to main)
- Node 24 Validation: active (node24-validation.yml, push+PR to main)
- Last activation: 2026-06-28 (Vague 3)

### Vague 4-bis (2026-06-29)
- PRs #63/#64/#65 merged to main — CI GREEN ✓
