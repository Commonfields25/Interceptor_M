# Sourcing Guide: Standardized Industrial Components

This guide provides resources and best practices for sourcing high-fidelity standardized mechanical components (fasteners, bearings, linear guides) for the Interceptor_M platform.

## 1. Digital Sourcing Libraries (Build123d Ecosystem)
For L3 CAD development, utilize these Python libraries to generate real hardware geometry instead of simplified holes:
- **bd_warehouse**: Industrial fasteners (screws, nuts, washers), flanges, and helical threads.
- **bd_vslot**: V-Slot and T-Slot aluminum profiles and associated hardware (rollers, T-nuts).

## 2. Catalog Platforms (3D/STEP Models)

### TraceParts
- **Best for**: Officially certified manufacturer components (screws, linear rails, bearings).
- **Features**: Real-time configuration (bolt length, shaft diameter) before STEP export.
- **URL**: [traceparts.com](https://www.traceparts.com)

### McMaster-Carr
- **Best for**: Hardware and fast shipping (US-centric but catalog is a gold standard).
- **Features**: Cleanest STEP models for almost every mechanical part.
- **URL**: [mcmaster.com](https://www.mcmaster.com)

### CADENAS PARTcommunity
- **Best for**: Automotive-grade and automation components.
- **URL**: [partcommunity.com](https://www.partcommunity.com)

### Community Platforms
- **GrabCAD**: Largest community for complete assemblies (motors, chassis). Filter by STEP/STP.
- **CGTrader/TurboSquid**: Useful for high-poly visual models, but check for "Engineering/CAD" sections.

## 3. Import Best Practices

- **Format**: Prioritize **STEP AP214**. It preserves manufacturer colors, aiding part distinction in complex assemblies.
- **Verification**: Always check **functional dimensions** (bore diameters, center-to-center distances) after import to ensure the model matches your purchase spec.
- **Tolerance**: ICAD parts use ISO 2768-m (Medium) for linear dimensions.

## 4. Fastener Standards in ICAD
All procedural parts in \`icad/parts/\` are built using standard metric fasteners defined in \`icad/standards.py\`:

| Thread | Clearance Hole (mm) | Tap Drill (mm) | Counterbore (mm) |
| :--- | :--- | :--- | :--- |
| M2 | 2.4 | 1.6 | 4.4 x 2.2 |
| M2.5 | 2.9 | 2.05 | 5.1 x 2.7 |
| M3 | 3.4 | 2.5 | 6.5 x 3.3 |
| M4 | 4.5 | 3.3 | 8.0 x 4.4 |
| M5 | 5.5 | 4.2 | 9.5 x 5.5 |

---
*Maintained by the Industrial Design Engineering Team.*
