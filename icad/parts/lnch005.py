from build123d import *
from icad.standards import Fasteners

def build_lnch005(params: dict = None):
    params = params or {}
    W = params.get("width", 100.0)
    T = params.get("thickness", 10.0)
    m5 = Fasteners.METRIC["M5"]
    with BuildPart() as p:
        Box(W, W, T)
        with Locations(GridLocations(W-20, W-20, 2, 2).locations):
            Cylinder(m5["clearance"]/2, T+2, mode=Mode.SUBTRACT)
    return p.part
