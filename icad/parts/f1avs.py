"""
F1-AVS — F1 Anti-Vibration Mount (Refined L3)
Material : Elastomer
Revision : v2.0-L3 (Standardized Fasteners)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_f1avs(params: dict = None):
    params = params or {}
    L = params.get("length", 25.0)
    W = params.get("width", 20.0)
    T = params.get("thickness", 5.0)

    m2_5 = Fasteners.METRIC["M2.5"]

    with BuildPart() as p:
        Box(L, W, T)

        # Standard Mounting (M2.5 Clearance)
        for sx in [-1, 1]:
            for sy in [-1, 1]:
                with Locations((sx * (L/2 - 4), sy * (W/2 - 4), 0)):
                    Cylinder(m2_5["clearance"] / 2, T + 2, mode=Mode.SUBTRACT)

    return p.part
