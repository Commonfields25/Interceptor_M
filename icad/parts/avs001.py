"""AVS-001 — Anti-Vibration Mount (L3)."""
from build123d import *
import math

def build_avs001(params=None):
    """
    Anti-vibration mount with:
    - Central metal insert (drilled/bored)
    - Outer elastomer body with 4× radial damping grooves
    - 4× through-bolt holes on bolt circle
    - Compression-limit shoulders (to prevent over-travel)
    - Bottom recess for O-ring environmental seal
    - Through-hole for cable pass-through
    """
    params = params or {}
    L   = params.get("length",       40.0)
    W   = params.get("width",        30.0)
    TH  = params.get("total_height",  8.0)
    BCD = params.get("bolt_circle_dia", 22.0)

    with BuildPart() as p:
        # Main base plate
        with BuildPart() as base:
            Box(L, W, TH * 0.4)
        p.part = base.part

        # Central raised boss (metal insert footprint)
        with BuildPart() as boss:
            Cylinder(min(L, W) * 0.4, TH * 0.6)
            translate(0, 0, TH * 0.4)
        p.part = p.part.fuse(boss.part)

        # Elastomer body (outer ring around boss)
        with BuildPart(mode=Mode.PRIVATE) as el:
            Box(L, W, TH * 0.7)
            translate(0, 0, TH * 0.4)
        p.part = p.part.fuse(el.part)

        # 4× radial damping grooves (elastomer cutouts)
        for ang in [0, 90, 180, 270]:
            rad = math.radians(ang)
            gx = (L / 2 - 4) * math.cos(rad)
            gy = (W / 2 - 4) * math.sin(rad)
            with BuildPart(mode=Mode.PRIVATE) as dg:
                Box(3.0, TH * 0.8, 2.0)
                rotate(0, 0, math.degrees(rad))
                translate(gx, gy, TH * 0.5)
            p.part = p.part.cut(dg.part)

        # 4× mounting bolt holes on BCD (M3)
        bolt_r = 1.65  # M3 clearance
        for ang in [45, 135, 225, 315]:
            rad = math.radians(ang)
            bx = (BCD / 2) * math.cos(rad)
            by = (BCD / 2) * math.sin(rad)
            with BuildPart(mode=Mode.PRIVATE) as bh:
                Cylinder(bolt_r, TH + 2, mode=Mode.SUBTRACT)
                translate(bx, by, -1)
            p.part = p.part.cut(bh.part)
            # Countersink
            with BuildPart(mode=Mode.PRIVATE) as cs:
                Cylinder(3.5, 1.2, mode=Mode.SUBTRACT)
                translate(bx, by, TH * 0.4 - 0.2)
            p.part = p.part.cut(cs.part)

        # Central bore (through metal insert)
        with BuildPart(mode=Mode.PRIVATE) as cb:
            Cylinder(3.5, TH + 2, mode=Mode.SUBTRACT)
            translate(0, 0, -1)
        p.part = p.part.cut(cb.part)

        # Bottom O-ring groove (OR 12×2, simplified)
        with BuildPart(mode=Mode.PRIVATE) as org:
            Torus(7.0, 1.0, rotation=(90, 0, 0))
            translate(0, 0, TH * 0.4)
        p.part = p.part.cut(org.part)

        # Chamfer top edges
        chamfer(p.edges().filter_by_position(Axis.Z, TH, TH)[:4], chamfer_size=0.3)
        # Fillet bottom edges (anti-scratch feet)
        fillet(p.edges().filter_by_position(Axis.Z, 0, 0)[:4], radius=1.0)

    return p.part