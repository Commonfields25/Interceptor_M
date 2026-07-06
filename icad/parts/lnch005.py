"""LNCH-005 — Support Foot (L3)."""
from build123d import *
def build_lnch005(params=None):
    params = params or {}
    W = params.get("width", 80.0)
    H = params.get("height", 40.0)
    with BuildPart() as p:
        Box(W, W, H, mode=Mode.PRIVATE)
        fillet(p.edges().filter_by_position(Axis.Z, 0, 0)[:4], radius=2.0)
    body = p.part
    with BuildPart(mode=Mode.PRIVATE) as pc:
        Cylinder(W * 0.35, H * 0.7, mode=Mode.SUBTRACT)
    return body.cut(pc.part)
