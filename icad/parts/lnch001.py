"""
LNCH-001 — Main Launch Rail (Refined L3)
Material : 6061-T6 Aluminium Extrusion
Revision : v3.1-L3 (PyCad Calibration)
"""
from build123d import *
from icad.standards import Fasteners

def build_lnch001(params: dict = None):
    params = params or {}
    L = params.get("length", 1000.0)
    W = params.get("width", 40.0)
    H = params.get("height", 40.0)

    m6 = Fasteners.METRIC.get("M6", {"clearance": 6.5, "head_dia": 10.0, "head_height": 6.0})

    with BuildPart() as p:
        # 1. Main Block (ADD mode)
        Box(W, H, L)

        # 2. T-Slots on 4 faces (SUBTRACT mode)
        for ang in [0, 90, 180, 270]:
            with Locations(Rot(0, 0, ang)):
                # Outer slot
                with Locations((0, H/2, 0)):
                    Box(8.0, 10.0, L + 2, mode=Mode.SUBTRACT)
                # Internal cavity
                with Locations((0, H/2 - 4.0, 0)):
                    Box(20.0, 6.0, L + 2, mode=Mode.SUBTRACT)

        # 3. Central Weight Reduction Bore
        Cylinder(10.0, L + 2, mode=Mode.SUBTRACT)

        # 4. Standard Mounting Holes
        with Locations(GridLocations(0, 200.0, 1, int(L/200)).locations):
            Cylinder(m6["clearance"] / 2, H + 2, mode=Mode.SUBTRACT)

    return p.part
