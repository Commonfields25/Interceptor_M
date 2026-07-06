"""F1-MOTOR — F1 Motor Mount (L3)."""
from build123d import *
def build_f1motor(params=None):
    params = params or {}
    D = params.get("diameter", 28.0)
    with BuildPart() as p:
        Cylinder(D / 2, 10.0, mode=Mode.PRIVATE)
        chamfer(p.edges().filter_by_position(Axis.Z, 10.0, 10.0)[:2], chamfer_size=0.5)
    body = p.part
    for ang in range(4):
        rad = math.radians(ang * 90)
        with BuildPart(mode=Mode.PRIVATE) as pc:
            Cylinder(1.6, 20.0, mode=Mode.SUBTRACT)
            translate((D/2-3)*math.cos(rad), (D/2-3)*math.sin(rad), 0)
        body = body.cut(pc.part)
    return body
