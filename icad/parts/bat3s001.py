"""BAT-3S-001 — 3S Battery Strap (L3)."""
from build123d import *
def build_bat3s001(params=None):
    params = params or {}
    L = params.get("length", 70.0)
    W = params.get("width", 35.0)
    H = params.get("height", 25.0)
    with BuildPart() as p:
        Box(L, W, 3.0, mode=Mode.PRIVATE)
        fillet(p.edges().filter_by_position(Axis.Z, 0, 0)[:2], radius=1.0)
    body = p.part
    with BuildPart(mode=Mode.PRIVATE) as ps:
        Box(L - 10, W * 0.4, H, mode=Mode.SUBTRACT)
    body = body.cut(ps.part)
    return body
