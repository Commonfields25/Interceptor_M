"""
simulation/montecarlo_pintercept.py
====================================
High-Fidelity Monte Carlo Analysis for Interceptor_M.
"""

import math
import random
import statistics
import csv
import os
import datetime
import numpy as np
from . import constants as C
from .sim_6dof import simulate_engagement, manoeuvre_rectiligne, manoeuvre_virage_constant, manoeuvre_weaving
from .flight_control_poc import GuidanceSystem

_P_MIN    = C.PORTEE_MIN_M
_P_MAX    = C.PORTEE_MAX_M
_ALT_MIN  = C.ALTITUDE_MIN_M
_ALT_MAX  = C.ALTITUDE_MAX_M
_V_CIBLE  = C.V_CIBLE_MAX_M_S

if C.GRAIN_ALEA is not None:
    random.seed(C.GRAIN_ALEA)
    np.random.seed(C.GRAIN_ALEA)

def tirer_config():
    alt_init_m  = random.uniform(_ALT_MIN, _ALT_MAX)
    portee_cibl_m = random.uniform(_P_MIN, _P_MAX)
    alt_cibl_m    = random.uniform(_ALT_MIN, _ALT_MAX)
    angle_cibl_rad  = random.uniform(0.0, 2.0 * math.pi)
    pos_cible = [portee_cibl_m * math.cos(angle_cibl_rad), portee_cibl_m * math.sin(angle_cibl_rad), alt_cibl_m]
    cap_init_rad = angle_cibl_rad
    pos_init_i = [0.0, 0.0, alt_init_m]
    vel_init_i = 100.0
    vel_cible_m_s = random.uniform(50.0, 150.0)
    cap_cible_rad = angle_cibl_rad + math.pi + random.uniform(-0.3, 0.3)
    r = random.random()
    if r < 0.4:
        manoeuvre_fn, m_type, m_intensity = manoeuvre_rectiligne, "Rectiligne", 0.0
    elif r < 0.7:
        g_load = random.uniform(2.0, 8.0)
        manoeuvre_fn = lambda etat, dt: manoeuvre_virage_constant(etat, dt, accel_g=g_load)
        m_type, m_intensity = "Virage", g_load
    else:
        g_load = random.uniform(2.0, 6.0)
        freq = random.uniform(0.1, 0.4)
        manoeuvre_fn = lambda etat, dt: manoeuvre_weaving(etat, dt, accel_g=g_load, freq_hz=freq)
        m_type, m_intensity = "Weaving", g_load
    return {
        "pos_init_i": pos_init_i, "vel_init_i_m_s": vel_init_i, "cap_init_rad": cap_init_rad,
        "pos_cible": pos_cible, "vel_cible_m_s": vel_cible_m_s, "cap_cible_rad": cap_cible_rad,
        "manoeuvre_fn": manoeuvre_fn, "m_type": m_type, "m_intensity": m_intensity, "range_init": portee_cibl_m
    }

def classify_failure(res):
    if res["intercept"]: return "Success"
    if res.get("lost_seeker"): return "Seeker Lost (FOR)"
    etat_f = res["etat_final_i"]
    v_final = np.linalg.norm(etat_f["vitesse"])
    if v_final < 80.0: return "Kinetic Exhaustion"
    if etat_f["position"][2] < 0.0: return "Ground Collision"
    return "Maneuver Saturation"

def run_monte_carlo(nb_tirages=100, mode="APN"):
    print(f"[Monte Carlo] Running {nb_tirages} iterations (Mode: {mode})...")
    results = []
    for i in range(nb_tirages):
        cfg = tirer_config()
        gs = GuidanceSystem(mode=mode, latency_steps=10)
        res = simulate_engagement(
            pos_init_m=cfg["pos_init_i"], vel_init_m_s=cfg["vel_init_i_m_s"], cap_init_rad=cfg["cap_init_rad"],
            pos_cible_m=cfg["pos_cible"], vel_cible_m_s=cfg["vel_cible_m_s"], cap_cible_rad=cfg["cap_cible_rad"],
            guidage_sys=gs, manoeuvre_c_fn=cfg["manoeuvre_fn"], keep_traj=False
        )
        results.append({
            "success": res["intercept"], "miss": res["distance_min_m"], "time": res["temps_s"],
            "range": cfg["range_init"], "v_target": cfg["vel_cible_m_s"], "m_type": cfg["m_type"],
            "m_intensity": cfg["m_intensity"], "fail_mode": classify_failure(res),
            "v_final": np.linalg.norm(res["etat_final_i"]["vitesse"])
        })
    return results

def generate_report(results_list, modes, n_tirages):
    report_path = "docs/analysis/PHYSICS_PERFORMANCE_REPORT.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write(f"---\nagent: E3\naction: Analysis\ntimestamp: {datetime.datetime.now().isoformat()}Z\nstatus: Active\n---\n\n# 🚀 PHYSICS PERFORMANCE REPORT\n\n")
        f.write(f"**Monte Carlo Analysis Summary** ({n_tirages} runs per mode)\n\n")
        f.write("| Metric | " + " | ".join(modes) + " |\n")
        f.write("| --- | " + " | ".join(["---"] * len(modes)) + " |\n")

        # P(intercept)
        p_ints = [sum(1 for r in res if r["success"]) / len(res) for res in results_list]
        f.write("| **P(intercept)** | " + " | ".join([f"{p*100:.1f} %" for p in p_ints]) + " |\n")

        # Miss Distance Stats
        avg_misses = [statistics.mean([r["miss"] for r in res]) for res in results_list]
        f.write("| **Avg Miss Distance** | " + " | ".join([f"{m:.2f} m" for m in avg_misses]) + " |\n")

        med_misses = [statistics.median([r["miss"] for r in res]) for res in results_list]
        f.write("| **Median Miss Distance** | " + " | ".join([f"{m:.2f} m" for m in med_misses]) + " |\n")

        p95_misses = [np.percentile([r["miss"] for r in res], 95) for res in results_list]
        f.write("| **P95 Miss Distance** | " + " | ".join([f"{m:.2f} m" for m in p95_misses]) + " |\n")

        # Terminal Velocity
        avg_vf = [statistics.mean([r["v_final"] for r in res]) for res in results_list]
        f.write("| **Avg Final Velocity** | " + " | ".join([f"{v:.1f} m/s" for v in avg_vf]) + " |\n")

        f.write("\n## 📊 FAILURE MODE ANALYSIS\n\n| Mode | " + " | ".join(modes) + " |\n| --- | " + " | ".join(["---"] * len(modes)) + " |\n")
        all_fm = sorted(list(set(r["fail_mode"] for res in results_list for r in res if not r["success"])))
        for fm in all_fm:
            row = [f"**{fm}**"]
            for res in results_list:
                count = sum(1 for r in res if r["fail_mode"] == fm)
                row.append(f"{count/len(res)*100:.1f} % ({count})")
            f.write("| " + " | ".join(row) + " |\n")

        f.write("\n## 🎯 SENSITIVITY ANALYSIS (APN)\n\n")
        apn_res = results_list[1]

        f.write("### Range Sensitivity\n\n| Range Bin | P(intercept) |\n| --- | --- |\n")
        for b in [(0, 1500), (1500, 3000), (3000, 5000)]:
            subset = [r for r in apn_res if b[0] <= r["range"] < b[1]]
            if subset:
                rate = sum(1 for r in subset if r["success"]) / len(subset)
                f.write(f"| {b[0]}-{b[1]}m | {rate*100:5.1f}% |\n")

        f.write("\n### Maneuver Intensity Sensitivity\n\n| Intensity Bin | P(intercept) |\n| --- | --- |\n")
        for b in [(0, 1), (1, 4), (4, 8)]:
            subset = [r for r in apn_res if b[0] <= r["m_intensity"] < b[1]]
            if subset:
                rate = sum(1 for r in subset if r["success"]) / len(subset)
                f.write(f"| {b[0]}-{b[1]}G | {rate*100:5.1f}% |\n")

    print(f"\n[Report] High-fidelity report generated at: {report_path}")

if __name__ == "__main__":
    n = 100
    res_pn = run_monte_carlo(n, mode="PN")
    res_apn = run_monte_carlo(n, mode="APN")
    generate_report([res_pn, res_apn], ["PN", "APN"], n)
