# Interceptor_M - Electronics & Systems Schematics

## 1. Component Overview
- **Flight Controller:** STM32H7 based, integrated IMU (ICM-42688-P) and Baro (BMP388).
- **Power Distribution:** Integrated 4-in-1 ESC (TPH1R204PL MOSFETs) and 5V Switching Regulator.
- **Payload Interface:** Modular UART/I2C headers for Seeker (IR/EO).

## 2. Traceability (Generated Files)
| Assembly | Schematic Path | Gerber Directory |
|---|---|---|
| Flight Controller | `engineering/electronics/Flight_Controller_schematic.json` | `engineering/electronics/Flight_Controller_gerbers/` |
| PDB / ESC | `engineering/electronics/PDB_ESC_Integrated_schematic.json` | `engineering/electronics/PDB_ESC_Integrated_gerbers/` |

## 3. Architecture Diagrams
(Refer to the Mermaid diagrams in previous versions of this document for high-level logic flow.)
