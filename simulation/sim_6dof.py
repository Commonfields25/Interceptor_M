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
_CX_BASE     = C.COEFF_TRAITEE_Cx_BASE
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
    return _CX_BASE * 1.2   # transonic bump (conservative)


def get_thrust(t_s, energy_used_j):
    """ Return DASH thrust while battery has energy remaining. """
    if energy_used_j < _BATT_J:
        return _POUSSEE_DASH
    return 0.0


def etat_initial(position_m, vitesse_m_s, cap_rad=None):
    """ Build initial state dict. cap_rad is ignored (kept for API compat). """
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
    commands = (a_lat, a_vert) — lateral and vertical accelerations in m/s².
    Returns (d_pos/dt, d_vel/dt, power_W).
    """
    pos  = etat["position"]
    vel  = etat["vitesse"]
    t    = etat["temps"]
    mass = etat["masse"]
    energy = etat["energy_used"]

    v_mod = np.linalg.norm(vel)
    if v_mod < 0.1:
        return np.zeros(3), np.zeros(3), 0.0

    # Unit-tangent
    ut = vel / v_mod
    if abs(ut[2]) > 0.9999:
        un = np.array([0.0, 1.0, 0.0])
    else:
        un = np.array([0.0, 0.0, 1.0]) - ut[2] * ut
    un /= np.linalg.norm(un)
    ub = np.cross(un, ut)

    # Atmospheric conditions
    T_amb, P_atm, rho, a_son = isa_atmosphere(pos[2])
    mach = v_mod / a_son
    cx = get_drag_coeff(mach)

    # Aerodynamic forces
    q_dyn  = 0.5 * rho * v_mod ** 2
    t_stag = T_amb * (1.0 + 0.2 * mach ** 2)
    (void) = t_stag          # reserved for temperature effects

    # Propulsion
    thrust = get_thrust(t, energy)
    drag   = q_dyn * _S_REF * cx

    # Acceleration command (lateral/normal) in body frame
    a_lat, a_vert = commands
    accel = thrust * ut / mass
    accel += (a_lat * ub + a_vert * un) / mass
    accel[2] -= _G0           # gravity along -z (altitude axis)

    # Power
    power_w = (thrust * v_mod) / _EFF
    return vel, accel, power_w


def integrer_rk4(etat, commands, dt):
    """
    P2 upgrade: Runge-Kutta 4th order integrator.
    Replaces the previous first-order Euler step.
    """
    k1_pos, k1_vel, k1_pow = derivees(etat, commands)

    etat_k2 = {
        "position"   : etat["position"]   + k1_pos * (dt / 2.0),
        "vitesse"    : etat["vitesse"]    + k1_vel * (dt / 2.0),
        "masse"      : etat["masse"],
        "temps"      : etat["temps"]      + dt / 2.0,
        "energy_used": etat["energy_used"] + k1_pow * (dt / 2.0),
    }
    k2_pos, k2_vel, k2_pow = derivees(etat_k2, commands)

    etat_k3 = {
        "position"   : etat["position"]   + k2_pos * (dt / 2.0),
        "vitesse"    : etat["vitesse"]    + k2_vel * (dt / 2.0),
        "masse"      : etat["masse"],
        "temps"      : etat["temps"]      + dt / 2.0,
        "energy_used": etat["energy_used"] + k2_pow * (dt / 2.0),
    }
    k3_pos, k3_vel, k3_pow = derivees(etat_k3, commands)

    etat_k4 = {
        "position"   : etat["position"]   + k3_pos * dt,
        "vitesse"    : etat["vitesse"]    + k3_vel * dt,
        "masse"      : etat["masse"],
        "temps"      : etat["temps"]      + dt,
        "energy_used": etat["energy_used"] + k3_pow * dt,
    }
    k4_pos, k4_vel, k4_pow = derivees(etat_k4, commands)

    # RK4 state update
    etat["position"]    = etat["position"]   + (k1_pos + 2.0*k2_pos + 2.0*k3_pos + k4_pos) * (dt / 6.0)
    etat["vitesse"]     = etat["vitesse"]    + (k1_vel + 2.0*k2_vel + 2.0*k3_vel + k4_vel) * (dt / 6.0)
    etat["energy_used"] += (k1_pow + 2.0*k2_pow + 2.0*k3_pow + k4_pow) * (dt / 6.0)
    etat["temps"]      += dt
    return etat


def integrer(etat, commands, dt):
    """ Alias: routes to RK4 (backward-compat API). """
    return integrer_rk4(etat, commands, dt)


# ── manoeuvre helpers (unchanged logic) ──────────────────────────────────────

def manoeuvre_rectiligne(etat_c, dt):
    """ Zero-correction maneuver — straight flight. """
    pos, vel = etat_c["position"], etat_c["vitesse"]
    pos += vel * dt
    etat_c["position"] = pos
    return etat_c


def manoeuvre_virage_constant(etat_c, dt, accel_g=5.0):
    """ Constant-rate turn at given G-load. """
    pos, vel = etat_c["position"], etat_c["vitesse"]
    v_h = math.sqrt(vel[0]**2 + vel[1]**2)
    if v_h < 0.1:
        pos += vel * dt
        etat_c["position"] = pos
        etat_c["temps"]    = etat_c.get("temps", 0.0) + dt
        return etat_c
    omega   = (accel_g * _G0) / v_h
    d_theta = omega * dt
    c, s    = math.cos(d_theta), math.sin(d_theta)
    vel[0], vel[1] = vel[0]*c - vel[1]*s, vel[0]*s + vel[1]*c
    pos += vel * dt
    etat_c["position"] = pos
    etat_c["vitesse"]  = vel
    etat_c["temps"]    = etat_c.get("temps", 0.0) + dt
    return etat_c


def simuler(position0,
            vitesse0,
            cap_initial_rad,
            guidage_sys=None,
            keep_traj=False):
    """
    Main 6-DOF simulation loop.
    Now uses RK4 for integration and dt = 1 ms (P2).
    """
    etat_i  = etat_initial(position0, vitesse0, cap_initial_rad)
    etat_c  = dict(etat_i)           # current trajectory state
    traj    = []
    temps   = 0.0
    dist_min_sq = float("inf")
    lost_seeker = False
    intercept   = False

    while temps < _DUREE_MAX:
        pos = etat_i["position"]
        vel = etat_i["vitesse"]
        dist_sq = (pos[0]**2 + pos[1]**2 + pos[2]**2)
        dist     = math.sqrt(dist_sq)

        if dist_sq < dist_min_sq:
            dist_min_sq = dist_sq
        if dist_sq < _SEUIL_SQ:
            intercept = True
            break

        # Look-angle check against target at origin
        if np.linalg.norm(vel) > 0.1 and dist > 0.1:
            look_angle = math.acos(min(np.dot(-vel, pos) / (np.linalg.norm(vel)*dist), 1.0))
            if look_angle > _FOR_LIMIT:
                lost_seeker = True
                break

        commands = (0.0, 0.0)
        if guidage_sys is not None:
            cmd = guidage_sys(etat_i, pos, vel, temps)
            if cmd is not None:
                cmd_lat, cmd_vert = cmd
                cmd_norm = math.sqrt(cmd_lat**2 + cmd_vert**2)
                if cmd_norm > _ACCEL_MAX:
                    factor = _ACCEL_MAX / cmd_norm
                    cmd_lat  *= factor
                    cmd_vert *= factor
                commands = (cmd_lat, cmd_vert)

        integrer_rk4(etat_i, commands, _DT)
        etat_c = manoeuvre_rectiligne(etat_c, _DT)
        temps += _DT
        if etat_i["position"][2] < -10.0:
            break
        if keep_traj:
            traj.append(dict(etat_i))

    return {
        "intercept"    : intercept,
        "lost_seeker"  : lost_seeker,
        "temps_total"  : temps,
        "dist_min"      : math.sqrt(dist_min_sq),
        "trajectoire"   : traj,
    }


if __name__ == "__main__":
    # Quick smoke-test: vertical launch
    pos0 = [0.0, 0.0, 0.0]
    vel0 = [0.0, 0.0, 70.0]
    res  = simuler(pos0, vel0, 0.0)
    print("Smoke-test — intercept:", res["intercept"],
          "| temps:", round(res["temps_total"], 3),
          "| dist_min:", round(res["dist_min"], 2))
