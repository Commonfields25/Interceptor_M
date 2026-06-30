# Interceptor_M — Simulation Tests (E3 Namespace)

## Overview
Dual-stack (GNU Octave / MATLAB) simulation and constraint verification suite
for the Interceptor_M project. All scripts are syntax-compatible with
**GNU Octave 8.x+** and **MATLAB R2023b+**.

## File Inventory

| File | Purpose | ISO 9001 | ISO 15288 |
|---|---|---|---|
| `run_all_tests.m` | Top-level orchestrator | §9.1 | §5.3.2.6 |
| `scripts/thermal_transient_pcb.m` | Lumped-RC thermal transient, 60 s | §8.5.1 | §5.3.2.4 |
| `scripts/aeroload_proxy.m` | DATCOM-style aero loads DD/DI/DC | §8.5.1 | §5.3.2.4 |
| `scripts/plot_results.m` | Post-processing 2D plots | §8.5.1 | — |
| `tests/constraint_test_runner.m` | Automated PASS/FAIL checks | §9.1 | §5.3.2.6 |
| `compliance/ISO*.md` | ISO clause linkage matrix | All | All |

## Running the Suite

### GNU Octave (8.x+)
```bash
cd engineering/simulation
octave --quiet --no-gui --eval "addpath(pwd); run_all_tests"
# Or individually:
octave --quiet --no-gui --eval "addpath('scripts'); addpath('tests'); run_all_tests"
```

### MATLAB (R2023b+)
```matlab
cd engineering/simulation
addpath(pwd)
addpath('scripts')
addpath('tests')
run_all_tests
% Or in parallel (Parallel Computing Toolbox):
parfor i = 1:3, run_all_tests; end
```

### CI (GitHub Actions — Ubuntu)
The workflow `.github/workflows/octave-sim-ci.yml` runs automatically on every
push to `main`, `develop`, `feat/E3/*`, and `fix/E3/*`.

## Acceptance Criteria

| Test | Metric | Threshold | ISO Clause |
|---|---|---|---|
| THERM-001 | T_junction peak | < 100 °C | ISO9001 §9.1 |
| THERM-002 | T_junction @ 45s | < 80 °C | ISO9001 §9.1 |
| THERM-003 | T_junction (heatsink 8 g) | < 85 °C | ISO9001 §9.1 |
| AERO-CL | Lift coefficient | CL > 0 (non-stall) | ISO9001 §9.1 |
| AERO-CLMAX | CL_max | < 2.0 | ISO9001 §9.1 |
| AERO-CD | Drag coefficient | CD < 0.15 | ISO9001 §9.1 |
| MASS-001 | Heatsink mass penalty | < 2% MTOW | ISO9001 §8.5.1 |
| ISO-001 | Namespace isolation | No E1/E2 cross-refs | ISO15288 §5.3.2.6 |

## ISO Linkage Summary
- **ISO 9001:2015** — §7.5 (doc control), §8.5.1 (process control), §9.1 (monitoring)
- **ISO/IEC 27001:2022** — Annex A §A.8.2, §A.8.25 (secure development)
- **ISO/IEC/IEEE 15288:2023** — §5.3.2 (development stage), §6.4–§6.8

## Namespace Constraint
E3 operates strictly within `engineering/simulation/` (per `governance/NAMESPACE-ISOLATION.md`).
