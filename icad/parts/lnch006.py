"""
LNCH-006 — Clamp Collar (Refined L3)
Material : 7075-T6 Aluminium
Revision : v3.1-L3 (Watertight Boolean Pass)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_lnch006(params: dict = None):
    params = params or {}
    OD = params.get("outer_diameter", 60.0)
    ID = params.get("inner_diameter", 40.0)
    L = params.get("length", 25.0)

    m5 = Fasteners.METRIC["M5"]

    with BuildPart() as p:
        # 1. Annular Body
        Cylinder(OD / 2, L)
        Cylinder(ID / 2, L + 2.0, mode=Mode.SUBTRACT)

        # 2. Split Gap - using wider overlap
        with Locations((OD/2, 0, 0)):
            Box(25.0, 3.0, L + 5.0, mode=Mode.SUBTRACT)

        # 3. Clamping Bolt Interface (M5)
        # Position with safety margins from edges
        y_off = 12.0
        with Locations((OD/2 - 10.0, y_off, 0)):
             Cylinder(m5["clearance"]/2, 30.0, rotation=Rot(90, 0, 0), mode=Mode.SUBTRACT)
        with Locations((OD/2 - 10.0, -y_off, 0)):
             Cylinder(m5["tap_drill"]/2, 30.0, rotation=Rot(90, 0, 0), mode=Mode.SUBTRACT)

    return p.part
