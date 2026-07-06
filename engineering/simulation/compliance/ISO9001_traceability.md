---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# ISO 9001:2015 — Simulation Requirements Traceability

## Document Control

| Field | Value |
|---|---|
| Standard | ISO 9001:2015 |
| Control ref | IS-9001-SIM-001 |
| Owner | Engineering / Simulation Team |
| Review cycle | Annual or on simulation baseline change |
| Classification | Internal |

---

## 1. Simulation Baseline Overview

The simulation baseline for **Interceptor_M** covers:

- **Thermal transient analysis** of avionics PCB assembly
- **Aerodynamic proxy modeling** for preliminary structural load estimation
- **Automated constraint testing** (DD / DI / DC envelopes)

All simulation scripts reside under `engineering/simulation/`.

---

## 2. Requirements Traceability Matrix

| Req ID | Description | Simulation Item | Pass Criterion | Evidence |
|---|---|---|---|---|
| REQ-THERM-001 | PCB junction temperature ≤ 85 °C (steady-state, no forced airflow) | `thermal_transient_pcb.m` | `T_junction_max <= 85` | Log output, artifact |
| REQ-THERM-002 | Thermal transient recovery < 60 s after duty cycle event | `thermal_transient_pcb.m` | `t_recovery <= 60 s` | Log output, artifact |
| REQ-THERM-003 | Heatsink mass ≤ 8 g (mechanical constraint) | `thermal_transient_pcb.m` | `heatsink_mass <= 8` | Log output |
| REQ-AERO-001 | Lift coefficient estimation within ±5 % of DATCOM reference | `aeroload_proxy.m` | `abs(CL_err) <= 0.05` | Plot, log |
| REQ-AERO-002 | Drag polar generation for DD / DI / DC flight envelopes | `aeroload_proxy.m` | Polar plotted for all 3 domains | PNG artifact |
| REQ-STR-001 | DD envelope: 1.0 g ≤ n ≤ 2.5 g, altitude 0–12 km | `constraint_test_runner.m` | PASS_DD == 1 | Log, exit code |
| REQ-STR-002 | DI envelope: 2.5 g ≤ n ≤ 7.5 g, altitude 0–9 km | `constraint_test_runner.m` | PASS_DI == 1 | Log, exit code |
| REQ-STR-003 | DC envelope: −1.0 g ≤ n ≤ −0.5 g (inverted), altitude 0–6 km | `constraint_test_runner.m` | PASS_DC == 1 | Log, exit code |
| REQ-STR-004 | Isolation verification: no cross-contamination with E1 / E2 | `constraint_test_runner.m` | PASS_ISO == 1 | Log, exit code |

---

## 3. Test Records Policy

### 3.1 Automated Records
- Every CI run on `ubuntu-latest` via `.github/workflows/octave-sim-ci.yml` generates timestamped logs in `engineering/simulation/logs/`.
- Artifacts (plots, logs) are archived for **30 days** via GitHub Actions `actions/upload-artifact@v4`.

### 3.2 Manual Test Records
- For offline validation with MATLAB, record the following in the **test log sheet**:
  - Run ID, date, operator, MATLAB version
  - Output of each script (exact stdout)
  - Pass/Fail determination
  - Signature and date

### 3.3 Nonconformance
- Any test failure (`exit code ≠ 0`) must be logged as a **NCR (Nonconformance Report)** in the project issue tracker.
- Root cause analysis and corrective action required before re-run.

---

## 4. Document Control Requirements (ISO 9001 §7.5)

| Requirement | Implementation |
|---|---|
| §7.5.1a — Identification | All simulation files include a header with revision, date, author |
| §7.5.1b — Revision status | Git tags and branch naming follow `feat(E3)/`, `fix(E3)/` convention |
| §7.5.2b — Approval | Changes approved via PR review before merge |
| §7.5.3 — Control of changes | Changes tracked via Git history; diffs reviewed in PR |
| §7.5.4 — Retention period | Simulation logs retained min. 3 years (or product lifecycle + 1 year) |

---

## 5. Controlled Documents List

| Document | Path | Rev | Owner |
|---|---|---|---|
| Thermal Simulation Baseline | `engineering/simulation/E3-THERMAL-SIMULATION.md` | current | E3 Team |
| Avionics Plan | `engineering/simulation/E3-AVIONICS-PLAN.md` | current | E3 Team |
| Constraint Test Runner | `engineering/simulation/tests/constraint_test_runner.m` | current | E3 Team |
| Thermal Transient PCB | `engineering/simulation/scripts/thermal_transient_pcb.m` | current | E3 Team |
| Aeroload Proxy | `engineering/simulation/scripts/aeroload_proxy.m` | current | E3 Team |
| This document | `compliance/ISO9001_traceability.md` | current | E3 Team |

*Revision history is maintained in Git commit messages.*
