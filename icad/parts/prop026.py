"""
PROP-026 — Tilt Pivot Bracket (G2)
Material: Al 7075-T6 + Steel Pin
"""
from build123d import *

def build_prop026(params: dict = None):
    params = params or {}
    pivot_dia = params.get("pivot_diameter", 8.0)
    width = params.get("width", 30.0)

    with BuildPart() as p:
        # Main Block
        Box(20, width, 25)
        # Pivot Bore
        with Locations(Rot(0, 90, 0)):
            Cylinder(pivot_dia/2 + 0.1, 30, mode=Mode.SUBTRACT)
        # Mounting Flange
        with Locations((0, 0, -10)):
            Box(40, width, 5, align=(Align.CENTER, Align.CENTER, Align.MAX))
        # Mounting Holes
        with Locations(GridLocations(30, width - 10, 2, 2).locations):
            with Locations((0, 0, -10)):
                Cylinder(4.2/2, 10, mode=Mode.SUBTRACT)
    return p.part
