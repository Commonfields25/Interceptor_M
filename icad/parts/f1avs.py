"""F1-AVS — F1 Anti-Vibration Mount (L3)."""
from build123d import *
def build_f1avs(params=None):
    params = params or {}
    L = params.get("length", 25.0)
    W = params.get("width", 20.0)
    with BuildPart() as p:
        Box(L, W, 4.0, mode=Mode.PRIVATE)
        fillet(p.edges().filter_by_position(Axis.Z, 0, 0)[:2], radius=1.0)
    body = p.part
    for x in [L*0.35, L*0.65]:
        with BuildPart(mode=Mode.PRIVATE) as pc:
            Cylinder(2.5, 12.0, mode=Mode.SUBTRACT)
            translate(x, W/2, 0)
        body = body.cut(pc.part)
    return body
