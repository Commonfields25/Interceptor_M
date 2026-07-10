"""
PROP-025 — Front Lift ESC Mount (G2)
Material: Al 6061-T6
"""
from build123d import *

def build_prop025(params: dict = None):
    params = params or {}
    W = params.get("width", 40.0)
    L = params.get("length", 60.0)

    with BuildPart() as p:
        Box(L, W, 2.0)
        # Standoff positions
        with Locations(GridLocations(L-10, W-10, 2, 2).locations):
            Cylinder(3.2/2, 10, mode=Mode.SUBTRACT)
        # Cable tie slots
        with Locations(GridLocations(L/2, 0, 2, 1).locations):
            Box(3, W - 10, 5, mode=Mode.SUBTRACT)
    return p.part
