"""
simulation/flight_control_poc.py
===============================
Loi de guidage par navigation proportionnelle (PN) 3D avec filtrage de Kalman.
"""

import math
import numpy as np
from . import constants as C
from .kalman_filter import LOSKalmanFilter

# ------------------------------------------------------------------
# Paramètres locaux
# ------------------------------------------------------------------
_GAIN_PN      = C.GAIN_PN
_ACCEL_MAX    = C.ACCELERATION_LATERALE_MAX_M_S2
_DT           = C.PAS_DE_TEMPS_S

class GuidanceSystem:
    def __init__(self):
        # Filtres pour Azimut et Elévation
        self.kf_az = LOSKalmanFilter(dt=_DT)
        self.kf_el = LOSKalmanFilter(dt=_DT)
        self.initialized = False

    def compute_guidance(self, etat_i, etat_c):
        pos_i = np.array(etat_i["position"])
        pos_c = np.array(etat_c["position"])
        vel_i = np.array(etat_i["vitesse"])
        vel_c = np.array(etat_c["vitesse"])

        rel_pos = pos_c - pos_i
        dist_sq = np.sum(rel_pos**2)
        if dist_sq < 0.01: return 0.0, 0.0 # Accel lat, Accel vert (simplifié)

        dist = math.sqrt(dist_sq)
        rel_vel = vel_c - vel_i

        # Angles LOS
        az = math.atan2(rel_pos[1], rel_pos[0])
        el = math.asin(rel_pos[2] / dist)

        if not self.initialized:
            self.kf_az.x = np.array([az, 0.0])
            self.kf_el.x = np.array([el, 0.0])
            self.initialized = True

        self.kf_az.predict()
        self.kf_el.predict()
        self.kf_az.update(az)
        self.kf_el.update(el)

        omega_az = self.kf_az.get_rate()
        omega_el = self.kf_el.get_rate()

        # Vitesse de rapprochement (closing velocity)
        v_clos = -np.dot(rel_pos, rel_vel) / dist

        # Commandes PN (accélérations normales à la LOS)
        # n_az = N * V_clos * omega_az * cos(el)
        # n_el = N * V_clos * omega_el
        accel_az = _GAIN_PN * v_clos * omega_az * math.cos(el)
        accel_el = _GAIN_PN * v_clos * omega_el

        # Compensation gravité simple
        accel_el += 9.81 * math.cos(el)

        return accel_az, accel_el

# Wrapper compatible avec sim_6dof qui attend une seule valeur lat_accel
# On va devoir adapter sim_6dof pour accepter une commande 3D ou projeter.
# Pour l'instant, on va modifier sim_6dof pour appeler une fonction de guidage qui rend (lat, vert).

def loi_guidage_3d(etat_i, etat_c, system):
    return system.compute_guidance(etat_i, etat_c)
