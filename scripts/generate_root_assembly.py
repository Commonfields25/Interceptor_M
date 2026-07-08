import os
import json
import csv
import math
from build123d import *
from icad.engine import CADEngine
from icad.standards import Fasteners
import icad.parts as parts

def generate_g3_baseline():
    engine = CADEngine(output_dir="exports/G3_DESIGN")

    # 1. DD-400 Integrated Assembly
    print("Generating DD-400 G3 Integrated Assembly...")

    # Create parts
    nose = parts.build_nc001({"diameter": 35.0, "length": 60.0})
    ring = parts.build_ncr001({"outer_diameter": 35.0, "inner_diameter": 28.0})
    hull = parts.build_chs001({"section_length": 200.0, "diameter": 35.0})

    # Position
    # Using list of solids to avoid Compound nesting issues if that was the cause
    dd_parts = [
        nose.moved(Location((0, 0, 222))), # 200 (hull) + 22 (ring)
        ring.moved(Location((0, 0, 200))),
        hull
    ]

    # Add Hardware
    screw_model = Fasteners.get_warehouse_fastener("M2.5", length=10)
    if screw_model:
        for loc in PolarLocations(36.0/2 + 3.0, 6).locations:
             # Fasteners at interface
             dd_parts.append(screw_model.moved(Location(loc) * Location((0, 0, 215))))

    dd_assy = Compound(label="DD-400_G3_ROOT", children=dd_parts)

    # 2. F1-Chaser High-Fidelity Assembly
    print("Generating F1-Chaser G3 High-Fidelity Assembly...")

    f1_body = parts.build_f1body01({"length": 120.0, "width": 80.0, "height": 35.0})
    f1_parts = [f1_body]

    # Structural Arms: 10mm OD Carbon Tubes
    arm_len = 80.0
    for ang in [45, 135, 225, 315]:
        arm = Cylinder(5.0, arm_len).cut(Cylinder(4.0, arm_len + 2.0))
        arm = arm.rotate(Axis.Y, 90).rotate(Axis.Z, ang)
        arm = arm.translate(( (arm_len/2)*math.cos(math.radians(ang)), (arm_len/2)*math.sin(math.radians(ang)), 17.5 ))
        f1_parts.append(arm)

        # Add Motors/Props at end of arms
        loc = (80.0 * math.cos(math.radians(ang)), 80.0 * math.sin(math.radians(ang)), 17.5)
        f1_parts.append(parts.build_f1motor({}).moved(Location(loc)))
        f1_parts.append(parts.build_f1prop({}).moved(Location(loc) * Location((0, 0, 15))))

    f1_assy = Compound(label="F1-CHASER_G3_ROOT", children=f1_parts)

    # Export & Reports
    for assy in [dd_assy, f1_assy]:
        engine.export_part(assy, assy.label)
        # engine.generate_report uses analyze_solid which tessellates.
        # For large assemblies this might be slow, so we check if it works.
        try:
            report = engine.generate_report(assy, assy.label, {"revision": "G3-L3-PyCad"})
            print(f"Validated {assy.label}: {report}")
        except Exception as e:
            print(f"Report failed for {assy.label}: {e}")

if __name__ == "__main__":
    generate_g3_baseline()
