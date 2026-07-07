"""
WING-001 — Carbon Fibre Wing Panel (Refined L3)
Material : Carbon Fiber / Foam Core | Process : Sculpted Solid / CNC
Revision : v2.0-L3 (Standardized Fasteners)
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
        # Simple trapezoidal wing box for L3 representation
        # (Loft is complex, keeping it simpler for robust generation)
        tip_chord = chord * taper
        with BuildSketch() as sk:
            with Locations((0, 0)):
                Rectangle(chord, thickness)
        with BuildSketch(Plane.XY.offset(span)) as sk2:
            with Locations((0, 0)):
                Rectangle(tip_chord, thickness)
        loft()

        # 1. Spar (Structural Reinforcement)
        with Locations((chord * 0.25, 0, span / 2)):
            Box(2.0, thickness + 1.0, span)

        # 2. Fastener Pilot Holes (M2.5 Clearance)
        for y in [span * 0.2, span * 0.5, span * 0.8]:
            with Locations((chord * 0.25, 0, y)):
                Cylinder(m2_5["clearance"] / 2, 10.0, mode=Mode.SUBTRACT)
                # Countersink for flat head
                with Locations((0, 0, thickness/2)):
                    Cylinder(m2_5["head_dia"] / 2, 1.0, mode=Mode.SUBTRACT)

    return p.part
