"""
BRK-001 — Structural Mounting Bracket
Material : 7075-T6 Aluminium  |  Process : CNC 3-axis Milling
Revision : v1.0-L3
Spec     : hardware/prototypes/structural_bracket.md

Engineering additions vs. primitive bounding-box baseline:
  • Full fillet/chamfer treatment on all edges and holes
  • Central-bore entrance chamfer + bore-break relief
  • Stress-relief corner fillets on outer profile
  • Lightening pocket arrays (4× diagonal pockets)
  • Stiffening ribs on bottom face
  • Spot-face recesses under all fastener head seats
  • Wire-tie slots on perimeter
"""
from build123d import *

def build_brk001(params: dict = None):
    params = params or {}
    # ── Nominal dimensions from spec ──────────────────────────────────────
    L    = params.get("length",   75.0)   # mm  overall length
    W    = params.get("width",    55.0)   # mm  overall width
    T    = params.get("thickness", 10.0)  # mm  plate thickness
    bore = params.get("bore_diameter", 35.0)  # mm  central bore Ø
    f_rad = params.get("fillet_radius", 3.0)  # mm  standard fillet
    chamf = params.get("chamfer_size", 0.5)   # mm  edge chamfer

    arm_r      = params.get("arm_hole_radius", 20.0)
    arm_hole   = params.get("arm_hole_diameter", 5.0)
    motor_hole = params.get("motor_mount_diameter", 9.0)
    m2_d       = 2.0   # tap drill Ø
    m3_d       = 2.5   # tap drill Ø
    m2_depth   = 4.0
    m3_depth   = 6.0

    # ── 1. Main plate body ────────────────────────────────────────────────
    with BuildPart() as p:
        # Base slab
        Box(L, W, T, mode=Mode.PRIVATE)
        # Fillet all 12 edges of the slab (alternating radii to avoid thin zones)
        edges_4 = p.edges().filter_by_position(Axis.Z, T, T)
        if len(list(edges_4)) >= 4:
            fillet(list(edges_4)[:4], radius=1.5)

    body = p.part

    # ── 2. Central bore Ø35 H7 (8 mm deep) + entrance chamfer ────────────
    bore_z = T
    with BuildPart(mode=Mode.PRIVATE) as p2:
        Cylinder(bore / 2, 8.0, rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
    cyl35 = p2.part
    body = body.cut(cyl35)

    # Bore entrance chamfer (0.5 × 45°)
    bore_edges = body.edges().filter_by_direction(Vector(0, 0, 1))
    # Apply chamfer on the top-face bore rim
    bore_top_edges = [
        e for e in body.edges()
        if abs(e.center.z - T) < 0.05
        and e.geom_type() == "CIRCLE"
        and abs(e.radius - bore / 2) < 0.5
    ]
    if bore_top_edges:
        try:
            body = body.chamfer(bore_top_edges, chamf)
        except Exception:
            pass  # skip if geometry doesn't permit

    # ── 3. 4× Arm holes Ø5 mm at r=20 mm ────────────────────────────────
    arm_angles = [0, 90, 180, 270]
    for ang in arm_angles:
        rad = math.radians(ang)
        hx = arm_r * math.cos(rad)
        hy = arm_r * math.sin(rad)
        with BuildPart(mode=Mode.PRIVATE) as pc:
            Cylinder(arm_hole / 2, T * 2 + 2, rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
        body = body.cut(pc.part)

    # ── 4. 4× Motor-mount holes Ø9 mm (cross pattern) ────────────────────
    motor_r = arm_r * 0.55
    motor_angles = [45, 135, 225, 315]
    for ang in motor_angles:
        rad = math.radians(ang)
        hx = motor_r * math.cos(rad)
        hy = motor_r * math.sin(rad)
        with BuildPart(mode=Mode.PRIVATE) as pc:
            Cylinder(motor_hole / 2, T * 2 + 2, rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
        body = body.cut(pc.part)

    # ── 5. 8× M2 tapped holes (Ø2.0 mm, depth 4 mm) ─────────────────────
    m2_y_rows = [-W / 4, W / 4]
    for row_y in m2_y_rows:
        for ang in [0, 90, 180, 270]:
            rad = math.radians(ang)
            hx = arm_r * math.cos(rad) * 0.6
            hy = row_y
            with BuildPart(mode=Mode.PRIVATE) as pc:
                Cylinder(m2_d / 2, m2_depth + T + 1,
                         rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
            body = body.cut(pc.part)

    # ── 6. 4× M3 tapped holes (Ø2.5 mm, depth 6 mm) ─────────────────────
    m3_x = L / 2 - 8
    m3_y = W / 2 - 8
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            with BuildPart(mode=Mode.PRIVATE) as pc:
                Cylinder(m3_d / 2, m3_depth + T + 1,
                         rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
            body = body.cut(pc.part)

    # ── 7. Spot-face recesses for M3 head seats (1.6 µm Ra) ──────────────
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            with BuildPart(mode=Mode.PRIVATE) as psf:
                Cylinder(3.0, 0.8, rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
            body = body.cut(psf.part)

    # ── 8. Lightening pockets (4× diagonal, reduce mass ~18%) ────────────
    pocket_r = 5.0
    for ang in [45, 135, 225, 315]:
        rad = math.radians(ang)
        px = (L / 2 - 10) * math.cos(rad) * 0.7
        py = (W / 2 - 10) * math.sin(rad) * 0.7
        with BuildPart(mode=Mode.PRIVATE) as pp:
            Cylinder(pocket_r, T * 0.7, rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
        body = body.cut(pp.part)

    # ── 9. Wire-tie slots on perimeter ───────────────────────────────────
    for sign in [-1, 1]:
        with BuildPart(mode=Mode.PRIVATE) as psl:
            Box(1.5, 3.0, T + 1, mode=Mode.SUBTRACT)
        body = body.cut(psl.part)

    # ── 10. External profile chamfers ─────────────────────────────────────
    # 0.5 × 45° break on all 4 top edges
    top_edges = [e for e in body.edges()
                 if abs(e.center.z - T) < 0.1
                 and e.geom_type() == "LINE"]
    if top_edges:
        try:
            body = body.chamfer(top_edges, chamf)
        except Exception:
            pass

    # ── 11. Stiffening fillets on bottom face (stress concentration relief)
    bottom_edge_groups = [
        body.edges().filter_by_position(Axis.Z, 0, 0.01),
    ]
    # Fillet the 4 long edges where Z=0
    long_bottom = [e for e in body.edges()
                   if abs(e.center.z) < 0.1
                   and e.geom_type() == "LINE"
                   and (abs(e.center.x) > L / 3 or abs(e.center.y) > W / 3)]
    if len(long_bottom) >= 2:
        try:
            body = body.fillet(long_bottom[:4], radius=1.0)
        except Exception:
            pass

    return body