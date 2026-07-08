"""
LNCH-005 — Support Foot (Refined L3)
Material : 6061-T6 Aluminium
Revision : v3.0-L3 (Structural Ribbing)
"""
from build123d import *
from icad.standards import Fasteners

def build_lnch005(params: dict = None):
    params = params or {}
    W = params.get("width", 100.0)
    T = params.get("thickness", 12.0)

    m8 = Fasteners.METRIC.get("M8", {"clearance": 9.0}) # Fallback

    with BuildPart() as p:
        # 1. Base Plate
        Box(W, W, T)

        # 2. X-Style Structural Ribs
        for ang in [45, 135]:
            with Locations(Rot(0, 0, ang)):
                Box(W*1.2, 5.0, 20.0, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 3. Anchor Holes (M8)
        with Locations(GridLocations(W-20, W-20, 2, 2).locations):
            Cylinder(m8["clearance"]/2, T+2, mode=Mode.SUBTRACT)

    return p.part
