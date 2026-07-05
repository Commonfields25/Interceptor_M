---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# Interceptor_M — Product Family Overview

**Strategy:** Common-platform modular product family
**Version:** 1.2.0 — Parameters synchronized to DD-400 baseline
**Date:** 2026-07-01

---

## 1. Product Strategy

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
| DD   | Defense        | High     | 400.0    | 380.0x200.0x100.0   | 0.150         | 2.0       | Active |
| DI   | Industrial     | High     | 300.0    | 365.0x180.0x90.0    | 0.135         | 1.8       | **BOM locked** |
| DC   | Civil          | Medium   | 250.0    | 350.0x160.0x80.0    | 0.120         | 1.5       | Active |

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

---

## 4. Governance Rule: SPEC LOCK
As of version 1.2.0, the MTOW and Fuselage dimensions for all three lines (DD, DI, DC) are **locked**. Any changes require a formal ECR (Engineering Change Request) and DG approval.

---

## 5. Milestone Alignment

| MS | Title | DI BOM relevance |
|----|-------|-----------------|
| M7 | **DI Product Specifications Lock & BOM** | **Primary owner - BOM locked** |
| M8 | RL Environment Hardening & Agent Rebalancing | - |
| M9 | Recrutement Ingenieur Conception & Design Industriel | Personnel |
