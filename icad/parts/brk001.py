"""
BRK-001 — Structural Mounting Bracket (Refined L3)
Material : AlSi10Mg Aluminium (DMLS) | Process : DMLS / CNC
Revision : v4.0-L3 (Optimized Mass Reduction)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_brk001(params: dict = None):
    params = params or {}
    L = params.get("length", 75.0)
    W = params.get("width", 55.0)
    T = params.get("thickness", 7.0)
    bore = params.get("bore_diameter", 35.0)

    m4 = Fasteners.METRIC["M4"]

    with BuildPart() as p:
        Box(L, W, T)
        Cylinder(bore / 2, T + 2.0, mode=Mode.SUBTRACT)

        # Isogrid Lightening
        with Locations(GridLocations(L-20, W-20, 2, 2).locations):
             Cylinder(9.0, T + 2.0, mode=Mode.SUBTRACT)

        # Standard Mounting
        with Locations(GridLocations(L-10.0, W-10.0, 2, 2).locations):
            Cylinder(m4["clearance"] / 2, T + 2.0, mode=Mode.SUBTRACT)

    return p.part
