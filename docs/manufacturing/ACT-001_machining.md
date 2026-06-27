# ACT-001 — Actuator Mount · Machining Notes

## Part Overview
| Property | Value |
|---|---|
| Part ID | ACT-001 |
| Material | 7075-T651 aluminium alloy |
| Density | 2.71 g/cm³ |
| Stock dimensions | 70 × 50 × 9 mm |
| Mass (all lines) | 55.49 g |
| MTOW sensitivity | **None** — fixed by E3 integration spec |

## Geometry Summary
- **Bounding box** : 65 × 45 × 7 mm (invariant across DC/DD/DI)
- **ESC pocket** : 30.5 × 15.5 × 8.5 mm
- **FC pocket** : 30.5 × 30.5 × 8.5 mm
- **Battery slot** : 20.5 mm wide strip
- **M3 clearance holes** : Ø3.3 mm × 4 at corners (interface to BRK-001)
- **M2 clearance holes** : Ø2.2 mm × 6 for ESC/FC standoffs

## Process Plan

### Op 10 — Face Mill Z=0 face
- Rough + finish face, Ra ≤ 1.6 µm

### Op 20 — Profile Mill outer contour (2D contouring)
- Roughing: 2 mm offset, 2 mm DOC
- Finishing: 0.3 mm stepover, single pass

### Op 30 — Pocket milling (ESC + FC)
- Roughing: z-level clearing, 0.5 mm floor stock
- Finishing: 2D contour pocket, 0.3 mm stepover
- Sequence: FC pocket first → ESC pocket → battery slot

### Op 40 — Drill M3 × 4 (corner holes, interface to BRK-001)
- Ø3.3 mm clearance drill, peck cycle, through
- Spot drill + 118° drill

### Op 50 — Drill M2 × 6 (ESC/FC standoff grid)
- Ø2.2 mm clearance drill, through

### Op 60 — OEL / CMM
- Pocket dimensions: length ±0.10 mm, depth ±0.10 mm
- M3 hole positions: ±0.05 mm from nominal corner grid
- Surface finish all pockets: Ra ≤ 1.6 µm

## GD&T Callouts
| Feature | Tolerance |
|---|---|
| ESC pocket dimensions | ±0.10 mm per side |
| FC pocket dimensions | ±0.10 mm per side |
| Pocket depth (ESC/FC) | ±0.10 mm |
| M3 hole positions | ±0.05 mm |
| Flatness Z=0 face | 0.03 mm |

## Tooling Required
- Ø25 face mill
- Ø6 / Ø8 / Ø10 flat end mills (pocket rough/finish)
- Ø3.3 mm HSS drill (M3 clearance)
- Ø2.2 mm HSS drill (M2 clearance)
- 3-axis CMM

## Cycle Time Estimate
| Op | Description | Est. Time |
|---|---|---|
| Op 10 | Face mill | 5 min |
| Op 20 | Profile contour | 8 min |
| Op 30 | Pockets (ESC/FC) | 12 min |
| Op 40 | M3 holes ×4 | 4 min |
| Op 50 | M2 holes ×6 | 3 min |
| Op 60 | OEL/CMM | 12 min |
| **Total** | | **≈ 44 min** |
