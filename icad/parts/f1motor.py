"""
F1-MOTOR — F1 Motor Mount (L3)
Material : 7075-T6 Aluminium | Process : CNC Milling
Revision : v3.3-L3 (Stability Fix)
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
        # Simple cylinder to avoid complex Bezier-revolve issues in drawings
        Cylinder(D/2, H)

        # Standard 19mm Pattern
        with Locations(GridLocations(19.0, 19.0, 2, 2).locations):
            Cylinder(m4["clearance"] / 2, H + 2.0, mode=Mode.SUBTRACT)

    return p.part
