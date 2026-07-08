"""
simulation/montecarlo_pintercept.py
====================================
Monte Carlo P(intercept) — Échantillonnage de l'enveloppe E1.
Optimized: Added parallel execution support for large batches.
"""

import math
import random
import statistics
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from . import constants as C
from .sim_6dof import (
    simulate_engagement,
    manoeuvre_rectiligne,
    manoeuvre_virage_constant,
)
from .flight_control_poc import GuidanceSystem

# ------------------------------------------------------------------
# Hot locals
# ------------------------------------------------------------------
_P_MIN = C.PORTEE_MIN_M
_P_MAX = C.PORTEE_MAX_M
_ALT_MIN = C.ALTITUDE_MIN_M
_ALT_MAX = C.ALTITUDE_MAX_M
_V_CIBLE = C.V_CIBLE_MAX_M_S

if C.GRAIN_ALEA is not None:
    random.seed(C.GRAIN_ALEA)
    np.random.seed(C.GRAIN_ALEA)


def tirer_config():
    alt_init_m = random.uniform(_ALT_MIN, _ALT_MAX)
    portee_cibl_m = random.uniform(_P_MIN, _P_MAX)
    alt_cibl_m = random.uniform(_ALT_MIN, _ALT_MAX)
    angle_cibl_rad = random.uniform(0.0, 2.0 * math.pi)

    pos_cible = [
        portee_cibl_m * math.cos(angle_cibl_rad),
        portee_cibl_m * math.sin(angle_cibl_rad),
        alt_cibl_m,
    ]

    cap_init_rad = angle_cibl_rad
    pos_init_i = [0.0, 0.0, alt_init_m]
    vel_init_i = 100.0

    vel_cible_m_s = random.uniform(50.0, 100.0)
    cap_cible_rad = angle_cibl_rad + math.pi + random.uniform(-0.2, 0.2)

    manoeuvre_fn = manoeuvre_rectiligne

    return {
        "pos_init_i": pos_init_i,
        "vel_init_i_m_s": vel_init_i,
        "cap_init_rad": cap_init_rad,
        "pos_cible": pos_cible,
        "vel_cible_m_s": vel_cible_m_s,
        "cap_cible_rad": cap_cible_rad,
        "manoeuvre_fn": manoeuvre_fn,
    }


def run_single_sim(seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    cfg = tirer_config()
    gs = GuidanceSystem()

    res = simulate_engagement(
        pos_init_m=cfg["pos_init_i"],
        vel_init_m_s=cfg.get("vel_init_i_m_s", cfg.get("vel_init_i", 100.0)),
        cap_init_rad=cfg["cap_init_rad"],
        pos_cible_m=cfg["pos_cible"],
        vel_cible_m_s=cfg["vel_cible_m_s"],
        cap_cible_rad=cfg["cap_cible_rad"],
        guidage_sys=gs,
        manoeuvre_c_fn=cfg["manoeuvre_fn"],
        keep_traj=False,
    )
    return res["intercept"], res["distance_min_m"]


def run_monte_carlo(nb_tirages=100, silencieux=False, parallel=True):
    if not silencieux:
        print(
            f"[Monte Carlo] Lancement de {nb_tirages} tirages (parallel={parallel})..."
        )

    succes = 0
    dist_mins = []

    if parallel and nb_tirages > 1:
        seeds = [random.randint(0, 1000000) for _ in range(nb_tirages)]
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(run_single_sim, seeds))

        for intercepted, dist in results:
            if intercepted:
                succes += 1
            dist_mins.append(dist)
    else:
        for i in range(nb_tirages):
            intercepted, dist = run_single_sim()
            if intercepted:
                succes += 1
            dist_mins.append(dist)

    p_estimee = succes / nb_tirages

    if not silencieux:
        print(f"  Succès              : {succes} / {nb_tirages}")
        print(f"  P(intercept)        : {p_estimee * 100:.2f} %")
        print(f"  Distance min moyenne: {statistics.mean(dist_mins):.2f} m")
        print(f"  Distance min min    : {min(dist_mins):.2f} m")

    return {
        "P_intercept": p_estimee,
        "nb_success": succes,
        "nb_tirages": nb_tirages,
    }


if __name__ == "__main__":
    run_monte_carlo(nb_tirages=100)
