"""
simulation/sim_6dof.py
======================
Simulateur 6-DOF simplifié pour l'intercepteur DD-400.
Amélioration : Boost-Sustain propulsion profile, Seeker FOR monitoring.
"""

import math
import numpy as np
from . import constants as C

# ------------------------------------------------------------------
# Paramètres locaux
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
_FOR_LIMIT   = math.radians(60.0) # Field of Regard (±60 deg)

# ISA Constants
_T0 = C.T0_ISA
_P0 = C.P0_ISA
_L  = C.L_ISA
_R  = C.R_AIR
_GAMMA = C.GAMMA_AIR

# Propulsion Constants (Boost-Sustain)
_DUREE_BOOST   = 2.0
_POUSSEE_BOOST = 60.0
_DUREE_SUSTAIN = 8.0
_POUSSEE_SUSTAIN = 20.0
_ISP           = C.ISP_S

def isa_atmosphere(altitude_m):
    h = min(max(altitude_m, 0.0), 11000.0)
    T = _T0 - _L * h
    P = _P0 * (T / _T0)**(_G0 / (_R * _L))
    rho = P / (_R * T)
    a = math.sqrt(_GAMMA * _R * T)
    return T, P, rho, a

def densite(altitude_m):
    _, _, rho, _ = isa_atmosphere(altitude_m)
    return rho

def get_drag_coeff(mach):
    if mach < 0.8: return _CX_BASE
    elif mach < 1.2: return _CX_BASE + (mach - 0.8) * (2.0 * _CX_BASE / 0.4)
    else: return (2.5 * _CX_BASE) / math.sqrt(mach**2 - 1.0)

def get_thrust(t_s):
    if t_s <= _DUREE_BOOST: return _POUSSEE_BOOST
    elif t_s <= (_DUREE_BOOST + _DUREE_SUSTAIN): return _POUSSEE_SUSTAIN
    return 0.0

def get_mass_flow(t_s):
    thrust = get_thrust(t_s)
    return thrust / (_ISP * _G0) if _ISP > 0 else 0.0

def etat_initial(position_m, vitesse_m_s, cap_rad):
    vx = vitesse_m_s * math.cos(cap_rad)
    vy = vitesse_m_s * math.sin(cap_rad)
    vz = 0.0
    return {
        "position": np.array(position_m, dtype=float),
        "vitesse" : np.array([vx, vy, vz], dtype=float),
        "masse"   : float(_M0),
        "temps"   : 0.0
    }

def derivees(etat, commands):
    pos, vel, masse, t = etat["position"], etat["vitesse"], etat["masse"], etat["temps"]
    v_mod = np.linalg.norm(vel)
    if v_mod < 0.1: return np.zeros(3), np.zeros(3), 0.0
    ut = vel / v_mod
    if abs(ut[2]) > 0.999: un = np.array([1.0, 0.0, 0.0])
    else:
        un = np.array([0.0, 0.0, 1.0]) - ut[2] * ut
        un /= np.linalg.norm(un)
    ub = np.cross(un, ut)
    T, P, rho, a_son = isa_atmosphere(pos[2])
    mach = v_mod / a_son
    cx = get_drag_coeff(mach)
    thrust = get_thrust(t)
    drag = 0.5 * rho * v_mod**2 * _S_REF * cx
    a_lat, a_vert = commands
    accel = ((thrust - drag) / masse) * ut + a_lat * ub + a_vert * un
    accel[2] -= _G0
    mdot = -get_mass_flow(t)
    return vel, accel, mdot

def integrer(etat, commands, dt):
    v, a, mdot = derivees(etat, commands)
    new_v = etat["vitesse"] + a * dt
    etat["position"] += 0.5 * (etat["vitesse"] + new_v) * dt
    etat["vitesse"] = new_v
    etat["masse"] += mdot * dt
    etat["temps"] += dt
    return etat

def manoeuvre_rectiligne(etat_c, dt):
    etat_c["position"] += np.array(etat_c["vitesse"]) * dt
    return etat_c

def manoeuvre_virage_constant(etat_c, dt, accel_g=5.0):
    pos, vel = etat_c["position"], etat_c["vitesse"]
    v_h = math.sqrt(vel[0]**2 + vel[1]**2)
    if v_h < 0.1:
        pos += vel * dt
        return etat_c
    omega = (accel_g * _G0) / v_h
    d_theta = omega * dt
    c, s = math.cos(d_theta), math.sin(d_theta)
    vx, vy = vel[0], vel[1]
    vel[0] = vx * c - vy * s
    vel[1] = vx * s + vy * c
    pos += vel * dt
    return etat_c

def manoeuvre_weaving(etat_c, dt, accel_g=5.0, freq_hz=0.5):
    t = etat_c.get("temps", 0.0)
    pos, vel = etat_c["position"], etat_c["vitesse"]
    v_h = math.sqrt(vel[0]**2 + vel[1]**2)
    if v_h < 0.1:
        pos += vel * dt
        etat_c["temps"] = t + dt
        return etat_c
    accel_lat = accel_g * _G0 * math.sin(2.0 * math.pi * freq_hz * t)
    omega = accel_lat / v_h
    d_theta = omega * dt
    c, s = math.cos(d_theta), math.sin(d_theta)
    vx, vy = vel[0], vel[1]
    vel[0] = vx * c - vy * s
    vel[1] = vx * s + vy * c
    pos += vel * dt
    etat_c["temps"] = t + dt
    return etat_c

def simulate_engagement(pos_init_m, vel_init_m_s, cap_init_rad,
                        pos_cible_m,   vel_cible_m_s, cap_cible_rad,
                        guidage_sys=None,
                        manoeuvre_c_fn=manoeuvre_rectiligne,
                        keep_traj=False):
    etat_i = etat_initial(pos_init_m, vel_init_m_s, cap_init_rad)
    vcx, vcy = vel_cible_m_s * math.cos(cap_cible_rad), vel_cible_m_s * math.sin(cap_cible_rad)
    etat_c = {"position": np.array(pos_cible_m, dtype=float), "vitesse": np.array([vcx, vcy, 0.0], dtype=float), "temps": 0.0}
    temps, traj, dist_min_sq, intercept = 0.0, [], float("inf"), False
    lost_seeker = False

    while temps < _DUREE_MAX:
        v_i = etat_i["vitesse"]
        v_mod = np.linalg.norm(v_i)
        rel_pos = etat_c["position"] - etat_i["position"]
        dist_sq = np.sum(rel_pos**2)
        dist = math.sqrt(dist_sq)

        if keep_traj and (len(traj) == 0 or (temps - traj[-1]["t"]) >= 0.05):
            traj.append({"t": round(temps, 3), "x": round(etat_i["position"][0], 1), "y": round(etat_i["position"][1], 1), "z": round(etat_i["position"][2], 1), "cx": round(etat_c["position"][0], 1), "cy": round(etat_c["position"][1], 1), "v": round(v_mod, 1)})

        if dist_sq < dist_min_sq: dist_min_sq = dist_sq
        if dist_sq < _SEUIL_SQ:
            intercept = True
            break

        # Seeker check
        if v_mod > 0.1 and dist > 0.1:
            look_angle = math.acos(np.dot(v_i, rel_pos) / (v_mod * dist))
            if look_angle > _FOR_LIMIT:
                lost_seeker = True
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
        if etat_i["position"][2] < -10.0: break

    return {"intercept": intercept, "temps_s": round(temps, 3), "trajectoire": traj, "distance_min_m": round(math.sqrt(dist_min_sq), 2), "etat_final_i": etat_i, "lost_seeker": lost_seeker}

if __name__ == "__main__":
    pass
