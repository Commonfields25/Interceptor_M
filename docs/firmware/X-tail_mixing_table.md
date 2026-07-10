# X-Tail Mixing Table (60°/30° Asymmetric)

## 1. Output Mapping
| Servo ID | Surface | Orientation | Function |
| :--- | :--- | :--- | :--- |
| XTAL-005 | UR | +60° | Pitch/Roll |
| XTAL-006 | UL | +60° | Pitch/Roll |
| XTAL-007 | LR | -30° | Yaw/Roll |
| XTAL-008 | LL | -30° | Yaw/Roll |

## 2. Mixing Matrix
| Input | UR (005) | UL (006) | LR (007) | LL (008) |
| :--- | :---: | :---: | :---: | :---: |
| **Pitch** | +1.0 | +1.0 | 0.0 | 0.0 |
| **Yaw** | 0.0 | 0.0 | +1.0 | -1.0 |
| **Roll** | +0.5 | -0.5 | +0.5 | -0.5 |

## 3. Transition Logic (Tilt-Rotor)
- **VTOL Mode**: Tilt @ 0°. Roll/Pitch handled by differential thrust. X-tail active for yaw.
- **Cruise Mode**: Tilt @ 90°. Ailerons handle roll. X-tail handles pitch and yaw via the mixing matrix above.
