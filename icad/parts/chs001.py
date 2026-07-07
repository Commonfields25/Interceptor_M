"""
CHS-001 — Main Chassis Section (Aviation L3)
Material : AlSi10Mg | Process : DMLS
Revision : v3.0-L3 (Internal T-Slot & Ribbing)
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
        # 1. Main Fuselage Hull
        Cylinder(D / 2, L)
        Cylinder(D / 2 - wall, L + 2, mode=Mode.SUBTRACT)

        # 2. Integrated T-Slot Rail (Inspired by V-Slot)
        # Positioned internally for module sliding
        with BuildSketch() as sk:
            with Locations((0, D/2 - wall - 2.0)):
                Rectangle(6.0, 4.0)
                # Slot cutout
                Rectangle(3.0, 3.0, mode=Mode.SUBTRACT)
        extrude(amount=L)

        # 3. Circumferential Stiffening Ribs
        for z in [L*0.2, L*0.5, L*0.8]:
            with Locations((0, 0, z)):
                with BuildSketch() as sk2:
                    Circle(D/2 - wall)
                    Circle(D/2 - wall - 1.0, mode=Mode.SUBTRACT)
                extrude(amount=2.0, both=True)

        # 4. Standard Mounting Bosses (M3)
        with Locations(PolarLocations(D/2 - wall, 4).locations):
            with Locations((0, 0, 5.0)):
                Cylinder(3.0, 10.0, mode=Mode.ADD)
                Cylinder(m3["tap_drill"] / 2, 12.0, mode=Mode.SUBTRACT)
            with Locations((0, 0, L - 5.0)):
                Cylinder(3.0, 10.0, mode=Mode.ADD)
                Cylinder(m3["tap_drill"] / 2, 12.0, mode=Mode.SUBTRACT)

    return p.part
