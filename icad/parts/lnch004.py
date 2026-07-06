"""LNCH-004 — Pivot Pin, hardened steel (L3)."""
from build123d import *
import math

def build_lnch004(params=None):
    """
    Precision pivot pin with:
    - Ground journal sections (bearing seats) at each end
    - Central enlarged shoulder
    - M8 threaded tip with jam-nut flat
    - Oil-feed hole through shoulder
    - 4× anti-rotation flats (wrench flats)
    """
    params = params or {}
    D     = params.get("diameter",       20.0)
    L     = params.get("length",        100.0)
    thread = params.get("thread_m",        "M8")
    L_jour = params.get("journal_len",  12.0)   # bearing seat length each end
    L_shld = params.get("shoulder_len",  30.0)  # central section length

    # Derived: threaded tip = M8 = 8 mm dia, 25 mm long
    D_thr  = 8.0
    L_thr  = 25.0

    with BuildPart() as p:
        # Left journal (bearing seat)
        with BuildPart(mode=Mode.PRIVATE) as jl:
            Cylinder(D / 2, L_jour)
        p.part = jl.part

        # Central shoulder (larger diameter)
        with BuildPart(mode=Mode.PRIVATE) as sh:
            Cylinder(D * 0.7, L_shld)
            translate(0, 0, L_jour)
        p.part = p.part.fuse(sh.part)

        # Right journal
        with BuildPart(mode=Mode.PRIVATE) as jr:
            Cylinder(D / 2, L_jour)
            translate(0, 0, L_jour + L_shld)
        p.part = p.part.fuse(jr.part)

        # Threaded tip (M8 × 25, simplified as plain cylinder with thread note)
        with BuildPart(mode=Mode.PRIVATE) as tt:
            Cylinder(D_thr / 2, L_thr)
            translate(0, 0, L - L_thr)
        p.part = p.part.fuse(tt.part)

        # Anti-rotation flats: 4× flats on shoulder (wrench flats)
        for ang in [0, 90, 180, 270]:
            rad = math.radians(ang)
            cx = (D * 0.65 / 2) * math.cos(rad)
            cy = (D * 0.65 / 2) * math.sin(rad)
            with BuildPart(mode=Mode.PRIVATE) as wf:
                Box(1.5, 5.5, L_shld + 4)
                translate(cx, cy, L_jour)
            p.part = p.part.cut(wf.part)

        # Oil-feed hole through centre (radial radial)
        with BuildPart(mode=Mode.PRIVATE) as oh:
            Cylinder(1.5, L_shld + 2*L_jour, rotation=(90, 0, 0))
            translate(0, D/2 + 0.1, L_jour + L_shld/2)
        p.part = p.part.cut(oh.part)

        # Shoulder-to-journal fillets (step transitions)
        fillet(p.edges().filter_by_position(Axis.Z, L_jour, L_jour)[:4], radius=2.0)
        fillet(p.edges().filter_by_position(Axis.Z, L_jour + L_shld, L_jour + L_shld)[:4], radius=2.0)

        # Chamfer on thread end
        chamfer(p.edges().filter_by_position(Axis.Z, L, L)[:2], chamfer_size=0.5)
        # Chamfer at journal entry
        chamfer(p.edges().filter_by_position(Axis.Z, 0, 0)[:2], chamfer_size=0.3)

    return p.part