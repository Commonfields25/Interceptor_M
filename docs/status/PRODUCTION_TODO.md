---
agent: Jules
action: Create
timestamp: 2026-06-29T14:30:00Z
related_gate: G2
status: Draft
---

# 🚀 PRODUCTION SUCCESS TO-DO LIST

The current STL plans in `models/Base_Launcher_Pieces/` are **insufficient** for manufacturing and high-fidelity simulation. They are primitive placeholders that lack the mechanical complexity required by the `Cahier_Charges_Prototype.md`.

## 🛠 1. Immediate Technical Remediation

- [ ] **SABOT-001 Design:** Create the interface sabot model between the 35mm drone and the 40mm launcher tube. This is the #1 missing critical part.
- [ ] **Tolerance Integration:** Refactor `create_launcher_parts.py` or move to manual CAD (Fusion 360) to implement **IT7/IT10 tolerances** on critical surfaces (Rails and Mounting Bracket).
- [ ] **Fastening Detail:** Add M3/M2 screw holes and Helicoil insert volumes to the `01_Main_Chassis` and `03_Drone_Mounting_Bracket`. Current STLs have no assembly points.
- [ ] **High-Fidelity Meshing:** Export models in **STEP format** (not just STL) to allow E1/E2 to perform Von Mises stress and CFD analysis.

## ⚙️ 2. Workflow "Release" Tasks

- [ ] **Close Condition C3:** Define the final deliverable package for G2 (STEP assembly + validated BOM).
- [ ] **Lift Agent Standby:** Request DG to formally release D3 and E1 from "Standby" to start Week 1 modeling.
- [ ] **Material Spec Lock:** Finalize the choice between AlSi10Mg (DMLS) and FDM ASA for the first prototype to set accurate weight parameters.

## 📋 3. Modeling Guidelines for Production Success

1. **Primitive-to-Parametric:** Transition from Python-generated box primitives to parametric CAD models with rounded fillets and draft angles for CNC/DMLS.
2. **Weight Management:** Strict adherence to the **290.71g structure budget**. Current low-poly STLs do not account for real material density or internal hollows.
3. **Assembly Check:** Perform a virtual "First Article Assembly" in Fusion 360 to ensure the `02_Launch_Rails` actually interface with the `03_Drone_Mounting_Bracket` without interference.

---
*Status: Priority 1 - Required to pass Gate G2.*
