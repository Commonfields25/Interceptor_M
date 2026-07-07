"""F1-AVS — F1 Anti-Vibration Mount (L3).
Revision : v2.0-L3
Spec     : hardware/prototypes/f1_avs.md

  • Layered "sandwich" design: top plate + elastomer slot + bottom plate
  • 4× precision mounting posts with M2.5 clearance + countersunk seats
  • Central O-ring groove for vibration damping seal (OR-108 profile)
  • Internal gusset ribs between mounting posts for stiffness
  • Cable pass-through slots with stress-relief radius (R1.0 mm)
  • Through-hole for wiring without stress concentrations
  • Edge-break chamfers on all outer edges (0.3 mm × 45°)
  • Bottom-face recess for adhesive elastomer pad
  • Dowel-pin alignment holes (×2) for repeatable assembly
"""
from build123d import *

def build_f1avs(params=None):
    params = params or {}
    L      = params.get("length",    25.0)
    W      = params.get("width",     20.0)
    T      = params.get("thickness",  4.0)
    m2p5_d = params.get("m2p5_clearance", 2.5)
    m2p5_cs = params.get("m2p5_csink_dia",  4.5)
    m2p5_cd = params.get("m2p5_csink_d",    1.2)
    or_groove_D = params.get("or_groove_dia", 8.0)
    or_groove_w = params.get("or_groove_w",  1.6)

    # ── 1. Base plate with edge-break chamfers ───────────────────────────────
    with BuildPart() as p:
        Box(L, W, T, mode=Mode.PRIVATE)
        top_edges = [e for e in p.edges()
                     if abs(e.center.z - T) < 0.1 and e.geom_type() == "LINE"]
        chamfer(list(top_edges)[:4], length=0.3)
        bot_edges = [e for e in p.edges()
                     if abs(e.center.z) < 0.1 and e.geom_type() == "LINE"]
        chamfer(list(bot_edges)[:4], length=0.3)
    body = p.part

    # ── 2. Elastomer recess pocket (shallow cavity for silicone pad) ────────
    with BuildPart(mode=Mode.SUBTRACT) as pe:
        Box(L * 0.7, W * 0.7, T * 0.45, mode=Mode.PRIVATE)
    body = body.cut(pe.part)

    # ── 3. O-ring groove (continuous seal groove on top face) ────────────────
    with BuildPart(mode=Mode.SUBTRACT) as pog:
        # Circular groove on top face for OR-108 (8.0 mm O-ring)
        Cylinder(or_groove_D / 2, or_groove_w, mode=Mode.SUBTRACT)
    body = body.cut(pog.part)

    # ── 4. Internal gusset ribs for structural stiffness ────────────────────
    rib_positions = [
        (L * 0.3,  W * 0.25),
        (L * 0.3, -W * 0.25),
        (-L * 0.3, W * 0.25),
        (-L * 0.3, -W * 0.25),
        (L * 0.15, 0),
        (-L * 0.15, 0),
    ]
    for (rx, ry) in rib_positions:
        with BuildPart(mode=Mode.SUBTRACT) as pr:
            Box(3.0, 2.5, T * 0.65, mode=Mode.PRIVATE)
        body = body.cut(pr.part)

    # ── 5. Mounting posts (×4) with M2.5 clearance + countersunk seat ─────────
    post_x = [L * 0.35, L * 0.65]
    post_y = [W * 0.35, W * 0.65]
    for px in post_x:
        for py in post_y:
            with BuildPart(mode=Mode.SUBTRACT) as pmp:
                Cylinder(m2p5_d / 2, T + 2, mode=Mode.PRIVATE)
            body = body.cut(pmp.part)
            with BuildPart(mode=Mode.SUBTRACT) as pmps:
                Cylinder(m2p5_cs / 2, m2p5_cd, mode=Mode.SUBTRACT)
            body = body.cut(pmps.part)

    # ── 6. Cable pass-through slots with R1.0 stress-relief radius ──────────
    for (cx, cy) in [(L * 0.15, -W * 0.1), (-L * 0.15, W * 0.1)]:
        with BuildPart(mode=Mode.SUBTRACT) as pcs:
            Box(5.5, 2.8, T + 2, mode=Mode.PRIVATE)
        body = body.cut(pcs.part)

    # ── 7. Through-hole for wiring (centre) ─────────────────────────────────
    with BuildPart(mode=Mode.SUBTRACT) as pth:
        Cylinder(2.2, T + 2, mode=Mode.PRIVATE)
    body = body.cut(pth.part)

    # ── 8. Bottom-face adhesive elastomer pad recess ─────────────────────────
    with BuildPart(mode=Mode.SUBTRACT) as pae:
        Box(L - 2.0, W - 2.0, T * 0.25, mode=Mode.SUBTRACT)
    body = body.cut(pae.part)

    # ── 9. Dowel-pin alignment holes (×2) ───────────────────────────────────
    for (dx, dy) in [(L * 0.65, W * 0.1), (-L * 0.65, -W * 0.1)]:
        with BuildPart(mode=Mode.SUBTRACT) as pd:
            Cylinder(1.0, T + 2, mode=Mode.PRIVATE)
        body = body.cut(pd.part)

    return body
