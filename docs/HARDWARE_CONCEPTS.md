# Hardware Lifecycle and BOM Strategy
**Project:** Interceptor_M
**Version:** 1.0 (v1.5 Baseline)
**Classification:** Confidential

## 1. Procurement Strategy: COTS vs. Custom
To minimize cost and lead time while maximizing performance, Interceptor_M follows a hybrid procurement strategy:

- **Custom Parts (High-IP):**
  - `BRK-001`, `ACT-001`, `NCR-001`: Custom machined or DMLS parts to meet the Ø40mm tube constraint.
  - `SABOT-001`: In-house 3D printed sacrificial part.
- **COTS (Commercial Off-The-Shelf):**
  - **MCU:** STM32H7 series (Standardization on Betaflight/Ardupilot hardware ecosystem where possible).
  - **Sensors:** ICM-42688 IMUs, BMP388 Barometers.
  - **Power:** TPH1R204PL MOSFETs for ESC integration.

## 2. Process Selection: DMLS vs. CNC
- **DMLS (AlSi10Mg):** Selected for complex internal geometries and rapid weight optimization. Primary for Phase 1 prototypes.
- **CNC (7075-T6):** Reserved for high-volume production or critical high-stress interfaces requiring IT7 tolerances.
- **FDM (ASA):** Used for non-structural aerodynamic fairings and the SABOT interface.

## 3. BOM Lifecycle & ISO 9001 Traceability
- **Level 1 (BOM_BASELINE):** The "Frozen" executive view.
- **Level 2 (BOM_consolidee):** The "Operational" view for assembly and manufacturing agents.
- **Level 3 (gen_geometry):** The "Parametric" view. Changes to geometry scripts automatically trigger BOM mass updates.

## 4. Maintenance & Recoverability
The Interceptor_M is designed for **80% recoverability** (Line DI). The modular PDB/ESC and Flight Controller are independent assemblies to allow quick field replacement after a successful kinetic intercept.

---
*Authored by Jules (Lead Designer) for G2 Readiness.*
