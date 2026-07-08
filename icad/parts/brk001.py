"""
BRK-001 — Structural Mounting Bracket (Aviation L3)
Material : AlSi10Mg | Process : DMLS (3D Metal Printing)
Revision : v2.0-L3 (Aggressive Weight Optimization - Pocketing)
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
        # 1. Main Body
        Box(L, W, T)

        # 2. Central Bore (H7 interface)
        Cylinder(bore / 2, T + 2, mode=Mode.SUBTRACT)

        # 3. Structural Isogrid v2.0 (Aggressive Lightening)
        # 8 pockets instead of 6, larger radius
        pocket_r = 7.0
        with Locations(PolarLocations(bore/2 + pocket_r + 1.5, 8).locations):
             Cylinder(pocket_r, T - 2.0, mode=Mode.SUBTRACT)

        # Additional corner pockets
        with Locations(GridLocations(L-15.0, W-15.0, 2, 2).locations):
             # Don't subtract where mounting holes are
             pass

        # 4. Standard Mounting Pattern (M4)
        with Locations(GridLocations(L-15.0, W-15.0, 2, 2).locations):
            Cylinder(m4["clearance"] / 2, T + 2, mode=Mode.SUBTRACT)
            with Locations((0, 0, T/2 - m4["counterbore_depth"]/2)):
                Cylinder(m4["counterbore_dia"] / 2, m4["counterbore_depth"], mode=Mode.SUBTRACT)

        # 5. Aerospace Finishing
        try:
            fillet(p.edges().filter_by(Axis.Z), radius=2.0)
        except:
            pass

    return p.part
