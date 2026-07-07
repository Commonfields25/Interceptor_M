"""
BAT-3S-001 — 3S Battery Strap Retention (Refined L3)
Material : 7075-T6 Aluminium
Revision : v2.0-L3 (Standardized Fasteners)
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
        slot_w = 22.0
        slot_l = 3.0
        for sx in [-1, 1]:
            with Locations((sx * (L/2 - 15), 0, 0)):
                Box(slot_l, slot_w, base_t + 2, mode=Mode.SUBTRACT)

        # 3. Standard End Mounting (M2.5 Clearance)
        for sx in [-1, 1]:
            with Locations((sx * (L/2 - 5), 0, 0)):
                Cylinder(m2_5["clearance"] / 2, base_t + 2, mode=Mode.SUBTRACT)
                # Countersink
                with Locations((0, 0, base_t - 0.5)):
                    Cylinder(m2_5["head_dia"] / 2, 1.0, mode=Mode.SUBTRACT)

    return p.part
