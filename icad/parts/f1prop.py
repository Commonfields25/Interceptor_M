"""F1-PROP — F1 Propeller Hub (L3)."""
from build123d import *
def build_f1prop(params=None):
    params = params or {}
    R = params.get("radius", 50.0)
    with BuildPart() as p:
        Cylinder(8.0, 4.0, mode=Mode.PRIVATE)
        chamfer(p.edges().filter_by_position(Axis.Z, 4.0, 4.0)[:2], chamfer_size=0.5)
    body = p.part
    for i in range(3):
        ang = 2 * math.pi * i / 3
        with BuildPart(mode=Mode.PRIVATE) as pb:
            Box(R * 0.8, 10.0, 2.0, rotation=(0, 0, math.degrees(ang)), mode=Mode.SUBTRACT)
        body = body.cut(pb.part)
    return body
