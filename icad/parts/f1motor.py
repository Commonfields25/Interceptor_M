"""
F1-MOTOR — F1 Motor Mount (PyCad Hi-Fi)
Material : 7075-T6 Aluminium | Process : CNC Milling
Revision : v3.1-L3 (PyCad Calibration)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_f1motor(params: dict = None):
    params = params or {}
    D = params.get("diameter", 28.0)
    H = params.get("height", 15.0)

    m4 = Fasteners.METRIC["M4"]

    with BuildPart() as p:
        # 1. Bell-Profile Hub
        with BuildSketch() as sk:
            with BuildLine() as l:
                l1 = Line((0, 0), (D/2, 0))
                l2 = Line((D/2, 0), (D/2, H*0.4))
                l3 = Bezier((D/2, H*0.4), (D/2 * 0.9, H*0.7), (D/2 * 0.6, H))
                l4 = Line((D/2 * 0.6, H), (0, H))
                l5 = Line((0, H), (0, 0))
            make_face()
        revolve(axis=Axis.Z)

        # 2. Cooling Vents (Internal)
        with Locations(PolarLocations(D/2 - 4.0, 8).locations):
            Cylinder(1.5, H + 2, mode=Mode.SUBTRACT)

        # 3. Standard Mounting Patterns (M4)
        # Using a standard 19mm square pattern
        with Locations(GridLocations(19.0, 19.0, 2, 2).locations):
            Cylinder(m4["clearance"] / 2, H + 2, mode=Mode.SUBTRACT)
            with Locations((0, 0, H/2)):
                Cylinder(m4["counterbore_dia"] / 2, 5.0, mode=Mode.SUBTRACT)

        # 4. Aerospace Finishing
        try:
            fillet(p.edges().filter_by(Axis.Z), radius=0.5)
        except:
            pass

    return p.part
