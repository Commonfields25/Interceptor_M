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
        if dist_sq < 0.01: return 0.0, 0.0

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

        # Unwrap angles
        z_az = az
        while z_az - self.kf_az.x[0] > math.pi: z_az -= 2*math.pi
        while z_az - self.kf_az.x[0] < -math.pi: z_az += 2*math.pi

        self.kf_az.update(z_az)
        self.kf_el.update(el)

        omega_az = self.kf_az.get_rate()
        omega_el = self.kf_el.get_rate()

        # Vitesse de rapprochement (closing velocity)
        v_clos = -np.dot(rel_pos, rel_vel) / dist

        # PN 3D
        accel_az = _GAIN_PN * v_clos * omega_az
        accel_el = _GAIN_PN * v_clos * omega_el

        # Compensation gravité
        accel_el += 9.81 * math.cos(el)

        return accel_az, accel_el

if __name__ == "__main__":
    gs = GuidanceSystem()
    print("Guidance initialized.")
