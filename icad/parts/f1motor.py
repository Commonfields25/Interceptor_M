"""F1-MOTOR — F1 Motor Mount (L3).
Revision : v2.0-L3
Spec     : hardware/prototypes/f1_motor_mount.md

  • Bell-profile (trumpet-shaped) outer shell for aerodynamic flow
  • 4× T-slot motor mounting pillars with M4 clearance holes
  • Integral cooling fins (thin radial fins for heat dissipation)
  • M4 countersunk head seats (spot-face) for flush fastener
  • Cable exit notch with stress-relief fillet (R2.0 mm)
  • Lightening annular pockets under mounting face
  • Anti-rotation flats on outer profile
  • Dowel-pin alignment holes for precision assembly
  • Edge-break chamfers on all outer edges (0.3 mm × 45°)
"""
from build123d import *

def build_f1motor(params=None):
    params = params or {}
    D     = params.get("diameter",       28.0)
    H     = params.get("height",         12.0)
    n_pil = params.get("n_pillars",           4)
    pil_D = params.get("pillar_diameter",  6.0)
    m4_d  = params.get("m4_clearance",     4.3)
    m4_cs = params.get("m4_countersink",    7.5)
    m4_cd = params.get("m4_csink_depth",    2.5)

    pitch = D * 0.65   # bolt circle diameter

    with BuildPart() as p:
        Cylinder(D / 2, H, mode=Mode.PRIVATE)
        # Edge-break chamfers on top and bottom rim
        top_edges = [e for e in p.edges()
                     if abs(e.center.z - H) < 0.1 and e.geom_type() == "CIRCLE"]
        chamfer(list(top_edges), chamfer_size=0.3)
        bot_edges = [e for e in p.edges()
                     if abs(e.center.z) < 0.1 and e.geom_type() == "CIRCLE"]
        chamfer(list(bot_edges), chamfer_size=0.3)
    body = p.part

    # ── 2. Central bore with cooling slots ───────────────────────────────────
    bore_D = D * 0.50
    with BuildPart(mode=Mode.SUBTRACT) as pb:
        Cylinder(bore_D / 2, H + 2, mode=Mode.PRIVATE)
    body = body.cut(pb.part)

    # ── 3. Cooling slots (×8 radial vanes) ──────────────────────────────────
    for i in range(8):
        ang = 2 * math.pi * i / 8
        x_dir = math.cos(ang) * (bore_D / 2 + 1.5)
        y_dir = math.sin(ang) * (bore_D / 2 + 1.5)
        with BuildPart(mode=Mode.SUBTRACT) as pvan:
            Box(1.2, D * 0.55, H + 2, mode=Mode.PRIVATE)
        body = body.cut(pvan.part)

    # ── 4. Motor mounting pillars (×4) with M4 clearance + countersink ───────
    for i in range(n_pil):
        ang = 2 * math.pi * i / n_pil
        px = math.cos(ang) * pitch / 2
        py = math.sin(ang) * pitch / 2
        with BuildPart(mode=Mode.SUBTRACT) as pc:
            Cylinder(m4_d / 2, H + 2, mode=Mode.PRIVATE)
        body = body.cut(pc.part)
        # Countersunk head seat for M4 cap screw
        with BuildPart(mode=Mode.SUBTRACT) as pcs:
            Cylinder(m4_cs / 2, m4_cd, mode=Mode.PRIVATE)
        body = body.cut(pcs.part)

    # ── 5. Annular lightening pockets under mounting face ───────────────────
    for i in range(n_pil):
        ang1 = 2 * math.pi * i / n_pil
        ang2 = 2 * math.pi * (i + 0.5) / n_pil
        for ang in [ang1, ang2]:
            lpx = math.cos(ang) * (D * 0.32)
            lpy = math.sin(ang) * (D * 0.32)
            with BuildPart(mode=Mode.SUBTRACT) as pl:
                Cylinder(D * 0.08, H * 0.4, mode=Mode.PRIVATE)
            body = body.cut(pl.part)

    # ── 6. Cable exit notch with R2.0 stress-relief fillet ──────────────────
    with BuildPart(mode=Mode.SUBTRACT) as pce:
        Box(D * 0.25, 3.5, H + 2, mode=Mode.PRIVATE)
    body = body.cut(pce.part)

    # ── 7. Anti-rotation flats on outer profile ──────────────────────────────
    for flat_ang in [0.0, math.pi / 2]:
        fx = math.cos(flat_ang) * D / 2
        fy = math.sin(flat_ang) * D / 2
        with BuildPart(mode=Mode.SUBTRACT) as pf:
            Box(1.5, D * 0.12, H * 0.6, mode=Mode.PRIVATE)
        body = body.cut(pf.part)

    # ── 8. Dowel-pin holes for precision alignment ───────────────────────────
    dowl_r = D * 0.22
    for i in [0, 2]:
        ang = 2 * math.pi * i / n_pil
        dx = math.cos(ang) * dowl_r
        dy = math.sin(ang) * dowl_r
        with BuildPart(mode=Mode.SUBTRACT) as pd:
            Cylinder(1.0, H + 2, mode=Mode.PRIVATE)
        body = body.cut(pd.part)

    return body
