"""
LNCH-004 — Pivot Pin (High-Fidelity L3)
Material : 17-4 PH Stainless Steel
Revision : v3.0-L3 (Bearing Journals & Wrench Flats)
"""
from build123d import *
from icad.standards import Fasteners

def build_lnch004(params: dict = None):
    params = params or {}
    D = params.get("diameter", 12.0)
    L = params.get("length", 80.0)

    with BuildPart() as p:
        # 1. Main Journal (Ground finish assumed)
        Cylinder(D/2, L)

        # 2. Hardened Head
        with Locations((0, 0, L)):
            Cylinder(D*0.8, 6.0, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # 3. Precision Wrench Flats (Standard size)
        with Locations((0, 0, L + 3.0)):
            Box(D*1.5, D*0.8, 6.0, mode=Mode.SUBTRACT)

        # 4. Locking Pin Hole (3mm)
        with Locations((0, 0, 5.0)):
            Cylinder(1.5, D+5.0, rotation=Rot(90, 0, 0), mode=Mode.SUBTRACT)

    return p.part
