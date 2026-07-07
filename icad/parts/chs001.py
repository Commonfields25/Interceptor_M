"""
CHS-001 — Main Chassis Section (Refined L3)
Material : AlSi10Mg | Process : DMLS
Revision : v2.0-L3 (Optimized Strength-to-Weight)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_chs001(params: dict = None):
    params = params or {}
    L = params.get("section_length", 100.0)
    D = params.get("diameter", 35.0)
    wall = params.get("wall_thickness", 1.5)

    m3 = Fasteners.METRIC["M3"]

    with BuildPart() as p:
        # 1. Outer Fuselage Tube
        Cylinder(D / 2, L)
        Cylinder(D / 2 - wall, L + 2, mode=Mode.SUBTRACT)

        # 2. Longitudinal Stiffening Ribs (Internal)
        rib_h = 1.0
        rib_w = 1.5
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            with Locations(( (D/2 - wall/2)*math.cos(rad), (D/2 - wall/2)*math.sin(rad), L/2 )):
                # Internal rib
                Box(rib_w, rib_h, L, rotation=Rot(0, 0, math.degrees(ang)))

        # 3. Inter-Module Mounting (M3 Tapped Bosses)
        for ang in [0, 90, 180, 270]:
            rad = math.radians(ang)
            bx = (D/2 - wall) * math.cos(rad)
            by = (D/2 - wall) * math.sin(rad)
            # Create a small boss inside the tube
            with Locations((bx, by, 5.0)):
                Cylinder(3.0, 10.0, mode=Mode.ADD)
                Cylinder(m3["tap_drill"] / 2, 12.0, mode=Mode.SUBTRACT)
            with Locations((bx, by, L - 5.0)):
                Cylinder(3.0, 10.0, mode=Mode.ADD)
                Cylinder(m3["tap_drill"] / 2, 12.0, mode=Mode.SUBTRACT)

    return p.part
