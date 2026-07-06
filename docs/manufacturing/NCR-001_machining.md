---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# NCR-001 — Nose-Cone Interface Ring · Machining Notes

## Part Overview
| Property | Value |
|---|---|
| Part ID | NCR-001 |
| Material | 316L stainless steel (bar stock, OD=48 mm, bore Ø35 mm, L=22 mm) |
| Density | 8.0 g/cm³ |
| Mass (DC) | 89.33 g |
| MTOW sensitivity | **Yes** — scales with MTOW (linear cube-root) |

## Geometry Summary (DC reference)
- **OD** : Ø44 mm (scales with MTOW)
- **Bore ID** : Ø35 mm (fixed — fuselage interface)
- **Length** : 20 mm (scales with MTOW)
- **O-ring groove** : Ø36.5 mm, 2.80 mm wide (axial midpoint at 1.4 mm)
- **Anti-rotation flats** : 2 × 6 mm wide, at 90° and 270° (12 and 6 o'clock)
- **M3 tapped holes** : Ø2.5 mm tap drill × 4 at r=20 mm from axis

## Process Plan

### Lathe Operations (primary)

### Op 10 — Rough Turn OD to Ø47.5 mm
- 316L work-hardens rapidly: use ceramic or CBN insert
- Max 0.5 mm DOC per pass

### Op 20 — Bore to Ø35.5 mm (rough bore)
- boring bar Ø25 min; interpolate if bar too large: rough drill Ø30 → interpolate

### Op 30 — Finish Bore Ø35.0 mm (H7)
- Single-point boring, Ra ≤ 0.8 µm

### Op 40 — Finish Turn OD to Ø44.0 mm
- Light finishing pass, Ra ≤ 0.8 µm

### Op 50 — O-ring Groove (Ø36.5 mm)
- Parting tool profiling or Vee profile tool
- Groove width 2.80 mm, depth = (36.5−35.0)/2 = 0.75 mm
- Verify groove diameter with gear micrometer or bore gauge

### Mill Operations (secondary)

### Op 60 — Anti-Rotation Flats × 2
- 2-axis milling, 6 mm flat at 90° and 270°
- Clamp with soft jaws or collet; mill from OD inward

### Op 70 — M3 Tapped Holes × 4 (radial, 90° apart)
- Spot drill + Ø2.5 mm tap drill through OD wall
- M3×0.5 tap, 4× equally spaced

### Op 80 — OEL / CMM
- Bore Ø35 H7, OD Ø44 g6, O-ring groove Ø36.5 ±0.05 mm
- Concentricity bore vs OD ≤ 0.03 mm
- Surface: Ra ≤ 0.8 µm (bore and OD)

## GD&T Callouts
| Feature | Tolerance |
|---|---|
| Bore Ø35 | Ø35 H7 (Ø34.979–Ø35.000 mm) |
| OD Ø44 | Ø44 g6 (Ø43.979–Ø44.000 mm) |
| O-ring groove | Ø36.5 ±0.05 mm |
| Concentricity bore/OD | 0.03 mm |
| M3 thread | M3×0.5, depth ≥ 5 mm |

## Tooling Required
- Lathe: Ø25 boring bar, parting / V-groove tool, CBN insert OD roughing
- Mill: Ø6 end mill (flats), spot drill + Ø2.5 drill, M3×0.5 tap
- Gear micrometer or bore gauge (groove verification)
- 3-axis CMM

## Cycle Time Estimate
| Op | Description | Est. Time |
|---|---|---|
| Op 10 | Rough turn OD | 10 min |
| Op 20 | Rough bore | 8 min |
| Op 30 | Finish bore | 6 min |
| Op 40 | Finish turn OD | 6 min |
| Op 50 | O-ring groove | 8 min |
| Op 60 | Mill flats ×2 | 6 min |
| Op 70 | M3 tap ×4 | 5 min |
| Op 80 | OEL/CMM | 15 min |
| **Total** | | **≈ 64 min** |
