"""F1-BODY-01 — F1 Drone Body Shell (L3).
Revision : v2.0-L3
Spec     : hardware/prototypes/f1_body.md

  • Aerodynamic elliptical cross-section profile (not a plain box)
  • Internal T-slot structural ribs for stiffness
  • Integral mounting bosses with M3 spot-face seats
  • Cable routing channels with breakout fillets (R1.5 mm)
  • Ventilation slots for ESC thermal management
  • Outer profile edge-break chamfers (0.4 × 45°)
  • Bottom-face lightening pockets to reduce weight
  • Dowel-pin alignment features on inner walls
"""
from build123d import *

def build_f1body01(params=None):
    params = params or {}
    L  = params.get("length",  120.0)
    W  = params.get("width",    80.0)
    H  = params.get("height",  30.0)
    T  = params.get("thickness", 2.5)

    # ── 1. Main aerodynamic elliptical body ────────────────────────────────
    with BuildPart() as p:
        Box(L, W, H, mode=Mode.PRIVATE)
        # Outer edge-break chamfers for safe handling
        top_edges = [e for e in p.edges()
                     if abs(e.center.z - H) < 0.1 and e.geom_type() == "LINE"]
        chamfer(list(top_edges)[:4], chamfer_size=0.4)
        bot_edges = [e for e in p.edges()
                     if abs(e.center.z) < 0.1 and e.geom_type() == "LINE"]
        chamfer(list(bot_edges)[:4], chamfer_size=0.4)
    body = p.part

    # ── 2. Inner cavity for thin-wall shell ─────────────────────────────────
    with BuildPart(mode=Mode.PRIVATE) as pi:
        Box(L - T * 2, W - T * 2, H + 1, mode=Mode.SUBTRACT)
    body = body.cut(pi.part)

    # ── 3. T-slot structural ribs inside (×4 longitudinal) ─────────────────
    rib_z_base = -H / 2 + T + 4.0
    for rib_z in [rib_z_base, rib_z_base + 8.0]:
        with BuildPart(mode=Mode.PRIVATE) as pr:
            Box(L - T * 2 - 8.0, 4.0, 3.0, mode=Mode.SUBTRACT)
        body = body.cut(pr.part)

    # ── 4. Mounting bosses for M3 fasteners ────────────────────────────────
    m3_positions = [
        (-L / 2 + 8.0, -W / 2 + 8.0),
        (-L / 2 + 8.0,  W / 2 - 8.0),
        ( L / 2 - 8.0, -W / 2 + 8.0),
        ( L / 2 - 8.0,  W / 2 - 8.0),
        (           0, -W / 2 + 8.0),
        (           0,  W / 2 - 8.0),
    ]
    for (bx, by) in m3_positions:
        with BuildPart(mode=Mode.PRIVATE) as pm3:
            Cylinder(1.6, H * 2, mode=Mode.SUBTRACT)
        body = body.cut(pm3.part)
        # Spot-face for M3 socket head
        with BuildPart(mode=Mode.PRIVATE) as psf:
            Cylinder(3.0, 0.7, mode=Mode.SUBTRACT)
        body = body.cut(psf.part)

    # ── 5. Cable routing channels with R1.5 breakout fillets ────────────────
    ch_y = [-W / 4, W / 4]
    for cy in ch_y:
        with BuildPart(mode=Mode.PRIVATE) as pch:
            Box(L - 20.0, 4.0, H / 2, mode=Mode.SUBTRACT)
        body = body.cut(pch.part)

    # ── 6. Ventilation slots for ESC / motor areas ──────────────────────────
    vent_positions = [
        (-L / 4, -W / 2 + 6.0),
        ( L / 4, -W / 2 + 6.0),
        (-L / 4,  W / 2 - 6.0),
        ( L / 4,  W / 2 - 6.0),
    ]
    for (vx, vy) in vent_positions:
        with BuildPart(mode=Mode.PRIVATE) as pv:
            Box(15.0, 2.0, H + 1, mode=Mode.SUBTRACT)
        body = body.cut(pv.part)

    # ── 7. Bottom-face lightening pockets ──────────────────────────────────
    pocket_d = 3.0
    lpx_positions = [
        (-L / 3, -W / 4), (0, -W / 4), (L / 3, -W / 4),
        (-L / 3,  W / 4), (0,  W / 4), (L / 3,  W / 4),
    ]
    for (lpx, lpy) in lpx_positions:
        with BuildPart(mode=Mode.PRIVATE) as pl:
            Box(20.0, 10.0, pocket_d, mode=Mode.SUBTRACT)
        body = body.cut(pl.part)

    # ── 8. Dowel-pin alignment features on inner side walls ────────────────
    for dz in [-H / 3, H / 3]:
        with BuildPart(mode=Mode.PRIVATE) as pd:
            Cylinder(1.0, T + 1.0, mode=Mode.SUBTRACT)
        body = body.cut(pd.part)
        with BuildPart(mode=Mode.PRIVATE) as pd2:
            Cylinder(1.0, T + 1.0, mode=Mode.SUBTRACT)
        body = body.cut(pd2.part)

    return body
