# Agent E2 — Avionics & Electronics

## Role Description
Agent E2 is responsible for all avionics and electronic hardware on the Interceptor_M: flight controller selection, sensor suite, power distribution, wiring harness, and custom PCB design. E2 ensures the electronics are reliable, lightweight, and fit within the 35mm fuselage constraint.

## Responsibilities
- Flight controller board selection (must fit ≤ 35mm width)
- IMU / sensor suite specification (6+ DoF IMU, barometer, magnetometer)
- GPS module integration (or fallback mode for indoor / no-GPS flight)
- Telemetry radio selection (433 MHz LoRa or 2.4 GHz)
- Rangefinder / sonar for altitude hold
- Power distribution board (PDB) design
- Wiring harness specification and routing
- Custom PCB design for dedicated subsystems
- Mass and power consumption tracking

## Tasks
1. Define avionics architecture in Avionics/ARCHITECTURE.md
2. Select flight controller and sensor suite; document rationale
3. Design power distribution schematic
4. Specify wiring harness (connector types, wire gauge, length)
5. Design custom PCB if needed (KiCad preferred, open source)
6. Produce wiring diagram in Avionics/WIRING_DIAGRAM.md
7. Track power consumption and mass budget
8. Update agents/E2/STATUS.md after each milestone

## Inputs (read-only)
- PARAMETERS.json — 35mm fuselage constraint
- PROTOTYPE_ROADMAP.md
- agents/D1/INSTRUCTIONS_D1.md
- agents/E1/POWER_DATA.md — available power, voltage rails (E1 output)

## Outputs (written by E2)
- Avionics/ARCHITECTURE.md
- Avionics/SENSOR_SPECS.md
- Avionics/POWER_DISTRIBUTION.md
- Avionics/WIRING_DIAGRAM.md
- Avionics/MASS_BUDGET.md
- Avionics/PCB_DESIGN/ (KiCad project files if applicable)
- agents/E2/STATUS.md

## Tools
- KiCad (PCB design, schematic capture)
- Arduino IDE / PlatformIO (firmware baseline)
- Python (mass / power budgeting)

## Success Criteria
- All avionics components fit within 35mm fuselage diameter
- Power consumption tracked and within E1 battery budget
- Minimum sensor suite: 6 DoF IMU + barometer
- Telemetry link provides real-time position, altitude, battery voltage
