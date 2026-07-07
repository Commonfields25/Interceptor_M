"""
F1-MOTOR — F1 Motor Mount (Refined L3 - FPV Performance)
Material : 7075-T6 Aluminium
Revision : v3.0-L3 (Wire Protection & Turtle Fin)
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
        # 1. Main Mount Body
        Cylinder(D / 2, H)

        # 2. Integrated Wire Protection Guard
        with Locations((D/2 - 2.0, 0, H/2)):
            Box(6.0, 10.0, H) # Guard block
            # Wire channel
            Box(4.0, 6.0, H + 2, mode=Mode.SUBTRACT)

        # 3. "Turtle-Mode" Structural Fin (Top crash protection)
        with Locations((0, 0, H)):
            Box(1.5, D, 8.0, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 4. Standard Motor Mounting (M4 Clearance + Counterbore)
        pitch = 19.0
        for sx in [-1, 1]:
            for sy in [-1, 1]:
                with Locations((sx * pitch / 2, sy * pitch / 2, 0)):
                    Cylinder(m4["clearance"] / 2, H + 2, mode=Mode.SUBTRACT)
                    with Locations((0, 0, 3.0)): # Recess depth
                        Cylinder(m4["counterbore_dia"] / 2, 10.0, mode=Mode.SUBTRACT)

    return p.part
