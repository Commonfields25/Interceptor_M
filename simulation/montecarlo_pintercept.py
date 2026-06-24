"""
simulation/montecarlo_pintercept.py
====================================
Monte Carlo P(intercept) — Échantillonnage de l'enveloppe E1.

On tire nb_tirages configurations aléatoires dans l'enveloppe d'engagement E1
(portée, altitude, vitesse et cap de la cible) et on lance la simulation
6-DOF + guidage PN pour chaque configuration.

Résultat : estimation de P(intercept) avec intervalle de confiance à 95 %
(approximation gaussienne sur la proportion).

Le nombre de tirages est défini par NB_TIRAGES dans constants.py.
"""

import math
import random
import statistics
from . import constants as C
from .sim_6dof import simulate_engagement
from .flight_control_poc import loi_guidage


# =============================================================================
# GRAIN ALÉATOIRE (reproductibilité)
# =============================================================================
if C.GRAIN_ALEA is not None:
    random.seed(C.GRAIN_ALEA)


# =============================================================================
# GÉNÉRATION D'UNE CONFIGURATION ALÉATOIRE DANS E1
# =============================================================================
def tirer_config():
    """
    Tire une configuration aléatoire dans l'enveloppe d'engagement E1.

    L'interceptor parte de l'origine (0, 0, altitude_init)
    et vise la cible située à une portée aleatoire dans [PORTEE_MIN_M, PORTEE_MAX_M].

    Paramètres de la cible
    ---------------------
    - Portée  : uniforme dans [PORTEE_MIN_M, PORTEE_MAX_M]
    - Altitude : uniforme dans [ALTITUDE_MIN_M, ALTITUDE_MAX_M]
    - Vitesse : uniforme dans [0.3 * V_CIBLE_MAX_M_S, V_CIBLE_MAX_M_S]
    - Cap cible : uniforme dans [0, 2π]

    L'interceptor a un cap initiale orienté vers la cible.

    Retourne
    --------
    dict — dictionnaire de paramètres d'engagement
    """
    # --- Position et vitesse de l'interceptor ---
    portee_m   = random.uniform(C.PORTEE_MIN_M, C.PORTEE_MAX_M)
    alt_init_m = random.uniform(C.ALTITUDE_MIN_M, C.ALTITUDE_MAX_M)
    cap_rad    = random.uniform(0.0, 2.0 * math.pi)

    pos_init_i = [0.0, 0.0, alt_init_m]
    vel_init_i = C.V_CIBLE_MAX_M_S   # vitesse interceptor ≈ Mach 2

    # --- Cible : portée aléatoire dans E1, altitude aléatoire ---
    portee_cibl_m   = random.uniform(C.PORTEE_MIN_M, C.PORTEE_MAX_M)
    alt_cibl_m      = random.uniform(C.ALTITUDE_MIN_M, C.ALTITUDE_MAX_M)
    cap_cibl_rad    = random.uniform(0.0, 2.0 * math.pi)

    pos_cible = [
        portee_cibl_m * math.cos(cap_cibl_rad),
        portee_cibl_m * math.sin(cap_cibl_rad),
        alt_cibl_m,
    ]
    vel_cible_m_s = random.uniform(
        0.3 * C.V_CIBLE_MAX_M_S,
        C.V_CIBLE_MAX_M_S
    )
    cap_cible_rad = random.uniform(0.0, 2.0 * math.pi)

    return {
        "pos_init_i"    : pos_init_i,
        "vel_init_i_m_s": vel_init_i,
        "cap_init_rad"  : cap_rad,
        "pos_cible"     : pos_cible,
        "vel_cible_m_s" : vel_cible_m_s,
        "cap_cible_rad" : cap_cible_rad,
    }


# =============================================================================
# LANCEMENT D'UN TIRAGE
# =============================================================================
def un_tirage():
    """
    Tire une configuration, lance la simulation, retourne True si intercept.
    """
    cfg = tirer_config()
    res = simulate_engagement(
        pos_init_m    = cfg["pos_init_i"],
        vel_init_m_s  = cfg["vel_init_i_m_s"],
        cap_init_rad  = cfg["cap_init_rad"],
        pos_cible_m   = cfg["pos_cible"],
        vel_cible_m_s = cfg["vel_cible_m_s"],
        cap_cible_rad = cfg["cap_cible_rad"],
        guidage_fn    = loi_guidage,
        alpha_rad     = 0.05,      # rad — faible incidence pour portance initiale
    )
    return res["intercept"]


# =============================================================================
# MONTE CARLO
# =============================================================================
def run_monte_carlo(nb_tirages=None, silencieux=False):
    """
    Exécute le Monte Carlo complet.

    Paramètres
    ----------
    nb_tirages : int ou None — nombre de tirages (défaut : C.NB_TIRAGES)
    silencieux : bool         — supprimer les prints intermédiaires

    Retourne
    --------
    dict {
        "P_intercept"       : float — probabilité d'interception estimée
        "nb_success"        : int   — nombre d'interceptions réussies
        "nb_tirages"        : int   — nombre total de tirages effectués
        "IC_95_bas"         : float — borne inférieure de l'IC à 95 %
        "IC_95_haut"        : float — borne supérieure de l'IC à 95 %
        "temps_moyen_s"     : float — temps moyen d'engagement (succès only)
    }
    """
    if nb_tirages is None:
        nb_tirages = C.NB_TIRAGES

    if not silencieux:
        print(f"[Monte Carlo] Lancement de {nb_tirages} tirages...")
        print(f"  Enveloppe E1 : portée [{C.PORTEE_MIN_KM}–{C.PORTEE_MAX_KM} km], "
              f"altitude [{C.ALTITUDE_MIN_M:.0f}–{C.ALTITUDE_MAX_M:.0f} m]")
        print(f"  Accélération lat max : {C.ACCELERATION_LATERALE_MAX_G} g "
              f"({C.ACCELERATION_LATERALE_MAX_M_S2:.1f} m/s²)")
        print(f"  Gain PN : {C.GAIN_PN} | Pas de temps : {C.PAS_DE_TEMPS_S} s")
        print()

    succes       = 0
    temps_list   = []
    report_every = max(1, nb_tirages // 10)

    for i in range(nb_tirages):
        cfg = tirer_config()
        res = simulate_engagement(
            pos_init_m    = cfg["pos_init_i"],
            vel_init_m_s  = cfg["vel_init_i_m_s"],
            cap_init_rad  = cfg["cap_init_rad"],
            pos_cible_m   = cfg["pos_cible"],
            vel_cible_m_s = cfg["vel_cible_m_s"],
            cap_cible_rad = cfg["cap_cible_rad"],
            guidage_fn    = loi_guidage,
            alpha_rad     = 0.05,
        )

        if res["intercept"]:
            succes += 1
            temps_list.append(res["temps_s"])

        if not silencieux and (i + 1) % report_every == 0:
            pct = 100.0 * (i + 1) / nb_tirages
            p_obs = 100.0 * succes / (i + 1)
            print(f"  [{pct:4.0f}%] {i + 1}/{nb_tirages} tirages → "
                  f"P(intercept) observée ≈ {p_obs:.2f} %")

    p_estimee = succes / nb_tirages

    # Intervalle de confiance à 95 % (approximation gaussienne / Wald)
    # IC = p ± z_0.975 * sqrt(p*(1-p)/n)
    if nb_tirages > 0 and succes > 0 and succes < nb_tirages:
        z       = 1.96
        margen  = z * math.sqrt(p_estimee * (1.0 - p_estimee) / nb_tirages)
        ic_bas  = max(0.0, p_estimee - margen)
        ic_haut = min(1.0, p_estimee + margen)
    else:
        ic_bas  = p_estimee
        ic_haut = p_estimee

    temps_moy = statistics.mean(temps_list) if temps_list else None

    if not silencieux:
        print()
        print("=" * 55)
        print(f"  RÉSULTATS — {nb_tirages} tirages")
        print("=" * 55)
        print(f"  Succès              : {succes} / {nb_tirages}")
        print(f"  P(intercept)        : {p_estimee:.4f}  ({p_estimee * 100:.2f} %)")
        print(f"  IC 95 %             : [{ic_bas:.4f} – {ic_haut:.4f}]  "
              f"[{ic_bas * 100:.2f} % – {ic_haut * 100:.2f} %]")
        if temps_moy is not None:
            print(f"  Temps moyen (succès): {temps_moy:.3f} s")
        print("=" * 55)

    return {
        "P_intercept"   : p_estimee,
        "nb_success"    : succes,
        "nb_tirages"    : nb_tirages,
        "IC_95_bas"     : ic_bas,
        "IC_95_haut"    : ic_haut,
        "temps_moyen_s" : temps_moy,
    }


# =============================================================================
# AUTO-TEST (petit nombre de tirages pour validation rapide)
# =============================================================================
if __name__ == "__main__":
    print("[montecarlo_pintercept] === Auto-test (100 tirages) ===")
    resultat = run_monte_carlo(nb_tirages=100, silencieux=False)
    print()
    print("Module exécutable sans erreur — P(intercept) estimée.")
