# ICAD Engine Learnings

## Core Architecture
- Using **Build123d** (OCP-based) provides superior robustness for L3 geometry compared to script-based FreeCAD.
- Fluent API and selection filters (e.g., `edges().filter_by(Axis.Z)`) solve the Topological Naming Problem common in CAD-as-code.

## Geometry Best Practices
- **L3 Fidelity**: Always include fillets and chamfers for manufacturing finish.
- **Conservative Chamfering**: Use `min(0.3, thickness * 0.1)` to prevent OCP kernel failures on thin walls.
- **Projections**: Use `project_to_viewport` for reliable 2D technical drawings without complex HLR algorithms.

## Deployment
- Modular part architecture allows rapid expansion (Drone vs. Launcher).
- YAML-driven CLI enables seamless integration into automated engineering pipelines.
