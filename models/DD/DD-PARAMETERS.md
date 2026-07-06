---
agent: D3
action: Update
timestamp: 2026-07-06T21:00:00Z
related_gate: G2
status: Validated
---

# DD — CAD Parameters & Specifications
**Version:** 1.2.0 | **Owner:** D3 (Defense / CAD)
**Projet:** Interceptor_M — Defense Line (DD)
**Gate:** G2 | **MTOW:** 400 g | **Length:** 380 mm

---

## 1. Reference Geometry

| Parameter | Value | Source |
|---|---|---|
| Fuselage outer diameter | 35 mm | PARAMETERS.json |
| Overall airframe length | 380 mm | D1 specification |
| Tube launcher bore (int. diameter) | 40 mm | PARAMETERS.json |
| Wall thickness | 2.0 mm | FEA baseline |
| Wings (4x delta) | span 150 mm, chord 60 mm | D2 aerodynamics |
| Cruciform empennage (4x) | span 75 mm, chord 40 mm | D2 aerodynamics |
| Nose ogive | Tangent, L/D = 3.5 | D2 aerodynamics |

## 2. Design Constraints

- [x] Target weight: MTOW = 400 g (tube diameter 35 mm x length 380 mm)
- [x] Sabot/launcher interface (40 mm bore)
- [x] Motor mount: brushless, 9/12 mm support
- [x] Fasteners: M2 (wings), M3 (motor mount)
- [x] Electronics compartment (E2): volume validated

## 3. Mass Budget Summary (per DD-CONCEPT.md)

| Subsystem | Mass (g) |
|---|---|
| Structure / airframe | 36 |
| Propulsion (motor + ESC) | 75 |
| Avionics (E3) | 28 |
| Electronics tray (E2) | 35 |
| Battery (LiPo 3S) | 72 |
| Fuel (jet-A) | 52 |
| Payload / seeker | 45 |
| Wings + fins | 34 |
| Fasteners / harness | 4 |
| **Total** | **381 g (19g margin to 400g MTOW)** |

## 4. Center of Gravity

- CG from nose tip: ~150 mm (39.5% of 380 mm length) — empty
- CG with fuel: ~158 mm (41.6% of 380 mm) — positive static margin confirmed

## 5. Planned Assembly

```
ROOT_ASSEMBLY
├── AIRFRAME (fuselage + ogive)
├── ELECTRONICS_TRAY (E2)
├── PROPULSION_UNIT (E1)
└── LAUNCHER_INTERFACE (sabot + rings)
```

## 6. CAD Tooling

- Inventor (primary) / SolidWorks (secondary)

## 7. G2 Deliverables

- [x] ROOT_ASSEMBLY_v0.1.iam
- [x] AIRFRAME_PART.F3D (or .SLDPRT)
- [x] BOM (Bill of Materials)
- [x] DD-PARAMETERS-v1.2.0.md (this document)

---
*Validated against Operation Stabilize baseline.*
*Updated 2026-07-06: v0.3 → v1.2.0 — MTOW and length aligned per DD-400 program (400g Electric/Pneumatic).*
