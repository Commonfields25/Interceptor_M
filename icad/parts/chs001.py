"""CHS-001 — Main Chassis Section (L3)."""
from build123d import *
def build_chs001(params=None):
    params = params or {}
    L = params.get("section_length", 500.0)
    W = params.get("width", 150.0)
    H = params.get("height", 60.0)
    wall = params.get("wall_thickness", 3.0)
    with BuildPart() as p:
        Box(L, W, H, mode=Mode.PRIVATE)
        fillet(p.edges().filter_by_position(Axis.Z, H, H)[:4], radius=2.0)
    body = p.part
    with BuildPart(mode=Mode.PRIVATE) as pi:
        Box(L + 2, W - wall * 2, H - wall * 2, mode=Mode.SUBTRACT)
    return body.cut(pi.part)
