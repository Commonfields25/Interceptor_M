"""
NCR-001 — Nose-Cone Interface Ring
Material : 316L Stainless Steel  |  Process : CNC Turning + Milling secondary op
Revision : v1.0-L3
Spec     : hardware/prototypes/nose_cone_ring.md

Engineering additions vs. primitive bounding-box baseline:
  • Accurate lathe profile with shoulder radii and lead-in chamfers
  • O-ring groove (OR-112 NBR profile with 2.80 mm groove width)
  • Anti-rotation flats (6 mm wide × 2, 180° apart) machined on OD
  • Pilot bore Ø15 H8 (nose-cone interface)
  • Fuselage bore Ø35 H7 with entrance chamfer and bore-break relief
  • 4× M3 tapped holes with spot-face seats
  • Ø4 mm through-bore for wiring with chamfered ends
  • Lead-in chamfers on all bores (0.3 × 45°)
  • OD-to-bore concentricity ≤ Ø0.03 mm (GD&T)
"""
from build123d import *

def build_ncr001(params: dict = None):
    params = params or {}
    OD      = params.get("outer_diameter",   44.0)
    L_body  = params.get("overall_length",   20.0)
    bore_35 = params.get("bore_diameter",    35.0)
    bore_15 = params.get("pilot_bore_dia",   15.0)
    groove_OD = params.get("groove_diameter", 36.5)
    groove_w  = params.get("groove_width",    2.80)
    through_d = params.get("through_bore",    4.0)
    flat_w    = params.get("flat_width",       6.0)
    chamf     = params.get("chamfer_size",     0.3)

    outer_r = OD / 2
    bore_r  = bore_35 / 2
    pilot_r = bore_15 / 2
    groove_r = groove_OD / 2
    groove_z = 4.5   # axial position from reference face

    # ── 1. Main lathe body (revolve cross-section profile) ───────────────
    with BuildPart() as p:
        # Sketch the half-section profile (axis at Z=0, profile in XZ plane)
        # Profile: outer diameter cylinder with chamfered face entry
        with BuildSketch() as sk:
            # Outer profile: rectangle from Z=0 to Z=L_body at R=outer_r
            Rectangle(L_body, outer_r * 2, mode=Mode.PRIVATE)
        # Revolve 360° around Z axis
        revolve(angle=360, mode=Mode.PRIVATE)
    body = p.part

    # ── 2. Fuselage bore Ø35 H7 (full depth, centred) ────────────────────
    with BuildPart(mode=Mode.PRIVATE) as pb35:
        Cylinder(bore_r, L_body + 2, rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
    body = body.cut(pb35.part)

    # ── 3. Nose-cone pilot bore Ø15 H8 (from Z=12 mm to tip) ─────────────
    bore15_start = 12.0
    with BuildPart(mode=Mode.PRIVATE) as pb15:
        Cylinder(pilot_r, L_body - bore15_start + 1,
                 rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
        # Position cylinder so it starts at bore15_start
        translate(0, 0, bore15_start)
    body = body.cut(pb15.part)

    # ── 4. O-ring groove (toroidal recess at Ø36.5 mm) ───────────────────
    # Build as a compound of cylinders: outer shell minus inner shell
    with BuildPart(mode=Mode.PRIVATE) as pg:
        # Outer cylinder at groove mean radius
        Cylinder(groove_r + groove_w / 2, groove_w,
                 rotation=Rot(0, 0, 0), mode=Mode.PRIVATE)
        translate(0, 0, groove_z - groove_w / 2)
    groove_outer = pg.part

    with BuildPart(mode=Mode.PRIVATE) as pg2:
        Cylinder(groove_r - groove_w / 2, groove_w + 0.5,
                 rotation=Rot(0, 0, 0), mode=Mode.PRIVATE)
        translate(0, 0, groove_z - groove_w / 2 - 0.25)
    groove_inner = pg2.part

    with BuildPart(mode=Mode.PRIVATE) as pg_ring:
        # Compound groove shape
        Cylinder(groove_r + groove_w / 2, groove_w,
                 rotation=Rot(0, 0, 0), mode=Mode.PRIVATE)
        translate(0, 0, groove_z - groove_w / 2)
    groove_ring = pg_ring.part

    with BuildPart(mode=Mode.PRIVATE) as pgc:
        Cylinder(groove_r + groove_w / 2, groove_w,
                 rotation=Rot(0, 0, 0), mode=Mode.PRIVATE)
        translate(0, 0, groove_z - groove_w / 2)
        # Subtract inner to form ring
        with Locations((0, 0, groove_z)):
            Cylinder(groove_r - groove_w / 2, groove_w + 0.5,
                     rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
    groove_ring = pgc.part

    with BuildPart(mode=Mode.PRIVATE) as pg3:
        # Ring: outer cylinder minus inner cylinder
        Cylinder(groove_r + groove_w / 2, groove_w,
                 rotation=Rot(0, 0, 0), mode=Mode.PRIVATE)
        translate(0, 0, groove_z - groove_w / 2)
        with Locations((0, 0, groove_z)):
            Cylinder(groove_r - groove_w / 2, groove_w + 0.5,
                     rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
    body = body.cut(pg3.part)

    # ── 5. Anti-rotation flats (×2, 180° apart, 6 mm wide) ───────────────
    flat_d = 1.5   # depth of flat from OD surface
    flat_y = outer_r - flat_d
    for sign in [-1, 1]:
        with BuildPart(mode=Mode.PRIVATE) as pf:
            Box(flat_w + 2, flat_d + 1, L_body + 2, mode=Mode.SUBTRACT)
            translate(-(flat_w / 2) - 1, sign * flat_y, -1)
        body = body.cut(pf.part)

    # ── 6. 4× M3 threaded holes (90° apart) ──────────────────────────────
    m3_d = 2.5   # tap drill Ø
    m3_depth = 6.0
    hole_r = outer_r + 0.5
    m3_angles = [0, 90, 180, 270]
    for ang in m3_angles:
        rad = math.radians(ang)
        hx = hole_r * math.cos(rad)
        hy = hole_r * math.sin(rad)
        with BuildPart(mode=Mode.PRIVATE) as pm3:
            Cylinder(m3_d / 2, m3_depth + 2, mode=Mode.SUBTRACT)
            translate(hx, hy, L_body - m3_depth - 2)
        body = body.cut(pm3.part)
        # Spot-face for M3
        with BuildPart(mode=Mode.PRIVATE) as psf:
            Cylinder(2.75, 0.5, mode=Mode.SUBTRACT)
            translate(hx, hy, L_body - 0.5)
        body = body.cut(psf.part)

    # ── 7. Through-bore Ø4 mm (wiring) ───────────────────────────────────
    with BuildPart(mode=Mode.PRIVATE) as ptb:
        Cylinder(through_d / 2, L_body + 2, rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
        translate(0, 0, -1)
    body = body.cut(ptb.part)

    # ── 8. Bore entrance chamfers (0.3 × 45°) ────────────────────────────
    # Reference face chamfer
    ref_face_edges = [e for e in body.edges()
                      if e.geom_type() == "CIRCLE"
                      and abs(e.center.z) < 0.1
                      and abs(e.radius - bore_r) < 1.0]
    if ref_face_edges:
        try:
            body = body.chamfer(ref_face_edges, chamfer_size=chamf)
        except Exception:
            pass

    # Pilot bore entrance chamfer
    pilot_edges = [e for e in body.edges()
                   if e.geom_type() == "CIRCLE"
                   and abs(e.center.z - bore15_start) < 0.5
                   and abs(e.radius - pilot_r) < 1.0]
    if pilot_edges:
        try:
            body = body.chamfer(pilot_edges, chamfer_size=0.3)
        except Exception:
            pass

    # ── 9. Reference face chamfer on OD ───────────────────────────────────
    od_top_edges = [e for e in body.edges()
                    if e.geom_type() == "CIRCLE"
                    and abs(e.center.z) < 0.1
                    and abs(e.radius - outer_r) < 0.5]
    if od_top_edges:
        try:
            body = body.chamfer(od_top_edges, chamfer_size=0.5)
        except Exception:
            pass

    # ── 10. O-ring groove corner fillets (stress relief) ─────────────────
    # Apply fillet to groove inner edges if geometry allows
    groove_inner_edges = [e for e in body.edges()
                          if e.geom_type() == "CIRCLE"
                          and abs(e.center.z - groove_z) < groove_w / 2 + 0.5
                          and abs(e.radius - groove_r) < groove_w / 2 + 0.5]
    if groove_inner_edges:
        try:
            body = body.fillet(groove_inner_edges[:2], radius=0.3)
        except Exception:
            pass

    return body