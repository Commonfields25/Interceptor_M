"""
LNCH-006 — Clamp Collar (Refined L3)
Material : 7075-T6 Aluminium
Revision : v2.0-L3 (Standardized Fasteners)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_lnch006(params: dict = None):
    params = params or {}
    OD = params.get("outer_diameter", 60.0)
    ID = params.get("inner_diameter", 40.0)
    L = params.get("length", 20.0)

    m5 = Fasteners.METRIC["M5"]

    with BuildPart() as p:
        # 1. Clamp Body
        Cylinder(OD / 2, L)
        Cylinder(ID / 2, L + 2, mode=Mode.SUBTRACT)

        # 2. Split Gap
        with Locations((OD/2, 0, L/2)):
            Box(20.0, 3.0, L + 2, mode=Mode.SUBTRACT)

        # 3. Clamping Bolt (M5 Tapped + Clearance)
        with Locations((OD/2 - 8.0, 0, L/2)):
            Cylinder(m5["clearance"] / 2, 40.0, rotation=Rot(90, 0, 0), mode=Mode.SUBTRACT)

    return p.part
