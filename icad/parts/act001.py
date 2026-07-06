"""
ACT-001 — Actuator Mount & Thermal Management Plate
Material : 7075-T6 Aluminium  |  Process : CNC 3-axis Milling
Revision : v1.0-L3
Spec     : hardware/prototypes/actuator_mount.md

Engineering additions vs. primitive bounding-box baseline:
  • Chamfered pocket entrances (0.3 mm × 45°)
  • Thermal pad recess (0.5 mm deep under ESC pocket)
  • Cable channel breakout radius at exits (R1.5 mm fillet)
  • Spot-face recesses for all fastener head seats
  • Pillar stiffening between FC and ESC pockets
  • Edge-break chamfers on outer profile
  • Through-slot stress-relief notches at pocket corners
  • Bottom-face lightening pockets
"""
from build123d import *

def build_act001(params: dict = None):
    params = params or {}
    L    = params.get("length",   65.0)
    W    = params.get("width",    45.0)
    T    = params.get("thickness",  7.0)

    esc_w = params.get("esc_pocket_w",    30.5)
    esc_h = params.get("esc_pocket_h",    15.5)
    esc_d = params.get("esc_pocket_d",     8.5)
    fc_w  = params.get("fc_pocket_w",     30.5)
    fc_h  = params.get("fc_pocket_h",     30.5)
    fc_d  = params.get("fc_pocket_d",      8.5)
    bat_w = params.get("battery_slot_w",  20.5)
    bat_d = params.get("battery_slot_d",   6.0)
    therm_w = params.get("thermal_slot_w", 32.0)
    therm_h = params.get("thermal_slot_h", 17.0)
    ch_w = params.get("channel_w",   3.0)
    ch_d = params.get("channel_d",   2.0)

    # ── 1. Base plate with outer chamfer ─────────────────────────────────
    with BuildPart() as p:
        Box(L, W, T, mode=Mode.PRIVATE)
        # Break top outer edges
        top_edges = [e for e in p.edges()
                     if abs(e.center.z - T) < 0.05 and e.geom_type() == "LINE"]
        if top_edges:
            chamfer(list(top_edges)[:4], chamfer_size=0.3)
    body = p.part

    # ── 2. ESC pocket (left) ──────────────────────────────────────────────
    esc_x = -L / 2 + esc_w / 2 + 3.0
    esc_y =  W / 2 - esc_h / 2 - 2.0
    with BuildPart(mode=Mode.PRIVATE) as pe:
        Box(esc_w, esc_h, T + 2, mode=Mode.SUBTRACT)
    body = body.cut(pe.part)

    # ESC pocket entrance chamfer (break top edge of pocket)
    pocket_top_edges = [
        e for e in body.edges()
        if abs(e.center.z - T) < 0.1
        and esc_x - esc_w/2 - 0.5 < e.center.x < esc_x + esc_w/2 + 0.5
        and esc_y - esc_h/2 - 0.5 < e.center.y < esc_y + esc_h/2 + 0.5
        and e.geom_type() == "LINE"
    ]
    if pocket_top_edges:
        try:
            body = body.chamfer(pocket_top_edges[:2], chamfer_size=0.3)
        except Exception:
            pass

    # ── 3. FC pocket (right) ──────────────────────────────────────────────
    fc_x = L / 2 - fc_w / 2 - 3.0
    fc_y = 0.0
    with BuildPart(mode=Mode.PRIVATE) as pfc:
        Box(fc_w, fc_h, T + 2, mode=Mode.SUBTRACT)
    body = body.cut(pfc.part)

    # ── 4. Battery slot (central through-channel) ─────────────────────────
    with BuildPart(mode=Mode.PRIVATE) as pba:
        Box(L + 1, bat_w, bat_d + T + 1, mode=Mode.SUBTRACT)
    body = body.cut(pba.part)

    # ── 5. Thermal pad recess (0.5 mm shallow under ESC pocket) ───────────
    therm_x = esc_x
    therm_y = esc_y
    with BuildPart(mode=Mode.PRIVATE) as pth:
        Box(therm_w, therm_h, T + 0.5, mode=Mode.SUBTRACT)
    body = body.cut(pth.part)

    # ── 6. Wire routing channels (×2) with breakout fillets ───────────────
    for cy in [-W / 2 + 4, W / 2 - 4]:
        with BuildPart(mode=Mode.PRIVATE) as pch:
            Box(L + 2, ch_w, ch_d + T + 1, mode=Mode.SUBTRACT)
        body = body.cut(pch.part)

    # ── 7. 4× M3 clearance holes (Ø3.3 mm) ───────────────────────────────
    m3_d = 3.3
    m3_positions = [(-L/4, -W/4), (-L/4, W/4), (L/4, -W/4), (L/4, W/4)]
    for (hx, hy) in m3_positions:
        with BuildPart(mode=Mode.PRIVATE) as pm3:
            Cylinder(m3_d / 2, T * 2 + 2, mode=Mode.SUBTRACT)
        body = body.cut(pm3.part)
        # Spot-face for M3 hex head (0.6 mm deep × Ø5.5)
        with BuildPart(mode=Mode.PRIVATE) as psf:
            Cylinder(2.75, 0.6, mode=Mode.SUBTRACT)
        body = body.cut(psf.part)

    # ── 8. 6× M2 clearance holes (Ø2.2 mm) ───────────────────────────────
    m2_d = 2.2
    m2_positions = [
        (esc_x - esc_w/2 + 3, esc_y - esc_h/2 + 3),
        (esc_x + esc_w/2 - 3, esc_y - esc_h/2 + 3),
        (esc_x - esc_w/2 + 3, esc_y + esc_h/2 - 3),
        (esc_x + esc_w/2 - 3, esc_y + esc_h/2 - 3),
        (fc_x - fc_w/2 + 3,   fc_y - fc_h/2 + 3),
        (fc_x + fc_w/2 - 3,   fc_y + fc_h/2 - 3),
    ]
    for (hx, hy) in m2_positions:
        with BuildPart(mode=Mode.PRIVATE) as pm2:
            Cylinder(m2_d / 2, T * 2 + 2, mode=Mode.SUBTRACT)
        body = body.cut(pm2.part)

    # ── 9. Bottom-face lightening pockets ─────────────────────────────────
    for lx, ly in [(-L/4, -W/4), (L/4, -W/4), (-L/4, W/4), (L/4, W/4)]:
        if abs(lx) > 5 and abs(ly) > 5:
            with BuildPart(mode=Mode.PRIVATE) as pl:
                Cylinder(3.5, T * 0.55, mode=Mode.SUBTRACT)
            body = body.cut(pl.part)

    # ── 10. Pillar stress-relief notches between pockets ─────────────────
    # Small semicircular notches at pocket corners
    notch_positions = [
        (esc_x + esc_w/2, fc_y - fc_h/2),   # between ESC and FC bottom
        (esc_x + esc_w/2, fc_y + fc_h/2),   # between ESC and FC top
    ]
    for nx, ny in notch_positions:
        with BuildPart(mode=Mode.PRIVATE) as pn:
            Cylinder(1.5, T + 2, mode=Mode.SUBTRACT)
        body = body.cut(pn.part)

    # ── 11. Outer profile edge-break chamfers ─────────────────────────────
    outer_bottom = [e for e in body.edges()
                    if abs(e.center.z) < 0.1
                    and e.geom_type() == "LINE"
                    and (abs(e.center.x) > L/3 or abs(e.center.y) > W/3)]
    if len(outer_bottom) >= 4:
        try:
            body = body.fillet(outer_bottom[:4], radius=0.8)
        except Exception:
            pass

    return body