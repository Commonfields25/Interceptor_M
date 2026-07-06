"""BAT-3S-001 — 3S Battery Strap (L3)."""
from build123d import *
import math

def build_bat3s001(params=None):
    """
    3S LiPo battery retention strap with:
    - Fabric-covered aluminium base plate
    - Adjustable velcro loop slot
    - Latch hooks (two-sided) for hook-and-loop fastener
    - Padding recess for battery wrap protection
    - Mounting holes at ends for chassis attachment (M2.5)
    - Side guides to prevent lateral battery movement
    """
    params = params or {}
    L      = params.get("length",           70.0)
    W      = params.get("width",            35.0)
    H      = params.get("height",           25.0)
    base_t = params.get("base_thickness",    2.0)

    with BuildPart() as p:
        # Base plate (aluminium, thin)
        with BuildPart() as base:
            Box(L, W, base_t)
        p.part = base.part

        # Side guide walls (upstand to restrain battery)
        for side in [-1, 1]:
            with BuildPart() as wall:
                Box(L, 3, H - base_t)
                translate(0, side * (W / 2 - 1.5), (H - base_t) / 2 + base_t)
            p.part = p.part.fuse(wall.part)

        # Velcro loop slot: thin rectangular channel
        with BuildPart(mode=Mode.PRIVATE) as vs:
            Box(L - 20, 4, H - base_t - 2)
            translate(0, 0, base_t + (H - base_t - 2) / 2)
        p.part = p.part.cut(vs.part)

        # Padding recess (thin recess in base top)
        with BuildPart(mode=Mode.PRIVATE) as pr:
            Box(L - 6, W - 6, 0.8, mode=Mode.SUBTRACT)
            translate(0, 0, base_t - 0.8)
        p.part = p.part.cut(pr.part)

        # End mounting holes (M2.5 clearance × 2)
        for x in [-L/2 + 5, L/2 - 5]:
            with BuildPart(mode=Mode.PRIVATE) as mh:
                Cylinder(1.4, base_t + 4, mode=Mode.SUBTRACT)   # M2.5
                translate(x, 0, -2)
            p.part = p.part.cut(mh.part)
            # Countersink
            with BuildPart(mode=Mode.PRIVATE) as cs:
                Cylinder(3.0, 0.8, mode=Mode.SUBTRACT)
                translate(x, 0, base_t - 0.2)
            p.part = p.part.cut(cs.part)

        # Latch hook feature (small detent bumps at each end)
        for x in [-L/2 + 3, L/2 - 3]:
            with BuildPart(mode=Mode.PRIVATE) as det:
                Cylinder(1.5, 1.5)
                translate(x, 0, base_t + 0.5)
            p.part = p.part.fuse(det.part)

        # Fillets on side walls (comfort, no sharp edges)
        fillet(p.edges().filter_by_position(Axis.X, -L/2, -L/2 + 3)[:4], radius=1.0)
        fillet(p.edges().filter_by_position(Axis.X,  L/2 - 3, L/2)[:4], radius=1.0)
        fillet(p.edges().filter_by_position(Axis.Y, -W/2, -W/2 + 3)[:4], radius=0.5)
        fillet(p.edges().filter_by_position(Axis.Y,  W/2 - 3, W/2)[:4], radius=0.5)

        # Chamfer top of side walls
        chamfer(p.edges().filter_by_position(Axis.Z, H, H)[:4], chamfer_size=0.3)

    return p.part