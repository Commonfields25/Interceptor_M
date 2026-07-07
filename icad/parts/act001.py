"""
ACT-001 — Actuator Mount & Thermal Plate (Refined L3)
Material : 7075-T6 Aluminium | Process : CNC 3-axis Milling
Revision : v2.0-L3 (Enhanced Heat Dissipation)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_act001(params: dict = None):
    params = params or {}
    L = params.get("length", 65.0)
    W = params.get("width", 45.0)
    T = params.get("thickness", 8.0) # Increased for fins

    m2 = Fasteners.METRIC["M2"]
    m3 = Fasteners.METRIC["M3"]

    with BuildPart() as p:
        # 1. Base Plate
        Box(L, W, 4.0) # Base 4mm

        # 2. Thermal Dissipation Fins (Top surface)
        fin_w = 1.0
        fin_gap = 2.0
        fin_h = 4.0
        n_fins = int(L / (fin_w + fin_gap))
        for i in range(n_fins):
            with Locations(( -L/2 + i*(fin_w+fin_gap) + fin_w/2, 0, 4.0 + fin_h/2 )):
                Box(fin_w, W - 10.0, fin_h)

        # 3. Component Pockets (Subtractive)
        # Main ESC/FC pocket
        with Locations((0, 0, 2.0)):
            Box(L - 10.0, W - 10.0, 4.0, mode=Mode.SUBTRACT)

        # 4. Standard Mounting (M3 Clearance + Counterbore)
        for sx in [-1, 1]:
            for sy in [-1, 1]:
                with Locations((sx * (L/2 - 5), sy * (W/2 - 5), 0)):
                    Cylinder(m3["clearance"] / 2, 10.0, mode=Mode.SUBTRACT)
                    with Locations((0, 0, 4.0 - m3["counterbore_depth"])):
                        Cylinder(m3["counterbore_dia"] / 2, m3["counterbore_depth"] + 1, mode=Mode.SUBTRACT)

        # 5. Cable Management Grooves
        for sy in [-1, 1]:
            with Locations((0, sy * (W/2 - 3), 2.0)):
                Box(L + 2, 2.0, 2.0, mode=Mode.SUBTRACT)

    return p.part
