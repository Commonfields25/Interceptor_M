---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# Nose-Cone Interface Ring — Design Specification
**Part ID:** NCR-001 | **Revision:** v0.1-draft
**Machining Process:** CNC Turning (Lathe) + Milling (secondary op)
**Governance ref:** PR #31 / Issue #32

---

## Function

Thrust Interface ring providing the structural and aerodynamic transition between the nose cone (fibreglass/CFRP) and the aluminium fuselage tube (Ø35 mm OD). Houses the O-ring seal groove for pneumatic launcher integrity and provides anti-rotation flats for secure assembly. Subject to launch impulse load (confirmed by E1 NDC — pending).

---

## Material

| Property | Value |
|---|---|
| **Alloy** | 316L Stainless Steel (Low Carbon) |
| **Condition** | Annealed (soft, machineable) |
| **Ultimate Tensile Strength** | ≥ 560 MPa |
| **Yield Strength** | ≥ 290 MPa |
| **Elongation** | ≥ 50% |
| **Corrosion resistance** | Excellent (low carbon = max corrosion resistance) |
| **Stock** | Ø45 mm × 25 mm bar (316L SS, 2B finish) |

> Rationale: 316L SS is required for the O-ring sealing groove — the repeated pneumatic pressure cycles demand a corrosion-resistant, ductile seat material. 316L is more machineable than 316 (lower carbon = less sensitisation). Bar stock ensures consistent bore concentricity.

---

## Key Dimensions

| Dimension | Nominal | Tolerance | GD&T Callout |
|---|---|---|---|
| Overall length | 20.0 mm | ±0.05 mm | — |
| Outer diameter | Ø44.0 mm | ±0.03 mm | — |
| Fuselage interface bore (Ø35 mm ID) | Ø35.0 mm | H7 (ø35.000/+0.025) | Ø35 H7 |
| Nose cone pilot bore | Ø15.0 mm | H8 (ø15.000/+0.027) | Ø15 H8 |
| O-ring groove (OR-112 NBR, 2.62 mm cross-section) | Ø36.5 mm groove Ø, 2.80 mm wide | ±0.05 mm | — |
| Anti-rotation flats (×2, 6 mm wide) | 6.0 mm | ±0.10 mm | Symmetric 180° apart |
| M3 threaded holes (×4, interface to fuselage clamp) | M3 × 0.5 | 4H | Thread perpendicularity ⊥0.05 mm |
| Through-bore for wiring | Ø4.0 mm | H8 | — |

---

## Geometric Tolerances (GD&T)

| Feature | Symbol | Value | Datum |
|---|---|---|---|
| Fuselage bore concentricity (to OD) | — | Ø0.03 mm | OD outer diameter |
| O-ring groove position (axial from face) | Position | ±0.05 mm | A (reference face) |
| Nose-cone bore concentricity | — | Ø0.04 mm | OD |
| Anti-rotation flats position | Position | ±0.10 mm | Centre axis |
| Face squareness (reference face // bore axis) | ⊥ | 0.03 mm/25 mm | Bore axis |
| O-ring groove surface finish | Ra | 0.4 µm | Critical — seal integrity |

---

## Surface Finish

| Zone | Ra | Process |
|---|---|---|
| O-ring groove (seal seat) | 0.4 µm | Diamond turning / fine boring |
| Fuselage bore wall | 0.8 µm | Fine boring + honing |
| Outer diameter | 0.8 µm | Turning finish pass |
| Anti-rotation flats | 3.2 µm | End mill, as machined acceptable |
| Threaded holes (M3) | 0.8 µm | Tap with cutting fluid |
| Through-bore (wiring) | 3.2 µm | Drill + ream |

---

## Manufacturing Process

### Operation 1 — CNC Turning (Lathe)
1. **Blank face:** Face both ends to overall length 20.0 ±0.05 mm
2. **Rough OD:** Turn outer diameter Ø44.5 mm (leaving 0.5 mm stock)
3. **Rough bore:** Bore fuselage ID Ø34.5 mm, pilot bore Ø14.5 mm
4. **Finish bore (Ø35 H7):** Finish-bore to Ø35.000/+0.025 mm, two-pass (rough + finish)
5. **Finish OD:** Finish-turn to Ø44.000 ±0.03 mm
6. **O-ring groove:** Precision groove turn (2.80 mm wide, Ø36.5 mm groove Ø) — check groove width and radial depth with optical comparator
7. **Face parting:** Part off from bar (if applicable)
8. **Passivate:** Nitric acid passivation per ASTM A967 (remove free iron from machining)

### Operation 2 — CNC Milling (Secondary)
1. **Fixture:** Locate on OD with 3-jaw or collet chuck
2. **Anti-rotation flats:** Mill 2× 6 mm wide flats, 180° apart
3. **Drill M3 tapped holes (×4):** Spot-drill, drill Ø2.5 mm, tap M3 × 0.5
4. **Drill through-bore:** Ø4.0 mm H8 (for wiring harness)
5. **Deburr:** Hand deburr, chamfer all bores 0.3 × 45°

---

## O-Ring Specification

| Property | Value |
|---|---|
| **Type** | NBR (Nitrile) O-ring, OR-112 |
| **Cross-section** | 2.62 mm (AS568-112) |
| **Groove Ø** | 36.5 mm (press-fit compression ~20%) |
| **Groove width** | 2.80 mm |
| **Durometer** | 70 Shore A |
| **Operating temperature** | -30 °C to +100 °C |
| **Pressure rating** | Up to 10 bar (sufficient for launcher pressure — pending E1 NDC) |

---

## Manufacturing / Inspection Checklist

### Machining
- [ ] Stock confirmed: Ø45 × 25 mm 316L SS bar
- [ ] Lathe tool library: OD rough/finish, ID rough/finish boring bar, parting tool, O-ring groove tool
- [ ] O-ring groove machined to ±0.05 mm width and Ø0.025 mm position

### Inspection
- [ ] Fuselage bore: Ø35 H7 CMM or bore gauge
- [ ] O-ring groove: groove width 2.80 ±0.05 mm — optical comparator or CMM
- [ ] O-ring groove surface Ra ≤ 0.4 µm — profilometer (critical)
- [ ] Pilot bore: Ø15 H8 pin gauge
- [ ] OD: Ø44.000 ±0.03 mm — micrometer
- [ ] Overall length: 20.0 ±0.05 mm — micrometer
- [ ] M3 threads: go gauge M3 × 0.5
- [ ] Anti-rotation flats: CMM or vernier — symmetric 180° ±0.5°
- [ ] Concentricity: dial indicator on bore vs OD, ≤ Ø0.03 mm
- [ ] Through-bore: Ø4 H8 pin gauge

### Post-Inspection
- [ ] Passivation certificate (ASTM A967)
- [ ] O-ring press-fit test: install OR-112 NBR, check no extrusion under 10 bar hydraulic hold (1 min)
- [ ] Mass: ≤ 55 g per part (316L SS density 8.0 g/cm³)
- [ ] Dimensional report attached to traveler
- [ ] E2 structural sign-off → E1 gate review

---

*Designer: D1 | Reviewer: E1 | Gate: E1 (primary gate)*
