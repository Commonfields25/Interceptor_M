---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# Interceptor_M — Mechanical Prototypes for Machining
**Branch:** `feat/mech/prototypes-machining`
**Status:** Draft — Pending D1/D2/D3 Build & E1 Gate Review
**Governance:** [PR #31 — Mechanical Dev Approval Governance](../governance/MECHANICAL_DEV_APPROVAL.md)
**Related Issues:** [#32](../issues/32) | [#33](../issues/33)

---

## Overview

This package defines the **first batch of machining-ready mechanical prototypes** for the Interceptor_M micro-drone interceptor system. All parts are sized to fit within the Ø40 mm launcher tube envelope and satisfy the 250 g MTOW budget.

### Key Project Parameters (from `PARAMETERS.json`)

| Parameter | Value |
|---|---|
| Launcher tube ID | Ø40 mm |
| Fuselage OD | Ø35 mm |
| Arm length | 75 mm |
| Wing chord | 60 mm |
| Fasteners | M2 / M3 |
| Motor mount | 9 mm / 12 mm |
| MTOW | 250 g |

### Prototype Parts — First Batch

| Part | File | Function | Material | Process |
|---|---|---|---|---|
| **Structural Bracket** | `structural_bracket.md` | Primary airframe junction & motor mount interface | 7075-T6 Aluminum | CNC 3-axis milling |
| **Actuator Mount** | `actuator_mount.md` | ESC / FC / battery tray securing bracket | 7075-T6 Aluminum | CNC 3-axis milling |
| **Nose-Cone Interface Ring** | `nose_cone_ring.md` | Mechanical interface between nose cone & fuselage tube | 316L Stainless Steel | CNC turning (lathe) |

---

## Manufacturing Process Summary

| Process | Used For | Notes |
|---|---|---|
| **CNC Milling (3-axis)** | Bracket, actuator mount | Aluminium 7075-T6 block, Ra 0.8µm finish |
| **CNC Turning** | Nose-cone ring | 316L SS bar stock, Ra 1.6µm finish, bore tolerance ±0.02 mm |
| **Manual finishing** | All parts | Deburr, passivate (SS), anodize (Al — T6) |

---

## Governance & Approval Chain

Per [MECHANICAL_DEV_APPROVAL.md](../governance/MECHANICAL_DEV_APPROVAL.md):

```
D3 (realisation) → D1 (corrections) → E1 (gate review) → D1 (approval sign-off)
```

- **Build:** D3 → D2
- **Structural/Materials review:** E2
- **Final gate:** E1 → D1

---

## Bill of Materials

See `BOM.csv` for full part list, quantities, stock sizes, and lead times.

## Parametric Geometry

See `gen_geometry.py` — generates point geometry and parameter sweeps.
Run: `python gen_geometry.py` → outputs `params.json`

---

*Classification: CONFIDENTIEL — Segment Défense — Commonfields25/Interceptor_M*
