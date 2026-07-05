# BRK-001 — Structural Junction Bracket — SPEC STUB

**STATUS: PRELIMINARY — source STEP not yet in repo**

## Part Identity

| Field        | Value                                |
|--------------|--------------------------------------|
| Part ID      | BRK-001                              |
| Description  | Structural Junction Bracket          |
| Material     | AlSi10Mg (DMLS)                      |
| Revision     | v2.0 (mass reduction: 135g → 90g)   |
| Owner        | Jules / D1                           |

## Geometric Constraints

| Parameter      | Value       | Ref                          |
|----------------|-------------|------------------------------|
| Main tube OD   | 40mm ±0.1   | params_DD/DI/DC.json         |
| Fuselage OD    | 35mm        | DI_product_specification.md  |
| Arm length     | 75mm        | params_DD                    |
| Hull thickness | 1.5–2.0mm   | DI_product_specification.md  |

## Critical Dimensions & Tolerances

- Tolerance grade: **IT10** (ISO 286)
- Surface finish: **Ra1.6µm** (ISO 1302)
- Mass target: **<90g** (reduced from 135g)
- All dimensions traceable to PARAMETERS.json

## Source STEP

`engineering/DC/BRK-001_v2.0.step`  
*⚠️ NOTE: STEP source file not yet committed to repo — required before DXF/PDF generation.*

## Deliverables

- [ ] `BRK-001_2D.dxf` — 5-view production drawing
- [ ] `BRK-001_2D.pdf` — PDF export with GD&T
- [ ] Mass verification post-pocketing (target <90g)
