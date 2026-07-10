# V3 Developer TODO

**Repo:** `Commonfields25/Interceptor_M` — branch `v3-dossier` (not yet merged to `main`)

## Priority 0 — Blocking
- [ ] Review and merge PR from `v3-dossier` → `main` (or confirm if `main` is protected and needs separate approval flow)
- [ ] Resolve total mass overshoot: current BOM totals 8587g, target MTOW is 6000g → identify where to cut weight (ticket INT-202)
- [ ] Finalize tail boom length (currently TBD) → locks the X-tail geometry (60°/30°) (ticket INT-201)

## Priority 1 — Data completion
- [ ] Measure/calculate mass for the 5 new G2 parts: PROP-022 to PROP-026 (currently marked TBD in BOM)
- [ ] Confirm NACA 4412 airfoil parameters are final for wing production drawings
- [ ] Validate motor layout (4+2 config) against updated mass budget

## Priority 2 — Structure & docs
- [ ] Reorganize repo folders to match target structure proposed in docs/v3/V3_dossier_complet.md
- [ ] Cross-check V3_matrices.csv (part→location, V2→V3 changes, new interfaces) against actual CAD assembly
- [ ] Add CAD/STEP files for new G2 parts once finalized (currently only referenced, not attached)

## Priority 3 — Nice to have
- [ ] Set up CI check to flag BOM mass total automatically if it exceeds MTOW
- [ ] Write short changelog entry summarizing V2 → V3 differences (12 changes already identified in matrix, just needs prose)

---
Files to check first: docs/v3/V3_dossier_complet.md, docs/v3/V3_BOM_complete.csv, docs/v3/V3_matrices.csv
