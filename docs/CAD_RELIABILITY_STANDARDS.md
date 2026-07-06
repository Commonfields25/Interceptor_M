---
action: Documentation
agent: Jules (Physics Expert)
related_gate: G2
status: Validated
timestamp: 2026-06-29 23:45:00+00:00
---

# CAD Reliability & Engineering Liability

## 1. Liability Classification

The Interceptor_M project uses two distinct levels of CAD data. Engineering liability is tied to this classification:

| Level | Format | Tooling | Usage | Liability |
|---|---|---|---|---|
| **L1: Conceptual** | `.stl` | Python / numpy-stl | Visualization, Swarm Sim, Volume Analysis | **NONE**. Use at own risk. |
| **L2: Engineering** | `.step`, `.f3d` | FreeCAD / Inventor | Stress Analysis (FEA), Integration | **LIMITED**. Verified by E1/D3. |
| **L3: Manufacturing** | `.step` + PDF | Validated CAD | CNC Machining, DMLS Printing | **FULL**. Requires DG Sign-off. |

## 2. Unit & Coordinate Standards
- **Units**: All dimensions in **Millimeters (mm)** unless explicitly labeled in SI (meters).
- **Coordinate System**: Right-handed.
  - **X**: Longitudinal (Nose-to-Tail).
  - **Y**: Lateral.
  - **Z**: Vertical.

## 3. Reliability Protocol for Procedural CAD
Procedural CAD scripts (`scripts/generate_part.py`, etc.) must include:
1. **Input Sanitization**: Block negative dimensions.
2. **Unit Header**: Explicit declaration of mm units.
3. **Conceptual Disclaimer**: Warning that output is L1-Conceptual.

## 4. Manufacturing Sign-off
No part generated via Python script is authorized for physical manufacture until it has been imported into an L2 Engineering environment, verified against `PARAMETERS.json`, and exported as a validated STEP file with a corresponding technical drawing.

---
*Standards established by Jules to prevent engineering failure.*
