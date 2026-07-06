"""
simulation/sim_6dof.py
======================
Simulateur 6-DOF pour l'intercepteur DD-400.
Modèle : Lancement pneumatique + Dash électrique.
P2 upgrade: Euler → RK4  |  Δt : 5 ms → 1 ms
"""

import math
import numpy as np
from . import constants as C

# Paramètres locaux
_M0          = C.MASSE_INTERCEPTOR_KG
_S_REF       = C.SURFACE_REF_M2
_CX_BASE     = getattr(C, "COEFF_TRAITEE_Cx_BASE", 0.35)
_CL_ALPHA    = C.COEFF_PORTANCE_CL_ALPHA
_G0          = C.G0
_DUREE_MAX   = C.DUREE_MAX_S
_DT          = C.PAS_DE_TEMPS_S        # maintenant 0.001 s (P2)
_SEUIL_SQ    = C.RL_INTERCEPT_RADIUS_M ** 2
_ACCEL_MAX   = C.ACCELERATION_LATERALE_MAX_M_S2
_FOR_LIMIT   = math.radians(60.0)

# Propulsion Constants (Electric)
_POUSSEE_DASH = C.POUSSEE_DASH_N
_BATT_J       = C.BATTERY_CAPACITY_J
_EFF          = C.ENERGY_EFFICIENCY

def isa_atmosphere(altitude_m):
    """ ISA atmospheric model (troposphere only, up to 11 km). """
    h  = min(max(altitude_m, 0.0), 11000.0)
    _T0_isa = 288.15;  _L = 0.0065;  _P0 = 101325.0
    _R = 287.05;       _gamma = 1.4
    T = _T0_isa - _L * h
    P = _P0 * (T / _T0_isa) ** (_G0 / (_R * _L))
    rho = P / (_R * T)
    a   = math.sqrt(_gamma * _R * T)
    return T, P, rho, a

def get_drag_coeff(mach):
    """ Drag coefficient: base value below Mach 0.8. """
    if mach < 0.8:
        return _CX_BASE
    return _CX_BASE + 0.5 * (mach - 0.8)**2

def get_thrust(t_s, energy_used_j):
    """ Return DASH thrust while battery has energy remaining. """
    if energy_used_j < _BATT_J:
        return _POUSSEE_DASH
    return 0.0

def etat_initial(position_m, vitesse_m_s, cap_rad=None):
    """ Build initial state dict. """
    return {
        "position"   : np.array(position_m, dtype=float),
        "vitesse"    : np.array(vitesse_m_s, dtype=float),
        "masse"      : float(_M0),
        "temps"      : 0.0,
        "energy_used": 0.0,
    }

def derivees(etat, commands):
    """
    Compute state derivatives for 6-DOF interceptor.
    Optimized for performance: replaced np.cross and redundant np.linalg.norm.
    """
    pos  = etat["position"]
    vel  = etat["vitesse"]
    t    = etat["temps"]
    mass = etat["masse"]
    energy = etat["energy_used"]

    v0, v1, v2 = vel
    v_sq = v0*v0 + v1*v1 + v2*v2
    v_mod = math.sqrt(v_sq)

    if v_mod < 0.1:
        return np.zeros(3), np.zeros(3), 0.0

    # Unit-tangent (ut)
    ut0, ut1, ut2 = v0/v_mod, v1/v_mod, v2/v_mod

    # Normal vector un
    if abs(ut2) > 0.9999:
        un0, un1, un2 = 0.0, 1.0, 0.0
    else:
        # Projection of Z onto normal plane
        un0, un1, un2 = -ut2*ut0, -ut2*ut1, 1.0 - ut2*ut2
        un_mod = math.sqrt(un0*un0 + un1*un1 + un2*un2)
        un0 /= un_mod; un1 /= un_mod; un2 /= un_mod

    # Binormal vector ub = un x ut (Manual cross product)
    ub0 = un1*ut2 - un2*ut1
    ub1 = un2*ut0 - un0*ut2
    ub2 = un0*ut1 - un1*ut0

    # Atmospheric conditions
    T_amb, P_atm, rho, a_son = isa_atmosphere(pos[2])
    mach = v_mod / a_son
    cx = get_drag_coeff(mach)

    # Aerodynamic forces
    drag = (0.5 * rho * v_sq) * _S_REF * cx
    thrust = get_thrust(t, energy)

    # Acceleration command
    a_lat, a_vert = commands

    # Combined force coefficients
    f_tangential = (thrust - drag) / mass
    f_lat = a_lat / mass
    f_vert = a_vert / mass

    accel0 = f_tangential * ut0 + f_lat * ub0 + f_vert * un0
    accel1 = f_tangential * ut1 + f_lat * ub1 + f_vert * un1
    accel2 = f_tangential * ut2 + f_lat * ub2 + f_vert * un2 - _G0

    return vel, np.array([accel0, accel1, accel2]), (thrust * v_mod) / _EFF

def integrer_rk4(etat, commands, dt):
    # k1
    k1_pos, k1_vel, k1_pow = derivees(etat, commands)

    # k2
    dt2 = dt * 0.5
    etat_k2 = {
        "position"   : etat["position"]   + k1_pos * dt2,
        "vitesse"    : etat["vitesse"]    + k1_vel * dt2,
        "masse"      : etat["masse"],
        "temps"      : etat["temps"]      + dt2,
        "energy_used": etat["energy_used"] + k1_pow * dt2,
    }
    k2_pos, k2_vel, k2_pow = derivees(etat_k2, commands)

    # k3
    etat_k3 = {
        "position"   : etat["position"]   + k2_pos * dt2,
        "vitesse"    : etat["vitesse"]    + k2_vel * dt2,
        "masse"      : etat["masse"],
        "temps"      : etat["temps"]      + dt2,
        "energy_used": etat["energy_used"] + k2_pow * dt2,
    }
    k3_pos, k3_vel, k3_pow = derivees(etat_k3, commands)

    # k4
    etat_k4 = {
        "position"   : etat["position"]   + k3_pos * dt,
        "vitesse"    : etat["vitesse"]    + k3_vel * dt,
        "masse"      : etat["masse"],
        "temps"      : etat["temps"]      + dt,
        "energy_used": etat["energy_used"] + k3_pow * dt,
    }
    k4_pos, k4_vel, k4_pow = derivees(etat_k4, commands)

    # Final integration
    dt6 = dt / 6.0
    etat["position"]    += (k1_pos + 2.0*k2_pos + 2.0*k3_pos + k4_pos) * dt6
    etat["vitesse"]     += (k1_vel + 2.0*k2_vel + 2.0*k3_vel + k4_vel) * dt6
    etat["energy_used"] += (k1_pow + 2.0*k2_pow + 2.0*k3_pow + k4_pow) * dt6
    etat["temps"]       += dt
    return etat

def manoeuvre_rectiligne(etat_c, dt):
    """ Zero-correction maneuver — straight flight. """
    pos, vel = etat_c["position"], etat_c["vitesse"]
    pos[0] += vel[0] * dt
    pos[1] += vel[1] * dt
    pos[2] += vel[2] * dt
    return etat_c

def manoeuvre_virage_constant(etat_c, dt, accel_g=5.0):
    """ Constant-rate turn at given G-load. """
    pos, vel = etat_c["position"], etat_c["vitesse"]
    v0, v1 = vel[0], vel[1]
    v_h = math.sqrt(v0*v0 + v1*v1)
    if v_h < 0.1:
        pos[0] += vel[0] * dt
        pos[1] += vel[1] * dt
        pos[2] += vel[2] * dt
        return etat_c
    omega   = (accel_g * _G0) / v_h
    d_theta = omega * dt
    c, s    = math.cos(d_theta), math.sin(d_theta)
    vel[0] = v0*c - v1*s
    vel[1] = v0*s + v1*c
    pos[0] += vel[0] * dt
    pos[1] += vel[1] * dt
    pos[2] += vel[2] * dt
    return etat_c

def simulate_engagement(pos_init_m, vel_init_m_s, cap_init_rad,
                        pos_cible_m, vel_cible_m_s, cap_cible_rad,
                        guidage_sys=None, manoeuvre_c_fn=None, keep_traj=False):
    """
    Simule un engagement complet. Optimized state updates.
    """
    cos_cap, sin_cap = math.cos(cap_init_rad), math.sin(cap_init_rad)
    v_init_vec = np.array([vel_init_m_s * cos_cap, vel_init_m_s * sin_cap, 0.0])
    etat_i = etat_initial(pos_init_m, v_init_vec)

    cos_tgt, sin_tgt = math.cos(cap_cible_rad), math.sin(cap_cible_rad)
    etat_c = {
        "position": np.array(pos_cible_m, dtype=float),
        "vitesse" : np.array([vel_cible_m_s * cos_tgt, vel_cible_m_s * sin_tgt, 0.0])
    }

    traj = []
    temps = 0.0
    dist_min_sq = float("inf")
    lost_seeker = False
    intercept = False

    while temps < _DUREE_MAX:
        pos_i = etat_i["position"]
        pos_c = etat_c["position"]
        rx, ry, rz = pos_c[0] - pos_i[0], pos_c[1] - pos_i[1], pos_c[2] - pos_i[2]
        dist_sq = rx*rx + ry*ry + rz*rz
        dist = math.sqrt(dist_sq)

        if dist_sq < dist_min_sq:
            dist_min_sq = dist_sq

        if dist < C.RL_INTERCEPT_RADIUS_M:
            intercept = True
            break

        if pos_i[2] < 0.0:
            break

        # Seeker look-angle
        vel_i = etat_i["vitesse"]
        v0, v1, v2 = vel_i
        v_mod = math.sqrt(v0*v0 + v1*v1 + v2*v2)
        if v_mod > 0.1 and dist > 0.1:
            dot_v_r = v0*rx + v1*ry + v2*rz
            look_angle = math.acos(max(min(dot_v_r / (v_mod * dist), 1.0), -1.0))
            if look_angle > _FOR_LIMIT:
                lost_seeker = True
                break

        commands = (0.0, 0.0)
        if guidage_sys is not None:
            cmd = guidage_sys.compute_guidance(etat_i, etat_c)
            if cmd is not None:
                cmd_lat, cmd_vert = cmd
                cmd_norm_sq = cmd_lat*cmd_lat + cmd_vert*cmd_vert
                if cmd_norm_sq > _ACCEL_MAX*_ACCEL_MAX:
                    factor = _ACCEL_MAX / math.sqrt(cmd_norm_sq)
                    cmd_lat  *= factor
                    cmd_vert *= factor
                commands = (cmd_lat, cmd_vert)

        integrer_rk4(etat_i, commands, _DT)
        if manoeuvre_c_fn:
            etat_c = manoeuvre_c_fn(etat_c, _DT)
        else:
            etat_c = manoeuvre_rectiligne(etat_c, _DT)

        temps += _DT
        if keep_traj:
            traj.append({
                "t": temps,
                "pos_i": pos_i.copy(),
                "pos_c": pos_c.copy()
            })

    return {
        "intercept"     : intercept,
        "lost_seeker"   : lost_seeker,
        "temps_total"   : temps,
        "distance_min_m": math.sqrt(dist_min_sq),
        "trajectoire"   : traj,
    }

def simuler(position0, vitesse0, cap_initial_rad, guidage_sys=None, keep_traj=False):
    v_vec = np.array(vitesse0, dtype=float)
    return simulate_engagement(position0, np.linalg.norm(v_vec), cap_initial_rad,
                              [0,0,0], 0, 0, guidage_sys, None, keep_traj)

if __name__ == "__main__":
    pos0 = [0.0, 0.0, 0.0]
    vel0 = [0.0, 0.0, 70.0]
    res  = simuler(pos0, vel0, 0.0)
    print("Smoke-test — intercept:", res["intercept"],
          "| temps:", round(res["temps_total"], 3),
          "| dist_min:", round(res["distance_min_m"], 2))
