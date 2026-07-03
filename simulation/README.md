---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# Interceptor_M Physics & Simulation Package

This package provides a 6-DOF (simplified) simulation environment for the Interceptor_M drone (DD-400 baseline).

## Improvements (Wave 7)

1.  **Atmosphere Model**: Implemented the **International Standard Atmosphere (ISA)** model, replacing the simple isothermal density model. Density, pressure, and temperature now vary with altitude according to standard tropospheric lapse rates.
2.  **Propulsion Model**: Added a time-varying **Motor Thrust** model with mass flow rate calculation. The interceptor's mass now decreases as propellant is consumed ($I_{sp} = 210s$), correctly affecting the Thrust-to-Weight Ratio and acceleration.
3.  **Target Maneuvers**: The target is no longer restricted to a straight line. It can now perform **maneuvers** such as constant-G turns, allowing for more realistic engagement scenarios.
4.  **Guidance & Filtering**:
    *   Implemented a **Linear Kalman Filter** (`kalman_filter.py`) to estimate the Line-of-Sight (LOS) rates from noisy measurements.
    *   Upgraded the Proportional Navigation (PN) guidance law to **3D PN** (`flight_control_poc.py`), using filtered LOS rates for both azimuth and elevation control.

## Running the Simulation

*   **Monte Carlo Analysis**: `python3 -m simulation.montecarlo_pintercept` evaluates the probability of interception over the E1 engagement envelope.
*   **Debug/Test Case**: `python3 -m simulation.debug_sim` runs a single engagement and prints the trajectory.
*   **Constants**: All physical and system constants are centralized in `constants.py`.

## Requirements
*   `numpy`
