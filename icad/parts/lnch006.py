"""LNCH-006 — Clamp Collar (L3)."""
from build123d import *
def build_lnch006(params=None):
    params = params or {}
    OD = params.get("outer_diameter", 50.0)
    ID = params.get("inner_diameter", 35.0)
    L = params.get("length", 25.0)
    with BuildPart() as p:
        Cylinder(OD / 2, L, mode=Mode.PRIVATE)
        chamfer(p.edges().filter_by_position(Axis.Z, L, L)[:2], chamfer_size=0.5)
    body = p.part
    with BuildPart(mode=Mode.PRIVATE) as pi:
        Cylinder(ID / 2, L + 2, mode=Mode.SUBTRACT)
        translate(0, 0, -1)
    body = body.cut(pi.part)
    for ang in [0, 120, 240]:
        rad = math.radians(ang)
        with BuildPart(mode=Mode.PRIVATE) as ps:
            Box(4.0, OD * 0.55, L + 2, rotation=(0, 0, math.degrees(rad)), mode=Mode.SUBTRACT)
        body = body.cut(ps.part)
    return body
