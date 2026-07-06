"""LNCH-002 — Side Rail, 1.5 m U-channel aluminium (L3)."""
from build123d import *
import math

def build_lnch002(params=None):
    """
    1.5 m side rail (U-channel) with:
    - Open U-section with inner guide lip
    - Clamp-mounting slots on back face
    - End milled for pinned joint
    - Cable-tie slots every 150 mm
    """
    params = params or {}
    L  = params.get("length",       1500.0)
    W  = params.get("width",         40.0)
    H  = params.get("height",        30.0)
    tf = params.get("flange_thick",   5.0)
    li = params.get("lip_inward",    4.0)

    with BuildPart() as p:
        # Main U-channel body
        with BuildSketch() as s:
            # Outer profile
            with Locations((0, H)):
                Rectangle(W, tf)                   # top flange
            with Locations((0, tf/2)):
                Rectangle(W, tf)                   # bottom flange
            with Locations((0, H/2)):
                Rectangle(6, H - 2*tf)            # web
            pass
        extrude(amount=L, mode=Mode.PRIVATE)

        # Inner guide lip (top, two rails)
        for x_off in [-W/4, W/4]:
            with BuildPart(mode=Mode.PRIVATE) as gl:
                Box(3, H - 2*tf - 2, L)
                translate(x_off, H/2, 0)
            p.part = p.part.cut(gl.part)

        # Clamp-mounting slots on back (bottom flange face)
        for z in range(75, int(L - 74), 150):
            with BuildPart(mode=Mode.PRIVATE) as cs:
                Box(W - 6, 3, 12)
                translate(0, tf/2, z)
            p.part = p.part.cut(cs.part)

        # End milled features (pinned joint detail at both ends)
        for z_end in [0, L]:
            with BuildPart(mode=Mode.PRIVATE) as em:
                Cylinder(4.0, 10, mode=Mode.SUBTRACT)
                translate(0, H - 4, z_end)
            p.part = p.part.cut(em.part)
            with BuildPart(mode=Mode.PRIVATE) as ef:
                Box(W, 2, 6)
                translate(0, H, z_end)
            p.part = p.part.cut(ef.part)

        # Cable-tie slots every 150 mm on back web
        for z in range(100, int(L - 99), 150):
            with BuildPart(mode=Mode.PRIVATE) as cts:
                Box(4, H - 2*tf - 4, 1.5)
                translate(-W/2 + 3, H/2, z)
            p.part = p.part.cut(cts.part)

        # Chamfers: top/bottom flanges edges
        chamfer(p.edges().filter_by_position(Axis.Y, H, H)[:4], chamfer_size=0.5)
        chamfer(p.edges().filter_by_position(Axis.Y, 0,  tf)[:4], chamfer_size=0.3)
        chamfer(p.edges().filter_by_position(Axis.Z, 0,  0)[:4], chamfer_size=0.5)
        chamfer(p.edges().filter_by_position(Axis.Z, L,  L)[:4], chamfer_size=0.5)

        # Fillets at web/flange junctions for stress relief
        fillet(p.edges().filter_by_position(Axis.Y, H - tf, H - tf)[:4], radius=1.0)
        fillet(p.edges().filter_by_position(Axis.Y, tf, tf)[:4], radius=1.0)

    return p.part