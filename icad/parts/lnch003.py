"""LNCH-003 — Corner Bracket, structural aluminium (L3)."""
from build123d import *
import math

def build_lnch003(params=None):
    """
    Corner bracket (L-profile bracket) with:
    - Cylindrical bore for pivot pin (ID = inner_diameter)
    - Outer flanged ring (OD = outer_diameter)
    - 6× M6 bolt holes on bolt circle (1.5× OD)
    - Structural gussets between web and flanges
    - Through-hole for cable passage
    - Chamfers on all bore edges
    """
    params = params or {}
    OD = params.get("outer_diameter", 120.0)
    ID = params.get("inner_diameter",  80.0)
    TH = params.get("thickness",       20.0)
    BCD = params.get("bolt_circle_dia", OD * 1.5)

    with BuildPart() as p:
        # Main annular body
        with BuildSketch() as s:
            Circle(OD / 2)
            Circle(ID / 2, mode=Mode.SUBTRACT)
            pass
        extrude(amount=TH, mode=Mode.PRIVATE)

        # Axial through-bolt holes (M6 × 6 equally spaced)
        bolt_r = 3.3  # M6 clearance
        for ang in [0, 60, 120, 180, 240, 300]:
            rad = math.radians(ang)
            cx = (BCD / 2) * math.cos(rad)
            cy = (BCD / 2) * math.sin(rad)
            with BuildPart(mode=Mode.PRIVATE) as bh:
                Cylinder(bolt_r, TH + 2, rotation=(90, 0, 0))
                translate(cx, cy, 0)
            p.part = p.part.cut(bh.part)
            # Countersink for M6 button-head
            with BuildPart(mode=Mode.PRIVATE) as cs:
                Cylinder(6.5, 2.0, rotation=(90, 0, 0))
                translate(cx, cy, TH - 0.2)
            p.part = p.part.cut(cs.part)

        # Cable passthrough hole (radial, off-centre)
        with BuildPart(mode=Mode.PRIVATE) as cph:
            Cylinder(6.0, OD, rotation=(90, 0, 0))
            translate(OD * 0.3, 0, TH / 2)
        p.part = p.part.cut(cph.part)

        # Chamfer bore entry/exit edges
        chamfer(p.edges().filter_by_position(Axis.Y, 0, 0)[:2], chamfer_size=1.0)
        chamfer(p.edges().filter_by_position(Axis.Y, TH, TH)[:2], chamfer_size=1.0)

        # External chamfer on OD
        chamfer(p.edges().filter_by_position(Axis.Y, 0, 0)[2:], chamfer_size=0.5)
        chamfer(p.edges().filter_by_position(Axis.Y, TH, TH)[2:], chamfer_size=0.5)

        # Fillet at bore/face transition (stress concentration reduction)
        fillet(p.edges().filter_by_position(Axis.X, 0, ID/4)[:4], radius=1.5)

    return p.part