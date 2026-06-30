"""
Interceptor Swarm RL Environment — 6-DOF Rigid-Body Dynamics
=============================================================
Standalone numpy implementation (no Isaac Gym required).
Updated to 400g DD platform physics.

State per agent (13 dims):
  [0:3]   position (ECI world frame) [m]
  [3:6]   velocity (ECI world frame) [m/s]
  [6:10]  attitude quaternion [qx,qy,qz,qw] (world-to-body)
  [10:13] body angular rates [rad/s] (p,q,r)

Action per agent (3 dims):
  [0] thrust fraction [0, 1]
  [1] body-rate pitch command [rad/s]
  [2] body-rate yaw command   [rad/s]

Authors: Jules (Physics Expert) | Refs: STATUS-REPORT.md, issue #15
"""

from __future__ import annotations
import numpy as np
try:
    from gymnasium.spaces import Box
except ImportError:
    from gym.spaces import Box
from typing import Dict, Optional
import math

# ─── Constants ────────────────────────────────────────────────────────────────
N_AGENTS_MAX: int = 4
DT: float = 0.01              # High-fidelity integration timestep [s]
MAX_STEPS: int = 2000         # Max episode length (20s @ 0.01s)

# Wind / disturbance (hardened difficulty — post-M8 DG decision 2026-06-30)
WIND_GUST_STD: float = 7.0       # m/s — was 0.0, +40% from prior estimate (+0% → +40%)
WIND_GUST_INTERVAL: float = 0.5  # s — update gust every 0.5s
WIND_GUST_MAG: float = 10.0      # m/s — max gust magnitude

# DD-400 Physical Constants
MASS: float = 0.400           # kg — MTOW
LENGTH: float = 0.380         # m
DIAMETER: float = 0.035       # m
S_REF: float = 0.001          # m² — frontal area (~35mm dia)

# Inertia: approximate as thin rod + point masses
Ixx: float = 0.5 * MASS * (DIAMETER/2)**2
Iyy: float = (1/12) * MASS * LENGTH**2
Izz: float = Iyy
INERTIA: np.ndarray = np.diag([Ixx, Iyy, Izz])

GRAVITY: np.ndarray = np.array([0.0, 0.0, -9.80665])  # m/s²

# Propulsion
MAX_THRUST: float = 12.0      # N (~3:1 TWR)
FUEL_CAPACITY: float = 0.052  # kg (from DD-PARAMETERS)

# Aerodynamics (from sim_6dof.py / constants.py)
CX_DRAG: float = 0.35
CL_ALPHA: float = 2.0
RHO_0: float = 1.225
H_SCALE: float = 8500.0

# Guidance / control (hardened)
BODY_RATE_MAX: float = 5.0    # rad/s — high maneuverability for 400g drone
BODY_RATE_TC: float = 0.1     # s — fast response

# Targets
TARGET_SPEED: float = 300.0   # m/s
D_INTERCEPT: float = 1.5      # m — reduced from 2.0m (-25%) per M8 hardening decision

# Reward
R_INTERCEPT: float = 1000.0
R_EFFICIENCY: float = 0.0
FUEL_PENALTY: float = 0.1
R_SEPARATION: float = 1.0
R_FRATRICIDE: float = -500.0
R_GROUND: float = -100.0

# ─── Physics Helpers ──────────────────────────────────────────────────────────
def get_density(alt: float) -> float:
    return RHO_0 * math.exp(-max(0, alt) / H_SCALE)

def quat_normalize(q: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(q)
    return q / n if n > 1e-12 else np.array([0., 0., 0., 1.])

def quat_to_dcm(q: np.ndarray) -> np.ndarray:
    qx, qy, qz, qw = q
    return np.array([
        [1 - 2*(qy**2 + qz**2),     2*(qx*qy + qz*qw),     2*(qx*qz - qy*qw)],
        [    2*(qy*qx - qz*qw), 1 - 2*(qx**2 + qz**2),     2*(qy*qz + qx*qw)],
        [    2*(qz*qx + qy*qw),     2*(qz*qy - qx*qw), 1 - 2*(qx**2 + qy**2)],
    ], dtype=np.float32)

def quat_derivative(q: np.ndarray, omega: np.ndarray) -> np.ndarray:
    qx, qy, qz, qw = q
    p, q_rate, r = omega
    return 0.5 * np.array([
         qw*p + qy*r - qz*q_rate,
         qw*q_rate + qz*p - qx*r,
         qw*r + qx*q_rate - qy*p,
        -qx*p - qy*q_rate - qz*r
    ], dtype=np.float32)

def quat_to_euler(q: np.ndarray) -> np.ndarray:
    qx, qy, qz, qw = q
    # Roll
    sr = 2*(qw*qx + qy*qz)
    cr = 1 - 2*(qx**2 + qy**2)
    roll = np.arctan2(sr, cr)
    # Pitch
    sp = 2*(qw*qy - qz*qx)
    sp = np.clip(sp, -1.0, 1.0)
    pitch = np.arcsin(sp)
    # Yaw
    sy = 2*(qw*qz + qx*qy)
    cy = 1 - 2*(qy**2 + qz**2)
    yaw = np.arctan2(sy, cy)
    return np.array([roll, pitch, yaw], dtype=np.float32)

def integrate_step(
    pos: np.ndarray, vel: np.ndarray,
    quat: np.ndarray, omega: np.ndarray,
    thrust_frac: float,
    omega_cmd_py: np.ndarray, # 2D: [pitch, yaw]
    dt: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    # Body rate command: [roll_rate=0, pitch_rate, yaw_rate]
    cmd_3d = np.array([0.0, omega_cmd_py[0], omega_cmd_py[1]], dtype=np.float32)

    # 1. Rate controller (first order)
    omega_dot = (cmd_3d - omega) / BODY_RATE_TC
    omega_new = np.clip(omega + omega_dot * dt, -BODY_RATE_MAX, BODY_RATE_MAX)

    # 2. Aero forces
    speed = np.linalg.norm(vel)
    rho = get_density(pos[2])
    q_inf = 0.5 * rho * speed**2

    # Drag
    drag_mag = q_inf * S_REF * CX_DRAG
    drag_world = -(drag_mag / (speed + 1e-6)) * vel if speed > 0.1 else np.zeros(3, dtype=np.float32)

    # Lift
    dcm = quat_to_dcm(quat)
    body_x = dcm[:, 0]
    if speed > 1.0:
        vel_unit = vel / speed
        cos_alpha = np.clip(np.dot(vel_unit, body_x), -1.0, 1.0)
        alpha = np.arccos(cos_alpha)
        lift_mag = q_inf * S_REF * CL_ALPHA * alpha

        lift_dir = body_x - cos_alpha * vel_unit
        lift_norm = np.linalg.norm(lift_dir)
        if lift_norm > 1e-6:
            lift_world = (lift_mag / lift_norm) * lift_dir
        else:
            lift_world = np.zeros(3, dtype=np.float32)
    else:
        lift_world = np.zeros(3, dtype=np.float32)

    # 3. Propulsion
    thrust_world = body_x * (MAX_THRUST * thrust_frac)

    # 4. Translation
    accel = (thrust_world + lift_world + drag_world + MASS * GRAVITY) / MASS
    vel_new = vel + accel * dt
    pos_new = pos + vel_new * dt

    # 5. Rotation (RK4)
    q0 = quat.astype(np.float32)
    w = omega_new.astype(np.float32)
    k1 = quat_derivative(q0, w)
    k2 = quat_derivative(q0 + 0.5*dt*k1, w)
    k3 = quat_derivative(q0 + 0.5*dt*k2, w)
    k4 = quat_derivative(q0 + dt*k3, w)
    quat_new = quat_normalize(q0 + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4))

    return pos_new, vel_new, quat_new, omega_new

# ─── Environment ──────────────────────────────────────────────────────────────
class SwarmInterceptEnv:
    def __init__(self, n_agents: int = 2, max_steps: int = MAX_STEPS):
        self.n_agents = n_agents
        self.max_steps = max_steps
        self.observation_space = Box(low=-np.inf, high=np.inf, shape=(13,), dtype=np.float32)
        self.action_space = Box(low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32)

    def reset(self, seed=None):
        self._rng = np.random.default_rng(seed)
        self._step_count = 0
        self._sim_time = 0.0
        self._pos = self._rng.uniform(-50, 50, (self.n_agents, 3)).astype(np.float32)
        self._pos[:, 2] = self._rng.uniform(500, 1000)
        self._vel = np.zeros((self.n_agents, 3), dtype=np.float32)
        self._quat = np.tile(np.array([0., 0., 0., 1.], dtype=np.float32), (self.n_agents, 1))
        self._omega = np.zeros((self.n_agents, 3), dtype=np.float32)
        self._alive = np.ones(self.n_agents, dtype=np.float32)
        self._tgt_pos = np.array([0.0, 0.0, 500.0], dtype=np.float32)
        self._tgt_vel = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self._wind_gust = np.zeros(3, dtype=np.float32)
        self._gust_timer = 0.0
        return self._get_obs()

    def step(self, actions):
        self._step_count += 1
        self._sim_time += DT
        rewards = np.zeros(self.n_agents)

        # Update wind gust every WIND_GUST_INTERVAL
        self._gust_timer += DT
        if self._gust_timer >= WIND_GUST_INTERVAL:
            self._gust_timer = 0.0
            self._wind_gust = self._rng.uniform(-WIND_GUST_MAG, WIND_GUST_MAG, 3).astype(np.float32)

        for i in range(self.n_agents):
            if self._alive[i] < 0.5: continue

            # Apply gust to velocity before integration
            v_gusted = self._vel[i] + self._wind_gust

            act = actions.get(i, np.zeros(3))
            p, v, q, o = integrate_step(
                self._pos[i], v_gusted, self._quat[i], self._omega[i],
                act[0], act[1:3], DT
            )
            self._pos[i], self._vel[i], self._quat[i], self._omega[i] = p, v, q, o

            dist = np.linalg.norm(self._pos[i] - self._tgt_pos)
            if dist < D_INTERCEPT:
                rewards[i] += R_INTERCEPT
                self._alive[i] = 0.0
            elif self._pos[i, 2] < 0:
                rewards[i] += R_GROUND
                self._alive[i] = 0.0

        done = np.all(self._alive < 0.5) or self._step_count >= self.max_steps
        return self._get_obs(), rewards, done, {}

    def _get_obs(self):
        obs = {}
        for i in range(self.n_agents):
            obs[i] = np.concatenate([self._pos[i], self._vel[i], self._quat[i], self._omega[i]])
        return obs

if __name__ == "__main__":
    env = SwarmInterceptEnv()
    obs = env.reset()
    print("6-DOF Physics Engine Upgraded (DD-400 platform).")
    for _ in range(100):
        obs, rewards, done, info = env.step({0: np.array([1.0, 0.1, 0.1]), 1: np.array([1.0, -0.1, -0.1])})
        if done: break
    print(f"Simulation completed. Final Pos Agent 0: {obs[0][:3]}")
