# ACT-001 — Actuator/FC/ESC Mount Specification

**Version:** 1.0.0  
**Date:** 2026-07-05  
**Owner:** Jules (Engineering Lead)  
**Phase:** P1 (Week 1-2)  
**Priority:** HIGH

---

## 1. OBJECTIVES

The ACT-001 Actuator/FC/ESC Mount is a **DMLS-manufactured mounting structure** that serves as the primary attachment point for all electronic speed controllers (ESCs), flight controllers (FC), and actuator drivers within the airframe. It must:

- Provide precise, vibration-dampened mounting for electronics
- Interface directly with BRK-001 structural bracket
- Maintain strict geometric alignment for flight-critical sensors (IMU, barometer)
- Be manufactured via **DMLS (Direct Metal Laser Sintering)** with AlSi10Mg powder

**Key Driver:** Precise bore alignment and vibration isolation features.

---

## 2. CRITICAL CONSTRAINTS

| Parameter | Value | Notes |
|-----------|-------|-------|
| Mass Target | **65g** | Hard limit per BOM v1.2.0 |
| Material | AlSi10Mg | DMLS process. No post-machining pockets. |
| Manufacturing Process | DMLS only | Single-process (no pocketing like BRK-001) |
| Bore Tolerance | H7 fit | Precision bore for actuator shafts |
| Surface Finish | As-DMLS | No machining required (cost driver) |
| Post-Processing | Stress relief | Mandatory before assembly |
| Traceability | Linked to PARAMETERS.json | All dimensions derived from central parameter store |

---

## 3. KEY DIMENSIONS & INTERFACES

### 3.1 Primary Interfaces

| Interface | Description | Critical Dimension |
|-----------|-------------|-------------------|
| **BRK-001 attachment** | Bolted connection to bracket | M5x0.8 threaded holes (qty 4) |
| **ESC mount points** | Vibration-isolated pads | Ø10mm pads, silicone mount |
| **FC mounting grid** | 30.5mm or 20mm square pattern | M3x0.5 holes |
| **Actuator shaft bore** | Through-bore for motor output | Ø8mm bore, H7 tolerance |
| **Wire routing channels** | Integral cable management | 5mm wide channels |

### 3.2 Dimensional Constraints

- **Overall envelope:** Derived from PARAMETERS.json `ACT-001_length`, `ACT-001_width`
- **Bore tolerance:** Ø8mm H7 (0/+0.015mm) — critical for actuator alignment
- **Mounting holes:** M5x0.8 x 8mm deep minimum
- **Surface roughness:** As-DMLS Ra 12.5μm (no post-machining)
- **Flatness:** Mounting faces ≤0.1mm total indicated runout

---

## 4. 2D DRAWING REQUIREMENTS

### 4.1 Views Required

| View | Scale | Purpose |
|------|-------|---------|
| **Front view** | 1:1 | Primary dimensions, mounting hole pattern |
| **Top view** | 1:1 | FC mounting grid, wire channels |
| **Right side view** | 1:1 | Actuator bore alignment, channel geometry |
| **Section A-A** | 2:1 | Bore detail, wall thicknesses |
| **Detail B** | 5:1 | Wire channel section (small feature) |
| **Isometric view** | 1:2 | GD&T callouts, surface finish notes |

### 4.2 Dimensions to Call Out

- Overall envelope (length x width x height)
- FC mounting grid (30.5mm or 20mm pattern)
- Actuator bore diameter (Ø8mm H7)
- Mounting hole locations (4x M5x0.8)
- ESC pad locations (3x Ø10mm)
- Wire channel widths (5mm)
- Mass callout: **65g as-built**

### 4.3 GD&T Requirements

| Feature | Tolerance Type | Value |
|---------|---------------|-------|
| Actuator bore | Cylindricity | 0.02mm |
| Actuator bore | Position to datum | Ø0.05mm |
| FC mounting holes | True position | Ø0.1mm |
| Mounting face | Flatness | 0.1mm |

---

## 5. VALIDATION PROCESS

| Step | Action | Owner | Acceptance Criteria |
|------|--------|-------|-------------------|
| 1 | 3D CAD model review | Jules / D1 | Model approved in Onshape |
| 2 | Mass estimation check | D1 | Estimated mass ≤65g from CAD properties |
| 3 | 2D drawing generation | D1 | All views, dimensions, GD&T present |
| 4 | Drawing review | Jules | All dimensions traceable to PARAMETERS.json |
| 5 | DMLS supplier data sheet review | Jules | AlSi10Mg material cert, as-DMLS surface spec |
| 6 | FAI (First Article Inspection) | Supplier | DIM measurements, bore gauge check |
| 7 | Mass verification | D1 | As-built mass ≤65g confirmed |

---

## 6. TRACEABILITY

| Source | Linked Data |
|--------|------------|
| PARAMETERS.json | `ACT-001_length`, `ACT-001_width`, `ACT-001_mass_target`, `actuator_bore_diameter` |
| BOM v1.2.0 | Line item ACT-001, AlSi10Mg, DMLS |
| 3D CAD (Onshape) | Assembly: `interceptor_main.asm`, Part: `act_001_v1.prt` |
| PRODUCTION_DRAWINGS_PLAN.md | Section 2.2, Phase P1 |

---

## 7. NOTES & OPEN ITEMS

- ⚠️ **CRITICAL:** Bore tolerance H7 is mandatory — no reworking possible with DMLS
- ⚠️ No post-machining allowed (cost/cycle time constraint)
- ⚠️ Stress relief mandatory — note on drawing
- ⏳ ESC isolation pad material (silicone durometer) — to specify
- ⏳ Wire routing channel fillet radius — to finalize in CAD
