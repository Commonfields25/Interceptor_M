"""F1-BODY-01 — F1 Drone Body Shell (L3)."""
from build123d import *
def build_f1body01(params=None):
    params = params or {}
    L = params.get("length", 120.0)
    W = params.get("width", 80.0)
    H = params.get("height", 30.0)
    with BuildPart() as p:
        Box(L, W, H, mode=Mode.PRIVATE)
        fillet(p.edges().filter_by_position(Axis.Z, H, H)[:4], radius=3.0)
    body = p.part
    with BuildPart(mode=Mode.PRIVATE) as pi:
        Box(L - 2.0, W - 2.0, H - 2.0, mode=Mode.SUBTRACT)
    return body.cut(pi.part)
