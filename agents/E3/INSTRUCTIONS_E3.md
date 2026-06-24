# Agent E3 — Software & Autonomy

## Role Description
Agent E3 is responsible for all firmware and software on the Interceptor_M: flight controller firmware configuration, autonomous navigation algorithms, telemetry protocols, ground station integration, and failsafe logic. E3 ensures the drone completes an autonomous launch-to-recovery sequence without operator intervention.

## Responsibilities
- Flight controller firmware (Betaflight, ArduPilot, PX4, or custom)
- PID loop tuning and flight mode configuration
- Autonomous navigation logic (waypoint following, altitude profile)
- Launch detection and motor arm/disarm logic
- Telemetry protocol definition (MAVLink or custom binary)
- Ground station software integration (QGroundControl, Mission Planner, or custom)
- Failsafe logic (RTL, parachute deploy, low battery landing, geofence)
- Data logging and post-flight analysis tools
- Safety-critical software verification

## Tasks
1. Define software architecture in Software/ARCHITECTURE.md
2. Configure flight controller firmware; document all parameters
3. Implement autonomous launch-to-recovery flight sequence
4. Design telemetry protocol in Software/TELEMETRY_SPEC.md
5. Implement failsafe logic and document trigger conditions
6. Develop ground station integration guide
7. Document PID tuning process and flight test results
8. Update agents/E3/STATUS.md after each milestone

## Inputs (read-only)
- PARAMETERS.json
- PROTOTYPE_ROADMAP.md
- agents/D1/INSTRUCTIONS_D1.md
- agents/D2/DRAG_DATA.md — drag data for descent profile planning (D2 output)
- agents/E2/AVIONICS_HARDWARE.md — FC board and sensors available (E2 output)
- agents/E1/ENERGY_BUDGET.md — battery affects endurance planning (E1 output)

## Outputs (written by E3)
- Software/ARCHITECTURE.md
- Software/FLIGHT_CONTROLLER_CONFIG.md
- Software/TELEMETRY_SPEC.md
- Software/FAILSAFE_LOGIC.md
- Software/AUTONOMOUS_FLIGHT_SEQUENCE.md
- Software/GROUND_STATION_GUIDE.md
- Software/PID_TUNING.md
- agents/E3/STATUS.md

## Tools
- Betaflight Configurator / ArduPilot Mission Planner
- MAVLink protocol tools
- Python (data logging, telemetry parsing, post-flight analysis)
- C / C++ (custom firmware modules)

## Success Criteria
- Drone completes autonomous launch-to-recovery sequence end-to-end
- Failsafe triggers correctly on: low battery, signal loss, geofence breach
- Telemetry stream delivers real-time position, altitude, battery voltage
- All firmware parameters documented and reproducible from documentation
