"""
NCR-001 — Nose-Cone Interface Ring (Refined L3)
Material : 7075-T6 Aluminium | Process : CNC 3-axis Milling
Revision : v2.0-L3 (Improved Sealing)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_ncr001(params: dict = None):
    params = params or {}
    OD = params.get("outer_diameter", 35.0)
    ID = params.get("inner_diameter", 28.0)
    L = params.get("length", 15.0)

    m2_5 = Fasteners.METRIC["M2.5"]

    with BuildPart() as p:
        # 1. Main Ring Body
        Cylinder(OD / 2, L)
        Cylinder(ID / 2, L + 2, mode=Mode.SUBTRACT)

        # 2. O-Ring Groove (Standard 1.5mm O-ring)
        # Groove dia = OD - 2.5mm, width = 1.8mm
        groove_od = OD - 0.5
        groove_id = OD - 3.0
        with Locations((0, 0, L/2)):
            # Create a torus-like cut for the groove
            Cylinder(groove_od / 2, 1.8, mode=Mode.SUBTRACT)
            Cylinder(groove_id / 2, 2.0, mode=Mode.ADD) # Re-add center to make it a groove

        # 3. Mounting Holes (M2.5 Tapped)
        hole_circle_r = (OD + ID) / 4
        for ang in range(0, 360, 60):
            rad = math.radians(ang)
            hx = hole_circle_r * math.cos(rad)
            hy = hole_circle_r * math.sin(rad)
            with Locations((hx, hy, L - 5.0)):
                Cylinder(m2_5["tap_drill"] / 2, 7.0, mode=Mode.SUBTRACT)

        # 4. Alignment Notch
        with Locations((OD/2, 0, L/2)):
            Box(4.0, 2.0, L + 2, mode=Mode.SUBTRACT)

    return p.part
