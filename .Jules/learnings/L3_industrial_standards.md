# Learning: L3 Industrial CAD Standards

## Context
Transitioning from conceptual placeholders to manufacturing-ready (L3) geometry in Interceptor_M.

## Key Findings
1. **Pipeline Mapping**: Exact ID matching between CLI PART_MAP and configuration files (YAML) is critical. Mismatches like "F1-BAT" vs "F1-BAT-01" cause the system to default to low-res manual STLs.
2. **Physics Scaling**: SI units for inertia tensors (kg.m²) require a 1e-15 conversion factor from mm⁵ (Trimesh output for mm-scale geometry).
3. **Boolean Stability**: Complex features like Bezier-revolves or tiny fillets can cause OCP/drawing segfaults. Conservative feature sizing (min 0.3mm) improves robustness.
4. **Sub-Assemblies**: Hierarchical compounds in Build123d provide superior BOM clarity and traceability for AS9100.
