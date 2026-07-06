---
action: Planning
agent: E3
related_gate: G2
status: Active
timestamp: 2026-07-01 20:10:00+00:00
---

# 📋 CORRECTIVE BACKLOG: REPOSITORY STABILIZATION

Prioritized list of tasks to resolve inconsistencies identified in the Wave 13 Audit.

## PRIORITY 1: Parameter & Baseline Synchronization (Blocker for CAD)

- [ ] **Task 1.1: Unified Parameter Lock**
    - Merge `PARAMETERS.json` and `simulation/constants.py`.
    - Enforce **L = 380 mm** and **MTOW = 400 g** across all configurations.
- [ ] **Task 1.2: Purge Rocket Legacy**
    - Rewrite `engineering/DI/D1_specifications.json` to remove SRM/HTPB references.
    - Standardize on "Electric Dash / Pneumatic Launch" terminology.
- [ ] **Task 1.3: Discipline Spec Realignment**
    - Update `docs/D2` and `docs/D3` to reflect the 400g airframe (removing Mach 2.2 / [RESOLVED] 2.5kg payload data).

## PRIORITY 2: Governance & Organizational Cleanup

- [ ] **Task 2.1: Agent Namespace Consolidation**
    - Delete redundant folders: `agents/D1_ingenierie`, `agents/E3_integration`, etc.
    - Transfer relevant mission `.json` files to primary agent folders (`agents/D1`, `agents/E3`).
- [ ] **Task 2.2: Protocol Enforcement**
    - Apply IAMD (YAML headers) to all Markdown files in `docs/` and `engineering/`.
    - Centralize all rules into `/governance/`.

## PRIORITY 3: Roadmap & Timeline Alignment

- [ ] **Task 3.1: Prototype Roadmap Update**
    - Align `PROTOTYPE_ROADMAP.md` with the 400g DD baseline.
- [ ] **Task 3.2: Milestone Synchronization**
    - Update `MILESTONE_PLAN.md` to bridge the gap between 2026 prototypes and 2027 certification.

---
*Authorized by Engineering Integration (E3) — 2026-07-01*
