"""
F1-AVS — F1 Anti-Vibration Mount (Refined L3)
Material : Elastomer
Revision : v3.0-L3 (PyCad Calibration & Robust Booleans)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_f1avs(params: dict = None):
    params = params or {}
    L = params.get("length", 25.0)
    W = params.get("width", 20.0)
    T = params.get("thickness", 5.0)

    m2_5 = Fasteners.METRIC["M2.5"]

    with BuildPart() as p:
        # 1. Main Elastomer Body
        Box(L, W, T)

        # 2. Standard Mounting (M2.5 Clearance)
        with Locations(GridLocations(L-8, W-8, 2, 2).locations):
            Cylinder(m2_5["clearance"] / 2, T + 2, mode=Mode.SUBTRACT)

        # 3. Damping Hole (Central)
        Cylinder(4.0, T + 2, mode=Mode.SUBTRACT)

    return p.part
