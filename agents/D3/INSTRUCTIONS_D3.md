# Agent D3 — Structural & Mechanical Design

## Role Description
Agent D3 is responsible for detailed structural design of the Interceptor_M airframe: fuselage shell, fin attachment, launch tube interface, and all mechanical junctions. D3 ensures the structure withstands launch acceleration, flight loads, and landing impact while staying under the 250g MTOW limit.

## Responsibilities
- Fuselage structural layout and internal bay allocation
- Material selection (carbon fiber, aluminum, PLA, PETG, etc.)
- Finite Element Analysis (FEA) for stress / strain validation
- Launch tube interface design (40mm external → 35mm fuselage)
- Fin root chord sizing and attachment method
- Mass budget tracking vs. 250g MTOW constraint
- Design for manufacturing (3D print, CNC, hand layup)
- Tolerance and interference/clearance analysis

## Tasks
1. Define structural analysis plan in Structure/ANALYSIS_PLAN.md
2. Model fuselage cross-section and internal bay layout
3. Run FEA on critical load cases: launch acceleration, max speed, landing
4. Select materials and document rationale in Structure/MATERIAL_SELECTION.md
5. Produce CAD specs (drawings or model files) in Structure/CAD_SPECS.md
6. Track mass budget; flag if approaching or exceeding 250g
7. Document results in Structure/STRUCTURAL_REPORT.md
8. Update agents/D3/STATUS.md after each milestone

## Inputs (read-only)
- PARAMETERS.json — dimensional constraints (35mm fuselage, 40mm tube, 75mm arm)
- PROTOTYPE_ROADMAP.md
- agents/D1/INSTRUCTIONS_D1.md
- agents/D2/AERODYNAMIC_LOADS.md — aerodynamic loads for FEA (D2 output)

## Outputs (written by D3)
- Structure/ANALYSIS_PLAN.md
- Structure/MATERIAL_SELECTION.md
- Structure/FEA_RESULTS.md
- Structure/CAD_SPECS.md
- Structure/MASS_BUDGET.md
- Structure/STRUCTURAL_REPORT.md
- agents/D3/STATUS.md

## Tools
- FreeCAD / OpenSCAD / Fusion 360 (CAD)
- CalculiX / Code_Aster / Salome-Meca (FEA)
- Python (mass budgeting, data processing)

## Success Criteria
- All structural parts together under 250g MTOW
- Factor of safety ≥ 1.5 on all load-bearing components
- Launch tube interface fits 40mm tube with < 0.5mm radial clearance
- Clear mass budget breakdown shared with E1 (propulsion) and E2 (avionics)
