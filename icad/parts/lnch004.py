from build123d import *
from icad.standards import Fasteners

def build_lnch004(params: dict = None):
    params = params or {}
    D = params.get("diameter", 12.0)
    L = params.get("length", 80.0)
    with BuildPart() as p:
        Cylinder(D/2, L)
        with Locations((0, 0, L/2)):
            Cylinder(D*0.75, 5.0)
    return p.part
