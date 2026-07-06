"""LNCH-005 — Support Foot, structural aluminium (L3)."""
from build123d import *
import math

def build_lnch005(params=None):
    """
    Adjustable support foot with:
    - Rectangular base plate with 4× bolt holes
    - Central cylindrical height adjuster socket
    - Diagonal gusset webs for stiffness
    - Rubber pad recess on base
    - Bolt pocket (countersunk head recess) in top face
    """
    params = params or {}
    W     = params.get("width",           80.0)
    H     = params.get("height",           40.0)
    sock  = params.get("socket_dia",       28.0)  # centre bore
    pad   = params.get("pad_recess_depth",  1.5)

    with BuildPart() as p:
        # Base plate (slightly wider than body, rounded corners)
        with BuildPart(mode=Mode.PRIVATE) as base:
            Box(W + 10, W + 10, 6.0)
        p.part = base.part

        # Main body (central block)
        with BuildPart(mode=Mode.PRIVATE) as body:
            Box(W, W, H - 6.0)
            translate(0, 0, 6.0)
        p.part = p.part.fuse(body.part)

        # Diagonal gusset webs (triangulate base to body)
        for ang in [45, 135, 225, 315]:
            rad = math.radians(ang)
            gx = (W / 2 - 4) * math.cos(rad)
            gy = (W / 2 - 4) * math.sin(rad)
            with BuildPart(mode=Mode.PRIVATE) as guss:
                Box(4.0, W * 0.9, H - 6.0)
                rotate(0, 0, math.degrees(rad))
                translate(gx, gy, 6.0 + (H - 6.0) / 2)
            p.part = p.part.fuse(guss.part)

        # Central height-adjuster socket (bore)
        with BuildPart(mode=Mode.PRIVATE) as soc:
            Cylinder(sock / 2, H + 4, mode=Mode.SUBTRACT)
            translate(0, 0, -2)
        p.part = p.part.cut(soc.part)

        # 4× mounting bolt holes in base (M8 clearance)
        for ang in [45, 135, 225, 315]:
            rad = math.radians(ang)
            bx = (W / 2 + 5) * math.cos(rad)
            by = (W / 2 + 5) * math.sin(rad)
            with BuildPart(mode=Mode.PRIVATE) as bh:
                Cylinder(4.3, 8, mode=Mode.SUBTRACT)   # M8 clearance
                translate(bx, by, -2)
            p.part = p.part.cut(bh.part)
            # Countersink
            with BuildPart(mode=Mode.PRIVATE) as cs:
                Cylinder(10.0, 2.5, mode=Mode.SUBTRACT)
                translate(bx, by, 3.9)
            p.part = p.part.cut(cs.part)

        # Rubber pad recess on base bottom
        with BuildPart(mode=Mode.PRIVATE) as rp:
            Box(W + 4, W + 4, pad, mode=Mode.SUBTRACT)
        p.part = p.part.cut(rp.part)

        # Fillets: base edges and gusset junctions
        fillet(p.edges().filter_by_position(Axis.Z, 0, 0)[:4], radius=2.0)
        fillet(p.edges().filter_by_position(Axis.Z, H, H)[:4], radius=1.5)
        fillet(p.edges().filter_by_position(Axis.X, W/2, W/2)[:4], radius=1.0)

        # All bottom edges chamfered
        chamfer(p.edges().filter_by_position(Axis.Z, 0, pad)[:8], chamfer_size=0.5)

    return p.part