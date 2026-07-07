"""
LNCH-001 — Main Launch Rail (Refined L3)
Material : 6061-T6 Aluminium Extrusion
Revision : v2.0-L3 (Standardized Fasteners)
"""
from build123d import *
from icad.standards import Fasteners

def build_lnch001(params: dict = None):
    params = params or {}
    L = params.get("length", 1000.0) # 1m section for CAD robustness
    W = params.get("width", 40.0)
    H = params.get("height", 40.0)

    m6 = Fasteners.METRIC.get("M6", {"clearance": 6.5, "head_dia": 10.0, "head_height": 6.0}) # Fallback if M6 not in standards

    with BuildPart() as p:
        # 1. Main T-Slot Profile (Simplified 4040)
        Box(W, H, L)
        # T-slots on 4 faces
        for ang in [0, 90, 180, 270]:
            with Locations(Rot(0, 0, ang)):
                with Locations((0, W/2, L/2)):
                    Box(8.0, 12.0, L + 2, mode=Mode.SUBTRACT)
                    # Slot throat
                    Box(20.0, 4.0, L + 2, mode=Mode.SUBTRACT)

        # 2. Mounting Holes (M6 Clearance)
        for z in range(100, int(L), 200):
            with Locations((0, 0, z)):
                Cylinder(m6["clearance"] / 2, H + 2, mode=Mode.SUBTRACT)

    return p.part
