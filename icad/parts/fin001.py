"""
FIN-001 — Stabilizing Fin (L3 Manufacturing)
Type: Trapezoidal Planform
"""
from build123d import *
import math

def build_fin001(params: dict = None):
    params = params or {}
    root_chord = params.get("root_chord", 40.0)
    tip_chord = params.get("tip_chord", 20.0)
    span = params.get("span", 30.0)
    thickness = params.get("thickness", 2.0)
    sweep = params.get("sweep_angle", 20.0)

    with BuildPart() as p:
        with BuildSketch() as sk:
            with BuildLine() as bl:
                p0 = (0, 0)
                p1 = (root_chord, 0)
                dx = span * math.tan(math.radians(sweep))
                p2 = (dx + tip_chord, span)
                p3 = (dx, span)
                Polyline(p0, p1, p2, p3, p0)
            make_face()
        extrude(amount=thickness/2, both=True)
    return p.part
