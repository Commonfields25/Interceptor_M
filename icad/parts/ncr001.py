"""
NCR-001 — Nose-Cone Interface Ring (PyCad Hi-Fi)
Material : 7075-T6 Aluminium | Process : CNC Milling
Revision : v3.0-L3 (Precision Gland & Alignment)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_ncr001(params: dict = None):
    params = params or {}
    OD = params.get("outer_diameter", 45.0)
    L = params.get("length", 22.0)
    ID = params.get("inner_diameter", 36.0)

    m2_5 = Fasteners.METRIC["M2.5"]

    with BuildPart() as p:
        # 1. Main Ring
        Cylinder(OD / 2, L)
        Cylinder(ID / 2, L + 2, mode=Mode.SUBTRACT)

        # 2. Precision O-Ring Gland (Rectangular for ISO 3601)
        # 1.5mm O-ring -> 2.1mm width, 1.2mm depth
        gland_od = OD - 0.2
        gland_depth = 1.2
        gland_w = 2.1
        with Locations((0, 0, L/2)):
            # Gland cut
            with BuildSketch() as sk:
                Circle(gland_od/2)
                Circle(gland_od/2 - gland_depth, mode=Mode.SUBTRACT)
            extrude(amount=gland_w, both=True, mode=Mode.SUBTRACT)

        # 3. Mounting Pattern (M2.5 Tapped)
        with Locations(PolarLocations(ID/2 + 3.0, 6).locations):
            Cylinder(m2_5["tap_drill"] / 2, 10.0, mode=Mode.SUBTRACT)

        # 4. Anti-Rotation D-Flat
        with Locations((OD/2, 0, L/2)):
            Box(5.0, 10.0, L + 2, mode=Mode.SUBTRACT)

    return p.part
