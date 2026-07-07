"""
LNCH-004 — Pivot Pin (Refined L3)
Material : 17-4 PH Stainless Steel
Revision : v2.0-L3 (Standardized Dimensions)
"""
from build123d import *
from icad.standards import Fasteners

def build_lnch004(params: dict = None):
    params = params or {}
    D = params.get("diameter", 12.0)
    L = params.get("length", 80.0)

    with BuildPart() as p:
        # 1. Main Pin Shaft
        Cylinder(D / 2, L)

        # 2. Enlarged Head
        with Locations((0, 0, L)):
            Cylinder(D * 0.75, 5.0, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 3. Cotter Pin Hole (Standard 3mm)
        with Locations((0, 0, 5.0)):
            Cylinder(1.6, D + 2, rotation=Rot(90, 0, 0), mode=Mode.SUBTRACT)

        # 4. Wrench Flats
        for sx in [-1, 1]:
            with Locations((sx * (D/2 + 2), 0, L + 2.5)):
                Box(4.0, D, 6.0, mode=Mode.SUBTRACT)

    return p.part
