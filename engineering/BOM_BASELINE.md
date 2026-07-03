---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# BOM Baseline — Interceptor_M

> **Status:** Baseline v1.5 | **Version:** 1.5 | **Date:** 2026-06-30
> **Owner:** Lead Designer (Jules) | **Classification:** Confidential

---

## 1. Objects & Artifacts
This baseline synchronizes the high-fidelity CAD models (v2.3) and the electronic schematics (v1.0) with the official Bill of Materials.

---

## 2. Integrated BOM Summary

| Part ID | Designation | Mass (DD) | Source |
|---|---|---|---|
| **BRK-001** | Structural Junction Bracket | 130.74g | `create_launcher_parts.py` |
| **ACT-001** | Actuator / FC / ESC Mount | 55.49g | `create_launcher_parts.py` |
| **NCR-001** | Nose-Cone Interface Ring | 104.48g | `model_parts.py` |
| **SABOT-001** | Launcher/Drone Sabot | 15.00g | `create_launcher_parts.py` |
| **FC-001** | Flight Controller (H7) | 12.50g | `gen_electronics.py` |
| **PDB-001** | Power Dist. Board | 18.00g | `gen_electronics.py` |
| **TOTAL** | | **336.21g** | |

---

## 3. ISO Traceability
- **Design Control:** All mass values derived from parametric script volume calculations.
- **Verification:** Current mass is 15% above target; structural pocketing task assigned to D1 for G3.

---
*Généré automatiquement — Baseline v1.5*
