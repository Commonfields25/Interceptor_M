# Airfoil Datasheet: NACA 4412

## 1. Profile Description
- **Type**: 4-digit NACA airfoil
- **Max Camber**: 4% at 40% chord
- **Max Thickness**: 12% at 30% chord
- **Target Platform**: Interceptor V3-1600 (1600mm span, 6kg MTOW)

## 2. Aerodynamic Coefficients (@ Re = 1.0e6)
| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Cl_max** | 1.5 | Maximum lift coefficient |
| **Cl_alpha** | 0.11 / deg | Lift curve slope |
| **Cd0** | 0.007 | Zero-lift drag coefficient |
| **Cm0** | -0.09 | Pitching moment at zero lift |
| **Stall Angle** | 14° | Angle of attack at stall |

## 3. Reynolds Number Calculation
- **Velocity (Cruise)**: 97 m/s
- **Chord (Avg)**: 0.200 m
- **Kinematic Viscosity (Air, SL)**: 1.46e-5 m²/s
- **Re** = (V * c) / ν = (97 * 0.2) / 1.46e-5 ≈ **1.33e6**

## 4. Geometry coordinates (Summary)
Generated via standard NACA 4-digit formula. Leading edge radius: 1.58% chord.
