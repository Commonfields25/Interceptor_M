"""
simulation/kalman_filter.py
===========================
Filtre de Kalman pour l'estimation du taux de la ligne de visée (LOS rate).
"""

import numpy as np

class LOSKalmanFilter:
    def __init__(self, dt=0.01):
        self.dt = dt
        # État : [angle_los, rate_los]
        self.x = np.array([0.0, 0.0])

        # Matrice de transition
        self.F = np.array([[1.0, dt],
                           [0.0, 1.0]])

        # Matrice de covariance de l'erreur
        self.P = np.eye(2) * 10.0

        # Bruit de processus (Q)
        q_sigma = 1.0
        self.Q = np.array([[0.25 * dt**4, 0.5 * dt**3],
                           [0.5 * dt**3, dt**2]]) * q_sigma**2

        # Matrice d'observation
        self.H = np.array([[1.0, 0.0]])

        # Bruit d'observation (R)
        self.R = np.array([[0.01]])

    def predict(self):
        # Optimization: Manual matrix multiplication for 2x2 state transition
        # self.x = self.F @ self.x
        x0 = self.x[0] + self.dt * self.x[1]
        x1 = self.x[1]
        self.x[0] = x0
        self.x[1] = x1

        # self.P = self.F @ self.P @ self.F.T + self.Q
        # F @ P = [[P00 + dt*P10, P01 + dt*P11], [P10, P11]]
        # (F @ P) @ F.T = [[(P00 + dt*P10) + dt*(P01 + dt*P11), P01 + dt*P11], [P10 + dt*P11, P11]]
        p00 = self.P[0,0] + self.dt * (self.P[1,0] + self.P[0,1]) + self.dt * self.dt * self.P[1,1] + self.Q[0,0]
        p01 = self.P[0,1] + self.dt * self.P[1,1] + self.Q[0,1]
        p10 = self.P[1,0] + self.dt * self.P[1,1] + self.Q[1,0]
        p11 = self.P[1,1] + self.Q[1,1]

        self.P[0,0] = p00
        self.P[0,1] = p01
        self.P[1,0] = p10
        self.P[1,1] = p11

    def update(self, z_angle):
        # Innovation
        y = z_angle - self.x[0]

        # Covariance d'innovation (S is 1x1)
        s_val = self.P[0,0] + self.R[0,0]

        # Gain de Kalman K = P @ H.T / S
        k0 = self.P[0,0] / s_val
        k1 = self.P[1,0] / s_val

        # Mise à jour de l'état
        self.x[0] += k0 * y
        self.x[1] += k1 * y

        # Mise à jour de la covariance: P = (I - KH)P
        # I - KH = [[1-k0, 0], [-k1, 1]]
        p00 = (1.0 - k0) * self.P[0,0]
        p01 = (1.0 - k0) * self.P[0,1]
        p10 = -k1 * self.P[0,0] + self.P[1,0]
        p11 = -k1 * self.P[0,1] + self.P[1,1]

        self.P[0,0] = p00
        self.P[0,1] = p01
        self.P[1,0] = p10
        self.P[1,1] = p11

    def get_rate(self):
        return self.x[1]
