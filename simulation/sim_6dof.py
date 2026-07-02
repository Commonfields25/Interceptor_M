"""
simulation/sim_6dof.py
======================
Simulateur 6-DOF simplifié pour l'intercepteur DD-400.
Inclut le modèle d'atmosphère standard (ISA), la dynamique de vol, la poussée, et le guidage 3D.
Version 1.2.0 - Modèle à masse constante (Electric Dash).
"""

import math
import numpy as np
from . import constants as C

# ------------------------------------------------------------------
# Paramètres locaux (mises en cache pour performance)
# ------------------------------------------------------------------
_M0          = C.MASSE_INTERCEPTOR_KG
_S_REF       = C.SURFACE_REF_M2
_CX_BASE     = C.COEFF_TRAITEE_Cx_BASE
_CL_ALPHA    = C.COEFF_PORTANCE_CL_ALPHA
_G0          = C.G0
_DUREE_MAX   = C.DUREE_MAX_S
_DT          = C.PAS_DE_TEMPS_S
_SEUIL_SQ    = C.RL_INTERCEPT_RADIUS_M ** 2
_ACCEL_MAX   = C.ACCELERATION_LATERALE_MAX_M_S2
_FOR_LIMIT   = math.radians(60.0)

# ISA Constants
_T0 = C.T0_ISA
_P0 = C.P0_ISA
_L  = C.L_ISA
_R  = C.R_AIR
_RHO0 = C.RHO0_ISA

# Propulsion Constants
_POUSSEE_MAX = C.POUSSEE_MAX_N
_DUREE_COMB  = C.DUREE_COMBUSTION_S

# =============================================================================
# MODÈLE ATMOSPHÉRIQUE (ISA)
# =============================================================================
def isa_atmosphere(altitude_m):
    h = min(max(altitude_m, 0.0), 11000.0)
    T = _T0 - _L * h
    P = _P0 * (T / _T0)**(_G0 / (_R * _L))
    rho = P / (_R * T)
    return T, P, rho

def densite(altitude_m):
    _, _, rho = isa_atmosphere(altitude_m)
    return rho

def get_thrust(t_s):
    if t_s < _DUREE_COMB:
        return _POUSSEE_MAX
    return 0.0

# =============================================================================
# DYNAMIQUE DE VOL
# =============================================================================
def etat_initial(pos_m, vel_m_s, cap_rad):
    vx = vel_m_s * math.cos(cap_rad)
    vy = vel_m_s * math.sin(cap_rad)
    return {
        "position": np.array(pos_m, dtype=float),
        "vitesse" : np.array([vx, vy, 0.0], dtype=float),
        "t"       : 0.0,
        "masse"   : float(_M0),
    }

def integrer(etat, accel_cmd, dt):
    pos = etat["position"]
    vel = etat["vitesse"]
    t   = etat["t"]
    masse = etat["masse"]

    v_mod = np.linalg.norm(vel)
    if v_mod < 1e-3:
        ut = np.array([1.0, 0.0, 0.0])
    else:
        ut = vel / v_mod

    # Vecteurs unitaires du repère Frenet
    k = np.array([0, 0, 1])
    ub = np.cross(ut, k)
    ub_norm = np.linalg.norm(ub)
    if ub_norm < 1e-6:
        # Singularity at vertical flight - assume arbitrary horizontal
        ub = np.array([0, 1, 0])
    else:
        ub /= ub_norm
    # un est orthogonal à ut et ub. Si ut horizontal, ub horizontal, un est vertical (UP).
    un = np.cross(ut, ub)

    # Atmosphère
    rho = densite(pos[2])

    # Traînée
    drag = 0.5 * rho * v_mod**2 * _S_REF * _CX_BASE

    # Poussée
    thrust = get_thrust(t)

    # Accélérations guidage
    a_lat  = accel_cmd[0]
    a_vert = accel_cmd[1]

    # Gravité
    g_vec = np.array([0, 0, -_G0])

    # Équation du mouvement
    # ut: forward, ub: right, un: up
    a_tot = ((thrust - drag) / masse) * ut + a_lat * ub + a_vert * un + g_vec

    # Mise à jour Euler
    etat["vitesse"]  += a_tot * dt
    etat["position"] += etat["vitesse"] * dt
    etat["t"]        += dt

# =============================================================================
# MANOEUVRES CIBLES
# =============================================================================
def manoeuvre_rectiligne(etat_c, dt):
    etat_c["position"] += etat_c["vitesse"] * dt
    return etat_c

def manoeuvre_virage_constant(etat_c, dt, g_load=3.0):
    v_vec = etat_c["vitesse"]
    v_mod = np.linalg.norm(v_vec)
    if v_mod < 0.1: return manoeuvre_rectiligne(etat_c, dt)

    radius = v_mod**2 / (g_load * _G0)
    omega  = v_mod / radius

    angle = omega * dt
    cos_a, sin_a = math.cos(angle), math.sin(angle)

    vx, vy = v_vec[0], v_vec[1]
    etat_c["vitesse"][0] = vx * cos_a - vy * sin_a
    etat_c["vitesse"][1] = vx * sin_a + vy * cos_a
    etat_c["position"]  += etat_c["vitesse"] * dt
    return etat_c

# =============================================================================
# SIMULATION ENGAGEMENT
# =============================================================================
def simulate_engagement(pos_init_m, vel_init_m_s, cap_init_rad,
                        pos_cible_m,   vel_cible_m_s, cap_cible_rad,
                        guidage_sys=None,
                        manoeuvre_c_fn=manoeuvre_rectiligne,
                        keep_traj=False):
    etat_i = etat_initial(pos_init_m, vel_init_m_s, cap_init_rad)

    vcx = vel_cible_m_s * math.cos(cap_cible_rad)
    vcy = vel_cible_m_s * math.sin(cap_cible_rad)
    etat_c = {
        "position": np.array(pos_cible_m, dtype=float),
        "vitesse": np.array([vcx, vcy, 0.0], dtype=float)
    }

    temps = 0.0
    traj  = []
    dist_min_sq = float("inf")
    intercept = False
    failure_mode = "Success"

    while temps < _DUREE_MAX:
        if keep_traj and (len(traj) == 0 or (temps - traj[-1]["t"]) >= 0.05):
            v_mod = np.linalg.norm(etat_i["vitesse"])
            traj.append({
                "t": round(temps, 3),
                "x": round(etat_i["position"][0], 1),
                "y": round(etat_i["position"][1], 1),
                "z": round(etat_i["position"][2], 1),
                "cx": round(etat_c["position"][0], 1),
                "cy": round(etat_c["position"][1], 1),
                "v": round(v_mod, 1)
            })

        rel_pos = etat_c["position"] - etat_i["position"]
        dist_sq = np.sum(rel_pos**2)
        if dist_sq < dist_min_sq: dist_min_sq = dist_sq
        if dist_sq < _SEUIL_SQ:
            intercept = True
            break

        # FOR check
        dist = math.sqrt(dist_sq)
        los_vec = rel_pos / dist
        v_i = etat_i["vitesse"]
        v_norm = np.linalg.norm(v_i)
        if v_norm > 1.0:
            cos_for = np.dot(v_i/v_norm, los_vec)
            if cos_for < math.cos(_FOR_LIMIT):
                intercept = False
                failure_mode = "Seeker Lost (FOR)"
                break

        commands = (0.0, 0.0)
        if guidage_sys is not None:
            commands = guidage_sys.compute_guidance(etat_i, etat_c)
            cmd_norm = math.sqrt(commands[0]**2 + commands[1]**2)
            if cmd_norm > _ACCEL_MAX:
                factor = _ACCEL_MAX / cmd_norm
                commands = (commands[0] * factor, commands[1] * factor)

        integrer(etat_i, commands, _DT)
        etat_c = manoeuvre_c_fn(etat_c, _DT)
        temps += _DT

        if etat_i["position"][2] < -5.0:
            failure_mode = "Ground Collision"
            break

    if not intercept and failure_mode == "Success":
        failure_mode = "Kinetic Exhaustion"

    return {
        "intercept": intercept,
        "temps_s": round(temps, 3),
        "trajectoire": traj,
        "distance_min_m": round(math.sqrt(dist_min_sq), 2),
        "failure_mode": failure_mode
    }

if __name__ == "__main__":
    # Smoke test
    res = simulate_engagement([0,0,100], 100, 0, [1000,0,100], 50, math.pi)
    print(f"Intercept: {res['intercept']} | Dist Min: {res['distance_min_m']}m | Mode: {res['failure_mode']}")
