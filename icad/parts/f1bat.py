"""
F1-BAT — F1 Battery Tray (Refined L3)
Material : 7075-T6 Aluminium
Revision : v2.0-L3 (Standardized Fasteners)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_f1bat(params: dict = None):
    params = params or {}
    L = params.get("length", 60.0)
    W = params.get("width", 30.0)
    H = params.get("height", 15.0)

    m3 = Fasteners.METRIC["M3"]

    with BuildPart() as p:
        # Base Tray
        Box(L, W, 2.0)
        # Side Walls
        for sy in [-1, 1]:
            with Locations((0, sy * (W/2 - 1), H/2)):
                Box(L, 2.0, H)

        # Mounting (M3 Clearance)
        for sx in [-1, 1]:
            with Locations((sx * (L/2 - 5), 0, 0)):
                Cylinder(m3["clearance"] / 2, 5.0, mode=Mode.SUBTRACT)

    return p.part
