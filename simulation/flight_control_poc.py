import math, numpy as np
from . import constants as C
from .kalman_filter import LOSKalmanFilter
_GAIN_PN, _ACCEL_MAX, _DT = C.GAIN_PN, C.ACCELERATION_LATERALE_MAX_M_S2, C.PAS_DE_TEMPS_S
class GuidanceSystem:
    def __init__(self, mode="PN", latency_steps=0):
        self.mode, self.latency_steps, self.initialized = mode, latency_steps, False
        self.kf_az, self.kf_el, self.prev_vel_c, self.measurement_buffer = LOSKalmanFilter(dt=_DT), LOSKalmanFilter(dt=_DT), None, []
    def compute_guidance(self, etat_i, etat_c):
        pos_i, pos_c, vel_i, vel_c = np.array(etat_i["position"]), np.array(etat_c["position"]), np.array(etat_i["vitesse"]), np.array(etat_c["vitesse"])
        rel_pos = pos_c - pos_i; dist_sq = np.sum(rel_pos**2)
        if dist_sq < 0.01: return 0.0, 0.0
        dist, rel_vel = math.sqrt(dist_sq), vel_c - vel_i; az_true, el_true = math.atan2(rel_pos[1], rel_pos[0]), math.asin(rel_pos[2] / dist)
        az_noisy, el_noisy = az_true + np.random.normal(0, 0.002), el_true + np.random.normal(0, 0.002); self.measurement_buffer.append((az_noisy, el_noisy))
        if len(self.measurement_buffer) > self.latency_steps: az_meas, el_meas = self.measurement_buffer.pop(0)
        else: az_meas, el_meas = az_noisy, el_noisy
        if not self.initialized: self.kf_az.x, self.kf_el.x, self.initialized, self.prev_vel_c = np.array([az_meas, 0, 0]), np.array([el_meas, 0, 0]), True, vel_c.copy()
        self.kf_az.predict(); self.kf_el.predict(); self.kf_az.update(az_meas); self.kf_el.update(el_meas); omega_az, omega_el, v_clos = self.kf_az.get_rate(), self.kf_el.get_rate(), -np.dot(rel_pos, rel_vel) / dist
        accel_az, accel_el = _GAIN_PN * v_clos * omega_az * math.cos(el_true), _GAIN_PN * v_clos * omega_el
        if self.mode == "APN":
            at = (vel_c - self.prev_vel_c) / _DT; at_perp = at - np.dot(at, rel_pos/dist) * (rel_pos/dist)
            accel_el += 0.5 * _GAIN_PN * at_perp[2]; ub_xy = np.array([-math.sin(az_true), math.cos(az_true), 0.0]); accel_az += 0.5 * _GAIN_PN * np.dot(at_perp, ub_xy)
        self.prev_vel_c = vel_c.copy(); accel_el += 9.81 * math.cos(el_true)
        cmd_norm = math.sqrt(accel_az**2 + accel_el**2)
        if cmd_norm > _ACCEL_MAX: factor = _ACCEL_MAX / cmd_norm; return accel_az*factor, accel_el*factor
        return accel_az, accel_el
