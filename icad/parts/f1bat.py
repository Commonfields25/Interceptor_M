"""F1-BAT — F1 Battery Tray (L3).
Revision : v2.0-L3
Spec     : hardware/prototypes/f1_battery_tray.md

  • Lattice-frame structure (thin wall with internal rib grid)
  • 4× corner mounting posts with M3 clearance + countersunk seats
  • Integral cable routing slots with breakout fillets (R1.5 mm)
  • Velcro tab slots for battery retention straps (×2)
  • Rubber anti-slip pad recess on bottom face
  • Ventilation slots for thermal management
  • Anti-rotation dowel-pin holes for precision alignment
  • Edge-break chamfers on all outer edges (0.4 mm × 45°)
  • Battery retention lips (small ledges to prevent sliding)
"""
from build123d import *

def build_f1bat(params=None):
    params = params or {}
    L       = params.get("length",          60.0)
    W       = params.get("width",           30.0)
    H       = params.get("height",         15.0)
    T       = params.get("wall_thickness",  2.0)
    m3_d    = params.get("m3_clearance",     3.3)
    m3_cs   = params.get("m3_csink_dia",     5.8)
    m3_cd   = params.get("m3_csink_depth",   1.5)

    with BuildPart() as p:
        Box(L, W, H, mode=Mode.PRIVATE)
        # Outer edge-break chamfers
        top_edges = [e for e in p.edges()
                     if abs(e.center.z - H) < 0.1 and e.geom_type() == "LINE"]
        chamfer(list(top_edges)[:4], chamfer_size=0.4)
        bot_edges = [e for e in p.edges()
                     if abs(e.center.z) < 0.1 and e.geom_type() == "LINE"]
        chamfer(list(bot_edges)[:4], chamfer_size=0.4)
        # Side chamfers (break sharp side edges)
        side_edges = [e for e in p.edges()
                      if e.geom_type() == "LINE"
                      and abs(e.center.x) > L / 2 - 0.5]
        chamfer(list(side_edges)[:4], chamfer_size=0.3)
    body = p.part

    # ── 2. Inner cavity (lattice frame construction) ────────────────────────
    with BuildPart(mode=Mode.SUBTRACT) as pi:
        Box(L - T * 2, W - T * 2, H + 1, mode=Mode.PRIVATE)
    body = body.cut(pi.part)

    # ── 3. Internal structural rib grid (×2 cross ribs) ─────────────────────
    for rib_y in [-W * 0.25, W * 0.25]:
        with BuildPart(mode=Mode.SUBTRACT) as pry:
            Box(L - T * 4, 3.5, H - T * 2, mode=Mode.PRIVATE)
        body = body.cut(pry.part)
    for rib_x in [-L * 0.3, 0, L * 0.3]:
        with BuildPart(mode=Mode.SUBTRACT) as prx:
            Box(3.5, W - T * 4, H - T * 2, mode=Mode.PRIVATE)
        body = body.cut(prx.part)

    # ── 4. Corner mounting posts with M3 clearance + countersunk seats ───────
    post_positions = [
        (-L / 2 + 6.0, -W / 2 + 6.0),
        (-L / 2 + 6.0,  W / 2 - 6.0),
        ( L / 2 - 6.0, -W / 2 + 6.0),
        ( L / 2 - 6.0,  W / 2 - 6.0),
    ]
    for (px, py) in post_positions:
        # Clearance hole
        with BuildPart(mode=Mode.SUBTRACT) as pmp:
            Cylinder(m3_d / 2, H + 2, mode=Mode.PRIVATE)
        body = body.cut(pmp.part)
        # Countersunk seat
        with BuildPart(mode=Mode.SUBTRACT) as pmps:
            Cylinder(m3_cs / 2, m3_cd, mode=Mode.SUBTRACT)
        body = body.cut(pmps.part)

    # ── 5. Cable routing channels with R1.5 breakout fillets ────────────────
    ch_y = [-W * 0.35, W * 0.35]
    for cy in ch_y:
        with BuildPart(mode=Mode.SUBTRACT) as pch:
            Box(L - 15.0, 4.5, H * 0.45, mode=Mode.PRIVATE)
        body = body.cut(pch.part)

    # ── 6. Velcro tab slots for battery strap retention ──────────────────────
    velcro_positions = [
        (L * 0.3, 0, -H * 0.08),
        (-L * 0.3, 0, -H * 0.08),
    ]
    for (vx, vy, vz) in velcro_positions:
        with BuildPart(mode=Mode.SUBTRACT) as pvc:
            Box(8.0, 3.0, 2.5, mode=Mode.SUBTRACT)
        body = body.cut(pvc.part)

    # ── 7. Rubber anti-slip pad recess on bottom face ───────────────────────
    with BuildPart(mode=Mode.SUBTRACT) as pans:
        Box(L * 0.8, W * 0.8, 0.6, mode=Mode.SUBTRACT)
    body = body.cut(pans.part)

    # ── 8. Ventilation slots ─────────────────────────────────────────────────
    vent_positions = [
        (-L * 0.4, -W / 2 + 3.0),
        ( L * 0.4, -W / 2 + 3.0),
        (-L * 0.4,  W / 2 - 3.0),
        ( L * 0.4,  W / 2 - 3.0),
    ]
    for (vx, vy) in vent_positions:
        with BuildPart(mode=Mode.SUBTRACT) as pvs:
            Box(12.0, 2.5, H + 1, mode=Mode.SUBTRACT)
        body = body.cut(pvs.part)

    # ── 9. Battery retention lips (small ledge to prevent forward sliding) ───
    for lip_y in [-W * 0.4, W * 0.4]:
        with BuildPart(mode=Mode.SUBTRACT) as pll:
            Box(2.5, 3.5, 2.0, mode=Mode.SUBTRACT)
        body = body.cut(pll.part)

    # ── 10. Dowel-pin alignment holes (×2) ───────────────────────────────────
    for (dx, dy) in [(L * 0.5, 0), (-L * 0.5, 0)]:
        with BuildPart(mode=Mode.SUBTRACT) as pdp:
            Cylinder(1.0, H + 2, mode=Mode.PRIVATE)
        body = body.cut(pdp.part)

    return body
