"""
BAT-3S-001 — 3S Battery Strap Retention (Refined L3)
Material : 7075-T6 Aluminium
Revision : v3.1-L3 (PyCad Calibration)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_bat3s001(params: dict = None):
    params = params or {}
    L = params.get("length", 70.0)
    W = params.get("width", 35.0)
    base_t = params.get("base_thickness", 2.5)

    m2_5 = Fasteners.METRIC["M2.5"]

    with BuildPart() as p:
        # 1. Base Plate
        Box(L, W, base_t)

        # 2. Velcro Strap Slots (Standard 20mm strap)
        with Locations(GridLocations(L-30, 0, 2, 1).locations):
            Box(3.0, 22.0, base_t + 2, mode=Mode.SUBTRACT)

        # 3. Standard End Mounting (M2.5 Clearance)
        with Locations(GridLocations(L-10, 0, 2, 1).locations):
            Cylinder(m2_5["clearance"] / 2, base_t + 2, mode=Mode.SUBTRACT)
            # Countersink
            with Locations((0, 0, base_t/2 - 0.5)):
                Cylinder(m2_5["head_dia"] / 2, 1.0, mode=Mode.SUBTRACT)

    return p.part
