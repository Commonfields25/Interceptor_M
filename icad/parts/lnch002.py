"""
LNCH-002 — Rail Mounting Bracket (Refined L3)
Material : 7075-T6 Aluminium
Revision : v3.0-L3 (Real Industrial Geometry)
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
        # 1. Structural L-Profile with Gusset
        with BuildSketch() as sk:
            with BuildLine() as bl:
                l1 = Line((0, 0), (L, 0))
                l2 = Line((L, 0), (L, T))
                l3 = Line((L, T), (T, T))
                l4 = Line((T, T), (T, W))
                l5 = Line((T, W), (0, W))
                l6 = Line((0, W), (0, 0))
            make_face()
        extrude(amount=40.0)

        # 2. Side Gusset (Stiffening)
        with Locations((T, T, 20.0)):
            Box(10.0, 10.0, 5.0, rotation=Rot(0, 45, 0))

        # 3. Standard Mounting Patterns (M5)
        # Horizontal base
        with Locations((L*0.7, T/2, 20.0)):
             Cylinder(m5["clearance"]/2, T+2, mode=Mode.SUBTRACT)
        # Vertical wall
        with Locations((T/2, W*0.7, 20.0)):
             Cylinder(m5["clearance"]/2, T+2, rotation=Rot(0, 90, 0), mode=Mode.SUBTRACT)

    return p.part
