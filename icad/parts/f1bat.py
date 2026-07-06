"""F1-BAT — F1 Battery Tray (L3)."""
from build123d import *
def build_f1bat(params=None):
    params = params or {}
    L = params.get("length", 60.0)
    W = params.get("width", 30.0)
    H = params.get("height", 15.0)
    with BuildPart() as p:
        Box(L, W, H, mode=Mode.PRIVATE)
        fillet(p.edges().filter_by_position(Axis.Z, H, H)[:4], radius=2.0)
    body = p.part
    with BuildPart(mode=Mode.PRIVATE) as pi:
        Box(L - 3.0, W - 3.0, H + 1, mode=Mode.SUBTRACT)
    return body.cut(pi.part)
