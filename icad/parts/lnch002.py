"""LNCH-002 — Side Rail (L3)."""
from build123d import *
def build_lnch002(params=None):
    params = params or {}
    L = params.get("length", 1500.0)
    W = params.get("width", 40.0)
    H = params.get("height", 30.0)
    with BuildPart() as p:
        Box(L, W, H, mode=Mode.PRIVATE)
        chamfer(p.edges().filter_by_position(Axis.Z, H, H)[:4], chamfer_size=1.0)
    return p.part
