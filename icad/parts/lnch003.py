"""
LNCH-003 — Rail End Stop (Refined L3)
Material : 7075-T6 Aluminium / Rubber
Revision : v2.0-L3 (Standardized Fasteners)
"""
from build123d import *
from icad.standards import Fasteners

def build_lnch003(params: dict = None):
    params = params or {}
    W = params.get("width", 40.0)
    H = params.get("height", 40.0)
    T = params.get("thickness", 15.0)

    m5 = Fasteners.METRIC["M5"]

    with BuildPart() as p:
        # 1. Block Body
        Box(W, H, T)

        # 2. Rubber Bumper Recess
        with Locations((0, 0, T/2)):
            Cylinder(10.0, 5.0, mode=Mode.SUBTRACT)

        # 3. Standard Mounting (M5 Clearance + Counterbore)
        with Locations((0, 0, -T/2)):
            Cylinder(m5["clearance"] / 2, T + 2, mode=Mode.SUBTRACT)
            with Locations((0, 0, 2.0)):
                Cylinder(m5["counterbore_dia"] / 2, m5["counterbore_depth"] + 1, mode=Mode.SUBTRACT)

    return p.part
