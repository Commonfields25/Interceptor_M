# Interceptor_M Prototype Part Catalog (Wave 17)

This directory contains the parametric definitions and geometry for the **DD-400 (Electric Dash)** prototype.

## Core Component List (Realistic Sizing)

| Part ID | Name | Material | Mass (g) | Notes |
| --- | --- | --- | --- | --- |
| **FUS-001** | Fuselage Tube | Al-7075 T6 | 131.2 | Ø35 x 380 mm (1.2t) |
| **BRK-001** | Structural Bracket | AlSi10Mg | 20.1 | DMLS internal frame |
| **ACT-001** | Actuator Mount | AlSi10Mg | 8.4 | Electronics tray |
| **WNG-001** | Delta Wings (x4) | CFRP | 21.6 | 150mm span |
| **FIN-001** | Tail Fins (x4) | Al-7075 | 8.1 | 75mm span |
| **SAB-001** | Launcher Sabot | PETG | 6.2 | Ø40 OD interface |
| **BATT-01** | 50kJ Battery Pack | LiPo | 90.0 | 3S configuration |
| **MOT-01** | 8N Electric Motor | BLDC | 40.0 | High-KV dash motor |
| **SEEK-01** | Ka-band Seeker | Sub-system | 35.0 | Radar front-end |
| **WHD-01** | Kinetic Warhead | Tungsten | 30.0 | High-density core |
| **TOTAL** | | | **390.6** | **Within 400g Limit** |

## Geometry Generation
Run the following script to regenerate the part data:
```bash
python3 hardware/prototypes/gen_geometry.py
```

## Assembly Verification
Run the following script to verify fit and tolerances:
```bash
python3 hardware/prototypes/verify_assembly.py
```

---
*Authorized by Defense CAD (D3) — 2026-07-02*
