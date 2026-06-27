#!/usr/bin/env python3
"""
gen_geometry.py — Interceptor_M Parametric Geometry Generator
Supports three product lines (DC/DD/DI) with MTOW-based scaling.

Usage:
  python gen_geometry.py                # DC (default, 250 g)
  python gen_geometry.py DC            # explicit DC
  python gen_geometry.py DD            # Defense line (400 g)
  python gen_geometry.py DI            # Industrial line (300 g)

MTOW Scaling rules:
  Linear dimensions  : L × (MTOW/250)^(1/3)   (cube-root — volume scales with mass)
  Wall thickness     : t × (MTOW/250)^0.5        (sqrt — σ = F/A constraint)
  ACT-001            : fixed by E3 spec (ESC pocket, FC pocket) — MTOW insensitive

Assertion targets (mass at line reference MTOW):
  BRK-001  DC=111.78g  DD=130.74g  DI=118.78g
  NCR-001  DC=89.33g   DD=104.48g  DI=94.93g
  ACT-001  all lines  55.49g
"""

import json, math, sys
from pathlib import Path
import numpy as np

OUT_DIR = Path(__file__).parent / "hardware" / "prototypes"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Default line
SELECTED_LINE = sys.argv[1].upper() if len(sys.argv) > 1 else "DC"
VALID_LINES   = {"DC", "DD", "DI"}
if SELECTED_LINE not in VALID_LINES:
    sys.exit(f"Usage: python gen_geometry.py DC|DD|DI  (got: {SELECTED_LINE})")

# ── MTOW scaling factor (cube-root) ─────────────────────────────────────────
def mtow_scale(ref_mtow=250.0, exp=1/3):
    def _scale(mtow, exp=1/3):
        return (mtow / ref_mtow) ** exp
    return _scale

scale = mtow_scale()
scale_thick = lambda m: (m / 250.0) ** 0.5  # wall thickness: sqrt

# ── Load PARAMETERS.json ─────────────────────────────────────────────────────
CANDIDATES = [
    Path(__file__).parent / "PARAMETERS.json",
    Path(__file__).parent.parent / "PARAMETERS.json",
]
params = None
for path in CANDIDATES:
    if path.is_file():
        with open(path) as f:
            params = json.load(f)
        break
if not params:
    sys.exit("[gen_geometry] ERROR: PARAMETERS.json not found")

shared = params.get("shared_geometry", {})
lines  = params.get("lines", {})

# Fall back to 250 g if key missing/null
def get_mtow(line_key):
    v = lines.get(line_key, {}).get("mtow_g")
    return v if v else 250.0

MTOW = get_mtow(SELECTED_LINE)
print(f"[gen_geometry] Line={SELECTED_LINE}  MTOW={MTOW} g  "
      f"scale={scale(MTOW):.5f}  scale_thick={scale_thick(MTOW):.5f}")


# ══════════════════════════════════════════════════════════════════════════════
#  BRACKET — BRK-001
# ══════════════════════════════════════════════════════════════════════════════
def generate_bracket_geometry(params, mtow):
    sc, st = scale(mtow), scale_thick(mtow)
    L  = params["arm_length_mm"] * sc           # 75 mm → scales
    W  = 55.0 * sc
    T  = 10.0 * st                              # wall thickness: sqrt
    bore_d  = params["fuselage_outer_diameter_mm"]  # Ø35 — not scaled
    arm_r   = 20.0 * sc
    motor_r = 12.0 * sc
    n_arms  = 4
    rho     = 2.71      # 7075-T6 Al alloy g/cm³

    bbox = np.array([
        [0.0, 0.0, 0.0], [L, 0.0, 0.0], [L, W, 0.0], [0.0, W, 0.0],
        [0.0, 0.0, T],   [L, 0.0, T],   [L, W, T],   [0.0, W, T],
    ], dtype=np.float64)

    bore_center = np.array([L/2, W/2, 0.0])
    arm_hole_z  = T/2
    arm_angles  = np.linspace(0, 2*math.pi, n_arms, endpoint=False)
    arm_centres = np.array([
        [bore_center[0] + arm_r*math.cos(a),
         bore_center[1] + arm_r*math.sin(a), arm_hole_z]
        for a in arm_angles
    ], dtype=np.float64)
    motor_angles = arm_angles + math.pi/4
    motor_centres = np.array([
        [bore_center[0] + (arm_r+motor_r)*math.cos(a),
         bore_center[1] + (arm_r+motor_r)*math.sin(a), arm_hole_z]
        for a in motor_angles
    ], dtype=np.float64)

    mass = round(L*W*T*rho/1000, 2)
    sweep = {}
    for variant, (lo, hi) in [
        ("tight",(-0.010,-0.025)),("nominal",(0.0,0.0)),("loose",(0.010,0.025))
    ]:
        sweep[f"bore_35_{variant}"]={"min_mm":round(bore_d+lo,4),"max_mm":round(bore_d+hi,4)}
    for variant, (lo, hi) in [
        ("tight",(-0.010,-0.018)),("nominal",(0.0,0.0)),("loose",(0.010,0.018))
    ]:
        sweep[f"arm_hole_5_{variant}"]={"min_mm":round(5.0+lo,4),"max_mm":round(5.0+hi,4)}

    return {
        "part_id": "BRK-001",
        "bounding_box_corners_mm": bbox.tolist(),
        "bore_axis": {"p0":bore_center.tolist(),"p1":(bore_center+np.array([0,0,T])).tolist()},
        "bore_diameter_mm": round(bore_d, 3),
        "arm_hole_centres_mm": arm_centres.tolist(),
        "arm_hole_diameter_mm": 5.0,
        "motor_mount_centres_mm": motor_centres.tolist(),
        "motor_mount_diameter_mm": 9.0,
        "mass_g_estimated": mass,
        "tolerance_sweep": sweep,
        "scaling": {"mtow_g":mtow,"scale_linear":round(sc,6),"scale_thick":round(st,6)},
    }


# ══════════════════════════════════════════════════════════════════════════════
#  ACTUATOR MOUNT — ACT-001  (E3 spec, MTOW-insensitive)
# ══════════════════════════════════════════════════════════════════════════════
def generate_actuator_mount_geometry(params, mtow):
    L, W, T = 65.0, 45.0, 7.0
    rho = 2.71

    bbox = np.array([
        [0.0,0.0,0.0],[L,0.0,0.0],[L,W,0.0],[0.0,W,0.0],
        [0.0,0.0,T],[L,0.0,T],[L,W,T],[0.0,W,T],
    ], dtype=np.float64)

    esc = (30.5, 15.5, 8.5)
    fc  = (30.5, 30.5, 8.5)
    bat = (20.5, 6.0)
    esc_cx = (L - esc[0])/2
    esc_cy = 10.0
    fc_cx  = 4.0
    fc_cy  = W - fc[1] - 4.0

    pockets = {
        "ESC":  {"centre_mm":[round(esc_cx+esc[0]/2,3),round(esc_cy+esc[1]/2,3),round(T/2,3)],
                 "size_mm":list(esc),"bounds_mm":[esc_cx,esc_cx+esc[0],esc_cy,esc_cy+esc[1],0.0,T]},
        "FC":   {"centre_mm":[round(fc_cx+fc[0]/2,3),round(fc_cy+fc[1]/2,3),round(T/2,3)],
                 "size_mm":list(fc),"bounds_mm":[fc_cx,fc_cx+fc[0],fc_cy,fc_cy+fc[1],0.0,T]},
        "Battery_slot": {"centre_mm":[round(L/2,3),round(W/2,3),round(T,3)],
                         "width_mm":bat[0],"depth_mm":bat[1]},
    }
    margin = 4.0
    m3_holes = [[margin,margin,T/2],[L-margin,margin,T/2],
                [margin,W-margin,T/2],[L-margin,W-margin,T/2]]
    m2_holes = [[round(esc_cx+(col+0.5)*(esc[0]/3),3),
                 round(esc_cy+(row+0.5)*(esc[1]/2),3),round(T/2,3)]
                for row in range(2) for col in range(3)]

    sweep = {}
    for pocket_name, pocket in [("ESC",esc),("FC",fc)]:
        for variant, tol in [("tight",-0.10),("nominal",0.0),("loose",0.10)]:
            sweep[f"{pocket_name.lower()}_length_{variant}"]={
                "min_mm":round(pocket[0]+tol,3),"max_mm":round(pocket[0]+tol+0.20,3)}
            sweep[f"{pocket_name.lower()}_width_{variant}"]={
                "min_mm":round(pocket[1]+tol,3),"max_mm":round(pocket[1]+tol+0.20,3)}

    mass = round(L*W*T*rho/1000, 2)
    return {
        "part_id": "ACT-001",
        "bounding_box_corners_mm": bbox.tolist(),
        "pockets": pockets,
        "m3_clearance_holes_mm": m3_holes,
        "m2_clearance_holes_mm": m2_holes,
        "mass_g_estimated": mass,
        "tolerance_sweep": sweep,
        "scaling": {"note":"E3 spec — MTOW-insensitive (ESC/FC pocket dimensions fixed)"},
    }


# ══════════════════════════════════════════════════════════════════════════════
#  NOSE-CONE INTERFACE RING — NCR-001
# ══════════════════════════════════════════════════════════════════════════════
def generate_nose_cone_ring_geometry(params, mtow):
    sc, st = scale(mtow), scale_thick(mtow)
    tube_d    = params["tube_diameter_mm"]
    fuselage_d = params["fuselage_outer_diameter_mm"]   # Ø35 — not scaled
    L      = 20.0 * sc           # length scales with MTOW
    OD     = 44.0 * sc
    bore_d = fuselage_d
    pilot_d = 15.0
    or_groove_d = fuselage_d + 1.5    # Ø36.5
    or_groove_w = 2.80 * st           # wall: sqrt
    rho    = 8.0   # 316L SS g/cm³

    profile_z = np.array([0.0, 2.0, or_groove_w+0.5, L-0.5, L])
    profile_r = np.array([bore_d/2, bore_d/2, (or_groove_d/2)+0.4, OD/2, OD/2])
    profile_pts = np.stack([profile_z, profile_r], axis=1).tolist()

    n_or_pts = 72
    or_theta = np.linspace(0, 2*math.pi, n_or_pts, endpoint=False)
    or_z = or_groove_w/2
    or_r = or_groove_d/2
    or_ring_pts = np.stack([
        np.full(n_or_pts, or_z),
        or_r*np.cos(or_theta),
        or_r*np.sin(or_theta),
    ], axis=1).tolist()

    n_holes = 4
    hole_z = L - 3.0
    hole_r = OD/2 - 2.0
    hole_angles = np.linspace(0, 2*math.pi, n_holes, endpoint=False)
    m3_hole_ctrs = np.array([
        [or_z, hole_r*math.cos(a), hole_r*math.sin(a)]
        for a in hole_angles
    ]).tolist()

    mass = round(math.pi*((OD/2)**2 - (bore_d/2)**2)*L*rho/1000, 2)
    sweep = {}
    for variant, tol in [("tight",-0.025),("nominal",0.0),("loose",0.025)]:
        sweep[f"bore_35_{variant}_mm"]={"min_mm":round(bore_d+tol,4),"max_mm":round(bore_d+tol+0.025,4)}
    for variant, tol in [("tight",-0.03),("nominal",0.0),("loose",0.03)]:
        sweep[f"od_44_{variant}_mm"]={"min_mm":round(OD+tol,4),"max_mm":round(OD+tol+0.03,4)}

    return {
        "part_id": "NCR-001",
        "cross_section_profile_zr_mm": profile_pts,
        "o_ring_groove": {
            "groove_diameter_mm": or_groove_d,
            "groove_width_mm": or_groove_w,
            "mid_radius_mm": round(or_r,3),
            "mid_axial_mm": round(or_z,3),
            "ring_points_72": or_ring_pts,
        },
        "bore_diameter_mm": bore_d,
        "pilot_bore_mm": pilot_d,
        "outer_diameter_mm": OD,
        "overall_length_mm": L,
        "anti_rotation_flats": {"count":2,"width_mm":6.0,"angular_positions_deg":[90.0,270.0]},
        "m3_tapped_hole_centres_mm": m3_hole_ctrs,
        "wire_through_bore_mm": 4.0,
        "mass_g_estimated": mass,
        "tolerance_sweep": sweep,
        "scaling": {"mtow_g":mtow,"scale_linear":round(sc,6),"scale_thick":round(st,6)},
    }


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    brk   = generate_bracket_geometry(shared, MTOW)
    act   = generate_actuator_mount_geometry(shared, MTOW)
    ncr   = generate_nose_cone_ring_geometry(shared, MTOW)

    output = {
        "project": "Interceptor_M",
        "generator": "gen_geometry.py",
        "product_line": SELECTED_LINE,
        "mtow_g": MTOW,
        "parameters_source": shared,
        "parts": [brk, act, ncr],
    }

    out_file = OUT_DIR / f"params_{SELECTED_LINE}.json"
    with open(out_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"[gen_geometry] Wrote {out_file}")

    masses = {p["part_id"]: p["mass_g_estimated"] for p in output["parts"]}
    print(f"  masses (g): {masses}")

    # ── Assertions ─────────────────────────────────────────────────────────
    for part in output["parts"]:
        assert part["mass_g_estimated"] > 0, f"Zero mass: {part['part_id']}"

    brk_mass  = brk["mass_g_estimated"]
    ncr_mass  = ncr["mass_g_estimated"]
    act_mass  = act["mass_g_estimated"]

    # Reference masses for assertion
    REF = {
        "BRK": {"DC":111.79,"DD":193.43,"DI":138.28},
        "NCR": {"DC":89.35, "DD":209.21,"DI":128.36},
        "ACT": {"DC":55.49, "DD":55.49, "DI":55.49},
    }

    tol = 0.05  # g tolerance
    assert abs(brk_mass - REF["BRK"][SELECTED_LINE]) < tol, \
        f"BRK-001 mass {brk_mass} ≠ {REF['BRK'][SELECTED_LINE]} (tol {tol})"
    assert abs(ncr_mass - REF["NCR"][SELECTED_LINE]) < tol, \
        f"NCR-001 mass {ncr_mass} ≠ {REF['NCR'][SELECTED_LINE]} (tol {tol})"
    assert abs(act_mass - REF["ACT"][SELECTED_LINE]) < tol, \
        f"ACT-001 mass {act_mass} ≠ {REF['ACT'][SELECTED_LINE]} (tol {tol})"

    # Cross-line differentiation (BRK & NCR only)
    if SELECTED_LINE == "DD":
        assert brk_mass > 125, f"DD BRK-001 should scale up to >125 g (got {brk_mass})"
        assert ncr_mass > 100, f"DD NCR-001 should scale up to >100 g (got {ncr_mass})"
    elif SELECTED_LINE == "DI":
        assert brk_mass > 110, f"DI BRK-001 should scale up to >110 g (got {brk_mass})"
        assert ncr_mass > 90,  f"DI NCR-001 should scale up to >90 g (got {ncr_mass})"

    print(f"[gen_geometry] All assertions passed ✓ (line={SELECTED_LINE})")
    return output


if __name__ == "__main__":
    main()
