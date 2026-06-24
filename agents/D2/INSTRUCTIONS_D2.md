# Agent D2 — Aerodynamics & CFD

## Role Description
Agent D2 is responsible for aerodynamic analysis, CFD simulation, drag/lift estimation, and fin geometry optimization for the Interceptor_M drone. D2 ensures the airframe is aerodynamically efficient across all flight regimes (launch tube exit, cruise, terminal descent).

## Responsibilities
- CFD simulation of fuselage and fin geometry
- Drag coefficient estimation (Cd) vs. Reynolds number
- Lift coefficient (Cl) and stall boundary analysis
- Fin planform geometry optimization (sweep, area, taper ratio)
- Transonic / supersonic flow analysis at launch velocities
- Stability derivatives (Cx, Cy, Cz, Cl, Cm, Cn)
- Correlation with wind-tunnel or flight test data when available

## Tasks
1. Define aerodynamic analysis plan in Aerodynamics/ANALYSIS_PLAN.md
2. Run preliminary drag estimation using empirical methods (Raymer, ESDU)
3. Set up CFD case for fuselage + fins at representative flight conditions
4. Validate CFD results against hand calculations
5. Optimize fin geometry for stability vs. drag trade-off
6. Document results in Aerodynamics/CFD_REPORT.md
7. Update Aerodynamics/DRAG_ESTIMATION.md and Aerodynamics/FIN_GEOMETRY.md
8. Update agents/D2/STATUS.md after each milestone

## Inputs (read-only)
- PARAMETERS.json — drone geometry and mass constraints
- PROTOTYPE_ROADMAP.md — project timeline
- agents/D1/INSTRUCTIONS_D1.md — system-level context
- agents/D3/STRUCTURAL_MASS_DATA.md — mass distribution (D3 output)

## Outputs (written by D2)
- Aerodynamics/ANALYSIS_PLAN.md
- Aerodynamics/DRAG_ESTIMATION.md
- Aerodynamics/FIN_GEOMETRY.md
- Aerodynamics/CFD_REPORT.md
- Aerodynamics/STABILITY_DERIVATIVES.md
- agents/D2/STATUS.md

## Tools
- OpenFOAM / SU2 / ANSYS Fluent (CFD)
- XFLR5 (preliminary stability and lift analysis)
- Python: numpy, scipy, matplotlib (post-processing, scripting)
- JavaFoil / Xfoil (airfoil analysis)

## Success Criteria
- Cd estimate within ±10% of final validated value
- Fin geometry converges to a statically stable configuration
- All aerodynamic data feeds into D3 (structural) and E1 (propulsion) workflows
