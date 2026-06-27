# Interceptor_M — Product Family Overview

**Version:** 0.1 | **Owner:** Product Management | **Date:** 2026-06-27
**Strategy:** Common-platform modular product family

---

## 1. Strategic Rationale

Rather than developing three isolated products, Interceptor_M adopts a **platform commonality strategy**: a shared set of core modules reduces non-recurring engineering cost, shortens time-to-market for each line, and simplifies logistics, training, and support.

This document defines the product family matrix, identifies shared vs. line-specific modules, and guides per-line development decisions.

---

## 2. Product Lines

| Line | Market | Priority | MTOW | Length | Status |
|------|--------|----------|------|--------|--------|
| **DD** | Defense / NATO C-UAS / SHORAD | P1 | 400 g | 380 mm | G2 in progress |
| **DI** | Industrial / critical infrastructure | P2 | TBD | TBD | Concept |
| **DC** | Civil / photo / delivery / agri | P3 | 250 g | TBD | Concept |

*DD specs locked per DEC-007. DC/DI specs pending market study and NDC development.*

---

## 3. Module Architecture Matrix

| Module | DD (Defense) | DI (Industrial) | DC (Civil) | Shared? |
|--------|-------------|-----------------|------------|---------|
| **Avionics / Flight Controller** | Yes | Yes | Yes | **Shared** |
| **Propulsion brick** | Yes | Yes | Yes | **Shared** |
| **Datalink / comms** | Yes | Yes | Yes | **Shared** |
| **Software stack** | Yes | Yes | Yes | **Shared** |
| Airframe | Sized for 400 g | Sized for TBD | Sized for 250 g | Line-specific |
| Payload | Warhead + seeker | Neutralisation payload | RGB / multispectral camera | Line-specific |
| MTOW / performance | 400 g / 380 mm | TBD | 250 g / TBD | Line-specific |

### 3.1 Shared Platform Modules

#### Avionics / Flight Controller
- Autopilot board (IMU, baro, MCU)
- Interfaces: PWM / CAN / UART
- Hosted software: mission stack (see SHARED-COMPONENTS.md)
- **DI note:** hardened to industrial temp range (−40 to +85 °C)

#### Propulsion Brick
- Integrated motor + ESC assembly
- Standardized mechanical interface (9/12 mm mount per PARAMETERS.json)
- Propeller / nozzle attachment: line-specific (D2 to size per CFD)
- **DI note:** extended endurance variant (TBD fuel fraction)

#### Datalink
- RF modem (UHF / S-band)
- Standard API: MAVLink or proprietary
- Encryption: **line-specific** — DD requires Type 1 crypto (NSA suite B); DI/DC use standard AES-128
- **DC note:** may use commercial LTE/satellite IoT for non-critical telemetry

#### Software Stack
- Ground Control Station (GCS) interface
- Flight mode state machine
- Navigation (INS/GNSS hybrid; GPS-denied mode for DD)
- Payload control interface
- OTA update capability
- **Note:** DD software adds: threat ID, terminal guidance law, kill-assessment

### 3.2 Line-Specific Modules

#### Airframe
- DD: 35 mm od x 380 mm L, tube-launched, delta wings + cruciform fins
- DI: Derived from DD airframe with enlarged volume for extended payload; length scaled proportionally
- DC: Lighter, smaller, simplified folding wing

#### Payload
- DD: Multi-mode seeker (RF+IR dual-mode preferred) + warhead (~45 g allocation per DD-CONCEPT.md)
- DI: Neutralisation payload (TBD type/mass; industrial mission TBD)
- DC: RGB camera or multispectral sensor (~50–100 g)

---

## 4. Platform Differentiation Logic

```
              +-------------+
              |  PLATFORM   | (common across all lines)
              |  CORE       |
              +-------------+
               /    |    \
              /     |     \
    +---------+ +----+----+ +---------+
    |   DD    | |    DI    | |   DC    |
    | Defense | |Industrial| |  Civil  |
    +---------+ +----------+ +---------+
```

Each line differentiates at the **payload** and **airframe scale** level. All lines share the same flight controller, propulsion, datalink, and software base — minimising per-line development cost.

---

## 5. Next Steps

| Action | Owner | Gate |
|--------|-------|------|
| Lock DI performance requirements | E1 + Marketing | DI-NDC |
| Lock DC geometry (scale from DD) | D3 | DC-spec |
| Platform interface control document (ICD) | E3 | G3 |
| Common GCS development kickoff | E3 | G2 (DD) |

---

*This document is maintained by the Product Management function. Any per-line spec changes must be reflected here and in the relevant line parameter file.*
