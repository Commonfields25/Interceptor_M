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
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z_angle):
        # Innovation
        y = z_angle - (self.H @ self.x)

        # Covariance d'innovation
        S = self.H @ self.P @ self.H.T + self.R

        # Gain de Kalman
        K = self.P @ self.H.T @ np.linalg.inv(S)

        # Mise à jour de l'état
        self.x = self.x + K @ y

        # Mise à jour de la covariance
        self.P = (np.eye(2) - K @ self.H) @ self.P

    def get_rate(self):
        return self.x[1]

if __name__ == "__main__":
    # Simple test
    kf = LOSKalmanFilter(dt=0.1)
    true_rate = 0.5 # rad/s
    angle = 0.0
    print("Test Kalman Filter (True Rate = 0.5):")
    for i in range(10):
        angle += true_rate * 0.1
        noisy_angle = angle + np.random.normal(0, 0.05)
        kf.predict()
        kf.update(noisy_angle)
        print(f"t={i*0.1:.1f}: Noisy Angle={noisy_angle:.3f}, Estimated Rate={kf.get_rate():.3f}")
