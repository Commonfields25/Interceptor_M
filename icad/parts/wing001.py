"""
WING-001 — Carbon Fibre Wing Panel (PyCad L3)
Material : Carbon Fiber / Foam Core | Process : DMLS Mold / CNC
Revision : v3.0-L3 (Internal Spar & Rib structure)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_wing001(params: dict = None):
    params = params or {}
    span = params.get("span", 150.0)
    chord = params.get("root_chord", 40.0)
    thickness = params.get("thickness", 2.0)
    taper = params.get("taper", 0.6)

    m2_5 = Fasteners.METRIC["M2.5"]

    with BuildPart() as p:
        # 1. Wing Outer Mold (Simplified Aerofoil)
        tip_chord = chord * taper
        with BuildSketch() as sk:
            # Root: Cambered rectangle
            Rectangle(chord, thickness)
        with BuildSketch(Plane.XY.offset(span)) as sk2:
            # Tip
            Rectangle(tip_chord, thickness)
        loft()

        # 2. Main Structural Spar (Internal Box Beam)
        with Locations((chord * 0.1, 0, span / 2)):
             Box(chord * 0.15, thickness + 0.5, span)

        # 3. Transverse Ribs (Weight Reduction / Stiffening)
        for y in [span * 0.25, span * 0.5, span * 0.75]:
            with Locations((0, 0, y)):
                Box(chord, thickness * 0.8, 2.0, mode=Mode.SUBTRACT)

        # 4. Standard Mounting Interfaces (M2.5)
        # Taper-aligned mounting
        with Locations((chord * 0.1, 0, 5.0)):
            Cylinder(m2_5["clearance"] / 2, 10.0, mode=Mode.SUBTRACT)

    return p.part
