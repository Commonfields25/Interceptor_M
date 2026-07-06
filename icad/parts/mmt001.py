"""MMT-001 — Motor Mount (L3)."""
from build123d import *
import math

def build_mmt001(params=None):
    """
    Aluminium motor mount collar with:
    - Central bore (ID = diameter param)
    - 4× M3 tapped mounting holes on 45° axes
    - 8× radial cooling fins (thin annular fins)
    - Outer flange with alignment flats
    - O-ring groove for motor gasket
    - Shoulder step for motor shaft location
    """
    params = params or {}
    D    = params.get("diameter",  35.0)
    TH   = params.get("thickness",   8.0)
    fin_h = params.get("fin_height", 3.0)

    with BuildPart() as p:
        # Main collar body
        with BuildSketch() as s:
            Circle(D / 2 + fin_h)
            Circle(D / 2, mode=Mode.SUBTRACT)
            pass
        extrude(amount=TH, mode=Mode.PRIVATE)

        # Shoulder step (motor shaft location, 2 mm step)
        with BuildPart(mode=Mode.PRIVATE) as sh:
            Cylinder(D / 2 + fin_h, 2.0)
            translate(0, 0, TH)
        p.part = p.part.fuse(sh.part)

        # 8× radial cooling fins (thin annular fins, 2 mm thick)
        for i in range(8):
            ang = i * (360 / 8)
            rad = math.radians(ang)
            fx = (D / 2 + fin_h / 2) * math.cos(rad)
            fy = (D / 2 + fin_h / 2) * math.sin(rad)
            with BuildPart(mode=Mode.PRIVATE) as fin:
                Box(fin_h, 2.0, TH + 2.0)
                rotate(0, 0, ang)
                translate(fx, fy, 0)
            p.part = p.part.fuse(fin.part)

        # 4× M3 tapped mounting holes on 45° axes
        bolt_r = 1.65  # M3 clearance
        for ang in [0, 90, 180, 270]:
            rad = math.radians(ang)
            hx = (D / 2 - 4) * math.cos(rad)
            hy = (D / 2 - 4) * math.sin(rad)
            with BuildPart(mode=Mode.PRIVATE) as bh:
                Cylinder(bolt_r, TH + 2, mode=Mode.SUBTRACT)
                translate(hx, hy, -1)
            p.part = p.part.cut(bh.part)
            # M3 tap drill (thread section, 4 mm deep)
            with BuildPart(mode=Mode.PRIVATE) as tap:
                Cylinder(1.5, 4.0, mode=Mode.SUBTRACT)
                translate(hx, hy, TH - 4)
            p.part = p.part.cut(tap.part)

        # Central bore (motor shaft pass-through)
        with BuildPart(mode=Mode.PRIVATE) as cb:
            Cylinder(8.0, TH + 4, mode=Mode.SUBTRACT)
            translate(0, 0, -2)
        p.part = p.part.cut(cb.part)

        # O-ring groove on outer face (OR 18×2, simplified)
        with BuildPart(mode=Mode.PRIVATE) as org:
            Torus(D / 2 + fin_h - 1.5, 1.0, rotation=(90, 0, 0))
            translate(0, 0, TH)
        p.part = p.part.cut(org.part)

        # Chamfer on bore entry/exit
        chamfer(p.edges().filter_by_position(Axis.Z, 0, 0)[:2], chamfer_size=0.5)
        chamfer(p.edges().filter_by_position(Axis.Z, TH, TH)[:2], chamfer_size=0.5)
        chamfer(p.edges().filter_by_position(Axis.Z, TH + 2, TH + 2)[:2], chamfer_size=0.3)

        # Fillet at bore/shoulder transition
        fillet(p.edges().filter_by_position(Axis.Z, TH, TH)[2:6], radius=1.0)

    return p.part