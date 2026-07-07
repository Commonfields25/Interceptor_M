from build123d import *
from icad.standards import Fasteners

def build_lnch002(params: dict = None):
    params = params or {}
    L = params.get("length", 60.0)
    W = params.get("width", 60.0)
    T = params.get("thickness", 8.0)
    m5 = Fasteners.METRIC["M5"]
    with BuildPart() as p:
        Box(L, T, 40.0)
        Box(T, W, 40.0)
        with Locations((L/2, 0, 0)):
            Cylinder(m5["clearance"]/2, 20, mode=Mode.SUBTRACT)
    return p.part
