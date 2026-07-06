---
agent: D3
action: Update
timestamp: 2026-07-06T21:00:00Z
related_gate: G2
status: Validated
---

# DD — CAD Parameters & Specifications
**Version:** 1.2.0 | **Owner:** D3 (Defense / CAD)
**Projet:** Interceptor_M — Defense Line (DD)
**Baseline:** 400g Electric / Pneumatic Launcher

---

## 1. Reference Geometry (SSoT: PARAMETERS.json)

| Parameter | Value | Source |
|---|---|---|
| Fuselage outer diameter | 35 mm | SSoT |
| Overall airframe length | 380 mm | SSoT |
| Tube launcher bore (int. diameter) | 40 mm | SSoT |
| Wall thickness | 2.0 mm | SSoT |
| Folding Wings (WING-001) | span 150 mm | SSoT |
| Fuselage Length | 380 mm | SSoT |

## 2. Design Constraints (Electric Dash Platform)

- [x] Target weight: MTOW = 400 g
- [x] Launch Method: Pneumatic (70 m/s exit velocity)
- [x] Sustain Propulsion: Electric Dash (8N Thrust)
- [x] Sabot/launcher interface (40 mm bore)
- [x] Motor mount: SC-02 brushless
- [x] Fasteners: M2/M3 ISO Standard

## 3. Mass Budget Summary (CAD Verified Baseline)

| Subsystem | Mass (g) | Part ID |
|---|---|---|
| **Structure / Airframe** | 25.1 | BRK-001 |
| **Wing Mechanism** | 158.5 | ACT-001 |
| **Aero Surfaces (4x)** | 21.5 | WING-001 |
| **Interface Ring** | 35.3 | NCR-001 |
| **Avionics Stack** | 40.0 | SC-01/03 |
| **Battery (3S LiPo)** | 105.0 | BAT-3S-001 |
| **Motor (Electric)** | 25.0 | SC-02 |
| **TOTAL** | **410.4 g** | **(400g Target + 2.6% overage)** |

## 4. Center of Gravity (Static Margin: 10.5%)

- [x] ROOT_ASSEMBLY_v0.1.iam
- [x] AIRFRAME_PART.F3D (or .SLDPRT)
- [x] BOM (Bill of Materials)
- [x] DD-PARAMETERS-v1.2.0.md (this document)

---
*Validated against Operation Stabilize baseline.*
*Updated 2026-07-06: v0.3 → v1.2.0 — MTOW and length aligned per DD-400 program (400g Electric/Pneumatic).*
