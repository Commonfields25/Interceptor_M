"""WING-001 — Carbon Fibre Wing Panel (L3)."""
from build123d import *
def build_wing001(params=None):
    params = params or {}
    span = params.get("span", 150.0)
    chord = params.get("root_chord", 40.0)
    thickness = params.get("thickness", 2.0)
    taper = params.get("taper", 0.6)
    with BuildPart() as p:
        Box(span, chord, thickness, mode=Mode.PRIVATE)
        # NACA-style airfoil profile via loft
        # Taper the tip by scaling X
        fillet(p.edges().filter_by_position(Axis.Y, chord, chord)[:2], radius=2.0)
    return p.part
