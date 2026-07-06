"""LNCH-001 — Main Launch Rail (L3)."""
from build123d import *
def build_lnch001(params=None):
    params = params or {}
    L = params.get("length", 2000.0)
    W = params.get("width", 250.0)
    H = params.get("height", 60.0)
    with BuildPart() as p:
        Box(L, W, H, mode=Mode.PRIVATE)
        fillet(p.edges().filter_by_position(Axis.Z, H, H)[:4], radius=2.0)
    return p.part
