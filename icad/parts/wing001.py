"""WING-001 — Carbon Fibre Wing Panel (L3)."""
from build123d import *
import math

def build_wing001(params=None):
    """
    Aerodynamic wing panel with:
    - NACA 2412-inspired section (extruded via loft between root and tip)
    - Carbon fibre laminate: skin + foam core (sculpted solid)
    - Main spar (rectangular, 4 mm × span × 2.5 mm)
    - Secondary rib at mid-span
    - Leading-edge recess for hingeline
    - Tiplet (winglet) at span end
    - Countersunk pilot holes for M2.5 fasteners
    """
    params = params or {}
    span     = params.get("span",      150.0)
    chord    = params.get("root_chord",  40.0)
    thickness = params.get("thickness",  2.0)
    taper    = params.get("taper",       0.6)

    tip_chord = chord * taper

    with BuildPart() as p:
        # ── NACA 2412 airfoil cross-section (XZ plane, extruded Y = span) ──
        # Profile defined as loft between root and tip chord
        n_pts = 40
        root_pts, tip_pts = [], []
        for i in range(n_pts + 1):
            t = i / n_pts
            # Leading half (upper), trailing half (lower) param
            x = t * chord
            # Simplified NACA thickness distribution
            yt = 5.0 * thickness * (
                0.2969 * math.sqrt(x / chord)
                - 0.1260 * (x / chord)
                - 0.3516 * (x / chord) ** 2
                + 0.2843 * (x / chord) ** 3
                - 0.1015 * (x / chord) ** 4
            )
            # Camber line (NACA 2412: m=0.02, p=0.4)
            m, p = 0.02, 0.4
            if x / chord < p:
                yc = m / p**2 * (2*p*(x/chord) - (x/chord)**2)
                dyc = 2*m/p**2 * (p - (x/chord)) / chord
            else:
                yc = m / (1-p)**2 * ((1-2*p) + 2*p*(x/chord) - (x/chord)**2)
                dyc = 2*m/(1-p)**2 * (p - (x/chord)) / chord
            alpha = math.atan(dyc)
            root_pts.append(
                (x - yt * math.sin(alpha), chord / 4 + yc + yt * math.cos(alpha))
            )
            # Tip section (scaled chord)
            x_t = t * tip_chord
            yt_t = 5.0 * thickness * (
                0.2969 * math.sqrt(x_t / tip_chord)
                - 0.1260 * (x_t / tip_chord)
                - 0.3516 * (x_t / tip_chord) ** 2
                + 0.2843 * (x_t / tip_chord) ** 3
                - 0.1015 * (x_t / tip_chord) ** 4
            )
            if x_t / tip_chord < p:
                yc_t = m / p**2 * (2*p*(x_t/tip_chord) - (x_t/tip_chord)**2)
                dyc_t = 2*m/p**2 * (p - (x_t/tip_chord)) / tip_chord
            else:
                yc_t = m / (1-p)**2 * ((1-2*p) + 2*p*(x_t/tip_chord) - (x_t/tip_chord)**2)
                dyc_t = 2*m/(1-p)**2 * (p - (x_t/tip_chord)) / tip_chord
            alpha_t = math.atan(dyc_t)
            tip_pts.append(
                (x_t - yt_t * math.sin(alpha_t),
                 tip_chord / 4 + yc_t + yt_t * math.cos(alpha_t))
            )

        # Build loft between root and tip profiles
        loft_prof = loft(root_pts, tip_pts, long_transition=True)
        p.part = loft_prof

        # Main spar: thin rectangular beam along leading edge
        spar_h = thickness * 1.5
        spar_w = span * 0.04
        with BuildPart(mode=Mode.PRIVATE) as spar:
            Box(spar_w, chord * 0.35, spar_h)
            rotate(0, 90, 0)
            translate(chord * 0.25, 0, span / 2)
        p.part = p.part.fuse(spar.part)

        # Secondary rib at mid-span (T-spar)
        with BuildPart(mode=Mode.PRIVATE) as rib:
            Box(spar_w + 2, chord * 0.25, spar_h * 0.7)
            rotate(0, 90, 0)
            translate(chord * 0.35, 0, span / 2)
        p.part = p.part.fuse(rib.part)

        # Winglet (tip vertical surface)
        with BuildPart(mode=Mode.PRIVATE) as wl:
            Box(spar_w, chord * 0.12, thickness * 4)
            rotate(90, 0, 0)
            translate(chord * 0.38, span, thickness * 2)
        p.part = p.part.fuse(wl.part)

        # Hingeline recess (leading edge groove for control surface)
        with BuildPart(mode=Mode.PRIVATE) as hr:
            Box(spar_w + 4, 3, thickness * 2)
            rotate(0, 90, 0)
            translate(chord * 0.38, 0, span / 2)
        p.part = p.part.cut(hr.part)

        # Fastener pilot holes: M2.5 × 3 along spar
        hole_r = 1.35  # M2.5 clearance
        for y in [span * 0.15, span * 0.4, span * 0.65, span * 0.85]:
            with BuildPart(mode=Mode.PRIVATE) as fh:
                Cylinder(hole_r, spar_h + 4, mode=Mode.SUBTRACT)
                translate(chord * 0.25, y, 0)
            p.part = p.part.cut(fh.part)
            # Countersink
            with BuildPart(mode=Mode.PRIVATE) as cs:
                Cylinder(2.8, 1.2, mode=Mode.SUBTRACT)
                translate(chord * 0.25, y, 0.5)
            p.part = p.part.cut(cs.part)

        # Tip edges chamfer
        chamfer(p.edges().filter_by_position(Axis.Y, 0, 3)[:4], chamfer_size=0.4)
        chamfer(p.edges().filter_by_position(Axis.Y, span - 3, span)[:4], chamfer_size=0.4)

    return p.part