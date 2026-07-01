"""
simulation/flight_control_poc.py
===============================
Loi de guidage par navigation proportionnelle augmentée (APN) 3D avec filtrage de Kalman.
Amélioration : Prise en compte du bruit et de la latence du seeker.
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
    def __init__(self, mode="PN", latency_steps=0):
        self.mode = mode
        self.kf_az = LOSKalmanFilter(dt=_DT)
        self.kf_el = LOSKalmanFilter(dt=_DT)
        self.initialized = False
        self.prev_vel_c = None

        # Simulation de latence
        self.latency_steps = latency_steps
        self.measurement_buffer = []

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

        # Mesures réelles (avec bruit blanc)
        az_true = math.atan2(rel_pos[1], rel_pos[0])
        el_true = math.asin(rel_pos[2] / dist)

        # Ajout de bruit de mesure (approx 2 mrad RMS)
        az_noisy = az_true + np.random.normal(0, 0.002)
        el_noisy = el_true + np.random.normal(0, 0.002)

        # Gestion de la latence
        self.measurement_buffer.append((az_noisy, el_noisy))
        if len(self.measurement_buffer) > self.latency_steps:
            az_meas, el_meas = self.measurement_buffer.pop(0)
        else:
            az_meas, el_meas = az_noisy, el_noisy # Pas encore de buffer plein

        if not self.initialized:
            self.kf_az.x = np.array([az_meas, 0.0, 0.0])
            self.kf_el.x = np.array([el_meas, 0.0, 0.0])
            self.initialized = True
            self.prev_vel_c = vel_c.copy()

        self.kf_az.predict()
        self.kf_el.predict()
        self.kf_az.update(az_meas)
        self.kf_el.update(el_meas)

        omega_az = self.kf_az.get_rate()
        omega_el = self.kf_el.get_rate()

        v_clos = -np.dot(rel_pos, rel_vel) / dist

        accel_az = _GAIN_PN * v_clos * omega_az * math.cos(el_true)
        accel_el = _GAIN_PN * v_clos * omega_el

        if self.mode == "APN":
            accel_target = (vel_c - self.prev_vel_c) / _DT
            ut_los = rel_pos / dist
            accel_target_perp = accel_target - np.dot(accel_target, ut_los) * ut_los

            accel_el += 0.5 * _GAIN_PN * accel_target_perp[2]
            ub_xy = np.array([-math.sin(az_true), math.cos(az_true), 0.0])
            accel_target_lat = np.dot(accel_target_perp, ub_xy)
            accel_az += 0.5 * _GAIN_PN * accel_target_lat

        self.prev_vel_c = vel_c.copy()
        accel_el += 9.81 * math.cos(el_true)

        return accel_az, accel_el

if __name__ == "__main__":
    pass
