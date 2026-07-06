"""LNCH-004 — Pivot Pin (L3)."""
from build123d import *
def build_lnch004(params=None):
    params = params or {}
    D = params.get("diameter", 20.0)
    L = params.get("length", 100.0)
    with BuildPart() as p:
        Cylinder(D / 2, L, mode=Mode.PRIVATE)
        chamfer(p.edges().filter_by_position(Axis.Z, L, L)[:2], chamfer_size=0.5)
    return p.part
