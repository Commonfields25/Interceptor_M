---
agent: Jules (Physics Expert)
action: Documentation
timestamp: 2026-06-29T23:35:00Z
status: Validated
---

# Procedural CAD & STL Generation

The Interceptor_M project supports procedural generation of CAD parts for both the launcher assembly and airframe components using Python scripts.

## 1. Prerequisites
To generate STL files, you need the `numpy-stl` library:
```bash
pip install numpy-stl
```

## 2. Generating Launcher Parts
The base launcher parts (Chassis, Rails, Brackets, etc.) are generated using:
```bash
python3 models/Base_Launcher_Pieces/create_launcher_parts.py
```
Output directory: `models/Base_Launcher_Pieces/`

**Generated Parts:**
- `01_Main_Chassis.stl`
- `02_Launch_Rails.stl`
- `03_Drone_Mounting_Bracket.stl`
- `04_Locking_Mechanism.stl`
- `05_Support_Feet.stl`
- `06_Side_Protection_Panel.stl`

## 3. Generating Airframe Parts
The generic airframe part generator is located at:
```bash
python3 scripts/generate_part.py
```
This script utilizes the shared parameters in `PARAMETERS.json` to dimension parts according to the product line (DD, DI, DC).

## 4. Integration with CAD Tools
The generated `.stl` files can be imported into standard CAD software (Inventor, SolidWorks, Fusion 360) for further refinement or 3D printing.

---
*Verified by Jules for Operation Stabilize.*
