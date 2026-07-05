# BRK-001 — Structural Junction Bracket Specification

**Version:** 1.0.0  
**Date:** 2026-07-05  
**Owner:** Jules (Engineering Lead)  
**Phase:** P1 (Week 1-2)  
**Priority:** HIGH

---

## 1. OBJECTIVES

The BRK-001 Structural Junction Bracket is a **critical structural component** serving as the load-bearing junction between the nose-cone assembly and the central body tube. It must:

- Provide secure mechanical attachment points for the nose-cone interface ring
- Transmit aerodynamic loads and inertial forces through the airframe
- Serve as a hardpoint for actuation/mechanism integration
- Be manufactured via **DMLS (Direct Metal Laser Sintering)** with AlSi10Mg powder

**Key Driver:** Mass reduction — current mass is **135g**, target is **<90g** (45g reduction required via pocketing).

---

## 2. CRITICAL CONSTRAINTS

| Parameter | Value | Notes |
|-----------|-------|-------|
| Mass Target | **<90g** | Mandatory. Reduce from 135g through pocketing. |
| Material | AlSi10Mg | DMLS process. Powder bed additive manufacturing. |
| Manufacturing Process | DMLS + Pocketing | Post-DMLS machining required for pocketing features. |
| Surface Finish | As-DMLS / machined | Tolerance zones must be machined post-DMLS. |
| Post-Processing | Stress relief + anodizing | Mandatory before assembly. |
| Traceability | Linked to PARAMETERS.json | All dimensions derived from central parameter store. |

---

## 3. KEY DIMENSIONS & INTERFACES

### 3.1 Primary Interfaces

| Interface | Description | Critical Dimension |
|-----------|-------------|-------------------|
| **Nose-cone attachment** | Bolted connection to NCR-001 | M6x1.0 threaded holes (qty 6, 60° pattern) |
| **Body tube splice** | Circumferential clamp/splice | Ø80mm nominal interface |
| **Actuator mounting** | Hardpoint for ACT-001 interface | Ø20mm bore, 40mm depth |
| **Pocketing zones** | Mass reduction pockets | Min wall 2.5mm after pocketing |

### 3.2 Dimensional Constraints

- **Overall envelope:** TBD from 3D CAD (derived from PARAMETERS.json `BRK-001_length`, `BRK-001_outer_diameter`)
- **Tolerancing:** All critical interfaces ±0.05mm
- **Surface roughness:** Machined faces Ra 1.6μm, as-DMLS faces Ra 12.5μm
- **Flatness:** Bearing surfaces ≤0.05mm total indicated runout

---

## 4. 2D DRAWING REQUIREMENTS

### 4.1 Views Required

| View | Scale | Purpose |
|------|-------|---------|
| **Front view** | 1:1 | Primary dimensions, hole pattern, interface details |
| **Top view** | 1:1 | Overall length, pocketing extent |
| **Section A-A** | 2:1 | Internal pocketing geometry, wall thicknesses |
| **Section B-B** | 2:1 | Actuator bore detail |
| **Section C-C** | 2:1 | Nose-cone flange interface |
| **Isometric annotation view** | 1:2 | GD&T callouts, surface finish notes |

### 4.2 Dimensions to Call Out

- Overall length and widths
- Threaded hole locations (6x M6x1.0, 60° pattern)
- Pocketing depth and widths (after DMLS)
- Body tube interface diameter
- Actuator bore diameter and depth
- All critical wall thicknesses (min 2.5mm)
- Surface finish callouts (machined vs. as-DMLS)
- Mass callout: **<90g as-built**

### 4.3 GD&T Requirements

| Feature | Tolerance Type | Value |
|---------|---------------|-------|
| Nose-cone flange face | Position | Ø0.1mm at R60mm |
| Threaded holes | True position to datum | Ø0.15mm |
| Actuator bore | Cylindricity | 0.05mm |
| Interface OD | Circularity | 0.1mm |

---

## 5. VALIDATION PROCESS

| Step | Action | Owner | Acceptance Criteria |
|------|--------|-------|-------------------|
| 1 | 3D CAD model review | Jules / D1 | Model approved in Onshape |
| 2 | Mass simulation check | D1 | FEA confirms <90g post-pocketing |
| 3 | 2D drawing generation | D1 | All views, dimensions, GD&T present |
| 4 | Drawing review | Jules | All dimensions traceable to PARAMETERS.json |
| 5 | DMLS supplier data sheet review | Jules | AlSi10Mg material cert required |
| 6 | FAI (First Article Inspection) | Supplier | DIM measurements, CMM report |
| 7 | Mass verification | D1 | As-built mass <90g confirmed |

---

## 6. TRACEABILITY

| Source | Linked Data |
|--------|------------|
| PARAMETERS.json | `BRK-001_length`, `BRK-001_outer_diameter`, `BRK-001_mass_target` |
| BOM v1.2.0 | Line item BRK-001, AlSi10Mg, DMLS |
| 3D CAD (Onshape) | Assembly: `interceptor_main.asm`, Part: `brk_001_v1.asm` |
| PRODUCTION_DRAWINGS_PLAN.md | Section 2.1, Phase P1 |

---

## 7. NOTES & OPEN ITEMS

- ⚠️ **CRITICAL:** Pocketing strategy must be finalized in 3D CAD before 2D drawing release
- ⚠️ As-DMLS surface must be identified on drawing with hatching convention
- ⚠️ Post-DMLS stress relief mandatory — note on drawing
- ⏳ DMLS supplier selection (e.g., 3D Systems, EOS) — pending quote
- ⏳ Anodizing supplier — pending contact
