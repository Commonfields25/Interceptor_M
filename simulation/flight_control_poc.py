"""
simulation/flight_control_poc.py
===============================
Loi de guidage par navigation proportionnelle (PN).

La commande d'accélération latérale est proportionnelle à la vitesse angulaire
de la ligne de visée (LOS) et à la vitesse relative interceptor–cible :

    a_cmd = N * |V_rel| * omega_LOS

où :
  N      = gain de navigation (C.GAIN_PN)
  V_rel  = vitesse relative interceptor – cible

"""

import math
from . import constants as C

# ------------------------------------------------------------------
# Hot locals — bound once, reused in every proportional_navigation() call
# ------------------------------------------------------------------
_GAIN_PN      = C.GAIN_PN
_ACCEL_MAX    = C.ACCELERATION_LATERALE_MAX_M_S2
_EPS          = 0.1            # minimum LOS norm (m)
_EPS_SQ       = _EPS * _EPS


# =============================================================================
# PROPORTIONAL NAVIGATION (PN)
# =============================================================================
def proportional_navigation(etat_interceptor, etat_cible):
    """
    Calcule la commande d'accélération latérale par la loi PN.

    a_cmd = N * |V_rel| * omega_LOS

    où :
      N      = gain de navigation (C.GAIN_PN)
      V_rel  = vitesse relative interceptor – cible

    Paramètres
    ----------
    etat_interceptor : dict — état de l'interceptor (position, vitesse)
    etat_cible       : dict — état de la cible (position, vitesse)

    Retourne
    --------
    float — accélération latérale commandée en m/s²
    """
    pos_i = etat_interceptor["position"]
    pos_c = etat_cible["position"]
    vel_i = etat_interceptor["vitesse"]
    vel_c = etat_cible.get("vitesse", [0.0, 0.0, 0.0])

    # Ligne de visée (LOS) : interceptor → cible
    los_x = pos_c[0] - pos_i[0]
    los_y = pos_c[1] - pos_i[1]
    los_z = pos_c[2] - pos_i[2]

    los_sq = los_x*los_x + los_y*los_y + los_z*los_z
    if los_sq < _EPS_SQ:
        return 0.0

    norme_los = math.sqrt(los_sq)

    # Vitesse relative
    vrx = vel_i[0] - vel_c[0]
    vry = vel_i[1] - vel_c[1]
    vrz = vel_i[2] - vel_c[2]

    # Cross product LOS × V_rel (component along binormal)
    omega_binorm = (los_x * vry - los_y * vrx)   # z-component only (planar)
    # Note: full 3-D LOS rate would be (LOS × V_rel) / |LOS|²
    # omega = cross(los, v_rel) / los_sq
    omega_x = (los_y * vrz - los_z * vry) / los_sq
    omega_y = (los_z * vrx - los_x * vrz) / los_sq
    omega_z = (los_x * vry - los_y * vrx) / los_sq

    # Module de la vitesse de rotation LOS (squared norm of rate vector)
    omega_LOS = math.sqrt(omega_x*omega_x + omega_y*omega_y + omega_z*omega_z)

    # Vitesse relative module
    v_rel = math.sqrt(vrx*vrx + vry*vry + vrz*vrz)

    # Commande PN : a = N * V_rel * omega_LOS
    a_cmd = _GAIN_PN * v_rel * omega_LOS

    los_unit_x = los_x / norme_los
    los_unit_y = los_y / norme_los
    los_unit_z = los_z / norme_los

    # Sign from z-component of cross(LOS_unit, V_rel_unit) to get turning direction
    v_rel_sq = vrx*vrx + vry*vry + vrz*vrz
    if v_rel_sq > 1e-12:
        v_rel_norm = math.sqrt(v_rel_sq)
        vrux = vrx / v_rel_norm
        vruy = vry / v_rel_norm
        vruz = vrz / v_rel_norm
        signe = los_unit_x * vruy - los_unit_y * vrux
    else:
        signe = 0.0

    if abs(signe) > 1e-9:
        direction = 1.0 if signe > 0.0 else -1.0
        a_cmd = direction * abs(a_cmd)
    else:
        a_cmd = 0.0

    return a_cmd


# =============================================================================
# INTERFACE WRAPPER (PN -> lat_accel)
# =============================================================================
def loi_guidage(etat_interceptor, etat_cible):
    """
    Interface wrapper pour proportional_navigation.
    """
    a_cmd = proportional_navigation(etat_interceptor, etat_cible)
    # Saturation en accélération latérale
    if a_cmd > _ACCEL_MAX:
        return _ACCEL_MAX
    elif a_cmd < -_ACCEL_MAX:
        return -_ACCEL_MAX
    return a_cmd


# =============================================================================
# AUTO-TEST
# =============================================================================
if __name__ == "__main__":
    print("[flight_control_poc] Test de la loi PN...")
    import math

    etat_i = {
        "position": [0.0, 0.0, 500.0],
        "vitesse" : [300.0, 0.0, 0.0],
    }
    etat_c = {
        "position": [2000.0, 0.0, 500.0],
        "vitesse" : [-200.0, 0.0, 0.0],
    }

    a_cmd = proportional_navigation(etat_i, etat_c)

    if abs(a_cmd) > _ACCEL_MAX:
        print(f"[flight_control_poc] Commande saturée : {a_cmd:.2f} m/s²  "
              f"(max = {_ACCEL_MAX:.2f} m/s²)")
    else:
        print(f"[flight_control_poc] Commande PN : {a_cmd:.2f} m/s²")
    print("[flight_control_poc] OK.")
