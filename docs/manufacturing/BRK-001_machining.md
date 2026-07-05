---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# BRK-001 — Structural Junction Bracket · Machining Notes

## Part Overview
| Property | Value |
|---|---|
| Part ID | BRK-001 |
| Material | 7075-T651 aluminium alloy |
| Density | 2.71 g/cm³ |
| Stock dimensions | 80 × 60 × 12 mm |
| Mass (DC) | 111.78 g |
| Hardness (target) | 86 HRB (7075-T6 spec) |

## Geometry Summary
- **Bounding box** : 75 × 55 × 10 mm (DC) — scales with MTOW
- **Central bore** : Ø35.0 mm, bore axis Z
- **Arm holes** : Ø5.0 mm × 4 at r=20 mm from bore centre (radial, 90° apart)
- **Motor-mount holes** : Ø9.0 mm × 4 at r=32 mm, 45° offset from arm holes

## Process Plan

### Op 10 — Face Mill (Top face Z=0)
- Climb mill, 2-flute Ø25 face mill, 6061 feed rate
- Roughing: 1.5 mm DOC, 0.5 mm stepover → 0.3 mm finish pass
- Surface goal: Ra ≤ 1.6 µm

### Op 20 — Bore Ø35 (rough + finish)
- Rough bore: Ø30 drill → 6 mm increment interpolation → Ø34.5
- Finish bore: single-point boring, Ø35 H7 tolerance
- Target: Ra ≤ 0.8 µm bore wall

### Op 30 — Arm holes Ø5 × 4 ( helical interpolation)
- Peck drill cycle, Ø5 H8, 4× equally spaced 90° apart at r=20 mm
- Deburr with 45° chamfer tool

### Op 40 — Motor-mount holes Ø9 × 4
- Through-hole, Ø9 H8, 45° offset from arm holes at r=32 mm
- Through deburring

### Op 50 — OEL / final inspection
- CMM: bore diameter, arm-hole positions (r=20 mm ±0.05 mm), perpendicularity
- Surface finish check: Ra ≤ 1.6 µm all faces

## GD&T Callouts
| Feature | Tolerance |
|---|---|
| Bore Ø35 | Ø35 H7 (Ø34.979–Ø35.000 mm) |
| Arm holes Ø5 | Ø5 H8 (Ø5.000–Ø5.018 mm) |
| Bore perpendicularity to Z face | 0.05 mm / 100 mm |
| Flatness top face | 0.03 mm |

## Tooling Required
- Ø25 face mill (aluminium, 2–3 flutes)
- Ø30 pilot drill, 6 mm carbide end mill for interpolation
- Ø5 HSS drill, Ø9 HSS drill
- Ø35 boring head / single-point boring bar
- 3-axis CMM for dimensional verification

## Cycle Time Estimate
| Op | Description | Est. Time |
|---|---|---|
| Op 10 | Face mill | 8 min |
| Op 20 | Bore Ø35 | 12 min |
| Op 30 | Arm holes Ø5×4 | 6 min |
| Op 40 | Motor holes Ø9×4 | 5 min |
| Op 50 | OEL/CMM | 15 min |
| **Total** | | **≈ 46 min** |
