# PDB & ESC - Detailed Schematic Summary
**Version:** 1.0
**Project:** Interceptor_M

## 1. Power Distribution
- **Main Input:** 2S-6S LiPo (XT60).
- **Current Sensing:** 0.5mOhm shunt resistor on negative rail.
- **BEC:** 5V/3A for Flight Controller and Peripherals.

## 2. ESC Logic (4-in-1)
- **Gate Drivers:** 4x Half-bridge drivers.
- **MOSFETs:** 12x TPH1R204PL (3 per phase).
- **Firmware:** BLHeli_32 compatible.

## 3. Interface Header
- **Pins:** VBAT, GND, CURR, TELEM, M1, M2, M3, M4.

---
*Generated for Design Review G2*
