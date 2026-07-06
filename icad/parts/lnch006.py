"""LNCH-006 — Clamp Collar, split-ring aluminium (L3)."""
from build123d import *
import math

def build_lnch006(params=None):
    """
    Split-ring clamp collar with:
    - Annular body with axial split gap
    - 3× radial bolt holes for tightening
    - Inner bore (ID = inner_diameter)
    - Outer flange with 3× mounting holes on BCD
    - 3× torque flats on outer diameter
    - Entry/exit chamfers on bore
    - Small split-gap notches at each end
    """
    params = params or {}
    OD  = params.get("outer_diameter",  50.0)
    ID  = params.get("inner_diameter",  35.0)
    L   = params.get("length",           25.0)
    BCD = params.get("bolt_circle_dia", OD * 1.3)
    N   = params.get("n_splits",             3)  # number of flange holes / flats

    with BuildPart() as p:
        # Main annular body
        with BuildSketch() as s:
            Circle(OD / 2)
            Circle(ID / 2, mode=Mode.SUBTRACT)
            pass
        extrude(amount=L, mode=Mode.PRIVATE)

        # Split gap: thin axial cut slot (2 mm wide)
        with BuildPart(mode=Mode.PRIVATE) as gap:
            Box(2.0, OD, L + 4, rotation=(0, 0, 0))
        p.part = p.part.cut(gap.part)

        # 3× torque flats on OD (for wrench grip)
        flat_w = 6.0
        flat_d = 2.0
        for ang in range(0, 360, int(360 / N)):
            rad = math.radians(ang)
            fx = (OD / 2 - flat_d / 2) * math.cos(rad)
            fy = (OD / 2 - flat_d / 2) * math.sin(rad)
            with BuildPart(mode=Mode.PRIVATE) as tf:
                Box(flat_w, flat_d, L + 2)
                rotate(0, 0, math.degrees(rad))
                translate(fx, fy, -1)
            p.part = p.part.cut(tf.part)

        # 3× radial clamping bolt holes on BCD (M4)
        bolt_r = 2.2  # M4 clearance
        for ang in range(0, 360, int(360 / N)):
            rad = math.radians(ang)
            bx = (BCD / 2) * math.cos(rad)
            by = (BCD / 2) * math.sin(rad)
            with BuildPart(mode=Mode.PRIVATE) as bh:
                Cylinder(bolt_r, OD + 2, rotation=(90, 0, 0))
                translate(bx, by, L / 2)
            p.part = p.part.cut(bh.part)
            # Countersink on OD face
            with BuildPart(mode=Mode.PRIVATE) as cs:
                Cylinder(4.5, 1.5, rotation=(90, 0, 0))
                translate(bx + (OD/2 + 0.1) * math.cos(rad),
                          by + (OD/2 + 0.1) * math.sin(rad),
                          L / 2)
            p.part = p.part.cut(cs.part)

        # 3× flange mounting holes (M5 through-collar, on same BCD, offset 60°)
        for ang in [30, 150, 270]:
            rad = math.radians(ang)
            fx = (BCD / 2) * math.cos(rad)
            fy = (BCD / 2) * math.sin(rad)
            with BuildPart(mode=Mode.PRIVATE) as fh:
                Cylinder(2.7, L + 2, rotation=(90, 0, 0))  # M5 tap
                translate(fx, fy, L / 2)
            p.part = p.part.cut(fh.part)

        # Chamfer bore entry/exit
        chamfer(p.edges().filter_by_position(Axis.Y, 0, 0)[:2], chamfer_size=0.8)
        chamfer(p.edges().filter_by_position(Axis.Y, L, L)[:2], chamfer_size=0.8)
        # OD chamfer
        chamfer(p.edges().filter_by_position(Axis.Y, 0, 0)[2:], chamfer_size=0.3)
        chamfer(p.edges().filter_by_position(Axis.Y, L, L)[2:], chamfer_size=0.3)

    return p.part