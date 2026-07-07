from build123d import *
from icad.standards import Fasteners

def build_lnch006(params: dict = None):
    params = params or {}
    OD = params.get("outer_diameter", 60.0)
    ID = params.get("inner_diameter", 40.0)
    L = params.get("length", 20.0)
    m5 = Fasteners.METRIC["M5"]
    with BuildPart() as p:
        Cylinder(OD/2, L)
        Cylinder(ID/2, L+2, mode=Mode.SUBTRACT)
        with Locations((OD/2, 0, 0)):
            Box(20, 2, L+2, mode=Mode.SUBTRACT)
    return p.part
