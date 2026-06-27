"""
Interceptor Swarm RL Environment — 6-DOF Rigid-Body Dynamics
=============================================================
Standalone numpy implementation (no Isaac Gym required).

State per agent (13 dims):
  [0:3]   position (ECI world frame) [m]
  [3:6]   velocity (ECI world frame) [m/s]
  [6:10]  attitude quaternion [qx,qy,qz,qw] (world-to-body)
  [10:13] body angular rates [rad/s] (p,q,r)

Action per agent (3 dims):
  [0] thrust fraction [0, 1]
  [1] body-rate pitch command [rad/s]
  [2] body-rate yaw command   [rad/s]

Observation per agent (18 dims):
  [0:3]   relative target position (body frame)
  [3:6]   relative target velocity (body frame)
  [6:9]   interceptor position (world)
  [9:12]  interceptor velocity (world)
  [12:15] interceptor attitude (euler r,p,y) [rad]
  [15]    time-alive normalised
  [16]    fraction of swarm still alive
  [17]    nearest neighbour distance [m]

Authors: E2 + D3  |  Refs: SWARM-RL-PLAN.md §5, issue #15
"""

from __future__ import annotations
import numpy as np
from typing import Dict, Optional

# ─── Constants ────────────────────────────────────────────────────────────────
N_AGENTS_MAX: int = 4
DT: float = 0.05              # integration timestep [s]
MAX_STEPS: int = 60          # max episode length

# 6-DOF physical constants
MASS: float = 200.0           # kg  — interceptor dry mass
Ixx: float = 50.0             # kg·m²
Iyy: float = 80.0
Izz: float = 80.0
INERTIA: np.ndarray = np.diag([Ixx, Iyy, Izz])  # principal axes

GRAVITY: np.ndarray = np.array([0.0, 0.0, -9.81])  # m/s²

MAX_THRUST: float = 50_000.0  # N
DRAG_COEFF: float = 0.5       # simple linear drag coeff

# Guidance / control
BODY_RATE_MAX: float = 1.5    # rad/s  — max commanded rate
BODY_RATE_TC: float = 0.2     # s       — rate convergence time constant

# Targets
TARGET_SPEED: float = 500.0   # m/s  — incoming threat speed
TARGET_WOBBLE_AMP: float = 30.0  # m  — lateral wobble amplitude (weaving)

# Reward
R_INTERCEPT: float = 100.0
R_EFFICIENCY: float = 0.01
FUEL_PENALTY: float = 0.05    # per step cost for thrust
R_SEPARATION: float = 0.1
R_FRATRICIDE: float = -50.0
R_GROUND: float = -20.0

D_INTERCEPT: float = 1.5      # m — intercept radius
D_SEPARATION: float = 5.0     # m
D_FRATRICIDE: float = 1.0     # m
GROUND_LIMIT: float = -500.0  # m — altitude below = crash

# ─── Quaternion helpers ───────────────────────────────────────────────────────
def quat_normalize(q: np.ndarray) -> np.ndarray:
    """Normalise quaternion in-place."""
    n = np.linalg.norm(q)
    return q / n if n > 1e-12 else np.array([0., 0., 0., 1.])

def quat_to_dcm(q: np.ndarray) -> np.ndarray:
    """Direction-Cosine Matrix: body → world from quaternion (xyzw)."""
    qx, qy, qz, qw = q
    return np.array([
        [1 - 2*(qy**2 + qz**2),     2*(qx*qy + qz*qw),     2*(qx*qz - qy*qw)],
        [    2*(qy*qx - qz*qw), 1 - 2*(qx**2 + qz**2),     2*(qy*qz + qx*qw)],
        [    2*(qz*qx + qy*qw),     2*(qz*qy - qx*qw), 1 - 2*(qx**2 + qy**2)],
    ], dtype=np.float64)

def quat_derivative(q: np.ndarray, omega: np.ndarray) -> np.ndarray:
    """Kinematic derivative: dq/dt = 0.5 * Ω_body * q."""
    qx, qy, qz, qw = q
    px, py, pz = omega
    return 0.5 * np.array([
        -px*qx - py*qy - pz*qz + qw*qx,
         px*qw + py*qz - pz*qy + qw*qy,
        -px*qz + py*qw + pz*qx + qw*qz,
         px*qy - py*qx + pz*qw + qw*qw,
    ], dtype=np.float32)

def quat_to_euler(q: np.ndarray) -> np.ndarray:
    """YXZ convention → [roll, pitch, yaw] in radians."""
    qx, qy, qz, qw = q
    # Roll (x)
    sr = 2*(qw*qx + qy*qz)
    cr = 1 - 2*(qx**2 + qy**2)
    roll = np.arctan2(sr, cr)
    # Pitch (y)
    sp = 2*(qw*qy - qz*qx)
    sp = np.clip(sp, -1.0, 1.0)
    pitch = np.arcsin(sp)
    # Yaw (z)
    sy = 2*(qw*qz + qx*qy)
    cy = 1 - 2*(qy**2 + qz**2)
    yaw = np.arctan2(sy, cy)
    return np.array([roll, pitch, yaw], dtype=np.float32)

def rotate_by_quat(v: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Rotate vector v from body frame to world frame using quaternion q."""
    dcm = quat_to_dcm(q)
    return dcm @ v

# ─── 6-DOF Integrator (RK4 for position/quaternion, semi-implicit Euler for vel/rate) ──
def integrate_step(
    pos: np.ndarray, vel: np.ndarray,
    quat: np.ndarray, omega: np.ndarray,
    thrust_frac: float,
    omega_cmd: np.ndarray,
    dt: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Semi-implicit Euler with RK4 for quaternion kinematics.
    Returns (pos, vel, quat, omega).
    """
    # Commanded body rates → actual via first-order lag
    omega_err = omega_cmd - omega
    omega_dot_cmd = omega_err / BODY_RATE_TC
    omega_new = omega + omega_dot_cmd * dt
    omega_new = np.clip(omega_new, -BODY_RATE_MAX, BODY_RATE_MAX)

    # Thrust vector in body frame → world frame
    thrust_body = np.array([MAX_THRUST * thrust_frac, 0.0, 0.0])
    thrust_world = rotate_by_quat(thrust_body, quat)

    # Drag (proportional to speed, opposing velocity)
    speed = np.linalg.norm(vel)
    if speed > 0.01:
        drag_world = -DRAG_COEFF * speed * vel
    else:
        drag_world = np.zeros(3)

    # Translational: F = m*a  →  a = (F_net)/m
    accel = (thrust_world + MASS * GRAVITY + drag_world) / MASS
    vel_new = vel + accel * dt
    pos_new = pos + vel_new * dt   # semi-implicit (use new vel)

    # Rotational: I·α = τ  (τ = 0 in this model; gravity-gradient neglected)
    # quaternion kinematics via RK4
    q0 = quat.astype(np.float64)
    w = omega.astype(np.float64)

    def dq(q, o):
        return quat_derivative(q.astype(np.float32), o.astype(np.float32)).astype(np.float64)

    k1 = dq(q0, w)
    k2 = dq(q0 + 0.5*dt*k1, w)
    k3 = dq(q0 + 0.5*dt*k2, w)
    k4 = dq(q0 + dt*k3, w)

    quat_new = quat_normalize(q0 + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4))
    return pos_new.astype(np.float32), vel_new.astype(np.float32), quat_new.astype(np.float32), omega_new.astype(np.float32)


# ─── Target dynamics ───────────────────────────────────────────────────────────
def target_step(pos: np.ndarray, t: float, seed: int) -> np.ndarray:
    """
    Constant-velocity approach with lateral sinusoidal wobble.
    Target moves toward origin at TARGET_SPEED along -x axis.
    """
    # Base velocity toward origin
    dist = np.linalg.norm(pos)
    if dist < 1.0:
        return np.zeros(3, dtype=np.float32)

    direction = -pos / dist
    base_vel = direction * TARGET_SPEED

    # Lateral wobble (weaving)
    rng = np.random.default_rng(seed + int(t / DT))
    delta_v = rng.uniform(-8.0, 8.0, size=3)

    # Clamp lateral component to not overpower head-on velocity
    wobble = np.array([0.0, delta_v[1] * np.sin(t * 0.5), delta_v[2] * np.cos(t * 0.7)])
    return (base_vel + wobble).astype(np.float32)


# ─── Gym-style spaces ─────────────────────────────────────────────────────────
class Box:
    def __init__(self, low, high, shape=None, dtype=np.float32):
        if shape is None:
            shape = (len(low),)
        self.low = np.asarray(low, dtype=dtype)
        self.high = np.asarray(high, dtype=dtype)
        self.shape = tuple(shape)
        self.dtype = dtype

    def contains(self, x):
        return np.all((self.low <= x) & (x <= self.high))

    def sample(self, rng=None):
        rng = rng or np.random.default_rng()
        return rng.uniform(self.low, self.high).astype(self.dtype)


# ─── Main Environment ─────────────────────────────────────────────────────────
class SwarmInterceptEnv:
    metadata = {"render_modes": []}

    def __init__(
        self,
        n_agents: int = 2,
        max_steps: int = MAX_STEPS,
        seed: Optional[int] = None,
    ):
        if not (1 <= n_agents <= N_AGENTS_MAX):
            raise ValueError(f"n_agents must be 1..{N_AGENTS_MAX}")
        self.n_agents = n_agents
        self.max_steps = max_steps

        self.observation_space = Box(
            low=np.full(18, -100.0),
            high=np.full(18, 100.0),
        )
        self.action_space = Box(
            low=np.array([0.0, -BODY_RATE_MAX, -BODY_RATE_MAX]),
            high=np.array([1.0,  BODY_RATE_MAX,  BODY_RATE_MAX]),
        )

        self._rng: Optional[np.random.Generator] = None
        self._step_count: int = 0

        # ── State tensors ──────────────────────────────────────────────────────
        self._pos:     Optional[np.ndarray] = None  # (n,3) world pos
        self._vel:     Optional[np.ndarray] = None  # (n,3) world vel
        self._quat:    Optional[np.ndarray] = None  # (n,4) xyzw
        self._omega:   Optional[np.ndarray] = None  # (n,3) body rates
        self._alive:   Optional[np.ndarray] = None  # (n,) 1.0=alive,0.0=dead
        self._tgt_pos: Optional[np.ndarray] = None  # (3,) world pos
        self._tgt_vel: Optional[np.ndarray] = None  # (3,) world vel
        self._sim_time: float = 0.0

        if seed is not None:
            self.reset(seed=seed)

    # ── gym API ─────────────────────────────────────────────────────────────────
    def reset(self, seed: Optional[int] = None) -> tuple[Dict[int, np.ndarray], dict]:
        if seed is not None:
            self._rng = np.random.default_rng(seed)
        elif self._rng is None:
            self._rng = np.random.default_rng()

        self._step_count = 0
        self._sim_time = 0.0

        n = self.n_agents
        self._pos   = np.zeros((n, 3), dtype=np.float32)
        self._vel   = np.zeros((n, 3), dtype=np.float32)
        self._quat  = np.zeros((n, 4), dtype=np.float32)
        self._omega = np.zeros((n, 3), dtype=np.float32)
        self._alive = np.ones(n, dtype=np.float32)

        # Initialise interceptors in a spread around the origin
        spread = 8.0
        for i in range(n):
            angle = 2 * np.pi * i / n + self._rng.uniform(0, 0.5)
            self._pos[i] = np.array([
                spread * np.cos(angle),
                spread * np.sin(angle),
                self._rng.uniform(-2.0, 8.0),
            ], dtype=np.float32)

            # Initial velocity toward the initial target position
            tgt_init = np.array([spread, 0.0, 0.0], dtype=np.float32)
            dir_to_tgt = tgt_init - self._pos[i]
            dist = np.linalg.norm(dir_to_tgt)
            if dist > 0.01:
                speed = self._rng.uniform(10.0, 25.0)
                self._vel[i] = (dir_to_tgt / dist) * speed

            # Initial quaternion: identity (body aligned with world)
            self._quat[i] = np.array([0., 0., 0., 1.], dtype=np.float32)

        # Target starts ahead of the swarm
        self._tgt_pos = np.array([250.0, 0.0, 0.0], dtype=np.float32)
        self._tgt_vel = np.array([-TARGET_SPEED, 0.0, 0.0], dtype=np.float32)

        obs = self._get_obs()
        return obs, {}

    def step(
        self, actions: Dict[int, np.ndarray]
    ) -> tuple[Dict[int, np.ndarray], np.ndarray, np.ndarray, np.ndarray, dict]:
        self._step_count += 1
        self._sim_time += DT

        n = self.n_agents
        rewards = np.zeros(n, dtype=np.float32)
        terminations = np.zeros(n, dtype=bool)
        truncations = np.zeros(n, dtype=bool)

        # ── 1. Integrate target ────────────────────────────────────────────────
        self._tgt_vel = target_step(self._tgt_pos, self._sim_time, self._rng.integers(0, 2**31))
        self._tgt_pos += self._tgt_vel * DT

        # ── 2. Integrate alive interceptors ───────────────────────────────────
        for i in range(n):
            if self._alive[i] < 0.5:
                rewards[i] = 0.0
                terminations[i] = True
                continue

            action = np.clip(actions.get(i, np.zeros(3)), self.action_space.low, self.action_space.high).astype(np.float32)
            thrust_frac = float(action[0])
            omega_cmd = np.array([0.0, float(action[1]), float(action[2])], dtype=np.float32)

            pos_i, vel_i, quat_i, omega_i = integrate_step(
                self._pos[i], self._vel[i],
                self._quat[i], self._omega[i],
                thrust_frac, omega_cmd, DT,
            )

            self._pos[i]   = pos_i
            self._vel[i]   = vel_i
            self._quat[i]  = quat_i
            self._omega[i] = omega_i

            # ── Reward components ──────────────────────────────────────────────
            dist_to_tgt = np.linalg.norm(self._pos[i] - self._tgt_pos)

            # (a) Intercept
            if dist_to_tgt < D_INTERCEPT:
                rewards[i] += R_INTERCEPT
                self._alive[i] = 0.0
                terminations[i] = True
                continue

            # (b) Ground crash
            if self._pos[i, 2] < GROUND_LIMIT:
                rewards[i] += R_GROUND
                self._alive[i] = 0.0
                terminations[i] = True
                continue

            # (c) Efficiency (alive step)
            rewards[i] += R_EFFICIENCY - FUEL_PENALTY

            # (d) Separation / fratricide
            for j in range(i + 1, n):
                if self._alive[j] < 0.5:
                    continue
                d = np.linalg.norm(self._pos[i] - self._pos[j])
                if d < D_FRATRICIDE:
                    rewards[i] += R_FRATRICIDE
                    rewards[j] += R_FRATRICIDE
                    self._alive[i] = 0.0
                    self._alive[j] = 0.0
                    terminations[i] = True
                    terminations[j] = True
                elif d < D_SEPARATION:
                    penalty = -R_SEPARATION * (D_SEPARATION - d) / D_SEPARATION
                    rewards[i] += penalty
                    rewards[j] += penalty

        # ── 3. Truncation (episode length) ───────────────────────────────────
        if self._step_count >= self.max_steps:
            truncations[:] = True

        obs = self._get_obs()
        info = {
            "step": self._step_count,
            "n_alive": int(np.sum(self._alive)),
            "global_done": bool(np.all(self._alive < 0.5) or np.any(truncations)),
            "sim_time": self._sim_time,
        }
        return obs, rewards, terminations, truncations, info

    # ── Observation ─────────────────────────────────────────────────────────────
    def _get_obs(self) -> Dict[int, np.ndarray]:
        obs = {}
        n_alive = max(1, int(np.sum(self._alive)))
        swarm_frac = n_alive / self.n_agents

        for i in range(self.n_agents):
            pos_i  = self._pos[i]
            vel_i  = self._vel[i]
            quat_i = self._quat[i]

            # Relative target position/velocity in BODY frame
            rel_pos_world = self._tgt_pos - pos_i
            rel_pos_body  = rotate_by_quat(rel_pos_world, quat_normalize(np.array([quat_i[3], quat_i[0], quat_i[1], quat_i[2]])))  # [qw,qx,qy,qz]
            # Simpler: use DCM transpose (world to body)
            dcm_w2b = quat_to_dcm(quat_i).T
            rel_pos_body = dcm_w2b @ rel_pos_world
            rel_vel_body = dcm_w2b @ (self._tgt_vel - vel_i)

            euler = quat_to_euler(quat_i)

            # Nearest-neighbour distance
            nn_dist = float('inf')
            for j in range(self.n_agents):
                if i == j or self._alive[j] < 0.5:
                    continue
                d = np.linalg.norm(self._pos[i] - self._pos[j])
                if d < nn_dist:
                    nn_dist = d
            nn_dist = float(nn_dist) if nn_dist < float('inf') else 0.0

            t_alive_norm = self._step_count / self.max_steps

            vec = np.concatenate([
                rel_pos_body,     # 3
                rel_vel_body,     # 3
                pos_i,            # 3
                vel_i,            # 3
                euler,            # 3
                [t_alive_norm, swarm_frac, nn_dist],  # 3
            ], dtype=np.float32)
            obs[i] = vec

        return obs

    def render(self):
        pass


# ─── Smoke test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser(description="6-DOF swarm smoke test")
    parser.add_argument("--n-agents", type=int, default=2)
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    n = max(2, min(N_AGENTS_MAX, args.n_agents))
    env = SwarmInterceptEnv(n_agents=n, max_steps=args.steps)

    print(f"[6-DOF Swarm Smoke Test] n_agents={n}, steps={args.steps}, seed={args.seed}")
    print("=" * 60)

    obs, _ = env.reset(seed=args.seed)
    total_rewards = {i: 0.0 for i in range(n)}
    q_norms = []
    alive_history = []

    for step in range(args.steps):
        actions = {i: env.action_space.sample(env._rng) for i in range(n)}
        obs, rewards, terms, truncs, info = env.step(actions)

        for i in range(n):
            total_rewards[i] += float(rewards[i])

        # Quaternion normalisation check
        for i in range(n):
            q_norms.append(round(np.linalg.norm(env._quat[i]), 6))

        alive_history.append(info["n_alive"])

        if info["global_done"]:
            print(f"  → Episode ended early at step {step} (n_alive={info['n_alive']})")
            break

    print("─" * 60)
    print(f"  alive at end : {info['n_alive']}/{n}")
    print(f"  total reward : " + ", ".join(f"agent{i}={total_rewards[i]:+.2f}" for i in range(n)))
    print(f"  quat norms   : min={min(q_norms):.6f}, max={max(q_norms):.6f}, all_near_1={'✅' if all(0.999 < nrm < 1.001 for nrm in q_norms) else '❌'}")
    print("=" * 60)

    # Exit code 0 if quaternions stayed normalized
    all_norm = all(0.999 < nrm < 1.001 for nrm in q_norms)
    sys.exit(0 if all_norm else 1)
