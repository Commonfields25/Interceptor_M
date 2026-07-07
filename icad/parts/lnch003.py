from build123d import *
from icad.standards import Fasteners

def build_lnch003(params: dict = None):
    params = params or {}
    W = params.get("width", 40.0)
    H = params.get("height", 40.0)
    T = params.get("thickness", 15.0)
    m5 = Fasteners.METRIC["M5"]
    with BuildPart() as p:
        Box(W, H, T)
        with Locations((0, 0, T/2)):
            Cylinder(10.0, 5.0, mode=Mode.SUBTRACT)
        with Locations(GridLocations(W-10, H-10, 2, 2).locations):
            Cylinder(m5["clearance"]/2, T+2, mode=Mode.SUBTRACT)
    return p.part
