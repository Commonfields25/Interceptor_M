"""
simulation/kalman_filter.py
===========================
Filtre de Kalman pour l'estimation du taux de la ligne de visée (LOS rate).
Amélioration : Adaptation aux mesures bruitées et latence.
"""

import numpy as np

class LOSKalmanFilter:
    def __init__(self, dt=0.01):
        self.dt = dt
        # État : [angle_los, rate_los, accel_los]
        self.x = np.array([0.0, 0.0, 0.0])

        # Matrice de transition (modèle d'accélération constante)
        self.F = np.array([[1.0, dt, 0.5 * dt**2],
                           [0.0, 1.0, dt],
                           [0.0, 0.0, 1.0]])

        self.P = np.eye(3) * 100.0

        # Bruit de processus (Q)
        q_sigma = 5.0 # Augmenté pour capturer les manoeuvres cibles
        self.Q = np.array([
            [dt**5/20, dt**4/8, dt**3/6],
            [dt**4/8,  dt**3/3, dt**2/2],
            [dt**3/6,  dt**2/2, dt]
        ]) * q_sigma**2

        self.H = np.array([[1.0, 0.0, 0.0]])
        self.R = np.array([[0.005]]) # Bruit de mesure angulaire (approx 5 mrad)

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z_angle):
        y = z_angle - (self.H @ self.x)
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(3) - K @ self.H) @ self.P

    def get_rate(self):
        return self.x[1]

if __name__ == "__main__":
    pass
