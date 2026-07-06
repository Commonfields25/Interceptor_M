"""CHS-001 — Main Chassis Section (L3)."""
from build123d import *
import math

def build_chs001(params=None):
    """
    Modular fuselage chassis section with:
    - Hollow square-tube (SWS) profile with wall_thickness
    - 4× longitudinal T-slot rails on inner face (cable routing)
    - Stiffening ribs every 100 mm along length
    - Bulkhead ring features at each end (for module mating)
    - 8× M4 tapped holes around each bulkhead (module attachment)
    - Diagonal brace channels (torque tube concept)
    - Access panels (cutout recesses with fastener holes)
    """
    params = params or {}
    L     = params.get("section_length", 500.0)
    W     = params.get("width",         150.0)
    H     = params.get("height",         60.0)
    wall  = params.get("wall_thickness",  3.0)

    with BuildPart() as p:
        # Outer shell (hollow box)
        with BuildPart() as outer:
            Box(L, W, H)
        p.part = outer.part

        # Inner cavity (hollow)
        with BuildPart(mode=Mode.PRIVATE) as inner:
            Box(L + 2, W - wall * 2, H - wall * 2)
            translate(0, 0, wall)
        p.part = p.part.cut(inner.part)

        # 4× longitudinal T-slot inner rails (cable routing)
        for x in [-W/2 + wall + 5, W/2 - wall - 5]:
            for z in [wall + 5, H - wall - 5]:
                with BuildPart(mode=Mode.PRIVATE) as tsl:
                    Box(L - 10, 4, 5)
                    translate(0, x, z)
                p.part = p.part.cut(tsl.part)

        # Bulkhead ring at each end
        for z_end in [0, L]:
            with BuildSketch(Plane(origin=(0, 0, z_end), axis=(0, 0, 1))) as br:
                with Locations((0, 0)):
                    Circle(W / 2 - wall, mode=Mode.SUBTRACT)
                    Circle(W / 4, mode=Mode.ADD)
                pass
            extrude(amount=wall * 2, both=True, mode=Mode.PRIVATE)

            # 8× M4 bulkhead attachment holes
            bolt_r = 2.2  # M4 clearance
            for ang in range(0, 360, 45):
                rad = math.radians(ang)
                bx = (W / 2 - wall - 8) * math.cos(rad)
                by = (W / 2 - wall - 8) * math.sin(rad)
                with BuildPart(mode=Mode.PRIVATE) as bh:
                    Cylinder(bolt_r, wall * 2 + 2, mode=Mode.SUBTRACT)
                    translate(bx, by, z_end)
                p.part = p.part.cut(bh.part)
                # Countersink
                with BuildPart(mode=Mode.PRIVATE) as cs:
                    Cylinder(4.5, 1.5, mode=Mode.SUBTRACT)
                    translate(bx, by, z_end)
                p.part = p.part.cut(cs.part)

        # Stiffening ribs every 100 mm
        rib_t = wall
        for z in range(100, int(L - 99), 100):
            with BuildPart(mode=Mode.PRIVATE) as rib:
                Box(rib_t, W - 2 * wall, H - 2 * wall)
                translate(z, 0, wall)
            p.part = p.part.cut(rib.part)

        # Diagonal brace channels (torque tube concept, two diagonal cuts)
        for z in [L * 0.25, L * 0.75]:
            for sign in [-1, 1]:
                with BuildPart(mode=Mode.PRIVATE) as db:
                    Box(3, (W - 2 * wall) * 0.7, (H - 2 * wall) * 0.7)
                    rotate(0, 45 * sign, 0)
                    translate(z, 0, wall + (H - 2 * wall) / 2)
                p.part = p.part.cut(db.part)

        # Access panel cutouts (top face)
        for z in range(100, int(L - 99), 200):
            with BuildPart(mode=Mode.PRIVATE) as ap:
                Box(80, wall + 1, 3, mode=Mode.SUBTRACT)
                translate(z, 0, H - wall)
            p.part = p.part.cut(ap.part)
            # Panel fastener holes (M2.5 × 4 per panel)
            for px in [z - 30, z + 30]:
                for py in [-W/4 + wall, W/4 - wall]:
                    with BuildPart(mode=Mode.PRIVATE) as fh:
                        Cylinder(1.35, wall + 4, mode=Mode.SUBTRACT)
                        translate(px, py, H - wall)
                    p.part = p.part.cut(fh.part)

        # All inner edges chamfered 0.5 mm
        chamfer(p.edges().filter_by_position(Axis.Z, wall, wall)[:8], chamfer_size=0.5)
        # Outer edges chamfered
        chamfer(p.edges().filter_by_position(Axis.Z, 0, 0)[:4], chamfer_size=0.8)
        chamfer(p.edges().filter_by_position(Axis.Z, H, H)[:4], chamfer_size=0.8)

    return p.part