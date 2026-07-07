"""
MMT-001 — Motor Mount (Refined L3)
Material : 7075-T6 Aluminium | Process : CNC 3-axis Milling
Revision : v2.0-L3 (Optimized Cooling)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_mmt001(params: dict = None):
    params = params or {}
    D = params.get("diameter", 35.0)
    TH = params.get("thickness", 8.0)

    m3 = Fasteners.METRIC["M3"]

    with BuildPart() as p:
        # 1. Main Collar
        Cylinder(D / 2 + 5.0, TH)
        Cylinder(D / 2, TH + 2, mode=Mode.SUBTRACT)

        # 2. Radial Cooling Fins (Interrupted Fins)
        fin_w = 1.2
        for ang in range(0, 360, 20):
            rad = math.radians(ang)
            with Locations(( (D/2 + 2.5)*math.cos(rad), (D/2 + 2.5)*math.sin(rad), TH/2 )):
                Box(5.0, fin_w, TH, rotation=Rot(0, 0, math.degrees(ang)))

        # 3. Standard Mounting Patterns (M3 Tapped)
        # Standard 16x19mm motor mounting
        for dx, dy in [(-8, -9.5), (8, 9.5), (-8, 9.5), (8, -9.5)]:
            with Locations((dx, dy, TH - 5.0)):
                Cylinder(m3["tap_drill"] / 2, 7.0, mode=Mode.SUBTRACT)

    return p.part
