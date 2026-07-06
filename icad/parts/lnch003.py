"""LNCH-003 — Corner Bracket (L3)."""
from build123d import *
def build_lnch003(params=None):
    params = params or {}
    OD = params.get("outer_diameter", 120.0)
    ID = params.get("inner_diameter", 80.0)
    with BuildPart() as p:
        Cylinder(OD / 2, 20.0, mode=Mode.PRIVATE)
        chamfer(p.edges().filter_by_position(Axis.Z, 20.0, 20.0)[:2], chamfer_size=1.0)
    body = p.part
    with BuildPart(mode=Mode.PRIVATE) as pi:
        Cylinder(ID / 2, 22.0, mode=Mode.SUBTRACT)
    return body.cut(pi.part)
