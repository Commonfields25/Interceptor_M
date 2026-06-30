"""
Actuator Dynamics Simulation — Fin Torque & Response (SC-06)
Part of the Interceptor_M Physics improvement package.
"""

import numpy as np

def calculate_hinge_moment(dynamic_pressure, area, chord_dist, alpha):
    """
    Simplified hinge moment calculation.
    M_h = q * S * c_h * C_h
    """
    # C_h_alpha estimate for a flat plate fin
    c_h_alpha = 0.05 # per degree
    moment = dynamic_pressure * area * chord_dist * (c_h_alpha * np.degrees(alpha))
    return moment

if __name__ == "__main__":
    # Test case: 300 m/s at SLP
    q = 0.5 * 1.225 * 300**2
    S_fin = 0.0004 # m2 (approx 40x10mm)
    c_h = 0.01 # 10mm lever arm
    alpha = np.radians(10)

    mh = calculate_hinge_moment(q, S_fin, c_h, alpha)
    print(f"Hinge Moment at Mach 0.88 (10 deg deflection): {mh:.4f} N·m")
    # 1 kg.cm = 0.098 N.m
    print(f"Required Torque: {mh/0.098:.4f} kg·cm")
