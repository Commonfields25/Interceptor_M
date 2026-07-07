"""
LNCH-005 — Support Foot (Refined L3)
Material : 6061-T6 Aluminium
Revision : v2.0-L3 (Standardized Fasteners)
"""
from build123d import *
from icad.standards import Fasteners

def build_lnch005(params: dict = None):
    params = params or {}
    W = params.get("width", 100.0)
    T = params.get("thickness", 10.0)

    m5 = Fasteners.METRIC["M5"]

    with BuildPart() as p:
        # 1. Base Plate
        Box(W, W, T)

        # 2. Stiffening Ribs
        for sx in [-1, 1]:
            with Locations((sx * (W/2 - 10), 0, T)):
                Box(4.0, W, 20.0, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 3. Standard Mounting (M5 Clearance)
        for sx in [-1, 1]:
            for sy in [-1, 1]:
                with Locations((sx * (W/2 - 15), sy * (W/2 - 15), 0)):
                    Cylinder(m5["clearance"] / 2, T + 2, mode=Mode.SUBTRACT)

    return p.part
