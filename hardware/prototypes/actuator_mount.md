---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# Actuator Mount — Design Specification
**Part ID:** ACT-001 | **Revision:** v0.1-draft
**Machining Process:** CNC 3-axis Milling
**Governance ref:** PR #31 / Issue #32

---

## Function

Actuator mounting bracket for the Interceptor_M electronics suite. Secures the Electronic Speed Controller (ESC), Flight Controller (FC), and battery within the fuselage envelope. Provides thermally managed mounting points and wire-routing channels. Interfaces with the structural bracket (BRK-001) via M3 screws.

---

## Material

| Property | Value |
|---|---|
| **Alloy** | 7075-T6 Aluminum |
| **Condition** | T6 (aged) |
| **Thermal conductivity** | 130 W/m·K (dissipates ESC heat) |
| **Stock** | 70 × 50 × 8 mm block |

> Rationale: High thermal conductivity of 7075-T6 dissipates ESC losses (~15 W). T6 condition ensures tapped M2 threads in thin sections do not strip. Thinner section (8 mm) vs. bracket (12 mm) saves 8.8 g per part.

---

## Key Dimensions

| Dimension | Nominal | Tolerance | GD&T Callout |
|---|---|---|---|
| Overall length | 65.0 mm | ±0.10 mm | — |
| Overall width | 45.0 mm | ±0.10 mm | — |
| Overall thickness | 7.0 mm | ±0.05 mm | — |
| ESC pocket (30 × 15 × 8 mm) | 30.5 mm × 15.5 mm × 8.5 mm | ±0.10 mm | — |
| FC pocket (30 × 30 × 8 mm) | 30.5 mm × 30.5 mm × 8.5 mm | ±0.10 mm | — |
| Battery slot width | 20.5 mm | ±0.10 mm | — |
| Battery slot depth | 6.0 mm | ±0.05 mm | — |
| M3 clearance holes (×4, interface to BRK-001) | Ø3.3 mm | H9 | Ø3.3 H9 |
| M2 clearance holes (×6, ESC/FC mounts) | Ø2.2 mm | H9 | Ø2.2 H9 |
| Wire routing channels (×2) | 3.0 mm wide × 2.0 mm deep | ±0.10 mm | — |
| Thermal slot (for ESC pad) | 32.0 mm × 17.0 mm | ±0.10 mm | — |

---

## Geometric Tolerances (GD&T)

| Feature | Symbol | Value | Datum |
|---|---|---|---|
| M3 hole position (×4) | Position | Ø0.12 mm total | A (bottom face) |
| ESC/FC pocket flatness | — | 0.05 mm | — |
| Pocket perpendicularity (sides) | ⊥ | 0.05 mm/25 mm | A |
| Overall flatness | — | 0.08 mm | — |
| Wire channel perpendicularity | ⊥ | 0.08 mm/25 mm | Relevant face |

---

## Surface Finish

| Zone | Ra | Process |
|---|---|---|
| Top face (component seating) | 0.8 µm | CNC milled |
| Pocket walls | 1.6 µm | End mill finish pass |
| Wire channels | 3.2 µm | Rough mill, as-is acceptable |
| Screw head seats | 1.6 µm | Spot-face op |
| Bottom face | 0.8 µm | Ground (if stock allows) |

---

## Manufacturing Process (CNC Milling — 3 Axis)

1. **Blank prep:** Face top to final thickness 7.0 ±0.05 mm
2. **Rough pocketing:** Machine ESC, FC, battery, thermal slot pockets 0.5 mm oversize
3. **Wire channel routing:** Route 2× channels 3 mm wide
4. **Finish pocketing:** Full depth finish pass on all pockets
5. **Drill & tap:** Ø3.3 mm clearance (×4), Ø2.2 mm clearance (×6)
6. **Finish profile:** Finish-mill outer contour
7. **Deburr:** Break all edges 0.2 mm × 45°
8. **Thermal interface pad:** Apply 0.5 mm thermal pad (e.g. Bergquist Sil-Pad) in ESC slot before assembly
9. **Surface treatment:** Anodize Type III — matte grey

---

## Manufacturing / Inspection Checklist

### Machining
- [ ] Stock confirmed: 70 × 50 × 8 mm 7075-T6 T6
- [ ] Pocketing toolpath verified (no gouging of adjacent walls)
- [ ] Thermal slot depth checked with depth micrometer
- [ ] Wire channels checked for burr-free interior

### Inspection
- [ ] ESC pocket: 30.5 × 15.5 mm caliper check (both axes)
- [ ] FC pocket: 30.5 × 30.5 mm caliper check
- [ ] Battery slot width: 20.5 mm caliper
- [ ] M3 clearance holes: Ø3.3 mm go pin gauge
- [ ] M2 clearance holes: Ø2.2 mm go pin gauge
- [ ] Wire channels: 3.0 mm go/no-go gauge
- [ ] Thermal slot flatness: 0.05 mm feeler gauge
- [ ] Overall flatness: surface plate test
- [ ] Mass: ≤ 14 g per part (target)

### Post-Inspection
- [ ] Thermal pad pre-applied or ready for assembly
- [ ] Anodizing specification: Type III matte grey
- [ ] Dimensional report attached
- [ ] E2 sign-off (materials review) → E1 gate sign-off

---

*Designer: D3 | Reviewer: E2 | Gate: E1*
