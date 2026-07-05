import math, numpy as np
from . import constants as C
_M0, _S_REF, _CX_BASE, _G0, _DUREE_MAX, _DT, _SEUIL_SQ, _ACCEL_MAX, _FOR_LIMIT = C.MASSE_INTERCEPTOR_KG, C.SURFACE_REF_M2, C.COEFF_TRAITEE_Cx_BASE, C.G0, C.DUREE_MAX_S, C.PAS_DE_TEMPS_S, C.RL_INTERCEPT_RADIUS_M ** 2, C.ACCELERATION_LATERALE_MAX_M_S2, math.radians(60.0)
_T0, _P0, _L, _R, _GAMMA, _POUSSEE_DASH, _BATT_J, _EFF = C.T0_ISA, C.P0_ISA, C.L_ISA, C.R_AIR, C.GAMMA_AIR, C.POUSSEE_DASH_N, C.BATTERY_CAPACITY_J, C.ENERGY_EFFICIENCY
def isa_atmo(h_m):
    h = min(max(h_m, 0), 11000.0); T = _T0 - _L * h; P = _P0 * (T / _T0)**(_G0 / (_R * _L))
    return T, P, P / (_R * T), math.sqrt(_GAMMA * _R * T)
def get_drag(mach): return _CX_BASE if mach < 0.8 else _CX_BASE + (mach - 0.8) * (2.0 * _CX_BASE / 0.4) if mach < 1.2 else (2.5 * _CX_BASE) / math.sqrt(mach**2 - 1.0)
def etat_init(p_m, v_ms, c_rad):
    vx, vy = v_ms * math.cos(c_rad), v_ms * math.sin(c_rad)
    return {"position": np.array(p_m, dtype=float), "vitesse": np.array([vx, vy, 0.0], dtype=float), "temps": 0.0, "energy": 0.0, "loads": {"max_g": 0.0, "max_q": 0.0, "max_temp": 0.0}}
def derivees(etat, cmds):
    pos, vel, t, energy = etat["position"], etat["vitesse"], etat["temps"], etat["energy"]
    v_mod = np.linalg.norm(vel)
    if v_mod < 0.1: return np.zeros(3), np.zeros(3), 0.0
    ut = vel / v_mod; un = np.array([0, 0, 1.0]) - ut[2] * ut; un = un / np.linalg.norm(un) if np.linalg.norm(un) > 1e-6 else np.array([1, 0, 0]); ub = np.cross(un, ut)
    T_amb, _, rho, a_son = isa_atmo(pos[2]); mach, q_dyn = v_mod / a_son, 0.5 * rho * v_mod**2
    t_stag, thrust, drag = T_amb * (1.0 + 0.2 * mach**2), _POUSSEE_DASH if energy < _BATT_J else 0.0, q_dyn * _S_REF * get_drag(mach)
    accel = ((thrust - drag) / _M0) * ut + cmds[0] * ub + cmds[1] * un; accel[2] -= _G0
    g_load = np.linalg.norm(accel + np.array([0, 0, _G0])) / _G0
    etat["loads"]["max_g"], etat["loads"]["max_q"], etat["loads"]["max_temp"] = max(etat["loads"]["max_g"], g_load), max(etat["loads"]["max_q"], q_dyn), max(etat["loads"]["max_temp"], t_stag)
    return vel, accel, (thrust * v_mod) / _EFF
def integrer(e, cmds, dt):
    v, a, p_w = derivees(e, cmds); e["position"] += v * dt; e["vitesse"] += a * dt; e["energy"] += p_w * dt; e["temps"] += dt; return e
def simulate_engagement(p_i, v_i, c_i, pc_i, vc_m, c_c, gs=None, manoeuvre_c_fn=lambda e, dt: e):
    e_i = etat_init(p_i, v_i, c_i); vcx, vcy = vc_m * math.cos(c_c), vc_m * math.sin(c_c); e_c = {"position": np.array(pc_i, dtype=float), "vitesse": np.array([vcx, vcy, 0.0], dtype=float)}; temps, dist_min_sq, intercept, lost_seeker = 0.0, float("inf"), False, False
    while temps < _DUREE_MAX:
        v_i, rel_p = e_i["vitesse"], e_c["position"] - e_i["position"]; v_mod, d_sq = np.linalg.norm(v_i), np.sum(rel_p**2); dist = math.sqrt(d_sq)
        if d_sq < dist_min_sq: dist_min_sq = d_sq
        if d_sq < _SEUIL_SQ: intercept = True; break
        if v_mod > 0.1 and dist > 0.1 and math.acos(np.clip(np.dot(v_i, rel_p) / (v_mod * dist), -1.0, 1.0)) > _FOR_LIMIT: lost_seeker = True; break
        cmd = gs.compute_guidance(e_i, e_c) if gs else (0, 0); integrer(e_i, cmd, _DT); e_c["position"] += e_c["vitesse"] * _DT; temps += _DT
        if e_i["position"][2] < -10.0: break
    return {"intercept": intercept, "temps_s": round(temps, 3), "distance_min_m": round(math.sqrt(dist_min_sq), 2), "etat_final_i": e_i, "lost_seeker": lost_seeker}
