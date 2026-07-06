---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# BOM Baseline — Interceptor_M

> **Status:** Baseline v1.2.0 | **Version:** 1.2.0 | **Date:** 2026-07-01
> **Owner:** Lead Designer (Jules) | **Classification:** Confidential

---

## 1. Objects & Artifacts
This baseline synchronizes the high-fidelity CAD models and the electronic schematics with the official Bill of Materials for the DD-400 platform.

---

## 2. Integrated BOM Summary (DD-400)

| Part ID | Designation | Mass | Material |
|---|---|---|---|
| **BRK-001** | Structural Junction Bracket | 135.0g | AlSi10Mg |
| **ACT-001** | Actuator / FC / ESC Mount | 65.0g | AlSi10Mg |
| **NCR-001** | Nose-Cone Interface Ring | 110.0g | 316L SS |
| **ELECTRONICS**| FC + PDB + Sensors | 50.0g | Mixed |
| **BATTERY** | 3S 650mAh | 115.0g | LiPo |
| **TOTAL (EST)** | | **475.0g** | |

> ⚠️ **Mass Warning:** Current estimated total (475g) exceeds MTOW (400g). Pocketing and optimization required in PHASE_2_DESIGN.

---

## 3. ISO Traceability
- **Design Control:** All mass values derived from PARAMETERS.json v1.2.0.
- **Verification:** Continuous mass tracking required for G3.

---
*Généré automatiquement — Baseline v1.2.0*
