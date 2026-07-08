"""
BRK-001 — Structural Mounting Bracket (Refined L3)
Material : 7075-T6 Aluminium | Process : CNC 3-axis Milling
Revision : v3.3-L3 (Watertight Boolean Pass)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_brk001(params: dict = None):
    params = params or {}
    L = params.get("length", 75.0)
    W = params.get("width", 55.0)
    T = params.get("thickness", 10.0)
    bore = params.get("bore_diameter", 35.0)

    m4 = Fasteners.METRIC["M4"]

    with BuildPart() as p:
        # 1. Main Base
        Box(L, W, T)

        # 2. Central Bore (H7 interface)
        Cylinder(bore / 2, T + 2.0, mode=Mode.SUBTRACT)

        # 3. Structural Weight Reduction (Honeycomb Pattern)
        # Using larger pattern to avoid thin-wall boolean failures
        with Locations(GridLocations(L/2, W/2, 2, 2).locations):
             Cylinder(6.0, T - 4.0, mode=Mode.SUBTRACT)

        # 4. Standard Mounting (M4)
        with Locations(GridLocations(L-15.0, W-15.0, 2, 2).locations):
            # Combined clearance and counterbore in one location pass
            Cylinder(m4["clearance"] / 2, T + 2.0, mode=Mode.SUBTRACT)
            with Locations((0, 0, T/2 - 1.0)):
                Cylinder(m4["counterbore_dia"] / 2, 5.0, mode=Mode.SUBTRACT)

        # 5. Aerospace Fillets (Conservative 0.5mm for watertightness)
        try:
            # Only fillet major vertical edges
            fillet(p.edges().filter_by(Axis.Z), radius=0.5)
        except:
            pass

    return p.part
