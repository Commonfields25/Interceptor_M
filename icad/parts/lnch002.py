"""
LNCH-002 — Rail Mounting Bracket (Refined L3)
Material : 7075-T6 Aluminium
Revision : v2.0-L3 (Standardized Fasteners)
"""
from build123d import *
from icad.standards import Fasteners

def build_lnch002(params: dict = None):
    params = params or {}
    L = params.get("length", 60.0)
    W = params.get("width", 60.0)
    T = params.get("thickness", 8.0)

    m5 = Fasteners.METRIC["M5"]

    with BuildPart() as p:
        # 1. L-Bracket Profile
        with BuildSketch() as sk:
            Rectangle(L, T, align=(Align.MIN, Align.MIN))
            Rectangle(T, W, align=(Align.MIN, Align.MIN))
        extrude(amount=40.0)

        # 2. Standard Mounting Holes (M5 Clearance)
        # Vertical face
        with Locations((T/2, W*0.7, 20.0)):
            Cylinder(m5["clearance"] / 2, T + 2, rotation=Rot(0, 90, 0), mode=Mode.SUBTRACT)
        # Horizontal face
        with Locations((L*0.7, T/2, 20.0)):
            Cylinder(m5["clearance"] / 2, T + 2, mode=Mode.SUBTRACT)

    return p.part
