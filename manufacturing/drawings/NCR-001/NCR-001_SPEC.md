# NCR-001 — Nose-Cone Interface Ring Specification

**Version:** 1.0.0  
**Date:** 2026-07-05  
**Owner:** Jules (Engineering Lead)  
**Phase:** P1 (Week 1-2)  
**Priority:** HIGH

---

## 1. OBJECTIVES

The NCR-001 Nose-Cone Interface Ring is a **CNC-turned precision component** serving as the structural and aerodynamic transition element between the interchangeable nose-cone assemblies and the main airframe body tube. It must:

- Provide precise geometric transition for aerodynamic continuity
- Serve as the primary bolted interface ring (BOLT CIRCLE PATTERN)
- Enable rapid nose-cone changeover for mission reconfiguration
- Be manufactured via **CNC Turning** with 316L Stainless Steel bar stock

**Key Driver:** Tight concentricity and precise bolt circle for repeatable nose-cone attachment.

---

## 2. CRITICAL CONSTRAINTS

| Parameter | Value | Notes |
|-----------|-------|-------|
| Mass Target | **110g** | Hard limit per BOM v1.2.0 |
| Material | 316L Stainless Steel | ASTM A276 / A479, annealed condition |
| Manufacturing Process | CNC Turning | Bar stock Øout x length, single setup preferred |
| Concentricity | ≤0.05mm TIR | Critical for aerodynamic surface continuity |
| Surface Finish | Ra 0.8μm (nose face) | Low roughness for fairing seal contact |
| Post-Processing | Passivation | Mandatory for 316L corrosion resistance |
| Traceability | Linked to PARAMETERS.json | All dimensions derived from central parameter store |

---

## 3. KEY DIMENSIONS & INTERFACES

### 3.1 Primary Interfaces

| Interface | Description | Critical Dimension |
|-----------|-------------|-------------------|
| **Nose-cone seat** | Tapered seat for cone interference fit | Ø60mm x 15° taper (or specified angle) |
| **Body tube splice** | Press-fit or clamp interface | Ø78mm nominal, h7 tolerance |
| **Bolt circle pattern** | Primary attachment to BRK-001 | Ø100mm BCD, 6x M6x1.0 holes |
| **O-ring groove** | Sealing for fairing joint | Ø2mm cross-section O-ring, groove per AS568 |
| **Lead-in chamfer** | Assembly aid | 1.5mm x 45° on body tube end |

### 3.2 Dimensional Constraints

- **Overall envelope:** Derived from PARAMETERS.json `NCR-001_outer_diameter`, `NCR-001_length`
- **Bolt circle diameter:** Ø100mm (6x M6x1.0 on 60° pattern)
- **Threaded holes:** M6x1.0, 10mm deep minimum, blind holes
- **Body tube interface OD:** Ø78mm h7 (tolerance critical for spline/press-fit)
- **Nose face runout:** ≤0.05mm TIR relative to body tube OD datum
- **Surface roughness:** Nose face Ra 0.8μm, body OD Ra 1.6μm, ID Ra 3.2μm

---

## 4. 2D DRAWING REQUIREMENTS

### 4.1 Views Required

| View | Scale | Purpose |
|------|-------|---------|
| **Front view** | 1:1 | Nose face, bolt circle pattern, O-ring groove |
| **Right side view** | 1:1 | Overall length, taper detail, lead-in chamfer |
| **Section A-A (longitudinal)** | 2:1 | Full internal profile, bore details |
| **Section B-B (bolt circle)** | 2:1 | Bolt pattern section through center |
| **Detail C (O-ring groove)** | 5:1 | AS568 groove dimensions, surface finish |
| **Detail D (taper seat)** | 5:1 | Taper angle and diameter callout |

### 4.2 Dimensions to Call Out

- Overall length (nose to body tube end)
- Body tube interface OD (Ø78mm h7)
- Bolt circle diameter (Ø100mm BCD)
- Bolt hole locations (6x M6x1.0, equispaced 60°)
- Thread depth (10mm min, blind)
- O-ring groove position and dimensions (AS568)
- Taper seat diameter and angle
- Lead-in chamfer (1.5mm x 45°)
- Concentricity callout: **≤0.05mm TIR**
- Mass callout: **110g as-machined**

### 4.3 GD&T Requirements

| Feature | Tolerance Type | Value |
|---------|---------------|-------|
| Nose face | Total runout to body OD | ≤0.05mm TIR |
| Bolt holes | True position to datum center | Ø0.1mm |
| Body tube bore | Cylindricity | 0.02mm |
| O-ring groove | Width and depth | ±0.02mm |
| Taper seat | Angle tolerance | ±0.25° |
| Bolt hole perpendicularity | Perpendicularity | 0.05mm/25mm |

---

## 5. VALIDATION PROCESS

| Step | Action | Owner | Acceptance Criteria |
|------|--------|-------|-------------------|
| 1 | 3D CAD model review | Jules / D1 | Model approved in Onshape |
| 2 | Machining setup review | D1 | Single-setup turning (minimize re-chucking) |
| 3 | 2D drawing generation | D1 | All views, dimensions, GD&T present |
| 4 | Drawing review | Jules | All dimensions traceable to PARAMETERS.json |
| 5 | Material cert request | Jules | 316L mill cert, chemistry + tensile |
| 6 | FAI (First Article Inspection) | Machinist | DIM measurements, CMM report, thread gauge |
| 7 | Passivation verification | D1 | Passivation cert (ASTM A967) |
| 8 | Mass verification | D1 | As-machined mass ≤110g confirmed |

---

## 6. TRACEABILITY

| Source | Linked Data |
|--------|------------|
| PARAMETERS.json | `NCR-001_outer_diameter`, `NCR-001_length`, `NCR-001_mass_target`, `bolt_circle_diameter`, `o_ring_size` |
| BOM v1.2.0 | Line item NCR-001, 316L SS, CNC Turning |
| 3D CAD (Onshape) | Assembly: `interceptor_main.asm`, Part: `ncr_001_v1.prt` |
| PRODUCTION_DRAWINGS_PLAN.md | Section 2.3, Phase P1 |

---

## 7. NOTES & OPEN ITEMS

- ⚠️ **CRITICAL:** Concentricity ≤0.05mm TIR is mandatory — measure on CMM
- ⚠️ Bolt holes must be blind (pressure tightness required for fairing seal)
- ⚠️ Passivation mandatory (316L is susceptible to sensitization without it)
- ⚠️ O-ring groove per AS568A — verify seal compatibility with mission fluid/temp
- ⏳ Taper seat angle — confirm with nose-cone designer (Jules to follow up)
- ⏳ Machinist selection (lathe capacity: min Ø100mm swing) — pending quote
