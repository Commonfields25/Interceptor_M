---
action: Documentation
agent: Jules
related_gate: G3
status: Active
timestamp: 2026-07-07 10:45:00+00:00
---

# Role: Industrial Design & Mechanical Engineer (L3)

The Industrial Design Engineer is responsible for the transition from numerical simulation results to manufacturing-ready (L3) CAD geometry.

## 1. Design Philosophy
- **Standardization First**: Always utilize `icad/standards.py` for fastener holes, bearing seats, and material properties.
- **Manufacturing Fidelity**: Every part must include realistic fillets (min 0.3mm) and chamfers to ensure CNC tool access and stress concentration reduction.
- **Parametric Integration**: Part dimensions must be linked to `PARAMETERS.json` to ensure consistency across DD, DI, and DC product lines.

## 2. Tools & Workflows
- **Core Engine**: `icad/engine.py` (Build123d based).
- **Standards**: Metric ISO standards for all hardware.
- **Sourcing**: Use industrial catalogs (McMaster-Carr, TraceParts) for COTS (Commercial Off-The-Shelf) parts. See [SOURCING_GUIDE.md](./manufacturing/SOURCING_GUIDE.md).

## 3. L3 Checklist for New Parts
1. [ ] **Fasteners**: Are clearance/tap holes standardized?
2. [ ] **Mass**: Does the calculated mass align with the 400g MTOW target?
3. [ ] **Tolerances**: Are IT7/IT10 fits applied to critical interfaces (e.g., motor mounts)?
4. [ ] **Assembly**: Have you run `scripts/verify_assembly_fit.py`?

---
*Standards maintained for Interceptor_M G3 Preliminary Design.*
