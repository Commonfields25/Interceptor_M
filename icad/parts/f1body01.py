"""
F1-BODY-01 — F1 Drone Body Shell (Refined L3)
Material : Carbon Fiber / 7075-T6 | Process : CNC / SLS
Revision : v3.1-L3 (PyCad Calibration)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_f1body01(params: dict = None):
    params = params or {}
    L = params.get("length", 120.0)
    W = params.get("width", 80.0)
    H = params.get("height", 35.0)
    T = params.get("wall_thickness", 2.0)

    m3 = Fasteners.METRIC["M3"]

    with BuildPart() as p:
        # 1. Main Hull
        with BuildSketch() as sk:
            Ellipse(L/2, W/2)
        extrude(amount=H)

        # 2. Hollow Shell
        with Locations((0, 0, T)):
            with BuildSketch() as sk2:
                Ellipse(L/2 - T, W/2 - T)
            extrude(amount=H, mode=Mode.SUBTRACT)

        # 3. Component Stacks (M3)
        with Locations(GridLocations(30.5, 30.5, 2, 2).locations):
            Cylinder(3.5, T + 2.0, mode=Mode.ADD)
            Cylinder(m3["clearance"] / 2, T + 4.0, mode=Mode.SUBTRACT)

        # 4. Aerospace Finishing (Safe fillets)
        try:
            fillet(p.edges().filter_by(Axis.Z), radius=1.0)
        except:
            pass

    return p.part
