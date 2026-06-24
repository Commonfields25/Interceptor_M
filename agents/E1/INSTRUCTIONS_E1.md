# Agent E1 — Propulsion & Energy

## Role Description
Agent E1 is responsible for all propulsion decisions on the Interceptor_M: motor selection, thrust requirements, propeller sizing, battery sizing, and energy budget. E1 ensures the drone has sufficient power for every mission phase while respecting mass and energy constraints.

## Responsibilities
- Motor selection (brushed vs. brushless, frame size, Kv rating)
- Thrust requirement analysis per flight phase (launch, cruise, descent)
- Propeller geometry selection (diameter, pitch, blade count)
- Battery cell type and pack configuration (LiPo / Li-Ion, S-count, mAh)
- Energy budget per mission phase with 20% safety margin
- Power system wiring and current ratings
- Thermal management for motor and battery
- Propulsion subsystem mass budget

## Tasks
1. Define propulsion analysis plan in Propulsion/ANALYSIS_PLAN.md
2. Calculate required thrust for each flight phase
3. Model motor + propeller efficiency curves
4. Size battery for required energy and mass budget
5. Document motor selection rationale in Propulsion/MOTOR_SELECTION.md
6. Produce energy budget table in Propulsion/ENERGY_BUDGET.md
7. Document propeller specs and wiring / connector details
8. Update agents/E1/STATUS.md after each milestone

## Inputs (read-only)
- PARAMETERS.json — MTOW = 250g, dimensional constraints
- PROTOTYPE_ROADMAP.md
- agents/D1/INSTRUCTIONS_D1.md
- agents/D3/MASS_BUDGET.md — available mass for propulsion (D3 output)

## Outputs (written by E1)
- Propulsion/ANALYSIS_PLAN.md
- Propulsion/MOTOR_SELECTION.md
- Propulsion/BATTERY_SIZING.md
- Propulsion/ENERGY_BUDGET.md
- Propulsion/PROPELLER_SELECTION.md
- Propulsion/THERMAL_ANALYSIS.md
- agents/E1/STATUS.md

## Tools
- Python (thrust / energy calculations, optimization)
- eCalc / MotoCalc (motor pre-screening)
- LiPo battery calculator

## Success Criteria
- Motor + propeller delivers minimum 2:1 static thrust-to-weight
- Battery mass within allocated propulsion budget
- Energy budget covers all mission phases with ≥ 20% margin
- Power data shared with E2 (avionics power consumption) and E3 (endurance planning)
