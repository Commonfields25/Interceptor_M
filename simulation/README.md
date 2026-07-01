# Interceptor_M Physics & Simulation Package

This package provides a high-fidelity 6-DOF simulation environment for the Interceptor_M drone (DD-400 baseline).

## Current Architecture: Electric & Pneumatic

The simulation implements the project's actual physical paradigm:
1.  **Compressed Air Launch**: High initial exit velocity ($V_{launch} = 70 \text{m/s}$) representing the pneumatic tube launch.
2.  **Electric Dash Propulsion**: A constant-mass model ($400\text{g}$) with an electric motor providing dash thrust ($8\text{N}$) and battery energy tracking ($50\text{kJ}$).
3.  **Atmosphere**: Full **International Standard Atmosphere (ISA)** model for tropospheric density and speed of sound.
4.  **Aerodynamics**: Mach-dependent drag ($C_x(M)$) including transonic rise.

## Guidance & Filtering

*   **3D Guidance**: Choice between standard Proportional Navigation (**PN**) and Augmented Proportional Navigation (**APN**).
*   **3rd-Order Kalman Filter**: Estimates LOS rates from noisy, latent seeker measurements.
*   **Seeker Simulation**: Includes a $\pm60^\circ$ Field-of-Regard (FOR) limit.

## Running the Simulation

*   **System Performance Analysis**: `python3 -m simulation.montecarlo_pintercept`
    *   Generates a detailed `PHYSICS_PERFORMANCE_REPORT.md` in `docs/analysis/`.
    *   Exports raw telemetry to `simulation/exports/`.

## Requirements
*   `numpy`
