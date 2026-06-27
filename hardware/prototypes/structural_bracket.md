# Structural Bracket — Design Specification
**Part ID:** BRK-001 | **Revision:** v0.1-draft
**Machining Process:** CNC 3-axis Milling
**Governance ref:** PR #31 / Issue #32

---

## Function

Primary airframe junction bracket. Connects the fuselage tube (Ø35 mm OD) to the four carbon-tube arms (Ø5 mm OD, 75 mm long) and provides the threaded motor-mount interface (9 mm / 12 mm standard). This is the main structural node of the Interceptor_M airframe.

---

## Material

| Property | Value |
|---|---|
| **Alloy** | 7075-T6 Aluminum |
| **Condition** | T6 (peak strength, aged) |
| **Ultimate Tensile Strength** | ≥ 572 MPa |
| **Yield Strength** | ≥ 503 MPa |
| **Hardness** | ~87 HRB |
| **Stock** | 80 × 60 × 12 mm block |

> Rationale: 7075-T6 offers the best strength-to-weight ratio among machinable aluminium alloys, critical for the 250 g MTOW budget. T6 temper provides max hardness for thread integrity (M2/M3 tapped holes).

---

## Key Dimensions

| Dimension | Nominal | Tolerance | GD&T Callout |
|---|---|---|---|
| Overall length | 75.0 mm | ±0.10 mm | — |
| Overall width | 55.0 mm | ±0.10 mm | — |
| Overall thickness | 10.0 mm | ±0.05 mm | — |
| Central bore (fuselage Ø35 mm) | Ø35.0 mm | H7 (ø35.000/+0.025) | Ø35 H7 |
| Bore depth | 8.0 mm | ±0.05 mm | — |
| Arm hole Ø (×4, Ø5 mm tube) | Ø5.0 mm | H8 (ø5.000/+0.018) | Ø5 H8 |
| Arm hole positions (radial from bore centre) | 20.0 mm | ±0.05 mm | True position Ø0.1 @ Ø20 |
| Motor mount holes (×4, Ø9 mm) | Ø9.0 mm | H8 (ø9.000/+0.022) | Ø9 H8 |
| M2 tapped holes (×8) | M2 × 0.4 | 4H tolerance class | — |
| M3 tapped holes (×4) | M3 × 0.5 | 4H tolerance class | — |

---

## Geometric Tolerances (GD&T)

| Feature | Symbol | Value | Datum |
|---|---|---|---|
| Central bore centre | Position | Ø0.08 mm | A (bottom face) |
| 4× arm holes (radial array) | Position | Ø0.10 mm total | A, B (bore axis) |
| Bottom face flatness | — | 0.05 mm | — |
| Thickness parallelism (top//bottom) | // | 0.08 mm | — |
| M2/M3 thread perpendicularity | ⊥ | 0.05 mm/25 mm | Relevant face |

---

## Surface Finish

| Zone | Ra | Process |
|---|---|---|
| Outer faces (structural) | 0.8 µm | CNC milled, as-machined |
| Bore wall (fuselage contact) | 0.4 µm | Fine pass / light polishing |
| Threaded holes | 0.8 µm | Tap with cutting fluid |
| Fastener head seats | 1.6 µm | Spot-face operation |

---

## Manufacturing Process (CNC Milling — 3 Axis)

1. **Blank preparation:** Face top/bottom to final thickness 10.0 ±0.05 mm
2. **Rough profile:** Machine outer contour 1 mm oversize, leaving 0.5 mm stock
3. **Bore machining:** Bore central Ø35 H7 in two passes (rough + finish)
4. **Arm hole drilling:** Drill 4× Ø5 H8 holes (radial 90° apart) + cross-holes for Ø9 motor mounts
5. **Tapping:** M2 (×8 depth 4 mm), M3 (×4 depth 6 mm) with cutting oil
6. **Finish profile:** Finish-mill outer contour to nominal
7. **Deburr:** Manual deburr all edges, chamfer bore entrance 0.5 × 45°
8. **Surface treatment:** Anodize Type III (hard coat) — matte grey, 25 µm min

---

## Manufacturing / Inspection Checklist

### Machining
- [ ] Stock dimensions confirmed: 80 × 60 × 12 mm 7075-T6
- [ ] Tool library loaded (Ø2, Ø3, Ø5, Ø6, Ø8 end mills; #0-80, M2, M3 taps)
- [ ] Work coordinate system set on bottom face
- [ ] Part is fixtured with step clamps, no lift
- [ ] All dimensions verified with CMM or digital caliper after machining

### Inspection
- [ ] Central bore Ø35 H7 — go/no-go gauge or CMM
- [ ] 4× arm holes Ø5 H8 — go/no-go pin gauge
- [ ] 4× motor mount holes Ø9 H8 — go/no-go pin gauge
- [ ] M2 threads — go gauge #0-80 M2, depth gauge
- [ ] M3 threads — go gauge M3×0.5, depth gauge
- [ ] Flatness of bearing faces — surface plate + feeler gauge
- [ ] Parallelism top//bottom — height gauge comparison
- [ ] Surface finish Ra ≤ 0.8 µm confirmed (profilometer or optical)
- [ ] Visual: no burrs, cracks, or tool marks

### Post-Inspection
- [ ] Anodizing specification confirmed (Type III, matte grey)
- [ ] Mass: ≤ 22 g per bracket (target)
- [ ] Dimensional report attached to traveler
- [ ] E2 sign-off (structural/materials) — per approval chain

---

*Designer: D2 | Reviewer: E2 | Gate: E1*
