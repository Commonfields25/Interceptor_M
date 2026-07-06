---
action: Create
agent: AC
related_gate: G2
status: Validated
timestamp: 2026-06-30 10:47:13+00:00
---

# 📏 CAD QUALITY & BEST PRACTICE STANDARDS

To move from "STL-like" prototypes to aviation-grade components, all Designers and Engineers must adhere to the following standards.

## 1. Geometric Fidelity
- **Explicit Features**: All functional interfaces (bores, threads, contact surfaces) must be explicitly modeled.
- **Surface Quality**: Apply standard fillets (min R2.0) and chamfers (0.5 x 45°) to all external edges to reduce stress concentration and improve finish.
- **Tolerancing**: Use ISO 2768-m (General) and explicit GD&T (e.g., H7/g6) for critical fits.

## 2. File Format & Interoperability
- **Primary Source**: .FCStd (FreeCAD) or .SLDPRT (SolidWorks).
- **Exchange Format**: **STEP AP214** (MUST include material color and metadata).
- **Prohibited**: Do not use .STL for mechanical engineering (it is a mesh format, unsuitable for precision machining).

## 3. Design for Manufacturing (DfM)
- **CNC**: Ensure tool accessibility (e.g., avoid internal sharp corners).
- **AM (DMLS)**: Design with support reduction in mind (45° rule). Use lattice structures for non-critical mass reduction.
- **Weight Optimization**: Every part MUST have a target mass and a calculated mass budget deviation < 5%.

## 4. Metadata Tagging
Every CAD file must include a Properties/Metadata block:
| Property | Value |
|---|---|
| Part_ID | e.g., BRK-001 |
| Material | e.g., Al 7075-T6 |
| Weight_g | Calculated value |
| Revision | vX.X |

---
*Enforced by AC Agent | Validated by DG*
