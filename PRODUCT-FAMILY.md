# Interceptor_M — Product Family Overview

**Strategy:** Common-platform modular product family
**Version:** 1.1 — DI BOM locked · All lines geometrically characterised
**Date:** 2026-06-28

---

## 1. Strategic Rationale

Shared platform strategy maximises reuse across three market segments
(Defense, Industrial, Civil) while preserving line-specific differentiation
in airframe scale, payload, and certification envelope.

| Dimension | Benefit |
|-----------|---------|
| Non-recurring engineering (NRE) | ~40 % vs independent designs |
| Component supply chain | Single source, volume pricing |
| Software / mission stack | Universal across DD / DI / DC |
| Certification | Platform commonality simplifies DO-178C argument |

---

## 2. Product Lines

| Line | Market         | Priority | MTOW (g) | Fuselage LxWxH (mm) | Wing Span (m) | Wall (mm) | Status |
|------|----------------|----------|----------|---------------------|---------------|-----------|--------|
| DD   | Defense        | High     | 400      | 444.45x210.53x111.11 | 1.754       | 2.530   | Active |
| DI   | Industrial     | High     | 300      | 403.81x191.28x100.95 | 1.594       | 2.191   | **BOM locked** |
| DC   | Civil          | Medium   | 250      | 380.00x180.00x95.00  | 1.500       | 2.000   | Active |

> **DI BOM Status:** Final. No changes without formal ECR (Engineering Change Request) + DG approval.

---

## 3. Module Architecture Matrix

| Module                  | DD | DI | DC | Shared across |
|-------------------------|----|----|----|---------------|
| Autopilot / FC board    | yes | yes | yes | **All lines** |
| Propulsion brick (motor+ESC) | yes | yes | yes | **All lines** |
| Datalink / RF modem     | yes | yes | yes | **All lines** |
| Software stack (GCS, nav, MAVLink) | yes | yes | yes | **All lines** |
| Ground Control Station  | yes | yes | yes | **All lines** |
| Launcher interface      | yes | yes | --  | DD + DI        |
| Airframe (line-specific) | yes | yes | yes | Line-specific |
| Payload (line-specific) | yes | yes | yes | Line-specific |

### 3.1 Shared Platform Modules (SC Registry)

#### SC-01 - Autopilot / Flight Controller Board
| Field | Value |
|-------|-------|
| **Component ID** | SC-01 |
| **Power** | 5 V / 3.3 V rails, ~200 mW idle |
| **Dimensions** | < 30 x 30 x 10 mm |
| **Interface** | PWM / CAN / UART |
| **TRL** | 4-5 (lab breadboard) |
| **Owner** | E3 |

#### SC-02 - Propulsion Brick (Motor + ESC Assembly)
| Field | Value |
|-------|-------|
| **Component ID** | SC-02 |
| **Power** | 50-150 W (sizing per D2 CFD) |
| **Attachment** | 3x M3 socket-head screws |
| **TRL** | 4 |
| **Owner** | E1 / D1 |

#### SC-03 - Datalink / RF Modem
| Field | Value |
|-------|-------|
| **Component ID** | SC-03 |
| **Interface** | UART (MAVLink or proprietary) |
| **Range** | > 5 km LOS (DD/DI); > 2 km (DC) |
| **TRL** | 4 |
| **Owner** | E2 |

#### SC-04 - Mission Software Stack
| Field | Value |
|-------|-------|
| **Component ID** | SC-04 |
| **Languages** | C / C++ / Python (sim only) |
| **TRL** | 4-5 |
| **Owner** | E3 |

#### SC-05 - Ground Control Station
| Field | Value |
|-------|-------|
| **Component ID** | SC-05 |
| **Interface** | IP (wired/wifi) or RF serial |
| **TRL** | 3 |
| **Owner** | E3 |

#### SC-06 - Launcher Interface
| Field | Value |
|-------|-------|
| **Component ID** | SC-06 |
| **Mechanical** | Tube bore 40 mm (DD/DI); TBD (DC) |
| **TRL** | 4 |
| **Owner** | D3 |

### 3.2 Line-Specific BOM Summaries

#### DD - Defense (MTOW 400 g)
| Part ID | Description | Material | Mass (g) |
|---------|-------------|----------|----------|
| BRK-001 | Structure primaire - Coque fuselage +支弍 | AlSi10Mg (DMLS) | 178.85 |
| ACT-001 | Verin tubulaire 3 axes | AlSi10Mg (DMLS) | 55.49 |
| NCR-001 | Carenage aero - Coque complexe | Nomex honeycomb + CF skins | 142.93 |
| **Total structural** | | | **377.27** |

#### DI - Industrial (MTOW 300 g) **BOM LOCKED**
| Part ID | Description | Material | Mass (g) |
|---------|-------------|----------|----------|
| BRK-001 | Structure primaire - Coque fuselage +支弍 | AlSi10Mg (DMLS) | 134.14 |
| ACT-001 | Verin tubulaire 3 axes | AlSi10Mg (DMLS) | 55.49 |
| NCR-001 | Carenage aero - Coque complexe | Nomex honeycomb + CF skins | 107.20 |
| **Total structural** | | | **296.83** |

#### DC - Civil (MTOW 250 g)
| Part ID | Description | Material | Mass (g) |
|---------|-------------|----------|----------|
| BRK-001 | Structure primaire - Coque fuselage +支弍 | AlSi10Mg (DMLS) | 111.78 |
| ACT-001 | Verin tubulaire 3 axes | AlSi10Mg (DMLS) | 55.49 |
| NCR-001 | Carenage aero - Coque complexe | Nomex honeycomb + CF skins | 89.33 |
| **Total structural** | | | | **256.60** |

---

## 4. Platform Differentiation Logic

```
              +-------------+
              |  PLATFORM   |  (common across all lines)
              |  CORE       |
              +-------------+
               /    |    \
              /     |     \
    +---------+ +----+----+ +---------+
    |   DD    | |    DI    | |   DC    |
    | Defense | |Industrial| |  Civil  |
    |  MTOW=400g  MTOW=300g  MTOW=250g
    +---------+ +----------+ +---------+
```

---

## 5. BOM Governance Rules

| Rule | Description |
|------|-------------|
| **DI BOM Lock** | DI structural parts are frozen as of 2026-06-28. Any change requires an ECR + DG approval. |
| **DD/DC Iterative** | DD and DC geometries are actively refined; BOM remains open pending D2/D3 CFD validation. |
| **SC Registry** | Shared components (SC-01 to SC-06) are versioned in `SHARED-COMPONENTS.md` and must not be silently substituted. |
| **DMLS Lots** | AlSi10Mg DMLS print batches must record lot number, machine ID, and build date on the traveller sheet. |
| **Mass Margins** | Structural mass must remain within +0% / -3% of BOM value. Exceedance triggers an NCR. |

---

## 6. Next Steps

| Action | Owner | Gate |
|--------|-------|------|
| Lock DC geometry (scale from DD/DI data) | D3 | DC-spec |
| Platform interface control document (ICD) | E3 | G3 |
| Common GCS development kickoff | E3 | G2 (DD) |
| Validate DI thermal margins (ACT-001 dissipation) | D2 | E2 |

---

## 7. Milestone Alignment

| MS | Title | DI BOM relevance |
|----|-------|-----------------|
| M5 | Branch Cleanup & Archive | - |
| M6 | CI Migration Node24 & Workflow Activation | Infrastructure only |
| **M7** | **DI Product Specifications Lock & BOM** | **Primary owner - BOM locked** |
| M8 | RL Environment Hardening & Agent Rebalancing | - |
| M9 | Recrutement Ingenieur Conception & Design Industriel | Personnel |

