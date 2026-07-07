"""
AVS-001 — Anti-Vibration Mount (Refined L3)
Material : Elastomer / 7075-T6 Aluminium
Revision : v2.0-L3 (Standardized Fasteners)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_avs001(params: dict = None):
    params = params or {}
    L = params.get("length", 40.0)
    W = params.get("width", 30.0)
    TH = params.get("total_height", 10.0)

    m3 = Fasteners.METRIC["M3"]

    with BuildPart() as p:
        # 1. Main Elastomer Body
        Box(L, W, TH)

        # 2. Central Metal Insert Footprint (Subtractive)
        with Locations((0, 0, TH/2)):
            Cylinder(8.0, 4.0, mode=Mode.SUBTRACT) # Recess for metal insert

        # 3. Damping Grooves (Refined geometry)
        for sx in [-1, 1]:
            with Locations((sx * (L/2 - 5), 0, 0)):
                Box(4.0, W - 10.0, TH + 2.0, mode=Mode.SUBTRACT)

        # 4. Standard Mounting (M3 Clearance)
        bcd = 24.0
        for ang in [45, 135, 225, 315]:
            rad = math.radians(ang)
            hx = (bcd / 2) * math.cos(rad)
            hy = (bcd / 2) * math.sin(rad)
            with Locations((hx, hy, 0)):
                Cylinder(m3["clearance"] / 2, TH + 2, mode=Mode.SUBTRACT)

    return p.part
