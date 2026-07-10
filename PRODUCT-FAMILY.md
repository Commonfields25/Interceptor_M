---
agent: Jules
action: Update
timestamp: 2026-07-05T15:20:33Z
status: Validated
---

# Interceptor_M — Product Family Overview

**Strategy:** Common-platform modular product family
**Version:** 2.0.0 — Parameters synchronized & F1 Line added
**Date:** 2026-07-05

---

## 1. Product Strategy

Shared platform strategy maximises reuse across market segments while preserving line-specific differentiation in airframe scale and propulsion.

| Dimension | Benefit |
|-----------|---------|
| Non-recurring engineering (NRE) | ~40 % vs independent designs |
| Component supply chain | Single source, volume pricing |
| Software / mission stack | Universal across all lines |

---

## 2. Product Lines

| Line | Market         | Priority | MTOW (g) | Fuselage L x Dia (mm) | Wing Span (m) | Wall (mm) | Status |
|------|----------------|----------|----------|-----------------------|---------------|-----------|--------|
| DD   | Defense        | High     | 400.0    | 380.0 x 35.0          | 0.150         | 3.0       | Active |
| DI   | Industrial     | High     | 300.0    | 365.0 x 35.0          | 0.135         | 1.8       | Locked |
| DC   | Civil          | Medium   | 250.0    | 350.0 x 35.0          | 0.120         | 1.5       | Active |
| F1   | High-Speed     | Research | 450.0    | 400.0 x 40.0          | N/A (Quad)    | 3.0       | Concept|

> **F1-Chaser:** High-speed interceptor utilizing a 4-propeller rocket-shaped airframe for chasing F1-class speed targets.

---

## 3. Module Architecture Matrix

| Module                  | DD | DI | DC | F1 | Shared across |
|-------------------------|----|----|----|----|---------------|
| Autopilot / FC board    | yes| yes| yes| yes| **All lines** |
| Propulsion brick        | yes| yes| yes| yes| **All lines** |
| Datalink / RF modem     | yes| yes| yes| yes| **All lines** |
| Launcher interface      | yes| yes| -- | yes| DD + DI + F1  |
| Folding Mechanism       | yes| yes| yes| -- | Winged lines  |

---

## 4. Governance Rule: SPEC LOCK
As of version 2.0.0, the MTOW and dimensions for DD, DI, DC, and F1 are **locked**.

