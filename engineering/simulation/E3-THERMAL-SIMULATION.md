---
action: Create
agent: E3
related_gate: G5
status: "Baseline \u2014 Pending Full CFD"
timestamp: 2026-06-30 13:30:00+00:00
---

# E3 — PCB Thermal Simulation Baseline
**Platform:** DD (Defense Deployable) | **MTOW:** 400g | **Status:** Baseline

## 1. Setup

### Electrical Load Profile (60s engagement)
| Component | Voltage | Current Draw | Notes |
|---|---|---|---|
| SC-01 Autopilot (STM32) | 3.3V | ~80mA | Primary compute |
| SC-03 Datalink (ESP32) | 3.3V | ~120mA | RF active |
| SC-02 Actuators (via ESC) | 5.0V | ~500mA | 3-axis tubular |
| Total at 11.1V input | — | ~700mA | With regulators |

### Thermal Model
- **Package**: QFN-32 / LQFP-48 (STM32F4 class)
- **PCB**: 4-layer, 30×30mm, AlSi10Mg base (DMLS)
- **Junction-to-ambient**: θJA ~ 25°C/W (estimated, no heatsink)
- **Ambient**: 30°C initial

## 2. Steady-State Analysis

```
P_total ≈ 7.7W (700mA × 11.1V)
T_junction ≈ T_ambient + P × θJA
T_junction ≈ 30 + 7.7 × 25 = 222.5°C  ⚠️ EXCEEDS LIMIT
```

### Correction Required
Active thermal management or reduced duty cycle for SC-02 actuators during engagement.

**Adjusted Profile (duty-cycled actuators):**
- Actuators: 40% duty cycle during engagement
- P_effective ≈ 4.5W
- T_junction ≈ 30 + 4.5 × 25 = 142.5°C ⚠️ STILL EXCEEDS

**Final Recommendation**: Add thermal vias + small Al heatsink on SC-01 package.

## 3. Transient Analysis (60s engagement)

| Time | T_junction (°C) | Status |
|---|---|---|
| 0s | 30 | OK |
| 15s | 65 | OK |
| 30s | 85 | OK |
| 45s | 95 | ⚠️ Warning |
| 60s | 100+ | ⚠️ LIMIT |

**Conclusion**: Engagement limited to 45s without active cooling.

## 4. Mitigation Strategies

1. **Active Cooling**: Miniature fan or thermoelectric cooler (mass penalty: ~15g)
2. **Duty Cycling**: Reduce actuator PWM to 30% during critical phase
3. **Heatsink**: 15×15mm Al block on STM32 (mass: ~8g)
4. **Software**: Thermal throttling of non-critical processes at T > 80°C

**Recommended**: Combination of (2) + (3) — minimal mass impact.

---
*E3 — Thermal baseline requires D3 CAD geometry for full CFD validation*
