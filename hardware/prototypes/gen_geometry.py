#!/usr/bin/env python3
"""
gen_geometry.py — Interceptor_M Machining Prototypes
Parametric point geometry & parameter sweep generator.

Reads PARAMETERS.json from the repo root, generates point clouds /
parameter sweeps for three representative machined parts, and writes
params.json to the same directory.

Run:  python gen_geometry.py
Output: params.json  (human-readable + machine-parseable)

Authors: D1/D2/D3 per governance PR #31
Review: E1 gate per MECHANICAL_DEV_APPROVAL.md
"""

import json
import math
from pathlib import Path

import numpy as np

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent.resolve()
OUT_JSON   = SCRIPT_DIR / "params.json"

# ── Default fallback parameters (from PARAMETERS.json) ───────────────────────
DEFAULTS = {
    "tube_diameter_mm": 40.0,
    "fuselage_outer_diameter_mm": 35.0,
    "arm_length_mm": 75.0,
    "wing_chord_mm": 60.0,
    "fasteners": ["M2", "M3"],
    "motor_mount_mm": [9.0, 12.0],
    "mtow_g": 250.0,
}

# ── Load parameters ────────────────────────────────────────────────────────────
def load_parameters() -> dict:
    """Load repo PARAMETERS.json; fall back to DEFAULTS if not found."""
    candidates = [
        SCRIPT_DIR.parent.parent / "PARAMETERS.json",   # repo root
        SCRIPT_DIR.parent.parent.parent / "PARAMETERS.json",  # workspace root
    ]
    for path in candidates:
        if path.is_file():
            with open(path) as f:
                data = json.load(f)
            print(f"[gen_geometry] Loaded parameters from {path}")
            return data
    print("[gen_geometry] WARNING: PARAMETERS.json not found — using defaults")
    return DEFAULTS


# ══════════════════════════════════════════════════════════════════════════════
#  BRACKET — Structural Junction (BRK-001)
# ══════════════════════════════════════════════════════════════════════════════

def generate_bracket_geometry(params: dict) -> dict:
    """
    Generates parametric geometry for the Structural Bracket (BRK-001).
    Points define the bounding-box, bore axes, and arm-hole array.

    Key dimensions derived from structural_bracket.md spec:
      Length L = 75 mm, Width W = 55 mm, Thickness T = 10 mm
      Central bore Ø35 mm,  arm holes Ø5 mm × 4 at r=20 mm,
      motor-mount holes Ø9 mm × 4 at r=12 mm offset from arm axis.
    """
    L        = params["arm_length_mm"]        # use arm-length param as length proxy
    bore_d   = params["fuselage_outer_diameter_mm"]   # Ø35 mm
    W        = 55.0
    T        = 10.0
    arm_r    = 20.0        # radial position of arm holes from bore centre
    motor_r  = 12.0        # radial offset for motor-mount holes
    n_arms   = 4
    n_motors = 4

    # ── Bounding-box corner points (mm) ──────────────────────────────────────
    bbox = np.array([
        [0.0,  0.0,  0.0],
        [L,    0.0,  0.0],
        [L,    W,    0.0],
        [0.0,  W,    0.0],
        [0.0,  0.0,  T],
        [L,    0.0,  T],
        [L,    W,    T],
        [0.0,  W,    T],
    ], dtype=np.float64)

    # ── Central bore axis (Z) ───────────────────────────────────────────────
    bore_center = np.array([L / 2, W / 2, 0.0])
    bore_axis_p0 = bore_center.copy()
    bore_axis_p1 = bore_center + np.array([0.0, 0.0, T])

    # ── Arm hole centres (radial array at z = T/2) ──────────────────────────
    arm_hole_z = T / 2
    arm_angles = np.linspace(0, 2 * math.pi, n_arms, endpoint=False)
    arm_centres = np.array([
        [bore_center[0] + arm_r * math.cos(a),
         bore_center[1] + arm_r * math.sin(a),
         arm_hole_z]
        for a in arm_angles
    ], dtype=np.float64)

    # ── Motor-mount hole centres (offset 45° from arm holes) ─────────────────
    motor_angles = arm_angles + math.pi / 4   # 45° offset
    motor_centres = np.array([
        [bore_center[0] + (arm_r + motor_r) * math.cos(a),
         bore_center[1] + (arm_r + motor_r) * math.sin(a),
         arm_hole_z]
        for a in motor_angles
    ], dtype=np.float64)

    # ── Parameter sweep (tolerance variation study) ─────────────────────────
    #   Variants: nominal, tight, loose  →  GD&T tolerance study for CMM
    bore_tols = {"nominal": (0.0, 0.0),
                 "tight":  (-0.010, -0.025),
                 "loose":  (+0.010, +0.025)}
    arm_tols  = {"nominal": (0.0, 0.0),
                 "tight":  (-0.010, -0.018),
                 "loose":  (+0.010, +0.018)}

    sweep = {}
    for variant, (lo, hi) in bore_tols.items():
        sweep[f"bore_35_{variant}"] = {
            "min_mm": round(bore_d + lo, 4),
            "max_mm": round(bore_d + hi, 4),
        }
    for variant, (lo, hi) in arm_tols.items():
        sweep[f"arm_hole_5_{variant}"] = {
            "min_mm": round(5.0 + lo, 4),
            "max_mm": round(5.0 + hi, 4),
        }

    return {
        "part_id": "BRK-001",
        "bounding_box_corners_mm": bbox.tolist(),
        "bore_axis": {"p0": bore_axis_p0.tolist(), "p1": bore_axis_p1.tolist()},
        "bore_diameter_mm": round(bore_d, 3),
        "arm_hole_centres_mm": arm_centres.tolist(),
        "arm_hole_diameter_mm": 5.0,
        "motor_mount_centres_mm": motor_centres.tolist(),
        "motor_mount_diameter_mm": 9.0,
        "mass_g_estimated": round(L * W * T * 2.71 / 1000, 2),   # 7075-T6 ρ=2.71 g/cm³
        "tolerance_sweep": sweep,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  ACTUATOR MOUNT (ACT-001)
# ══════════════════════════════════════════════════════════════════════════════

def generate_actuator_mount_geometry(params: dict) -> dict:
    """
    Generates parametric geometry for the Actuator Mount (ACT-001).
    Dimensions from actuator_mount.md spec.

    Key: ESC pocket 30.5×15.5×8.5 mm, FC pocket 30.5×30.5×8.5 mm,
         battery slot 20.5 mm wide, 4× M3 clearance holes.
    """
    L      = 65.0
    W      = 45.0
    T      = 7.0
    esc    = (30.5, 15.5, 8.5)
    fc     = (30.5, 30.5, 8.5)
    bat    = (20.5, 6.0)
    m3_d   = 3.3      # clearance hole diameter
    m2_d   = 2.2

    # ── Overall bounding box ──────────────────────────────────────────────────
    bbox = np.array([
        [0.0,  0.0,  0.0],
        [L,    0.0,  0.0],
        [L,    W,    0.0],
        [0.0,  W,    0.0],
        [0.0,  0.0,  T],
        [L,    0.0,  T],
        [L,    W,    T],
        [0.0,  W,    T],
    ], dtype=np.float64)

    # ── Pocket centre positions (relative to part bottom-left corner = 0,0,0)
    #    ESC: centred horizontally, 10 mm from right edge
    esc_cx = (L - esc[0]) / 2
    esc_cy = 10.0
    #    FC: top-left corner
    fc_cx  = 4.0
    fc_cy  = W - fc[1] - 4.0
    #    Battery: strip between ESC and FC, along full length
    bat_cx = 0.0
    bat_cy = (W - bat[0]) / 2

    pockets = {
        "ESC": {
            "centre_mm":  [round(esc_cx + esc[0]/2, 3),
                           round(esc_cy + esc[1]/2, 3),
                           round(T / 2, 3)],
            "size_mm":    list(esc),
            "bounds_mm":  [esc_cx, esc_cx + esc[0],
                            esc_cy, esc_cy + esc[1],
                            0.0,    T],
        },
        "FC": {
            "centre_mm":  [round(fc_cx + fc[0]/2, 3),
                           round(fc_cy + fc[1]/2, 3),
                           round(T / 2, 3)],
            "size_mm":    list(fc),
            "bounds_mm":  [fc_cx, fc_cx + fc[0],
                            fc_cy, fc_cy + fc[1],
                            0.0,   T],
        },
        "Battery_slot": {
            "centre_mm":  [round(L / 2, 3),
                           round(W / 2, 3),
                           round(T, 3)],
            "width_mm":   bat[0],
            "depth_mm":   bat[1],
        },
    }

    # ── M3 clearance holes — 4× at corners (interface to BRK-001) ───────────
    margin = 4.0
    m3_holes = [
        [margin,           margin,           T / 2],
        [L - margin,       margin,           T / 2],
        [margin,           W - margin,       T / 2],
        [L - margin,       W - margin,       T / 2],
    ]

    # ── M2 clearance holes — 6× grid for ESC/FC standoffs ──────────────────
    m2_holes = []
    for row in range(2):
        for col in range(3):
            x = esc_cx + (col + 0.5) * (esc[0] / 3)
            y = esc_cy + (row + 0.5) * (esc[1] / 2)
            m2_holes.append([round(x, 3), round(y, 3), round(T / 2, 3)])

    # ── Parameter sweep: pocket dimensions ──────────────────────────────────
    sweep = {}
    for pocket_name, pocket in [("ESC", esc), ("FC", fc)]:
        for variant, tol in [("tight", -0.10), ("nominal", 0.0), ("loose", 0.10)]:
            sweep[f"{pocket_name.lower()}_length_{variant}"] = {
                "min_mm": round(pocket[0] + tol, 3),
                "max_mm": round(pocket[0] + tol + 0.20, 3),
            }
            sweep[f"{pocket_name.lower()}_width_{variant}"] = {
                "min_mm": round(pocket[1] + tol, 3),
                "max_mm": round(pocket[1] + tol + 0.20, 3),
            }

    return {
        "part_id": "ACT-001",
        "bounding_box_corners_mm": bbox.tolist(),
        "pockets": pockets,
        "m3_clearance_holes_mm": m3_holes,
        "m2_clearance_holes_mm": m2_holes,
        "mass_g_estimated": round(L * W * T * 2.71 / 1000, 2),   # 7075-T6 ρ=2.71
        "tolerance_sweep": sweep,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  NOSE-CONE INTERFACE RING (NCR-001)
# ══════════════════════════════════════════════════════════════════════════════

def generate_nose_cone_ring_geometry(params: dict) -> dict:
    """
    Generates parametric geometry for the Nose-Cone Interface Ring (NCR-001).
    Dimensions from nose_cone_ring.md spec.
    Turning on lathe: axis = Z.  OD=44, ID=35, L=20.
    O-ring groove at Ø36.5 mm, width 2.80 mm.
    2× anti-rotation flats, 4× M3 tapped holes.
    """
    tube_d  = params["tube_diameter_mm"]     # Ø40 mm launcher tube (reference only)
    fuselage_d = params["fuselage_outer_diameter_mm"]  # Ø35 mm

    L       = 20.0
    OD      = 44.0
    bore_d  = fuselage_d     # Ø35 mm — matches fuselage
    pilot_d = 15.0
    or_groove_d  = fuselage_d + 1.5          # Ø36.5 mm
    or_groove_w  = 2.80
    m3_d    = 2.5    # tap drill for M3 × 0.5
    wire_d  = 4.0
    n_flats = 2
    n_holes = 4

    # ── Cross-section profile (lathe: points along radius vs axial position Z)
    #    Z=0: reference face (nose side); Z=L: clamp side
    profile_z = np.array([0.0, 2.0, or_groove_w + 0.5, L - 0.5, L])
    profile_r = np.array([
        bore_d / 2,               # Ø35 bore
        bore_d / 2,               # Ø35 bore
        (or_groove_d / 2) + 0.4,  # O-ring groove outer edge
        OD / 2,                   # full OD
        OD / 2,                   # full OD
    ])
    profile_pts = np.stack([profile_z, profile_r], axis=1).tolist()

    # ── O-ring groove points (parametric ring) ──────────────────────────────
    n_or_pts = 72
    or_theta = np.linspace(0, 2 * math.pi, n_or_pts, endpoint=False)
    or_z     = or_groove_w / 2      # axial midpoint of groove
    or_r     = or_groove_d / 2      # radial midpoint of groove
    or_ring_pts = np.stack([
        np.full(n_or_pts, or_z),
        or_r * np.cos(or_theta),
        or_r * np.sin(or_theta),
    ], axis=1).tolist()

    # ── Anti-rotation flat centres (mill operation) ─────────────────────────
    flat_angle = 90.0        # first flat at 12 o'clock; second at 6 o'clock
    flat_width = 6.0        # mm

    # ── M3 tapped hole centres (radial, 90° apart, at Z = L - 3 mm) ─────────
    hole_z = L - 3.0
    hole_r = OD / 2 - 2.0
    hole_angles = np.linspace(0, 2 * math.pi, n_holes, endpoint=False)
    m3_hole_ctrs = np.array([
        [or_z, hole_r * math.cos(a), hole_r * math.sin(a)]
        for a in hole_angles
    ]).tolist()

    # ── Parameter sweep: bore ID variation ───────────────────────────────────
    sweep = {}
    for variant, tol in [("tight", -0.025), ("nominal", 0.0), ("loose", 0.025)]:
        sweep[f"bore_35_{variant}_mm"] = {
            "min_mm": round(bore_d + tol, 4),
            "max_mm": round(bore_d + tol + 0.025, 4),
        }
    for variant, tol in [("tight", -0.03), ("nominal", 0.0), ("loose", 0.03)]:
        sweep[f"od_44_{variant}_mm"] = {
            "min_mm": round(OD + tol, 4),
            "max_mm": round(OD + tol + 0.03, 4),
        }

    return {
        "part_id": "NCR-001",
        "cross_section_profile_zr_mm": profile_pts,
        "o_ring_groove": {
            "groove_diameter_mm": or_groove_d,
            "groove_width_mm":    or_groove_w,
            "mid_radius_mm":      round(or_r, 3),
            "mid_axial_mm":       round(or_z, 3),
            "ring_points_72":     or_ring_pts,
        },
        "bore_diameter_mm":     bore_d,
        "pilot_bore_mm":        pilot_d,
        "outer_diameter_mm":    OD,
        "overall_length_mm":   L,
        "anti_rotation_flats": {
            "count": n_flats,
            "width_mm": flat_width,
            "angular_positions_deg": [90.0, 270.0],
        },
        "m3_tapped_hole_centres_mm": m3_hole_ctrs,
        "wire_through_bore_mm": wire_d,
        "mass_g_estimated": round(
            math.pi * ((OD/2)**2 - (bore_d/2)**2) * L * 8.0 / 1000, 2
        ),   # 316L SS ρ=8.0 g/cm³
        "tolerance_sweep": sweep,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("[gen_geometry] Starting Interceptor_M prototype parameter generation")
    params = load_parameters()

    bracket   = generate_bracket_geometry(params)
    actuator  = generate_actuator_mount_geometry(params)
    ring      = generate_nose_cone_ring_geometry(params)

    output = {
        "project": "Interceptor_M",
        "package": "hardware/prototypes",
        "generator": "gen_geometry.py",
        "revision": "v0.1-draft",
        "parameters_source": params,
        "parts": [bracket, actuator, ring],
    }

    with open(OUT_JSON, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[gen_geometry] Wrote {OUT_JSON}")
    print(f"  Parts generated: {[p['part_id'] for p in output['parts']]}")
    print(f"  Est. masses (g): {[p['mass_g_estimated'] for p in output['parts']]}")

    # ── Sanity checks ────────────────────────────────────────────────────────
    for part in output["parts"]:
        assert part["part_id"].startswith(("BRK", "ACT", "NCR")), \
            f"Invalid part_id: {part['part_id']}"
        assert part["mass_g_estimated"] > 0, \
            f"Zero/negative mass for {part['part_id']}"
        assert "tolerance_sweep" in part, \
            f"Missing tolerance_sweep for {part['part_id']}"

    # BRK-001: 4 arm holes, 4 motor holes
    brk = bracket
    assert len(brk["arm_hole_centres_mm"]) == 4,    "BRK arm holes != 4"
    assert len(brk["motor_mount_centres_mm"]) == 4,  "BRK motor holes != 4"

    # ACT-001: 4 M3 + 6 M2 clearance holes
    act = actuator
    assert len(act["m3_clearance_holes_mm"]) == 4,   "ACT M3 holes != 4"
    assert len(act["m2_clearance_holes_mm"]) == 6,   "ACT M2 holes != 6"

    # NCR-001: 4 M3 tapped holes, 72-point O-ring ring
    ncr = ring
    assert len(ncr["m3_tapped_hole_centres_mm"]) == 4, "NCR M3 holes != 4"
    assert len(ncr["o_ring_groove"]["ring_points_72"]) == 72, "NCR OR ring != 72 pts"

    print("[gen_geometry] All assertions passed ✓")
    return output


if __name__ == "__main__":
    main()
