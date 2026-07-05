import math
import numpy as np
from . import constants as C
_M0, _S_REF, _CX_BASE, _G0, _DUREE_MAX, _DT, _SEUIL_SQ, _ACCEL_MAX, _FOR_LIMIT = C.MASSE_INTERCEPTOR_KG, C.SURFACE_REF_M2, C.COEFF_TRAITEE_Cx_BASE, C.G0, C.DUREE_MAX_S, C.PAS_DE_TEMPS_S, C.RL_INTERCEPT_RADIUS_M ** 2, C.ACCELERATION_LATERALE_MAX_M_S2, math.radians(60.0)
_T0, _P0, _L, _R, _GAMMA = C.T0_ISA, C.P0_ISA, C.L_ISA, C.R_AIR, C.GAMMA_AIR
_POUSSEE_DASH, _BATT_J, _EFF = C.POUSSEE_DASH_N, C.BATTERY_CAPACITY_J, C.ENERGY_EFFICIENCY

def isa_atmosphere(altitude_m):
    h = min(max(altitude_m, 0.0), 11000.0)
    T = _T0 - _L * h
    P = _P0 * (T / _T0)**(_G0 / (_R * _L))
    rho, a = P / (_R * T), math.sqrt(_GAMMA * _R * T)
    return T, P, rho, a

def get_drag_coeff(mach):
    if mach < 0.8: return _CX_BASE
    elif mach < 1.2: return _CX_BASE + (mach - 0.8) * (2.0 * _CX_BASE / 0.4)
    return (2.5 * _CX_BASE) / math.sqrt(mach**2 - 1.0)

def get_thrust(t_s, energy_used_j): return _POUSSEE_DASH if energy_used_j < _BATT_J else 0.0

def etat_initial(position_m, vitesse_m_s, cap_rad):
    vx, vy = vitesse_m_s * math.cos(cap_rad), vitesse_m_s * math.sin(cap_rad)
    return {"position": np.array(position_m, dtype=float), "vitesse": np.array([vx, vy, 0.0], dtype=float), "masse": float(_M0), "temps": 0.0, "energy_used": 0.0, "loads": {"max_g": 0.0, "max_q": 0.0, "max_temp": 0.0}}

def derivees(etat, commands):
    pos, vel, t, energy = etat["position"], etat["vitesse"], etat["temps"], etat["energy_used"]
    v_mod = np.linalg.norm(vel)
    if v_mod < 0.1: return np.zeros(3), np.zeros(3), 0.0
    ut = vel / v_mod
    un = np.array([0, 0, 1.0]) - ut[2] * ut
    un = un / np.linalg.norm(un) if np.linalg.norm(un) > 1e-6 else np.array([1, 0, 0])
    ub = np.cross(un, ut)
    T_amb, _, rho, a_son = isa_atmosphere(pos[2])
    mach, q_dyn = v_mod / a_son, 0.5 * rho * v_mod**2
    t_stag, thrust, drag = T_amb * (1.0 + 0.2 * mach**2), get_thrust(t, energy), q_dyn * _S_REF * get_drag_coeff(mach)
    a_lat, a_vert = commands
    accel = ((thrust - drag) / _M0) * ut + a_lat * ub + a_vert * un
    accel[2] -= _G0
    g_load = np.linalg.norm(accel + np.array([0, 0, _G0])) / _G0
    etat["loads"]["max_g"], etat["loads"]["max_q"], etat["loads"]["max_temp"] = max(etat["loads"]["max_g"], g_load), max(etat["loads"]["max_q"], q_dyn), max(etat["loads"]["max_temp"], t_stag)
    return vel, accel, (thrust * v_mod) / _EFF

def integrer(etat, commands, dt):
    v, a, p_w = derivees(etat, commands)
    etat["position"], etat["vitesse"], etat["energy_used"], etat["temps"] = etat["position"] + v * dt, etat["vitesse"] + a * dt, etat["energy_used"] + p_w * dt, etat["temps"] + dt
    return etat

def simulate_engagement(pos_i, vel_i, cap_i, pos_c_init, vel_c_mod, cap_c, guidage_sys=None, manoeuvre_c_fn=lambda e, dt: e, keep_traj=False):
    etat_i = etat_initial(pos_i, vel_i, cap_i)
    vcx, vcy = vel_c_mod * math.cos(cap_c), vel_c_mod * math.sin(cap_c)
    etat_c = {"position": np.array(pos_c_init, dtype=float), "vitesse": np.array([vcx, vcy, 0.0], dtype=float), "temps": 0.0}
    temps, dist_min_sq, intercept, lost_seeker = 0.0, float("inf"), False, False
    while temps < _DUREE_MAX:
        v_i, rel_pos = etat_i["vitesse"], etat_c["position"] - etat_i["position"]
        v_mod, dist_sq = np.linalg.norm(v_i), np.sum(rel_pos**2)
        dist = math.sqrt(dist_sq)
        if dist_sq < dist_min_sq: dist_min_sq = dist_sq
        if dist_sq < _SEUIL_SQ: intercept = True; break
        if v_mod > 0.1 and dist > 0.1:
            if math.acos(np.clip(np.dot(v_i, rel_pos) / (v_mod * dist), -1.0, 1.0)) > _FOR_LIMIT: lost_seeker = True; break
        cmd = guidage_sys.compute_guidance(etat_i, etat_c) if guidage_sys else (0, 0)
        integrer(etat_i, cmd, _DT); etat_c["position"] += etat_c["vitesse"] * _DT; temps += _DT
        if etat_i["position"][2] < -10.0: break
    return {"intercept": intercept, "temps_s": round(temps, 3), "distance_min_m": round(math.sqrt(dist_min_sq), 2), "etat_final_i": etat_i, "lost_seeker": lost_seeker}
