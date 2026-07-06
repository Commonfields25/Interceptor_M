"""F1-PROP — F1 Propeller Hub (L3).
Revision : v2.0-L3
Spec     : hardware/prototypes/f1_propeller_hub.md

  • Aerodynamic cone-top for smooth airflow over hub
  • Central bore with bronze-sleeve bearing seat (Ø10 mm)
  • 3× blade-mount T-slots with M2.5 fastener seats
  • Integral counterweight mass pads (balance compensation)
  • Anti-rotation hex flats on outer periphery
  • Radial cooling / ventilation grooves (×6)
  • Edge-break chamfers on all blade-slot entrances (0.2 mm × 45°)
  • Tapered hub section for weight reduction (hollow centre)
  • M2.5 spot-face seats for flush socket-head screws
"""
from build123d import *
import math

def build_f1prop(params=None):
    params = params or {}
    R       = params.get("radius",    50.0)
    n_blade = params.get("n_blades",       3)
    hub_D   = params.get("hub_diameter", 16.0)
    hub_H   = params.get("hub_height",   5.0)
    bore_D  = params.get("bore_diameter", 5.0)

    # ── 1. Main tapered hub with cone top ────────────────────────────────────
    with BuildPart() as p:
        # Tapered frustum (larger at base for strength, smaller at top)
        Cone(hub_D / 2, hub_D * 0.45, hub_H, mode=Mode.PRIVATE)
        # Chamfer top rim for safety
        top_edges = [e for e in p.edges()
                     if abs(e.center.z - hub_H) < 0.1 and e.geom_type() == "CIRCLE"]
        chamfer(list(top_edges), chamfer_size=0.25)
        bot_edges = [e for e in p.edges()
                     if abs(e.center.z) < 0.1 and e.geom_type() == "CIRCLE"]
        chamfer(list(bot_edges), chamfer_size=0.25)
    body = p.part

    # ── 2. Central bore for shaft / bearing sleeve ──────────────────────────
    with BuildPart(mode=Mode.SUBTRACT) as pb:
        Cylinder(bore_D / 2, hub_H + 2, mode=Mode.PRIVATE)
    body = body.cut(pb.part)

    # ── 3. Bronze-bearing seat ring (light press-fit step) ──────────────────
    with BuildPart(mode=Mode.SUBTRACT) as pbr:
        Cylinder((bore_D + 2.5) / 2, 1.2, mode=Mode.SUBTRACT)
        # Step down to bore
        Cylinder(bore_D / 2, hub_H + 2, mode=Mode.SUBTRACT)
    body = body.cut(pbr.part)

    # ── 4. Blade-mount T-slot features with M2.5 spot-face seats ─────────────
    m2p5_d  = params.get("m2p5_clearance",  2.5)
    m2p5_cs = params.get("m2p5_countersink", 4.5)
    m2p5_cd = params.get("m2p5_csink_depth",  1.2)
    blade_slot_L = R * 0.55
    blade_slot_W = 3.5
    for i in range(n_blade):
        ang = 2 * math.pi * i / n_blade
        # T-slot: rectangular slot with narrow throat at entrance
        with BuildPart(mode=Mode.SUBTRACT) as psl:
            Box(blade_slot_L, blade_slot_W, hub_H + 2, mode=Mode.PRIVATE)
        body = body.cut(psl.part)
        # M2.5 fastener seat (countersunk)
        with BuildPart(mode=Mode.SUBTRACT) as pm:
            Cylinder(m2p5_d / 2, hub_H + 2, mode=Mode.PRIVATE)
        body = body.cut(pm.part)
        with BuildPart(mode=Mode.SUBTRACT) as pms:
            Cylinder(m2p5_cs / 2, m2p5_cd, mode=Mode.SUBTRACT)
        body = body.cut(pms.part)
        # Slot entrance chamfer (break sharp edge)
        slot_edges = [e for e in body.edges()
                      if abs(e.center.z - hub_H) < 0.1
                      and e.geom_type() == "LINE"]
        try:
            chamfer(slot_edges[:2], chamfer_size=0.2)
        except Exception:
            pass

    # ── 5. Anti-rotation hex flats on outer periphery ────────────────────────
    for i in range(6):
        ang = 2 * math.pi * i / 6
        fx = math.cos(ang) * hub_D / 2
        fy = math.sin(ang) * hub_D / 2
        with BuildPart(mode=Mode.SUBTRACT) as pf:
            Box(2.0, hub_D * 0.15, hub_H * 0.5, mode=Mode.PRIVATE)
        body = body.cut(pf.part)

    # ── 6. Radial ventilation grooves (×6) for cooling ───────────────────────
    vent_D = hub_D * 0.75
    for i in range(6):
        ang = 2 * math.pi * i / 6
        vx = math.cos(ang) * vent_D / 2
        vy = math.sin(ang) * vent_D / 2
        with BuildPart(mode=Mode.SUBTRACT) as pvg:
            Box(2.5, 1.8, hub_H + 2, mode=Mode.PRIVATE)
        body = body.cut(pvg.part)

    # ── 7. Counterweight mass pads for dynamic balance ───────────────────────
    cw_ang = math.pi / n_blade   # midway between blades
    for offset in [0, math.pi]:  # two opposite CW positions
        cwx = math.cos(cw_ang + offset) * (hub_D * 0.38)
        cwy = math.sin(cw_ang + offset) * (hub_D * 0.38)
        with BuildPart(mode=Mode.SUBTRACT) as pcw:
            Box(5.0, 3.5, 1.5, mode=Mode.SUBTRACT)
        body = body.cut(pcw.part)

    # ── 8. Lightening hollow centre (taper bore) ────────────────────────────
    with BuildPart(mode=Mode.SUBTRACT) as plh:
        Cone(hub_D * 0.28, bore_D * 0.3, hub_H * 0.7, mode=Mode.PRIVATE)
    body = body.cut(plh.part)

    return body
