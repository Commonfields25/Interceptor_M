---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# Flight Controller (FC) - Detailed Schematic Summary
**Version:** 1.0
**Project:** Interceptor_M

## 1. Power Architecture
- **Input:** 5V from PDB via Header P1.
- **Filtering:** 10uF + 100nF decoupling on all VDD rails.
- **LDO:** Integrated 3.3V LDO for MCU and sensors.

## 2. MCU: STM32H743VIT6
- **Clock:** 24MHz External Crystal.
- **Debug:** SWD Interface on Header J2.
- **Interfaces:**
  - SPI1: ICM-42688-P (IMU)
  - SPI2: MicroSD (Blackbox)
  - I2C1: BMP388 (Baro)
  - USART1: RX/TX for Receiver (ELRS/Crossfire)
  - USART2: GPS (M10)

## 3. Netlist Summary (Critical Pins)
| Pin | Function | Target |
|---|---|---|
| PA5 | SPI1_SCK | IMU |
| PA6 | SPI1_MISO | IMU |
| PA7 | SPI1_MOSI | IMU |
| PB6 | I2C1_SCL | Baro |
| PB7 | I2C1_SDA | Baro |
| PC10 | UART3_TX | ESC Telemetry |

---
*Generated for Design Review G2*
