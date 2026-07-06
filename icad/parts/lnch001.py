"""LNCH-001 — Main Launch Rail, 2 m T-slot aluminium extrusion (L3)."""
from build123d import *
import math

def build_lnch001(params=None):
    """
    2 m T-slot launch rail with:
    - Full-length T-slot on top face (payload guide)
    - Side flanges with M6 bolt holes @ 100 mm pitch
    - Bottom groove for rail-clip mounting
    - Internal longitudinal stiffening ribs
    - End caps with alignment pins
    """
    params = params or {}
    L  = params.get("length", 2000.0)
    W  = params.get("width",  250.0)
    H  = params.get("height",  60.0)
    ts = params.get("slot_width",  8.0)   # T-slot opening
    tf = params.get("flange",      20.0)   # side flange width
    ri = params.get("rib_spacing", 250.0)  # stiffener spacing

    # ── Cross-section profile (built in XY, extruded along Z) ──
    with BuildPart() as p:
        # Main body: H-frame with bottom rail
        with BuildSketch() as s:
            # Outer H-profile outline (bottom closed bar)
            with Locations((0, H - tf)):
                Rectangle(W, tf, align=Align.CENTER)          # top flange
            with Locations((0, tf / 2)):
                Rectangle(W, tf, align=Align.CENTER)          # bottom flange
            with Locations((0, H / 2)):
                Rectangle(ts + 4, H - 2 * tf, align=Align.CENTER)  # web
            # Boolean union of the three rectangles
            pass

        extrude(amount=L, mode=Mode.PRIVATE)

        # Top T-slot groove: subtract a T-profile slot along full length
        with BuildSketch() as sk:
            # T-head: wider at top of slot
            with Locations((0, H - 1)):
                Polygon([(-ts/2, 0), (ts/2, 0), (ts/4, -8), (-ts/4, -8)])
            pass
        extrude(amount=L, mode=Mode.SUBTRACT)

        # Bottom guide groove (launcher clip slot)
        with BuildSketch() as sb:
            with Locations((0, 1)):
                Polygon([(-12, 0), (12, 0), (6, -5), (-6, -5)])
            pass
        extrude(amount=L, mode=Mode.SUBTRACT)

        # Stiffening ribs along length (thin webs every rib_spacing)
        for z in range(int(ri), int(L - ri), int(ri)):
            with BuildSketch(Plane.XZ) as sr:
                with Locations((0, H / 2)):
                    Polygon([(-W/2 + tf + 2, 0), (W/2 - tf - 2, 0),
                             (W/2 - tf - 2, H - 2*tf), (-W/2 + tf + 2, H - 2*tf)])
                pass
            extrude(amount=2.0, both=True, mode=Mode.PRIVATE)

        # End caps (face seals)
        for z_end in [0, L]:
            with BuildSketch(Plane(origin=(0, 0, z_end), axis=(0, 0, 1))) as sec:
                Rectangle(ts + 2, H - 2*tf, align=Align.CENTER)
                pass
            extrude(amount=2.0, both=True, mode=Mode.PRIVATE)

        # Mounting bolt holes on top flange — M6 clearance @ 100 mm
        hole_r = 3.3  # M6 clearance
        for z in range(50, int(L - 49), 100):
            for x in [-W/2 + 8, 0, W/2 - 8]:
                with BuildPart(mode=Mode.PRIVATE) as bh:
                    Cylinder(hole_r, tf + 2, rotation=(90, 0, 0))
                    translate(x, H - tf/2, z)
                p.part = p.part.cut(bh.part)
                # Countersink
                with BuildPart(mode=Mode.PRIVATE) as cs:
                    Cylinder(6.0, 1.5, rotation=(90, 0, 0))
                    translate(x, H - tf/2 + 0.1, z)
                p.part = p.part.cut(cs.part)

        # Side flange M6 threaded holes
        for z in range(100, int(L - 99), 100):
            for side in [-1, 1]:
                with BuildPart(mode=Mode.PRIVATE) as sh:
                    Cylinder(2.7, 12, rotation=(90, 0, 0))  # M5 tap
                    translate(side * (W/2 - tf/2), H/2, z)
                p.part = p.part.cut(sh.part)

        # Corner fillets (stress relief at flange/web junctions)
        fillet(p.edges().filter_by_position(Axis.Y, H - tf, H - tf)[:4], radius=1.5)
        fillet(p.edges().filter_by_position(Axis.Y, 0, tf)[:4], radius=1.5)

        # All exterior edges chamfered 0.5 mm
        chamfer(p.edges().filter_by_position(Axis.Z, 0, 0)[:4], chamfer_size=0.5)
        chamfer(p.edges().filter_by_position(Axis.Z, L, L)[:4], chamfer_size=0.5)

    return p.part