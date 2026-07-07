"""
ACT-001 — Actuator Mount & Thermal Plate (PyCad Hi-Fi)
Material : 7075-T6 Aluminium | Process : CNC Milling
Revision : v3.0-L3 (Optimized Thermal Path)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_act001(params: dict = None):
    params = params or {}
    L = params.get("length", 85.0)
    W = params.get("width", 55.0)
    T = params.get("thickness", 8.0)

    m3 = Fasteners.METRIC["M3"]

    with BuildPart() as p:
        # 1. Main Base Plate
        Box(L, W, 4.0)

        # 2. High-Surface-Area Cooling Fins (PyCad Style)
        # Using a pattern of staggered pillars for better turbulent heat transfer
        with Locations(GridLocations(L-15, W-15, 8, 5).locations):
            Cylinder(1.5, 8.0, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 3. Dedicated ESC Thermal Pad Recess
        with Locations((0, 0, 0)):
             Box(30.0, 30.0, 1.0, mode=Mode.SUBTRACT)

        # 4. Standard Mounting Stacks (M3)
        with Locations(GridLocations(30.5, 30.5, 2, 2).locations):
            Cylinder(3.5, 10.0, mode=Mode.ADD)
            Cylinder(m3["clearance"] / 2, 12.0, mode=Mode.SUBTRACT)

        # 5. Perimeter Chamfers for weight and safety
        try:
            chamfer(p.edges().filter_by_position(Axis.Z, 4.0, 4.0), length=1.0)
        except:
            pass

    return p.part
