import math, random, statistics, csv, os, datetime, numpy as np
from . import constants as C
from .sim_6dof import simulate_engagement
from .flight_control_poc import GuidanceSystem
_P_MIN, _P_MAX, _ALT_MIN, _ALT_MAX, _V_CIBLE, _V_LAUNCH = C.PORTEE_MIN_M, C.PORTEE_MAX_M, C.ALTITUDE_MIN_M, C.ALTITUDE_MAX_M, C.V_CIBLE_MAX_M_S, C.V_LAUNCH_M_S

def tirer_config():
    a_i, p_c, a_c, ang_c = random.uniform(_ALT_MIN,_ALT_MAX), random.uniform(_P_MIN,_P_MAX), random.uniform(_ALT_MIN,_ALT_MAX), random.uniform(0, 2*math.pi)
    pos_c = [p_c*math.cos(ang_c), p_c*math.sin(ang_c), a_c]
    return {"p_i": [0,0,a_i], "v_i": _V_LAUNCH, "c_i": ang_c, "p_c": pos_c, "v_c_m": random.uniform(30,_V_CIBLE), "c_c": ang_c+math.pi+random.uniform(-0.5,0.5), "r_init": p_c}

def classify_failure(res):
    if res["intercept"]: return "Success"
    if res.get("lost_seeker"): return "Seeker Lost (FOR)"
    ef = res["etat_final_i"]
    if ef["energy_used"] >= C.BATTERY_CAPACITY_J: return "Battery Depleted"
    return "Maneuver Saturation"

def run_monte_carlo(nb=100, mode="APN"):
    results = []
    for i in range(nb):
        c = tirer_config(); gs = GuidanceSystem(mode=mode, latency_steps=10)
        r = simulate_engagement(c["p_i"], c["v_i"], c["c_i"], c["p_c"], c["v_c_m"], c["c_c"], guidage_sys=gs)
        loads = r["etat_final_i"]["loads"]
        results.append({"success": r["intercept"], "miss": r["distance_min_m"], "range": c["r_init"], "fail_mode": classify_failure(r), "max_g": loads["max_g"], "max_q": loads["max_q"], "max_temp": loads["max_temp"]})
    return results

if __name__ == "__main__":
    n = 50
    for m in ["PN", "APN"]:
        res = run_monte_carlo(n, m)
        print(f"Mode {m}: P(int) = {sum(1 for r in res if r['success'])/n*100}%")
