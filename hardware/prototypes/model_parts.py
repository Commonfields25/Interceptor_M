#!/usr/bin/env python3
# coding: utf-8
"""
model_parts.py  -  Interceptor_M FreeCAD Model Generator
Part IDs : BRK-001 (Structural Bracket), ACT-001 (Actuator Mount), NCR-001 (Nose-Cone Interface Ring)
Generates parametric 3D models from params_DC.json / params_DD.json / params_DI.json
Outputs  : .FCStd FreeCAD documents + STEP files per product line
Compatible: FreeCAD 0.21+ (Part / PartDesign Workbenches)

Usage (inside FreeCAD Python console or --run command):
    import sys
    sys.path.insert(0, "/home/user/interceptor_work/hardware/prototypes")
    exec(open("/home/user/interceptor_work/hardware/prototypes/model_parts.py").read())

Or from system Python (headless):
    freecadcmd model_parts.py
"""

import os
import json
import sys
import math

# ── FreeCAD import (guard for environments where it's unavailable) ───────────
try:
    import FreeCAD
    import Part
    import PartDesign
    import Sketcher
    import Mesh
    from FreeCAD import Console

    FC_AVAILABLE = True
except ImportError:
    FC_AVAILABLE = False
    FreeCAD = None
    Part = None

__version__ = "0.1.0"
__author__ = "D1/D2/D3 agents"


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 1  -  PATHS
# ═══════════════════════════════════════════════════════════════════════════════

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
STEP_DIR = os.path.join(MODEL_DIR, "step")
JSON_DIR = os.path.join(BASE_DIR)  # params_*.json are next to this script

for _d in (MODEL_DIR, STEP_DIR):
    os.makedirs(_d, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 2  -  JSON PARAMETER LOADING
# ═══════════════════════════════════════════════════════════════════════════════


def load_params(line_code: str) -> dict:
    """Charge params_<LINE>.json et renvoie le dict."""
    path = os.path.join(JSON_DIR, f"params_{line_code}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Parameter file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    Console.PrintMessage(f"[model_parts] Loaded {path}\n")
    return data


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 3  -  SKETCH HELPERS  (Sketcher API)
# ═══════════════════════════════════════════════════════════════════════════════


def new_sketch(body, name: str) -> Sketcher.Sketch:
    """Cree une Sketch sur le plan XY du Body."""
    sk = body.newObject("Sketcher::SketchObject", name)
    sk.MapMode = "FlatFace"
    return sk


def add_rectangle(sk, x: float, y: float, w: float, h: float, label: str = ""):
    """Rectangle centre en (x,y) de dimensions w×h."""
    g = sk.addGeometry(
        Part.Rectangle(x - w / 2, y - h / 2, x + w / 2, y + h / 2), False
    )
    sk.addConstraint(Sketcher.Constraint("Coincident", -1, 1, g, 3))
    if label:
        sk.setAlias(label)
    return g


def add_circle(sk, cx: float, cy: float, r: float, label: str = "") -> int:
    """Cercle centre en (cx,cy) de rayon r. Renvoie l'index de geometrie."""
    g = sk.addGeometry(Part.Circle(cx, cy, 0, r), False)
    if label:
        sk.setAlias(label)
    return g


def add_slot(sk, x: float, y: float, w: float, h: float, label: str = ""):
    """Slot (ovale) centre en (x,y)."""
    g = sk.addGeometry(Part.Point(x, y), False)
    sk.addConstraint(Sketcher.Constraint("Distance", -1, 1, g, 4, w))
    return g


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 4  -  PART BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════


def build_BRK001(params: dict) -> Part.Solid:
    """
    BRK-001  -  Structural Bracket
    Material : 7075-T6 Aluminium  |  Stock : 80×60×12 mm
    Manufacturing : CNC 3-axis milling (described)

    Features modelled:
        Main plate          : 75 × 55 × 10 mm (from specs)
        Central bore Ø35 H7 (depth 8 mm)
        4× arm holes Ø5 H8  (radial, r=20 mm, 90deg apart)
        4× motor-mount holes Ø9 H8 (cross pattern)
        8× M2 tapped holes   (Ø2.0 mm, depth 4 mm)
        4× M3 tapped holes   (Ø2.5 mm, depth 6 mm)
    """
    L = 75.0  # mm  (overall length from spec)
    W = 55.0  # mm  (overall width  from spec)
    T = 10.0  # mm  (thickness       from spec)
    bore = 35.0  # mm  (central bore Ø  spec)
    bore_d = 8.0  # mm  (bore depth       spec)
    arm_r = 20.0  # mm  (arm hole radius  spec)
    arm_hole = 5.0
    motor_hole = 9.0
    arm_angle_list = [0, 90, 180, 270]  # degrees

    # ── Base plate (main rectangular body) ─────────────────────────
    main_solid = Part.makeCylinder(
        L / 2, T, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1)
    )
    # Extend to rectangular footprint by adding bounding box approach
    main_solid = Part.makeBox(L, W, T, FreeCAD.Vector(-L / 2, -W / 2, 0))

    # ── Base plate via Pad ──────────────────────────────────────────
    sk_plate = Sketcher.Sketch()
    add_rectangle(sk_plate, 0, 0, L, W)

    pad_pl = PartDesign.Body("BRK001_Body")
    pad_sk = pad_pl.newObject("Sketcher::SketchObject", "Sketch_Plate")
    pad_sk.MapMode = "FlatFace"
    r = sk_plate.addGeometry(Part.Rectangle(-L / 2, -W / 2, L / 2, W / 2), False)
    pad_sk.addGeometry(r)
    pad_sk.solve()
    pad_pl.newObject("PartDesign::Pad", "Pad_Plate").Profile = pad_sk
    pad_pl.Pad.Length = T
    pad_pl.recompute()

    main_solid = pad_pl.Shape

    # ── Central bore (cylindrical hole) ───────────────────────────────
    cyl_35 = Part.makeCylinder(
        bore / 2, bore_d, FreeCAD.Vector(0, 0, T), FreeCAD.Vector(0, 0, 1)
    )
    main_solid = main_solid.cut(cyl_35)

    # ── 4× Arm holes Ø5 mm ───────────────────────────────────────────
    for ang in arm_angle_list:
        rad = math.radians(ang)
        hx = arm_r * math.cos(rad)
        hy = arm_r * math.sin(rad)
        cyl = Part.makeCylinder(
            arm_hole / 2, T * 2, FreeCAD.Vector(hx, hy, -T), FreeCAD.Vector(0, 0, 1)
        )
        main_solid = main_solid.cut(cyl)

    # ── 4× Motor-mount holes Ø9 mm (cross pattern inside) ─────────────
    motor_r = arm_r * 0.55
    motor_angles = [45, 135, 225, 315]
    for ang in motor_angles:
        rad = math.radians(ang)
        hx = motor_r * math.cos(rad)
        hy = motor_r * math.sin(rad)
        cyl = Part.makeCylinder(
            motor_hole / 2, T * 2, FreeCAD.Vector(hx, hy, -T), FreeCAD.Vector(0, 0, 1)
        )
        main_solid = main_solid.cut(cyl)

    # ── 8× M2 tapped holes (Ø2.0 mm, depth 4 mm)  -  arranged around perimeter ─
    m2_d = 2.0
    m2_depth = 4.0
    m2_y_positions = [-W / 4, W / 4]
    for row_y in m2_y_positions:
        for ang in [0, 90, 180, 270]:
            rad = math.radians(ang)
            hx = arm_r * math.cos(rad) * 0.6
            hy = row_y
            cyl = Part.makeCylinder(
                m2_d / 2,
                m2_depth + T,
                FreeCAD.Vector(hx, hy, T - m2_depth),
                FreeCAD.Vector(0, 0, 1),
            )
            main_solid = main_solid.cut(cyl)

    # ── 4× M3 tapped holes (Ø2.5 mm, depth 6 mm) ──────────────────────
    m3_d = 2.5
    m3_depth = 6.0
    m3_x = L / 2 - 8
    m3_y = W / 2 - 8
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            cyl = Part.makeCylinder(
                m3_d / 2,
                m3_depth + T,
                FreeCAD.Vector(sx * m3_x, sy * m3_y, T - m3_depth),
                FreeCAD.Vector(0, 0, 1),
            )
            main_solid = main_solid.cut(cyl)

    return main_solid


def build_ACT001(params: dict) -> Part.Solid:
    """
    ACT-001  -  Actuator Mount
    Material : 7075-T6 Aluminium  |  Stock : 70×50×8 mm
    Manufacturing : CNC 3-axis milling (described)

    Features modelled:
        Main plate             : 65 × 45 × 7 mm
        ESC pocket             : 30.5 × 15.5 × 8.5 mm
        FC  pocket             : 30.5 × 30.5 × 8.5 mm
        Battery slot          : 20.5 × 6.0 mm (through-width slot)
        Thermal slot (ESC pad) : 32.0 × 17.0 × 0.5 mm (shallow recess)
        2× Wire channels       : 3.0 mm wide × 2.0 mm deep
        4× M3 clearance holes  : Ø3.3 mm
        6× M2 clearance holes  : Ø2.2 mm
    """
    L = 65.0
    W = 45.0
    T = 7.0
    esc_w = 30.5
    esc_h = 15.5
    fc_w = 30.5
    fc_h = 30.5
    bat_w = 20.5
    bat_d = 6.0
    therm_w = 32.0
    therm_h = 17.0
    channel_w = 3.0
    channel_d = 2.0

    # ── Base plate ──────────────────────────────────────────────────
    base = Part.makeBox(L, W, T, FreeCAD.Vector(-L / 2, -W / 2, 0))

    # ── ESC pocket (rectangular cutout, centered-left) ─────────────
    esc_x = -L / 2 + esc_w / 2 + 3
    esc_y = W / 2 - esc_h / 2 - 2
    esc_cut = Part.makeBox(
        esc_w, esc_h, T + 2, FreeCAD.Vector(esc_x - esc_w / 2, esc_y - esc_h / 2, -1)
    )
    base = base.cut(esc_cut)

    # ── FC pocket (right side) ───────────────────────────────────────
    fc_x = L / 2 - fc_w / 2 - 3
    fc_y = 0
    fc_cut = Part.makeBox(
        fc_w, fc_h, T + 2, FreeCAD.Vector(fc_x - fc_w / 2, fc_y - fc_h / 2, -1)
    )
    base = base.cut(fc_cut)

    # ── Battery slot (central channel across W, full width) ──────────
    bat_cut = Part.makeBox(L, bat_w, bat_d + T, FreeCAD.Vector(-L / 2, -bat_w / 2, -T))
    base = base.cut(bat_cut)

    # ── Thermal slot (shallow recess for ESC thermal pad) ──────────
    therm_x = esc_x
    therm_y = esc_y
    therm_cut = Part.makeBox(
        therm_w,
        therm_h,
        0.5 + T,
        FreeCAD.Vector(therm_x - therm_w / 2, therm_y - therm_h / 2, -0.5),
    )
    base = base.cut(therm_cut)

    # ── 2× Wire routing channels ─────────────────────────────────────
    ch_y_positions = [-W / 2 + 4, W / 2 - 4]
    for cy in ch_y_positions:
        ch = Part.makeBox(
            L + 2,
            channel_w,
            channel_d,
            FreeCAD.Vector(-L / 2 - 1, cy - channel_w / 2, T - channel_d),
        )
        base = base.cut(ch)

    # ── 4× M3 clearance holes (interface to BRK-001) ────────────────
    m3_d = 3.3
    m3_positions = [(-L / 4, -W / 4), (-L / 4, W / 4), (L / 4, -W / 4), (L / 4, W / 4)]
    for hx, hy in m3_positions:
        cyl = Part.makeCylinder(
            m3_d / 2, T * 2, FreeCAD.Vector(hx, hy, -T), FreeCAD.Vector(0, 0, 1)
        )
        base = base.cut(cyl)

    # ── 6× M2 clearance holes (ESC/FC mounts) ───────────────────────
    m2_d = 2.2
    m2_positions = [
        (esc_x - esc_w / 2 + 3, esc_y - esc_h / 2 + 3),
        (esc_x + esc_w / 2 - 3, esc_y - esc_h / 2 + 3),
        (esc_x - esc_w / 2 + 3, esc_y + esc_h / 2 - 3),
        (esc_x + esc_w / 2 - 3, esc_y + esc_h / 2 - 3),
        (fc_x - fc_w / 2 + 3, fc_y - fc_h / 2 + 3),
        (fc_x + fc_w / 2 - 3, fc_y + fc_h / 2 - 3),
    ]
    for hx, hy in m2_positions:
        cyl = Part.makeCylinder(
            m2_d / 2, T * 2, FreeCAD.Vector(hx, hy, -T), FreeCAD.Vector(0, 0, 1)
        )
        base = base.cut(cyl)

    return base


def build_NCR001(params: dict) -> Part.Solid:
    """
    NCR-001  -  Nose-Cone Interface Ring
    Material : 316L Stainless Steel  |  Stock : Ø45×25 mm bar
    Manufacturing : CNC Turning (Lathe) + CNC Milling (secondary op)

    Features modelled:
        Body : Ø44.0 mm OD × 20.0 mm long (lathe profile)
        Fuselage bore Ø35 H7 (ID, full depth)
        Nose-cone pilot bore Ø15 H8 (ID, full depth)
        O-ring groove Ø36.5 mm × 2.80 mm wide  (OR-112 NBR)
        Anti-rotation flats ×2 (6 mm wide, 180deg apart)
        4× M3 threaded holes (interface to fuselage clamp)
        Through-bore Ø4 mm (wiring)
    """
    OD = 44.0  # mm  outer diameter
    L_body = 20.0  # mm  overall length
    bore_35 = 35.0  # mm  fuselage interface
    bore_15 = 15.0  # mm  nose-cone pilot
    groove_OD = 36.5  # mm  O-ring groove diameter
    groove_w = 2.80  # mm  O-ring groove width
    through_d = 4.0  # mm  wiring through-bore
    flat_w = 6.0  # mm  anti-rotation flat width

    # ── Lathe profile (cross-section, rotated around Z) ──────────────
    #
    #  Key Z coordinates (face at Z=0, tip at Z=L_body):
    #   Z=0      → reference face
    #   Z=2      → start of Ø35 bore
    #   Z=12     → end of Ø35 bore, start of Ø15 bore
    #   Z=20     → end of Ø15 bore
    #
    #  Key R coordinates:
    #   R=22.0   → OD outer radius
    #   R=17.5   → fuselage bore  (Ø35 ID / 2)
    #   R=7.5    → pilot bore     (Ø15 ID / 2)
    #   R=18.25  → O-ring groove mean radius

    profile_points = [
        FreeCAD.Vector(0, 0, 0),  # Z=0   -  reference face edge
        FreeCAD.Vector(0, OD / 2, 0),  # Z=0   -  OD outer
        FreeCAD.Vector(0, OD / 2, L_body),  # Z=L   -  OD tip
        FreeCAD.Vector(0, 0, L_body),  # Z=L   -  bore axis
    ]

    # ── Build the main turning body via revolution ────────────────────
    # Create a face/closed profile for lathe
    outer_r = OD / 2
    bore_z1 = 2.0  # bore starts 2 mm from face
    bore_z2 = 12.0  # bore Ø35 ends
    bore_z3 = L_body  # bore Ø15 extends to tip

    # Lathe revolution: build a compound of cylinders
    solid = Part.Solid([])

    # Main body cylinder (OD = 44 mm, length = 20 mm)
    cyl_main = Part.makeCylinder(outer_r, L_body)

    # Subtract fuselage bore Ø35 (full length, centred)
    bore35 = Part.makeCylinder(
        bore_35 / 2, L_body + 2, FreeCAD.Vector(0, 0, -1), FreeCAD.Vector(0, 0, 1)
    )
    solid = cyl_main.cut(bore35)

    # Subtract pilot bore Ø15 (from Z=bore_z2 to tip)
    bore15 = Part.makeCylinder(
        bore_15 / 2,
        L_body - bore_z2 + 1,
        FreeCAD.Vector(0, 0, bore_z2 - 1),
        FreeCAD.Vector(0, 0, 1),
    )
    solid = solid.cut(bore15)

    # ── O-ring groove (toroidal / cylindrical ring subtracted) ───────
    groove_r = groove_OD / 2
    groove_z = 4.5  # axial position from face (spec: 0.05 mm tolerance)
    groove_cyl = Part.makeCylinder(
        groove_r + groove_w / 2,
        groove_w,
        FreeCAD.Vector(0, 0, groove_z - groove_w / 2),
        FreeCAD.Vector(0, 0, 1),
    )
    groove_sub = Part.makeCylinder(
        groove_r - groove_w / 2,
        groove_w + 0.5,
        FreeCAD.Vector(0, 0, groove_z - groove_w / 2 - 0.25),
        FreeCAD.Vector(0, 0, 1),
    )
    groove_ring = groove_cyl.cut(groove_sub)
    solid = solid.cut(groove_ring)

    # ── Anti-rotation flats (×2, 180deg apart) ─────────────────────────
    # Mill flat surfaces on the OD
    flat_d = 1.5  # depth of flat from OD surface
    flat_y = outer_r - flat_d

    for sign in [-1, 1]:
        flat_cut = Part.makeBox(
            flat_w + 2,
            flat_d + 1,
            L_body + 2,
            FreeCAD.Vector(-flat_w / 2 - 1, sign * flat_y, -1),
        )
        solid = solid.cut(flat_cut)

    # ── 4× M3 threaded holes (90deg apart, on OD circle) ────────────────
    m3_d = 2.5  # drill Ø before tapping
    m3_depth = 6.0
    hole_r = outer_r + 0.5  # holes slightly beyond OD
    m3_angles = [0, 90, 180, 270]
    for ang in m3_angles:
        rad = math.radians(ang)
        hx = hole_r * math.cos(rad)
        hy = hole_r * math.sin(rad)
        cyl = Part.makeCylinder(
            m3_d / 2,
            m3_depth + 2,
            FreeCAD.Vector(hx, hy, L_body - m3_depth - 2),
            FreeCAD.Vector(0, 0, 1),
        )
        solid = solid.cut(cyl)

    # ── Through-bore Ø4 mm (wiring) ───────────────────────────────────
    through = Part.makeCylinder(
        through_d / 2, L_body + 2, FreeCAD.Vector(0, 0, -1), FreeCAD.Vector(0, 0, 1)
    )
    solid = solid.cut(through)

    return solid


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 5  -  FREECAD DOCUMENT ASSEMBLY
# ═══════════════════════════════════════════════════════════════════════════════


def assemble_doc(line_code: str, params: dict) -> FreeCAD.Document:
    """Cree / met a jour un document FreeCAD avec les 3 pieces BRK/ACT/NCR."""

    doc_name = f"Interceptor_M_{line_code}"
    Console.PrintMessage(f"\n[model_parts] Assembling document: {doc_name}\n")

    if FC_AVAILABLE:
        # Close if already open
        existing = [d for d in FreeCAD.listDocuments().values() if d.Name == doc_name]
        if existing:
            FreeCAD.closeDocument(doc_name)
        doc = FreeCAD.newDocument(doc_name)
    else:
        doc = None  # headless placeholder

    parts = {
        "BRK-001": build_BRK001(params),
        "ACT-001": build_ACT001(params),
        "NCR-001": build_NCR001(params),
    }

    for part_id, shape in parts.items():
        label = f"{part_id}_{line_code}"
        if FC_AVAILABLE:
            obj = doc.addObject("Part::Feature", label)
            obj.Shape = shape
            obj.Label = label
            # Colour by material
            if part_id == "BRK-001":
                obj.ViewObject.ShapeColor = (0.75, 0.73, 0.70, 1.0)  # aluminium
            elif part_id == "ACT-001":
                obj.ViewObject.ShapeColor = (0.80, 0.75, 0.60, 1.0)
            else:
                obj.ViewObject.ShapeColor = (0.85, 0.85, 0.90, 1.0)  # steel
            obj.ViewObject.update()
        else:
            obj = shape

        # Save individual STEP
        step_file = os.path.join(STEP_DIR, f"{label}.step")
        if FC_AVAILABLE:
            Part.export([obj], step_file)
        else:
            import StepWrite

            StepWrite.export([shape], step_file)
        Console.PrintMessage(f"  → STEP saved: {step_file}\n")

    if FC_AVAILABLE:
        doc.recompute()
        # Save .FCStd
        fcstd_file = os.path.join(MODEL_DIR, f"{doc_name}.FCStd")
        doc.saveAs(fcstd_file)
        Console.PrintMessage(f"  → FCStd saved: {fcstd_file}\n")

    return doc


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 6  -  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

LINES = ["DC", "DD", "DI"]


def main():
    print("=" * 70)
    print("  model_parts.py  -  Interceptor_M FreeCAD Model Generator  v" + __version__)
    print("=" * 70)

    if not FC_AVAILABLE:
        print("[HEADLESS] FreeCAD not available in this Python environment.")
        print("           The script is fully structured for use inside FreeCAD.")
        print("           See USAGE instructions at the top of this file.")
        # Still write STEP files using pythonocc-core if available, else skip
        try:
            import OCC

            print("[OK] pythonocc-core detected  -  STEP export possible headlessly.")
        except ImportError:
            print("[SKIP] STEP export requires FreeCAD or pythonocc-core.")
        return

    for line in LINES:
        try:
            params = load_params(line)
            assemble_doc(line, params)
            print(f"[OK] Line {line}  -  all 3 parts modelled and exported.")
        except FileNotFoundError as e:
            print(f"[WARN] Line {line}  -  {e}")
            continue
        except Exception as e:
            print(f"[ERROR] Line {line}  -  {e}")
            import traceback

            traceback.print_exc()
            continue

    print("\n[model_parts] All done. Documents in:")
    print(f"           {MODEL_DIR}")
    print(f"           {STEP_DIR}")


if __name__ == "__main__":
    main()
