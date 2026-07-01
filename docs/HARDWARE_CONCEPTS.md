# Hardware Lifecycle and BOM Strategy
**Project:** Interceptor_M
**Version:** 1.1 (v1.6 Baseline)
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

## 2. Technical Rationales for Material & Process Selection

### 2.1 DMLS (AlSi10Mg) - Phase 1 Prototyping
Selected for its ability to produce complex internal geometries (lattices, integrated cooling channels) that are unmachinable.
- **Benefit:** Rapid iteration of the structural bracket (`BRK-001`) with topology optimization.
- **Constraint:** Surface finish requires secondary CNC machining on mating faces to reach IT7/IT10 standards.

### 2.2 CNC (7075-T6 Aluminium) - Phase 2 / Production
Reserved for parts requiring high fatigue resistance and precise tolerances.
- **7075-T6 Rationale:** Highest strength-to-weight ratio for aluminium alloys, critical for the high-G launch forces from the compressed air system.
- **IT7/IT10 Strategy:** Critical interfaces (launcher rails, motor seats) are specified at IT7 (±0.015mm) to ensure repeatable launch ballistics. Non-critical structural elements use IT10 (±0.05mm) to reduce manufacturing cost.

### 2.3 Sacrificial Engineering: SABOT-001
The `SABOT-001` is designed as a **sacrificial wear item**.
- **Role:** Protects the drone's primary airframe from friction and thermal shock during the compressed air release.
- **Material:** FDM ASA (Acrylonitrile Styrene Acrylate) for high UV resistance and impact strength, enabling low-cost replacements between sorties.

## 3. BOM Lifecycle & ISO 9001 Traceability
- **Level 1 (BOM_BASELINE):** The "Frozen" executive view.
- **Level 2 (BOM_consolidee):** The "Operational" view for assembly and manufacturing agents.
- **Level 3 (gen_geometry):** The "Parametric" view. Changes to geometry scripts automatically trigger BOM mass updates.

## 4. Maintenance & Recoverability
The Interceptor_M is designed for **80% recoverability** (Line DI). The modular PDB/ESC and Flight Controller are independent assemblies to allow quick field replacement after a successful kinetic intercept.

---
*Authored by Jules (Lead Designer) for G2 Readiness.*
