"""
AVS-001 — Anti-Vibration Mount (Refined L3)
Material : Elastomer / 7075-T6 Aluminium
Revision : v3.1-L3 (PyCad Calibration)
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
            Cylinder(8.0, 4.0, mode=Mode.SUBTRACT)

        # 3. Damping Grooves
        with Locations(GridLocations(L-10, 0, 2, 1).locations):
             Box(4.0, W - 10.0, TH + 2.0, mode=Mode.SUBTRACT)

        # 4. Standard Mounting (M3 Clearance)
        bcd = 24.0
        with Locations(PolarLocations(bcd/2, 4, start_angle=45).locations):
            Cylinder(m3["clearance"] / 2, TH + 2, mode=Mode.SUBTRACT)

        # Ensure watertightness by adding fillets carefully
        try:
            fillet(p.edges().filter_by(Axis.Z), radius=1.0)
        except:
            pass

    return p.part
