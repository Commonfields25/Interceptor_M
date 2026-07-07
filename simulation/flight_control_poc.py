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
_GAIN_PN = C.GAIN_PN
_ACCEL_MAX = C.ACCELERATION_LATERALE_MAX_M_S2
_DT = C.PAS_DE_TEMPS_S


class GuidanceSystem:
    def __init__(self):
        # Filtres pour Azimut et Elévation
        self.kf_az = LOSKalmanFilter(dt=_DT)
        self.kf_el = LOSKalmanFilter(dt=_DT)
        self.initialized = False

    def compute_guidance(self, etat_i, etat_c):
        pos_i = etat_i["position"]
        pos_c = etat_c["position"]
        vel_i = etat_i["vitesse"]
        vel_c = etat_c["vitesse"]

        # Optimized relative vector math
        rx, ry, rz = pos_c[0] - pos_i[0], pos_c[1] - pos_i[1], pos_c[2] - pos_i[2]
        dist_sq = rx * rx + ry * ry + rz * rz
        if dist_sq < 0.01:
            return 0.0, 0.0

        dist = math.sqrt(dist_sq)
        vx, vy, vz = vel_c[0] - vel_i[0], vel_c[1] - vel_i[1], vel_c[2] - vel_i[2]

        # Angles LOS
        az = math.atan2(ry, rx)
        el = math.asin(rz / dist)

        if not self.initialized:
            self.kf_az.x[0] = az
            self.kf_az.x[1] = 0.0
            self.kf_el.x[0] = el
            self.kf_el.x[1] = 0.0
            self.initialized = True

        self.kf_az.predict()
        self.kf_el.predict()

        # Unwrap angles
        z_az = az
        az_kf = self.kf_az.x[0]
        while z_az - az_kf > math.pi:
            z_az -= 2.0 * math.pi
        while z_az - az_kf < -math.pi:
            z_az += 2.0 * math.pi

        self.kf_az.update(z_az)
        self.kf_el.update(el)

        omega_az = self.kf_az.x[1]
        omega_el = self.kf_el.x[1]

        # Vitesse de rapprochement (closing velocity)
        v_clos = -(rx * vx + ry * vy + rz * vz) / dist

        # PN 3D
        accel_az = _GAIN_PN * v_clos * omega_az
        accel_el = _GAIN_PN * v_clos * omega_el

        # Compensation gravité
        accel_el += 9.81 * math.cos(el)

        return accel_az, accel_el


if __name__ == "__main__":
    gs = GuidanceSystem()
    print("Guidance initialized.")
