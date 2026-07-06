"""
SABOT-001 — Drone Sabot (Launch Disruptor)
Material : ASA (Acrylonitrile Styrene Acrylate)  |  Process : FDM / SLS
Revision : v2.0-L3
Spec     : launcher_parts.yaml

Engineering additions vs. primitive hollow cylinder baseline:
  • Snap-lock retention fingers (3× equally spaced)
  • Centering ring groove on bore ID
  • Lead-in chamfer on bore entrance
  • Outer surface texture grooves (print layer aid)
  • Structural gussets between fingers
"""
from build123d import *

def build_sabot001(params: dict = None):
    params = params or {}
    OD    = params.get("outer_diameter", 40.0)
    ID    = params.get("inner_diameter", 35.0)
    L     = params.get("length",         60.0)
    n_fingers = params.get("n_fingers", 3)

    outer_r = OD / 2
    inner_r = ID / 2

    # ── 1. Main body (hollow cylinder) ───────────────────────────────────
    with BuildPart() as p:
        Cylinder(outer_r, L, mode=Mode.PRIVATE)
        with BuildSketch() as sk:
            Circle(outer_r, mode=Mode.PRIVATE)
        revolve(angle=360, mode=Mode.PRIVATE)
    body = p.part

    # ── 2. Central bore ───────────────────────────────────────────────────
    with BuildPart(mode=Mode.PRIVATE) as pb:
        Cylinder(inner_r, L + 2, rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
        translate(0, 0, -1)
    body = body.cut(pb.part)

    # ── 3. Lead-in chamfer on bore entrance (0.5 × 45°) ──────────────────
    bore_edges = [e for e in body.edges()
                  if e.geom_type() == "CIRCLE"
                  and abs(e.center.z) < 0.1
                  and abs(e.radius - inner_r) < 1.0]
    if bore_edges:
        try:
            body = body.chamfer(bore_edges, chamfer_size=0.5)
        except Exception:
            pass

    # ── 4. Centering ring groove on bore ID ──────────────────────────────
    groove_z = L * 0.4
    groove_r = inner_r - 0.8
    groove_w = 1.5
    with BuildPart(mode=Mode.PRIVATE) as pg:
        Cylinder(groove_r + groove_w / 2, groove_w,
                 rotation=Rot(0, 0, 0), mode=Mode.PRIVATE)
        translate(0, 0, groove_z - groove_w / 2)
        Cylinder(groove_r - groove_w / 2, groove_w + 0.5,
                 rotation=Rot(0, 0, 0), mode=Mode.SUBTRACT)
        translate(0, 0, groove_z - groove_w / 2 - 0.25)
    body = body.cut(pg.part)

    # ── 5. Snap-lock fingers (3× equally spaced) ─────────────────────────
    finger_w = 6.0   # mm
    finger_depth = 2.0   # mm
    for i in range(n_fingers):
        ang = 2 * math.pi * i / n_fingers
        cx = (outer_r - finger_depth / 2) * math.cos(ang)
        cy = (outer_r - finger_depth / 2) * math.sin(ang)
        with BuildPart(mode=Mode.PRIVATE) as pf:
            Box(finger_w, finger_depth, L * 0.6, mode=Mode.SUBTRACT)
            translate(cx, cy, L * 0.2)
            rotate(0, 0, math.degrees(ang))
        body = body.cut(pf.part)

    # ── 6. Outer surface texture grooves (print aid, 1 mm pitch) ─────────
    groove_pitch = 1.0
    n_grooves = int(L / groove_pitch)
    for i in range(1, n_grooves, 2):
        z = i * groove_pitch
        with BuildPart(mode=Mode.PRIVATE) as ptg:
            Torus(groove_pitch / 4, 0.15,
                  rotation=Rot(90, 0, 0), mode=Mode.SUBTRACT)
            translate(0, 0, z)
        try:
            body = body.cut(ptg.part)
        except Exception:
            pass

    # ── 7. Structural gussets between snap fingers ────────────────────────
    for i in range(n_fingers):
        ang1 = 2 * math.pi * i / n_fingers
        ang2 = 2 * math.pi * ((i + 1) % n_fingers) / n_fingers
        # Small gusset fill at base of sabot
        mid_ang = (ang1 + ang2) / 2
        gx = (outer_r - 1.0) * math.cos(mid_ang)
        gy = (outer_r - 1.0) * math.sin(mid_ang)
        with BuildPart(mode=Mode.PRIVATE) as pguss:
            Box(2.0, 2.0, L * 0.15, mode=Mode.SUBTRACT)
            translate(gx, gy, 0)
        try:
            body = body.cut(pguss.part)
        except Exception:
            pass

    return body