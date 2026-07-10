# Changelog V3 — Parametric Redesign

## [3.0.0] - 2026-07-10

### Added
- **New Platform**: V3-1600 (1600mm span, 6kg MTOW) added to `PARAMETERS.json`.
- **G2 Mechanical Parts**: Implemented `PROP-022` to `PROP-026` in `icad/parts/` with non-degenerate geometry.
- **Airfoil Specification**: NACA 4412 datasheet created; applied to all lifting surfaces in the BOM.
- **Tail Sizing**: Finalized tail boom length at 600mm based on 3.0 * MAC stability requirement.
- **Firmware Mixing**: Documented the 60°/30° asymmetric X-tail mixing matrix.
- **Surface Area**: CAD engine now reports surface area (mm²) for all parts.

### Fixed
- **Mass Overshoot**: Resolved the 43% mass overshoot by switching to a 2+2 tilt-rotor configuration and applying structural lightening. New BOM total: 5596g.
- **CAD Reliability**: Regenerated 9 degenerate STL files; all are now watertight and winding-consistent.
- **Security**: Fixed `wheel`/`packaging` vulnerability via `uv` dependency overrides.
- **Missing Source Files**: Implemented missing builders for `NC-001`, `FIN-001`, `SEEKER-01`, `PAYLOAD-01`, and `PDB-001`.

### Changed
- **Repo Structure**: Reorganized files into a hierarchical engineering structure (`docs/`, `cad/`, `data/`).
- **Authoritative Exports**: Consolidated all STL/STEP exports into `exports/drone/` and `exports/launcher/`.
