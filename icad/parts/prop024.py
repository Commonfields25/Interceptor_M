"""
PROP-024 — Front Lift Pylon Link (G2)
Material: Al 7075-T6 | Process: CNC
"""
from build123d import *

def build_prop024(params: dict = None):
    params = params or {}
    L = params.get("length", 100.0)
    W = params.get("width", 20.0)
    T = params.get("thickness", 8.0)

    with BuildPart() as p:
        Box(L, W, T)
        # Attachment holes
        with Locations((L/2 - 10, 0, 0)):
            Cylinder(5.2/2, T + 2, mode=Mode.SUBTRACT)
        with Locations((-L/2 + 10, 0, 0)):
            Cylinder(5.2/2, T + 2, mode=Mode.SUBTRACT)
        # Weight reduction pockets
        with Locations((0, 0, 0)):
            Box(L - 40, W - 8, T + 2, mode=Mode.SUBTRACT)
    return p.part
