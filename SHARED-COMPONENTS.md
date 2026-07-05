---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# Interceptor_M — Shared Components Registry

**Version:** 0.1 | **Owner:** E3 (Integration) | **Date:** 2026-06-27
**Family lines:** DD / DI / DC | **Status:** Initial registry

---

## Purpose

This document is the master registry of modular building blocks shared across the Interceptor_M product family. Each entry defines the interface, responsible agent, TRL, and applicable lines.

---

## SC-01 — Autopilot / Flight Controller Board

| Field | Value |
|-------|-------|
| **Component ID** | SC-01 |
| **Name** | Autopilot / Flight Controller |
| **Description** | Integrated IMU + barometer + MCU on single PCB; runs mission software stack |
| **Interface** | PWM (actuators), CAN (payload), UART (datalink) |
| **Power** | 5 V / 3.3 V rails, ~200 mW idle |
| **Dimensions** | < 30 x 30 x 10 mm |
| **Owner** | E3 |
| **TRL** | 4–5 (lab breadboard) |
| **Family lines** | DD, DI, DC |
| **Variant notes** | DI variant: extended temp range (−40 to +85 °C); DD variant: added SAASM/GPS-denied nav mode |

---

## SC-02 — Propulsion Brick (Motor + ESC Assembly)

| Field | Value |
|-------|-------|
| **Component ID** | SC-02 |
| **Name** | Propulsion Brick |
| **Description** | Brushless outrunner motor + integrated ESC; standardized mechanical mount |
| **Interface** | PWM input, 9 or 12 mm motor mount bore (PARAMETERS.json) |
| **Power** | 50–150 W (sizing per D2 CFD) |
| **Mechanical attachment** | 3x M3 socket-head screws |
| **Owner** | E1 / D1 |
| **TRL** | 4 |
| **Family lines** | DD, DI, DC |
| **Variant notes** | DC variant: lower power (shorter endurance, lighter load); DI variant: higher efficiency / fuel fraction TBD |

---

## SC-03 — Datalink Module

| Field | Value |
|-------|-------|
| **Component ID** | SC-03 |
| **Name** | Datalink / RF Modem |
| **Description** | UHF or S-band RF modem; bidirectional telemetry + command uplink |
| **Interface** | UART (MAVLink or proprietary) |
| **Encryption** | **Line-specific** — AES-128 (DC/DI), Type 1 NSA Suite B (DD) |
| **Range** | > 5 km LOS (DD/DI); > 2 km (DC) |
| **Owner** | E2 |
| **TRL** | 4 |
| **Family lines** | DD, DI, DC |
| **Variant notes** | DD: Type 1 crypto module mandatory; DC: may substitute LTE/IoT for non-critical telemetry |

---

## SC-04 — Software Stack (Mission Software)

| Field | Value |
|-------|-------|
| **Component ID** | SC-04 |
| **Name** | Mission Software Stack |
| **Description** | Flight control firmware + GCS communication + navigation + payload control |
| **Repository** | TBD (engineering/simulation/) |
| **Language** | C / C++ / Python (sim only) |
| **Owner** | E3 |
| **TRL** | 4–5 |
| **Family lines** | DD, DI, DC |
| **Variant notes** | DD adds: terminal guidance law (PN / APN), threat identification, kill-assessment; DC adds: camera gimbal control API |

---

## SC-05 — Ground Control Station (GCS)

| Field | Value |
|-------|-------|
| **Component ID** | SC-05 |
| **Name** | Ground Control Station |
| **Description** | Operator UI for mission planning, telemetry display, override control |
| **Interface** | IP (wired/wifi) or RF serial |
| **Owner** | E3 |
| **TRL** | 3 |
| **Family lines** | DD, DI, DC |
| **Variant notes** | DD: classified C2 interface; DC: commercial tablet-compatible UI |

---

## SC-06 — Launcher Interface (Sabot + Ring Set)

| Field | Value |
|-------|-------|
| **Component ID** | SC-06 |
| **Name** | Launcher Interface |
| **Description** | Sabot + retaining rings; standardized for 40 mm tube bore |
| **Interface** | Mechanical (tube bore 40 mm) |
| **Owner** | D3 |
| **TRL** | 4 |
| **Family lines** | DD, DI (tube-launched); DC (TBD) |
| **Variant notes** | DI: enlarged sabot for larger airframe TBD |

---

## Registry Maintenance

| Rule | Description |
|------|-------------|
| **Adding a component** | Create new SC-XX entry; assign ID sequentially; update family lines field |
| **Changing an interface** | Requires ICD update; notify all affected line owners |
| **Deprecating a component** | Mark `[DEPRECATED vX.X]` in header; do not delete from registry |
| **Versioning** | Update `**Version:**` and `**Date:**` on each change |

---

*Maintained by E3 (Integration). Coordinate with E1 (systems), D1/D2 (platform sizing), and line owners before modifying shared interfaces.*
