"""
MMT-001 — Motor Mount (Refined L3)
Material : 7075-T6 Aluminium | Process : CNC 3-axis Milling
Revision : v3.1-L3 (PyCad Calibration)
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

        # 2. Radial Cooling Fins
        with Locations(PolarLocations(D/2 + 2.5, 18).locations):
            Box(5.0, 1.2, TH)

        # 3. Standard Mounting Patterns (M3 Tapped)
        # 16x19mm pattern
        with Locations([(8, 9.5, TH/2), (-8, -9.5, TH/2), (-8, 9.5, TH/2), (8, -9.5, TH/2)]):
            Cylinder(m3["tap_drill"] / 2, TH + 2, mode=Mode.SUBTRACT)

    return p.part
