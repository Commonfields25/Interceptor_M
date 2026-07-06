"""MMT-001 — Motor Mount (L3)."""
from build123d import *
def build_mmt001(params=None):
    params = params or {}
    D = params.get("diameter", 35.0)
    with BuildPart() as p:
        Cylinder(D / 2, 8.0, mode=Mode.PRIVATE)
        chamfer(p.edges().filter_by_position(Axis.Z, 8.0, 8.0)[:2], chamfer_size=0.5)
    body = p.part
    for ang in [0, 90, 180, 270]:
        rad = math.radians(ang)
        hx, hy = (D/2 - 4) * math.cos(rad), (D/2 - 4) * math.sin(rad)
        with BuildPart(mode=Mode.PRIVATE) as pc:
            Cylinder(1.5, 15.0, mode=Mode.SUBTRACT)
            translate(hx, hy, 0)
        body = body.cut(pc.part)
    with BuildPart(mode=Mode.PRIVATE) as pb:
        Cylinder(8.0, 10.0, mode=Mode.SUBTRACT)
    return body.cut(pb.part)
