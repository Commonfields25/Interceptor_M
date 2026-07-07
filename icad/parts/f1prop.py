"""
F1-PROP — F1 Propeller Hub (Aviation L3 - PyCad)
Material : 7075-T6 Aluminium
Revision : v5.0-L3 (Folding Mechanics & SI Calibration)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_f1prop(params: dict = None):
    params = params or {}
    hub_D = params.get("hub_diameter", 22.0)
    hub_H = params.get("hub_height", 14.0)
    bore_D = params.get("bore_diameter", 5.0)

    m2 = Fasteners.METRIC["M2"]

    with BuildPart() as p:
        # 1. Main Hub Core
        Cylinder(bore_D/2 + 4.0, hub_H)
        # Shaft bore (H7)
        Cylinder(bore_D/2, hub_H + 2, mode=Mode.SUBTRACT)

        # 2. Blade Pivot Arms
        arm_w = 10.0
        arm_l = 10.0
        with Locations(PolarLocations(bore_D/2 + 4.0 + arm_l/2 - 2.0, 2).locations):
            Box(arm_l, arm_w, hub_H)

        # 3. Blade Slots (Clearing space for blade roots)
        slot_w = 4.0
        with Locations(PolarLocations(bore_D/2 + 4.0 + arm_l - 2.0, 2).locations):
            Box(8.0, slot_w, hub_H + 2, mode=Mode.SUBTRACT)

        # 4. Pin Holes (M2 Horizontal for folding)
        with Locations(PolarLocations(bore_D/2 + 4.0 + arm_l - 2.0, 2).locations):
            # Correct rotation for horizontal pin
            with Locations(Rot(90, 0, 0)):
                Cylinder(m2["clearance"]/2, arm_w + 5, mode=Mode.SUBTRACT)

        # 5. Lock-nut Recess
        with Locations((0, 0, hub_H - 4.0)):
            Cylinder(8.5/2, 5.0, mode=Mode.SUBTRACT)

        # 6. Weight Reduction (Side Scallops)
        with Locations(PolarLocations(bore_D/2 + 5.0, 2, start_angle=90).locations):
            Cylinder(4.0, hub_H + 2, mode=Mode.SUBTRACT)

        # 7. Quality Finishing
        try:
            fillet(p.edges().filter_by(Axis.Z), radius=1.0)
        except:
            pass

    return p.part
