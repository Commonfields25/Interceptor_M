"""AVS-001 — Anti-Vibration Mount (L3)."""
from build123d import *
def build_avs001(params=None):
    params = params or {}
    L = params.get("length", 40.0)
    W = params.get("width", 30.0)
    with BuildPart() as p:
        Box(L, W, 5.0, mode=Mode.PRIVATE)
        chamfer(p.edges().filter_by_position(Axis.Z, 5.0, 5.0)[:4], chamfer_size=0.3)
    body = p.part
    for x in [L*0.3, L*0.7]:
        with BuildPart(mode=Mode.PRIVATE) as pc:
            Cylinder(3.0, 12.0, mode=Mode.SUBTRACT)
        body = body.cut(pc.part)
    return body
