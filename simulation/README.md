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

## Advanced Improvements (Wave 8)

1.  **Aerodynamics**: Added **Mach-dependent drag** coefficient with transonic rise and supersonic decay.
2.  **Propulsion**: Implemented a **Boost-Sustain** thrust profile (60N boost / 20N sustain).
3.  **Guidance**: Added **Augmented Proportional Navigation (APN)** to compensate for target acceleration.
4.  **Targeting**: Implemented **Weaving (sinusoidal)** evasive maneuvers.
5.  **Filtering**: Enhanced the Kalman Filter to 3rd order (position, velocity, acceleration) and added simulation of **measurement noise and seeker latency**.

## Performance Comparison
The upgrade from PN to APN shows a significant improvement in intercept probability (89% vs 82%) and a reduction in average miss distance against complex maneuvers.
