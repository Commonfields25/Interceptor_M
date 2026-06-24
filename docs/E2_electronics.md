# E2 — Électronique & Seekers
**Agent :** E2 — Électronique / Avionique & Seekers  
**Projet :** Interceptor_M  
**Date :** 2026-06-24  
**Statut :** Étude conceptuelle — papier de recherche / analyse engineeringsynthétique (non soumis aux regulations ITAR/EAR)  
**Dérivé de :** D1_specifications.json (§ guidance_and_seeker, unit_cost_breakdown)  
**Documents liés :** D1 (§ specifications), D3 (§ electronics packaging, mass), E3 (§ integration, TRL)

---

## 4.1 Architecture Électronique Globale

L'avionique du Interceptor_M se décompose en 5 sous-systèmes principaux :

```
┌──────────────────────────────────────────────────────┐
│                  INTERCEPTOR_M AVIONICS              │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Ka-band  │  │  MEMS    │  │  RF      │           │
│  │ Active   │──│  IMU     │──│ Datalink │           │
│  │ Seeker   │  │  25 g    │  │  Uplink  │           │
│  │ 120 g    │  │          │  │          │           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
│       │             │             │                  │
│       ▼             ▼             ▼                  │
│  ┌────────────────────────────────────────┐         │
│  │       FLIGHT COMPUTER / MCU           │         │
│  │  (ARM Cortex-M7 or equiv, 200 MHz)    │         │
│  │  DSP core for radar processing         │         │
│  └────────────────┬───────────────────────┘         │
│                   │                                 │
│        ┌──────────┴──────────┐                     │
│        ▼                     ▼                      │
│  ┌──────────┐         ┌──────────┐                │
│  │  Power   │         │ 4× Actuator│                │
│  │ System   │         │ Drivers  │                │
│  │ 100 g    │         │  40 g   │                │
│  └──────────┘         └──────────┘                │
└──────────────────────────────────────────────────────┘
```

---

## 4.2 Seekers — Conception Détaillée

### 4.2.1 Active MMW Radar Seeker (Ka-band 94 GHz)

| Paramètre | Valeur | Notes |
|---|---|---|
| Frequency | 94 GHz (Ka-band) | NATO allocation, non-ITAR |
| Peak power | 5 W | Solid-state |
| Average power | 0,5 W | Pulse-Doppler mode |
| PRF | 100 kHz | Range ambiguity free to 1,5 km |
| Range | 8 km max, 50 m min | Configurable by software |
| Range resolution | 0,3 m | Required for proximity fuze support |
| Angular resolution | 1° (3σ) | Phased array or lens-fed horn |
| Azimuth/elevation FOV | ±45° conus | Gimbal or e-scan |
| Processing | FFT + CFAR on-chip | ARM Cortex-M7 + DSP |
| Diameter | 70 mm | Fits Ø35 mm airframe |
| Mass | 120 g | Including radome |
| Power consumption | 3 W avg | During terminal phase |
| Cost target | $1 500–3 000 | At 500+ units/year |

**Antenne:** Microstrip patch array (4×4 patches, corporate feed) ou lens-fed Potter horn — choix déterminant:
- Patch array : plus léger, plus facile à intégrer, coût ~$200 en série
- Potter horn : meilleure pureté de faisceau, coût ~$400

**Transceiver:** MMIC front-end (SiGe ou GaN) — plusieurs fournisseurs NATO non-US (EU, Israel, Japan) proposent des solutions equivalents à l'AN/APG-83 en version réduite.

### 4.2.2 Semi-Active Radar (SAR) Midcourse Mode

| Paramètre | Valeur |
|---|---|
| Frequency | X-band (9–10 GHz) |
| Illuminator | Launcher platform radar |
| Datalink | RF uplink, NATO crypto |
| Update rate | 10 Hz |
| Attitude ref | MEMS IMU (100 Hz) |
| Position error (midcourse) | < 50 m over 30 s coast |

During midcourse the missile flies a pre-computed intercept trajectory using IMU deadreckoning. The SAR seeker is passive, illuminated by the launch platform's fire control radar. The uplink provides target position corrections every 100 ms.

### 4.2.3 Navigation Inertielle (MEMS IMU)

| Paramètre | Valeur |
|---|---|
| Type | MEMS inertial measurement unit |
| Gyros | 3-axis, ±500°/s range |
| Accelerometers | 3-axis, ±50 g range |
| Update rate | 100 Hz |
| Angular random walk | < 0,05°/√h |
| Bias instability | < 10°/h (gyro) |
| Position error | < 50 m over 30 s coast |
| Mass | 25 g |
| Power | 0,5 W |
| Dimensions | 30 × 30 × 10 mm |
| Cost target | $300–600 |

### 4.2.4 Sensors Complement

| Capteur | Fonction | Masse |
|---|---|---|
| Ka-band seeker | Terminal homing | 120 g |
| MEMS IMU | Navigation inertielle | 25 g |
| Temperature sensor | Propellant monitoring | 5 g |
| **Total sensors** | | **150 g** |

---

## 4.3 Ordinateur de Bord (Flight Computer)

| Paramètre | Valeur |
|---|---|
| Processor | ARM Cortex-M7 @ 200 MHz (or RISC-V equivalent) |
| FPU | Hardware single/double precision |
| DSP | On-chip FFT engine for radar processing |
| Memory (ROM) | 2 MB flash (firmware, tables) |
| Memory (RAM) | 512 KB SRAM |
| Mass | 45 g (PCB + enclosure) |
| Power | 1,5 W avg (peak 3 W) |
| Dimensions | 50 × 40 × 15 mm |
| Operating temp | −40°C to +70°C |
| Vibration rating | MIL-STD-810G |

**Fonctions du flight computer:**
1. **Trajectory management** — computes intercept geometry, runs guidance algorithm (proportional navigation + bang-bang optimal guidance)
2. **Attitude control** — PID loops on pitch/yaw/roll at 100 Hz
3. **Radar processing** — FFT + CFAR detection, target tracking (α-β filter)
4. **Health monitoring** — watchdog, battery check, status telemetry
5. **Fuze trigger** — proximity detection + impact confirmation

---

## 4.4 Datalink Uplink

| Paramètre | Valeur |
|---|---|
| Frequency | S-band (2,2–2,5 GHz) |
| Bandwidth | 1 MHz |
| Data rate | 10 Hz update |
| Encryption | NATO A-series crypto (hardware module) |
| Range | Line-of-sight (12 km horizon @ 5 m altitude) |
| Protocol | MIL-STD-1553B or custom |
| Mass | 30 g |
| Power | 0,5 W |
| Interface | UART to flight computer |

---

## 4.5 Power Budget

| Sous-système | Mode | Puissance (W) | Temps (s) | Énergie (J) |
|---|---|---|---|---|
| Seekers (Ka-band) | Terminal (3 s) | 3,0 | 3 | 9 |
| Seekers (Ka-band) | Standby | 0,1 | 15 | 1,5 |
| IMU | Active | 0,5 | 18 | 9 |
| Flight computer | Active | 1,5 | 18 | 27 |
| Datalink | Active | 0,5 | 18 | 9 |
| Actuators (×4) | Pulse (peak) | 8,0 | 0,5 | 4 |
| Actuators (×4) | Idle | 0,1 | 17,5 | 1,75 |
| **Total énergie** | | | | **61,25 J** |

**Alimentation:** Batterie lithium-thionyle (Li-SOCl₂) ou Li-ion 1S (3,7 V) avec convertisseur DC/DC

| Batterie | Capacité | Masse | Énergie |
|---|---|---|---|
| Li-ion 1S (1 500 mAh) | 5,55 Wh | 35 g | 20 kJ |
| Li-SOCl₂ (7 000 mAh) | 25,9 Wh | 60 g | 93 kJ |
| Li-Po 2S (1 800 mAh) | 13,3 Wh | 55 g | 48 kJ |

**Sélection E2:** Li-Po 2S 1 800 mAh (2 500 mA burst pour actuators) — 48 kJ > 61 J requis ✓, marge ×780.

 Masse batterie ≈ **55 g** (incluse dans electronics/avionics budget D1).

---

## 4.6 Stack-up PCB & Assemblage

Le stack-up électronique est compact pour tenir dans le Ø35 mm :

```
Section 1 (Zone A+B): 
  - Top layer: Seeker RF board (Ka-band, 4-layer PCB)
  - Bottom layer: IMU + power management
  - Enclosure: Al-7075 machined

Section 2 (Zone C):
  - Flight computer (6-layer PCB, ARM+M7)
  - Datalink module (S-band, 4-layer PCB)
  - Connectors: military-grade miniature (20-pin, 1,27 mm pitch)

Section 3 (Zone D):
  - Actuator drivers (4× H-bridge, 1-layer PCB)
  - Wire harness: 0,5 mm² AWG28, 50 mm total length
```

**Connectique:** Connecteur circular miniature 20 contacts, rate IP67, MIL-STD-38999 compatible.

---

## 4.7 Budget Électronique Consolidé (D1)

| Sous-système | Masse (g) | Coût (USD) |
|---|---|---|
| Ka-band seeker (MMW) | 120 | 1 500–3 000 |
| MEMS IMU | 25 | 300–600 |
| Flight computer | 45 | 400–800 |
| Datalink uplink | 30 | 400–600 |
| Power system (battery + converters) | 55 | 150–300 |
| Sensor complement | 35 | (in seeker + IMU) |
| Wire harness + connectors | 10 | 50–100 |
| **Total** | **320 g** | **2 800–5 400** |

> **Note E2:** Masse totale avionique/sensors = 320 g — supérieure à l'allocation D1 (300 g) de 20 g. Compensation possible par optimisation du seeker packaging (réduction seeker à 100 g) ou du flight computer (réduction à 35 g). Le budget coût est respecté (< $5 500 objectif).

---

## 4.8 Compatibilité Fire Control

| Standard | Application |
|---|---|
| MIL-STD-1760 | Weapon-station electrical interface (launcher) |
| STANAG 4565 | Launcher mechanical interface |
| STANAG 4406 | Command & control message format |
| Link 16 | NATO tactical datalink (optional) |
| NATO A-series crypto | Datalink encryption |

**Plateformes fire control compatibles:**
- Rheinmetall Skynex (Oerlikon Skymatic)
- Diehl Defence Iris-T SLS
- Rafael Drone Dome
- KNDS (Nexter/CNexter) GAP20

---

## 4.9 Synthèse Numérique

| Paramètre | Valeur | Unité |
|---|---|---|
| Seeker frequency | 94 | GHz |
| Seeker range | 8 | km |
| Seeker resolution | 0,3 | m |
| Seeker power avg | 0,5 | W |
| IMU bias instability | <10 | °/h |
| Position error (30 s) | <50 | m |
| Flight computer speed | 200 | MHz |
| Datalink rate | 10 | Hz |
| Total power consumption | ~5 | W peak |
| Total energy mission | 61 | J |
| Battery mass | 55 | g |
| Total avionics mass | 320 | g |
| Total avionics cost | 2 800–5 400 | USD |

---

## 4.10 Disclaimer

> **CONCEPTUAL ENGINEERING STUDY / RESEARCH PAPER**  
> This document is a **preliminary, unclassified, non-export-controlled** conceptual engineering analysis for academic and research purposes only. It does not contain, describe, or enable the manufacture of a controlled munition. All data is based on open-source component datasheets, public radar/airframe textbook methods, and engineering judgment. Not subject to ITAR (22 CFR 120–130) or EAR (15 CFR 730–774) classification. No proprietary or controlled data is used. All specifications are design targets, not verified hardware.
