# Octave / MATLAB Simulation & Constraint Tests

> E3 — engineering/simulation/ | Version 1.0 | 2026-06-30
> Compatible with GNU Octave 8.x+ and MATLAB R2023b+

---

## 1. Overview

This directory contains Octave/MATLAB-compatible `.m` scripts for thermal and aerodynamic simulation, plus an automated constraint test runner.

**Files**

| File | Description |
|---|---|
| `scripts/thermal_transient_pcb.m` | 60s transient PCB thermal (lumped RC ODE) |
| `scripts/aeroload_proxy.m` | Lift / Drag / Moment proxy (DATCOM-style) |
| `scripts/plot_results.m` | Generate 2D figures (PDF) |
| `tests/constraint_test_runner.m` | Automated PASS/FAIL constraint checks |

---

## 2. Requirements

| Environment | Version | Notes |
|---|---|---|
| GNU Octave | ≥ 8.x | Preferred (free). Install via `apt install octave` |
| MATLAB | ≥ R2023b | Use `--batch` mode or live editor |

No proprietary toolboxes required — all scripts use core MATLAB/Octave functions only.

---

## 3. Running in GNU Octave

### Option A — Interactive REPL
```bash
cd engineering/simulation/
octave --no-gui
```

Then inside Octave:
```matlab
addpath scripts tests

% Run thermal simulation
[t, T, s] = thermal_transient_pcb();

% Run aeroload proxy
[CL, CD, CM, sa] = aeroload_proxy(5, 0.8);

% Run all constraint tests
[results, ok] = constraint_test_runner('all');

% Generate plots
plot_results('all');
```

### Option B — Batch mode (no GUI)
```bash
octave --no-gui --eval "
  addpath('scripts','tests');
  [t,T,s] = thermal_transient_pcb();
  [CL,CD,CM] = aeroload_proxy(0, 0.8);
  [r,ok] = constraint_test_runner('all');
  plot_results('all');
  exit;
"
```

PDF figures are saved to the current working directory.

---

## 4. Running in MATLAB

### Live Editor / Interactive
```matlab
addpath(genpath('engineering/simulation'));
[t, T, s] = thermal_transient_pcb();
[CL, CD, CM, sa] = aeroload_proxy(5, 0.8);
[r, ok] = constraint_test_runner('all');
plot_results('all');
```

### Batch mode
```bash
matlab -batch "addpath('scripts','tests'); [r,ok]=constraint_test_runner('all'); exit"
```

### Optional toolboxes (falls back gracefully if unavailable)
- **Signal Processing Toolbox** → not required (no filters used)
- **Optimization Toolbox** → not required
- **Aerospace Toolbox** → not required

---

## 5. Test Descriptions

| Test ID | Category | Description | Threshold |
|---|---|---|---|
| THERM-001 | Thermal | Junction T < 100°C (60s) | < 100 °C |
| THERM-002 | Thermal | T at 30s < 80°C (warning) | < 80 °C |
| THERM-003 | Thermal | With heatsink: T < 85°C | < 85 °C |
| AERO-05..14 | Aero | Positive lift across ±5° AoA | CL > 0 |
| AERO-CLMAX | Aero | CL_max below stall realism | < 2.0 |
| AERO-CD-M15 | Aero | Drag at M=1.5 | < 0.15 |
| MASS-001 | Mass | Thermal penalty < 2% MTOW | < 8 g |

---

## 6. Output Interpretation

```
*** CONSTRAINT TEST RUNNER — E3 / engineering/simulation/ ***
  Namespace : engineering/simulation/
  OK       : All file operations restricted to E3 namespace

============================================================
               CONSTRAINT TEST RESULTS
============================================================
ID          Category     Result     Description
------------------------------------------------------------
THERM-001   Thermal      PASS       Junction temperature < 100°C
THERM-002   Thermal      PASS       Warning threshold at 30s
AERO-00005  Aerodynamic  PASS       CL at alpha=-5°
...
------------------------------------------------------------
  Total : 8 PASS  /  0 FAIL  /  8 TOTAL
============================================================
  OVERALL  : **ALL CONSTRAINTS SATISFIED — PASS**
============================================================
```

---

## 7. Governing Standards

- `governance/rules.md` v1.2 — E3 delegated gates (G5 simulation GO)
- `PARAMETERS.json` v1.0.2 — DD/DI/DC platform parameters
- `engineering/simulation/E3-THERMAL-SIMULATION.md` — thermal baseline
- `engineering/simulation/E3-AVIONICS-PLAN.md` — avionics/HIL protocol

---

*E3 — All scripts restricted to engineering/simulation/ namespace*
