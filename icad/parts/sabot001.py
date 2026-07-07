"""
SABOT-001 — Drone Sabot (Refined L3)
Material : ASA | Process : FDM / SLS
Revision : v3.0-L3 (Optimized Deployment)
"""
from build123d import *
import math

def build_sabot001(params: dict = None):
    params = params or {}
    OD = params.get("outer_diameter", 39.8) # 0.2mm tolerance for 40mm bore
    ID = params.get("inner_diameter", 35.2) # 0.2mm tolerance for 35mm fuselage
    L = params.get("length", 40.0)

    with BuildPart() as p:
        # 1. Main Sabot Body (Half-shell design for release)
        Cylinder(OD / 2, L)
        Cylinder(ID / 2, L + 2, mode=Mode.SUBTRACT)

        # 2. Friction-Reducing Outer Grooves
        groove_w = 2.0
        n_grooves = 5
        for i in range(n_grooves):
            with Locations((0, 0, (i+1) * L / (n_grooves+1))):
                # Thin toroidal cut
                with BuildSketch() as sk:
                    Circle(OD/2 + 1.0)
                    Circle(OD/2 - 0.5, mode=Mode.SUBTRACT)
                extrude(amount=groove_w, both=True, mode=Mode.SUBTRACT)

        # 3. Release Split (Cut in half)
        # In a real sabot, these are two separate parts.
        # Here we just model one half or a split line.
        with Locations((0, OD/2, L/2)):
            Box(OD + 2, 0.5, L + 2, mode=Mode.SUBTRACT)

        # 4. Resilience Fingers (Snap locks)
        for ang in [0, 120, 240]:
            rad = math.radians(ang)
            with Locations(( (ID/2)*math.cos(rad), (ID/2)*math.sin(rad), L )):
                # Small flexible tab
                Box(4.0, 2.0, 6.0, align=(Align.CENTER, Align.CENTER, Align.MIN))

    return p.part
