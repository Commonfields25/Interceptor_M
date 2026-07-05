# 🏭 PRODUCTION DRAWINGS PLAN — Interceptor_M

**STATUS: PRELIMINARY — pending Engineering validation**

---

**Version:** 1.0.0  
**Date:** 2026-07-05  
**Updated:** 2026-07-05  
**Owner:** Jules (Lead Engineer), D1 (Industrial Design)  
**Phase:** P1-P2 (Weeks 1-4, July 5-29, 2026)

---

## EXECUTIVE SUMMARY

This document defines the 2D CAD production drawings strategy for the Interceptor_M manufacturing phase. Three critical components require detailed 2D working drawings:

1. **BRK-001** — Structural Junction Bracket (DMLS AlSi10Mg)
2. **ACT-001** — Actuator/FC/ESC Mount (DMLS AlSi10Mg)
3. **NCR-001** — Nose-Cone Interface Ring (316L SS)

All drawings will be produced using LibreCAD with rigorous traceability to PARAMETERS.json, 3D CAD models, and engineering validation.

---

## CRITICAL CONSTRAINTS & PARAMETERS

### Mass Budget (BOM v1.2.0)

| Part    | Mass Target | Material   | Process         |
|---------|-------------|------------|-----------------|
| BRK-001 | **<90g** (reduced from 135g) | AlSi10Mg  | DMLS + Pocketing |
| ACT-001 | 65g         | AlSi10Mg   | DMLS + CNC      |
| NCR-001 | 110g        | 316L SS     | CNC Turning     |
| **TOTAL** | **<=265g** (was 310g) | | |

### Geometric Constraints

| Parameter           | Value          | Ref |
|---------------------|----------------|-----|
| Main tube OD        | 40mm ±0.1     | params_DD/DI/DC.json |
| Fuselage OD         | 35mm           | DI_product_specification.md |
| Arm length          | 75mm           | params_DD |
| Wing chord           | 60mm           | params_DI |
| Hull thickness       | 1.5–2.0mm      | DI_product_specification.md |

### Tolerances & Surface Finish

| Grade  | IT Grade | Surface Ra  | Application          |
|--------|----------|-------------|----------------------|
| Fine   | IT7      | Ra0.8µm     | Actuator mounting faces, FC/ESC flat |
| Medium | IT10     | Ra1.6–3.2µm | Bracket, ring general |

---

## PRODUCTION TIMELINE

| Phase | Dates         | Days | Activities                              |
|-------|---------------|------|----------------------------------------|
| 0     | Jul 5         | 0    | Kick-off, STEP file collection          |
| 1     | Jul 6–12      | 1–7  | BRK-001 v2.0 CAD pocketing + 2D drawings |
| 2     | Jul 13–19     | 8–14 | ACT-001 2D drawings (E3 source STEP)    |
| 3     | Jul 20–26     | 15–21| NCR-001 2D drawings (D3 source STEP)    |
| Close | Jul 27–29     | 22–24| Review, RFQ, BOM update                 |

---

## DRAWING DELIVERABLES SPECIFICATION

Each production drawing must include:
- **5 standard views**: Front, Top, Side, Section A-A, Section B-B
- **GD&T callouts**: Position, perpendicularity, flatness per ISO 1101
- **Title block**: Part ID, Revision, Date, Scale, Material, Tolerancing standard
- **Tolerance block**: General ISO 2768-m; special IT7/IT10 per part
- **Surface finish callouts**: Ra values per ISO 1302
- **Mass annotation**: Target mass per BOM

---

## COMPONENT-SPECIFIC PLANS

### BRK-001 — Structural Junction Bracket

- **Source STEP**: `engineering/DC/BRK-001_v2.0.step` *(pending — not yet in repo)*
- **Revision**: v2.0 (mass reduction from 135g → 90g)
- **Material**: AlSi10Mg  
- **Process**: DMLS + pocket milling  
- **Tolerance**: IT10  
- **Surface**: Ra1.6µm  
- **Mass target**: <90g  
- **Drawing**: 2D working drawing with GD&T  
- **Owner**: Jules / D1

### ACT-001 — Actuator/FC/ESC Mount

- **Source STEP**: `engineering/E3/ACT-001_mount.step` *(pending)*
- **Material**: AlSi10Mg  
- **Process**: DMLS base + CNC finishing  
- **Tolerance**: IT7 for mounting faces  
- **Surface**: Ra0.8µm on FC/ESC faces  
- **Mass target**: 65g  
- **Drawing**: 2D with tight tolerance callouts  
- **Owner**: Jules / E3

### NCR-001 — Nose-Cone Interface Ring

- **Source STEP**: `engineering/D3/NCR-001_ring.step` *(pending)*
- **Material**: 316L Stainless Steel  
- **Process**: CNC Turning  
- **Key dimensions**: OD 110±0.2mm, ID 32±0.1mm, M3x0.5 thread, O-ring gland per ISO 3384 NBR  
- **Tolerance**: IT10 general / IT7 thread  
- **Surface**: Ra3.2µm  
- **Mass target**: 110g  
- **Drawing**: 2D turning drawing with thread notation  
- **Owner**: Jules / D3

---

## WORKFLOW STEPS

1. **Source collection**: Gather STEP files from D1 (BRK-001), E3 (ACT-001), D3 (NCR-001)
2. **Model review**: Validate geometry against PARAMETERS.json constraints
3. **Pocketing / revision** (BRK-001 v2.0): Reduce mass 135g → 90g, re-export STEP
4. **2D drawing production**: Generate .dxf from STEP, add GD&T, title blocks
5. **Engineering validation**: Cross-check dimensions vs PARAMETERS.json
6. **PDF release + RFQ package**: Finalize for supplier quote

---

## TRACEABILITY MATRIX

| Drawing  | Param Ref          | STEP Source        | BOM Mass  |
|----------|--------------------|--------------------|-----------|
| BRK-001  | params_DD/DI/DC    | engineering/DC/    | <90g      |
| ACT-001  | params_DI          | engineering/E3/    | 65g       |
| NCR-001  | params_DC          | engineering/D3/    | 110g      |

---

## FAILURE MODES & ESCALATION

| Risk                            | Mitigation                         | Escalation     |
|---------------------------------|------------------------------------|----------------|
| STEP file not delivered on time | Day 0 sign-off from D1/E3/D3       | Jules → DG     |
| Mass target not met             | Re-run FEA after pocketing          | Jules → DG     |
| Tolerance conflict with params  | Lock tolerance block before drawing | Jules → Eng    |
| Supplier RFQ rejected           | Pre-qualify 2 suppliers             | Jules → DG     |

---

## SUCCESS CRITERIA

- [ ] BRK-001 v2.0 STEP in repo with pocketing confirmed
- [ ] All 3 .dxf drawings complete and PDF-exported
- [ ] All dimensions traceable to PARAMETERS.json
- [ ] Mass budget: total ≤265g
- [ ] BOM v1.3.0 updated with new masses
- [ ] RFQ package sent to ≥2 suppliers
- [ ] 3 issues closed

---

## RESOURCE ALLOCATION

| Resource    | Allocation   | Notes                     |
|-------------|--------------|---------------------------|
| Jules       | 60%          | Lead, drawing production  |
| D1 (CAD)    | 20%          | BRK-001 STEP supply       |
| E3 (CAD)    | 10%          | ACT-001 STEP supply       |
| D3 (CAD)    | 10%          | NCR-001 STEP supply       |

---

## NEXT ACTIONS

| # | Action                        | Owner | Due  |
|---|-------------------------------|-------|------|
| 1 | Confirm STEP delivery dates   | Jules | Jul 6 |
| 2 | BRK-001 v2.0 pocketing + 2D   | D1/Jules | Jul 12 |
| 3 | ACT-001 2D drawings           | E3/Jules | Jul 19 |
| 4 | NCR-001 2D drawings           | D3/Jules | Jul 26 |
| 5 | RFQ package release           | Jules  | Jul 29 |

---

## DOCUMENT CONTROL

| Version | Date       | Author | Changes         |
|---------|------------|--------|-----------------|
| 1.0.0   | 2026-07-05 | Jules  | Initial release |
