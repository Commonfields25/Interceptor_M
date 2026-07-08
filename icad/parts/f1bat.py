"""
F1-BAT — F1 Battery Tray (Refined L3)
Material : 7075-T6 Aluminium
Revision : v3.0-L3 (PyCad Calibration & Robust Booleans)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_f1bat(params: dict = None):
    params = params or {}
    L = params.get("length", 60.0)
    W = params.get("width", 30.0)
    H = params.get("height", 15.0)
    T = params.get("wall_thickness", 2.0)

    m3 = Fasteners.METRIC["M3"]

    with BuildPart() as p:
        # 1. Main Tray Box
        Box(L, W, 2.0) # Base

        # 2. Side Walls
        with Locations(GridLocations(0, W - 2.0, 1, 2).locations):
            Box(L, 2.0, H, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 3. Internal Stiffening Ribs (Cross-grid)
        with Locations(GridLocations(L/2, W/2, 2, 2).locations):
            Box(2.0, 2.0, H, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 4. Standard Mounting Patterns (M3)
        with Locations(GridLocations(L-10, 0, 2, 1).locations):
            Cylinder(m3["clearance"] / 2, 10.0, mode=Mode.SUBTRACT)

        # 5. Velcro Strap Channels
        with Locations(GridLocations(L/3, 0, 2, 1).locations):
            Box(3.0, W + 2.0, 2.0, mode=Mode.SUBTRACT)

        # 6. Safety Finishing
        try:
            # Conservative chamfer on base edges
            chamfer(p.edges().filter_by_position(Axis.Z, 0, 0), length=0.3)
        except:
            pass

    return p.part
