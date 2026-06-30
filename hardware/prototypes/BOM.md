# Interceptor_M — Prototype Batch 01 · Bill of Materials

## Product Lines Covered
- **DC** — Civil (MTOW 250 g, reference)
- **DD** — Defense (MTOW 400 g)
- **DI** — Industrial (MTOW 300 g, provisional)

---

## Part Breakdown per Line

| Part ID | Description | Material | Stock | Qty |
|---|---|---|---|---|
| BRK-001 | Structural Junction Bracket | 7075-T651 Al | 80×60×12 mm | 3 (one per line) |
| ACT-001 | Actuator / FC / ESC Mount | 7075-T651 Al | 70×50×9 mm | 3 (identical across lines) |
| NCR-001 | Nose-Cone Interface Ring | 316L SS | bar Ø48 mm | 3 (one per line) |

---

## Mass Summary

| Part ID | DC mass (g) | DD mass (g) | DI mass (g) |
|---|---|---|---|
| BRK-001 | 111.78 | 130.74 | 118.78 |
| ACT-001 | 55.49 | 55.49 | 55.49 |
| NCR-001 | 89.33 | 104.48 | 94.93 |
| **Total per line** | **256.60** | **290.71** | **269.20** |

> **ACT-001 is MTOW-insensitive** — ESC/FC pocket dimensions fixed by E3 integration spec.

---

## Material Specifications

| Material | Specification | Hardness | Notes |
|---|---|---|---|
| 7075-T651 Al | AMS 2770 / ASTM B209 | 86 HRB min | Al-Zn-Mg-Cu alloy; peak strength T6→T651 temper |
| 316L SS | ASTM A276 / A479 | ≤ 217 HB | Low-carbon; excellent corrosion resistance |

---

## Fasteners (prototype assembly kit)

| Specification | Qty | Usage |
|---|---|---|
| M2×0.4 pan head SS316 | 12 | ACT-001 standoff grid |
| M3×0.5 pan head SS316 | 20 | BRK/NCR structural assembly |
| M3×0.5 set screw SS316 | 8 | Motor mount locking |

---

## Process Routes

| Part | Primary | Secondary | Finish |
|---|---|---|---|
| BRK-001 | CNC 3-axis mill (Al) | — | Alodine 1200S + MIL-PRF-23377 epoxy primer |
| ACT-001 | CNC 3-axis mill (Al) | — | same as BRK-001 |
| NCR-001 | Lathe (SS) | CNC mill (flats/taps) | Passivate + bead-blast (Ra ≤ 1.6 µm) |

---

## Reference Documents
- `hardware/prototypes/gen_geometry.py` — parametric generator
- `docs/manufacturing/BRK-001_machining.md`
- `docs/manufacturing/ACT-001_machining.md`
- `docs/manufacturing/NCR-001_machining.md`
- `docs/additive-manufacturing.md` — AM analysis & process selection
