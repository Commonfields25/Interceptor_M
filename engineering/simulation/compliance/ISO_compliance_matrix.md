---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# ISO Compliance Matrix — Simulation Namespace

## Document Control

| Field | Value |
|---|---|
| Control ref | IS-MATRIX-SIM-004 |
| Owner | Engineering / Simulation Team |
| Last updated | 2026-06-30 |
| Classification | Internal |

---

## 1. Overview

This matrix maps every simulation script and test artifact to the relevant ISO clauses from:

- **ISO 9001:2015** — Quality management systems
- **ISO 27001:2022** — Information security
- **ISO 15288:2023** — Systems engineering — System lifecycle processes

---

## 2. Script-to-Clause Matrix

| Script / File | ISO 9001 Clauses | ISO 27001 Clauses | ISO 15288 Clauses |
|---|---|---|---|
| `scripts/thermal_transient_pcb.m` | §7.5.1, §7.5.3, §8.5.1 | §A.8.2, §A.8.3 | §6.4, §6.6, §6.7 |
| `scripts/aeroload_proxy.m` | §7.5.1, §7.5.3, §8.5.1 | §A.8.2, §A.8.3 | §6.4, §6.6, §6.7 |
| `scripts/plot_results.m` | §7.5.1, §7.5.3 | §A.8.2 | §6.6, §6.7 |
| `tests/constraint_test_runner.m` | §7.5.1, §7.5.2, §8.5.1 | §A.8.2, §A.9.1 | §6.4, §6.6, §6.7, §6.8 |
| `E3-THERMAL-SIMULATION.md` | §7.5.1, §7.5.2, §7.5.3 | §A.8.2 | §6.4, §6.5 |
| `E3-AVIONICS-PLAN.md` | §7.5.1, §7.5.2, §7.5.3 | §A.8.2 | §6.4, §6.5 |
| `README_TESTS.md` | §7.5.1, §8.5.1 | §A.8.2 | §6.4, §6.8 |
| `.github/workflows/octave-sim-ci.yml` | §8.5.1, §9.1.1 | §A.9.1, §A.9.4, §A.12.1 | §6.7, §7.1 |
| `compliance/ISO9001_traceability.md` | All §7.5 clauses | §A.8.2, §A.8.3 | §6.4, §7.1 |
| `compliance/ISO27001_security.md` | §7.5.1 | §A.8.2, §A.8.3, §A.9.1–§A.9.4 | §6.5 |
| `compliance/ISO15288_process.md` | §7.5.1 | §A.8.2 | §6.3–§6.8, §7.1 |
| `compliance/README.md` (this folder) | §7.5.1, §8.5.1 | §A.8.2 | §6.4, §6.8 |

---

## 3. ISO 9001:2015 Clause Detail

| Clause | Requirement | Simulation Application | Status |
|---|---|---|---|
| §7.5.1a | Document identification | Header in every `.m` file (name, rev, date, author) | ✅ |
| §7.5.1b | Revision status | Git history + branch naming convention | ✅ |
| §7.5.2b | Approval | PR review before merge | ✅ |
| §7.5.3 | Control of changes | Changes tracked in Git; diffs reviewed in PR | ✅ |
| §7.5.4 | Retention | CI logs retained min. 3 years (product lifecycle + 1 yr) | ✅ |
| §8.5.1 | Control of production / service provision | Simulation runs as a validated process; exit codes used | ✅ |
| §9.1.1 | Monitoring and measurement | CI monitors test results; PASS/FIL per run | ✅ |

---

## 4. ISO 27001:2022 Clause Detail

| Clause | Requirement | Simulation Application | Status |
|---|---|---|---|
| §A.8.2 | Information classification | All simulation assets classified as Internal | ✅ |
| §A.8.3 | Information handling | Scripts reviewed; no secrets or PII embedded | ✅ |
| §A.9.1 | Access control policy | Branch protection + at least 1 approving review | ✅ |
| §A.9.2 | User registration | GitHub team membership management | ✅ |
| §A.9.4 | Password-less authentication | PAT / GHA token via stdin only; no hardcoded secrets | ✅ |
| §A.12.1 | Operational procedures | CI runbook defined in workflow YAML | ✅ |

---

## 5. ISO 15288:2023 Clause Detail

| Clause | Requirement | Simulation Application | Status |
|---|---|---|---|
| §6.3 | Stakeholder needs & requirements | REQ-* requirements in traceability doc | ✅ |
| §6.4 | System requirements definition | REQ-* mapped to scripts | ✅ |
| §6.5 | System architectural design | Modular script architecture (see §2.3 of ISO15288_process.md) | ✅ |
| §6.6 | System implementation | MATLAB/Octave compatible scripts; SI units | ✅ |
| §6.7 | System verification | Automated Octave CI + MATLAB manual validation | ✅ |
| §6.8 | System validation | REQ-* thresholds checked by `constraint_test_runner.m` | ✅ |
| §7.1 | Configuration management | Git-controlled baseline; PR + review gate | ✅ |

---

## 6. Verification Checklist

| Check | Method | Owner | Frequency |
|---|---|---|---|
| All `.m` scripts run on GNU Octave 8.x+ | CI workflow | CI | Every push/PR |
| All `.m` scripts run on MATLAB R2023b+ | Manual run | Operator | Per release |
| Requirements traceability updated | Review in PR | Lead Eng | Per change |
| ISO docs current | Review in PR | Compliance | Annual |
| No secrets in simulation namespace | Code review + grep scan | All contributors | Per PR |
| CI artifacts archived | GitHub Actions | CI | Every run |

---

## 7. Revision History

| Rev | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2026-06-30 | E3 Simulation Team | Initial matrix |
