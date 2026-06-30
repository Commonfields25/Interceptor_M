"""
simulation/sim_6dof.py
======================
Modèle de vol simplifié 6-DOF (point-masse 3D).

L'interceptor est modélisé comme un point matériel de masse m avec :
  - Traînée proportionnelle à v² et Cx
  - Portance perpendiculaire à la vitesse (commande en incidence / alpha)
  - Poussée axiale (nulle par défaut — missile purement réactif)
  - Gravité
  - Accélération latérale limitée à ACCELERATION_LATERALE_MAX

Le pilote (flight_control_poc.py) fournit la commande d'accélération latérale
en sortie de la loi PN ; ce module intègre la dynamique 3D correspondante.

Fonction principale : simulate_engagement(...)
"""

import math
from . import constants as C

# ------------------------------------------------------------------
# Hot locals — bound once, reused in every derivees() call
# ------------------------------------------------------------------
_M_G         = C.MASSE_INTERCEPTOR_KG
_S_REF       = C.SURFACE_REF_M2
_CX_DRAG     = C.COEFF_TRAITEE_Cx
_CL_ALPHA    = C.COEFF_PORTANCE_CL_ALPHA
_G0          = C.G0
_DUREE_MAX   = C.DUREE_MAX_S
_DT          = C.PAS_DE_TEMPS_S
_SEUIL_SQ    = 5.0 * 5.0          # SEUIL_INTERCEPT_M² (avoids sqrt in loop)
_ACCEL_MAX   = C.ACCELERATION_LATERALE_MAX_M_S2


# =============================================================================
# CONVERSION ANGULAIRE
# =============================================================================
def deg_to_rad(d):
    return d * math.pi / 180.0


def rad_to_deg(r):
    return r * 180.0 / math.pi


# =============================================================================
# MODÈLE ATMOSPHÉRIQUE (ISA niveau mer — simplification)
# =============================================================================
_H_SCALE   = 8500.0           # m — hauteur d'échelle de l'atmosphère
_RHO_0     = C.MASSE_VOLUME_AIR_SLP

def densite(altitude_m):
    """
    Masse volumique de l'air en fonction de l'altitude (modèle isotherme simple).
    Retourne kg/m³.
    """
    return _RHO_0 * math.exp(-altitude_m / _H_SCALE)


# =============================================================================
# ACTIONS AÉRODYNAMIQUES
# =============================================================================
def trainee(vitesse_m_s, altitude_m):
    """
    Module de la force de traînée (N).
    D = 0.5 * rho * v² * S_ref * Cx
    """
    rho = densite(altitude_m)
    return 0.5 * rho * (vitesse_m_s ** 2.0) * _S_REF * _CX_DRAG


def portance(vitesse_m_s, incidence_rad, altitude_m):
    """
    Module de la force de portance (N).
    L = 0.5 * rho * v² * S_ref * C_L_alpha * alpha
    """
    rho = densite(altitude_m)
    c_l = _CL_ALPHA * incidence_rad
    return 0.5 * rho * (vitesse_m_s ** 2.0) * _S_REF * c_l


# =============================================================================
# ÉTAT INITIAL
# =============================================================================
def etat_initial(position_m, vitesse_m_s, cap_rad):
    """
    Construire un dictionnaire d'état pour l'intégrateur.

    Paramètres
    ----------
    position_m : list[float, float, float]  [x, y, z] en m
    vitesse_m_s  : float  module de la vitesse en m/s
    cap_rad      : float  cap (azimut) en rad

    Retourne
    --------
    dict — état complet du système
    """
    vx = vitesse_m_s * math.cos(cap_rad)
    vy = vitesse_m_s * math.sin(cap_rad)
    vz = 0.0  # vol planar (pas de pente initiale)

    return {
        "position": list(position_m),    # [x, y, z]
        "vitesse" : [vx, vy, vz],        # [vx, vy, vz]
        "masse"   : _M_G,
    }


# =============================================================================
# DÉRIVÉES (équations du mouvement)
# =============================================================================
def derivees(etat, alpha_rad, lat_accel_m_s2):
    """
    Calcul des dérivées de l'état (Euler explicite).

    Paramètres
    ----------
    etat          : dict  — état actuel (position, vitesse, masse)
    alpha_rad     : float — angle d'incidence en rad (portance)
    lat_accel_m_s2 : float — accélération latérale commandée en m/s² (axe perpendiculaire au plan de vol)

    Retourne
    --------
    list — [dx, dy, dz, dvx, dvy, dvz]
    """
    pos = etat["position"]
    vel = etat["vitesse"]

    vx, vy, vz = vel
    v_sq = vx*vx + vy*vy + vz*vz
    vitesse_module = math.sqrt(v_sq)

    # Sécurité : si vitesse quasi-nulle, on garde le cap
    if vitesse_module < 0.1:
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    inv_v = 1.0 / vitesse_module
    ux = vx * inv_v
    uy = vy * inv_v
    uz = vz * inv_v

    # Repère local (T, N, B) — tangent, normal (vertical), binormal (lateral)
    grav_z = -_G0
    portance_z = portance(vitesse_module, alpha_rad, pos[2]) / _M_G
    accel_verticale = grav_z + portance_z

    norm_plan = math.sqrt(ux*ux + uy*uy + 0.0001)
    nz = (1.0 if accel_verticale > 0.001 else -1.0) if abs(accel_verticale) > 0.001 else 0.0

    # Binormal (perpendiculaire au plan) = direction de la commande latérale
    bx = -uy
    by =  ux
    bz = 0.0
    norm_b = math.sqrt(bx*bx + by*by + bz*bz) + 1e-9
    bx /= norm_b
    by /= norm_b
    bz /= norm_b

    # Traînée (opposée à la vitesse)
    d_tr = trainee(vitesse_module, pos[2]) / _M_G

    # Accélérations dans chaque direction
    dvx = -d_tr * ux + lat_accel_m_s2 * bx
    dvy = -d_tr * uy + lat_accel_m_s2 * by
    dvz = -d_tr * uz + lat_accel_m_s2 * bz + accel_verticale * nz

    return [vx, vy, vz, dvx, dvy, dvz]


# =============================================================================
# INTÉGRATION (Euler explicite)
# =============================================================================
def integrer(etat, alpha_rad, lat_accel_m_s2, dt):
    """
    Avance l'état d'un pas de temps dt (méthode d'Euler explicite).
    """
    dr = derivees(etat, alpha_rad, lat_accel_m_s2)
    pos = etat["position"]
    vel = etat["vitesse"]

    pos[0] += dr[0] * dt
    pos[1] += dr[1] * dt
    pos[2] += dr[2] * dt

    vel[0] += dr[3] * dt
    vel[1] += dr[4] * dt
    vel[2] += dr[5] * dt

    return etat


# =============================================================================
# SIMULATION D'UN ENGAGEMENT COMPLET
# =============================================================================
def simulate_engagement(pos_init_m, vel_init_m_s, cap_init_rad,
                        pos_cible_m,   vel_cible_m_s, cap_cible_rad,
                        guidage_fn=None, alpha_rad=0.0,
                        keep_traj=False):
    """
    Simule un engagement interceptor / cible.

    L'interceptor démarre en pos_init_m et tente d'intercepter la cible
    qui suit une trajectoire rectiligne à vitesse constante.

    Paramètres
    ----------
    pos_init_m      : [float, float, float]  position initiale interceptor [x, y, z] en m
    vel_init_m_s    : float                  vitesse module interceptor en m/s
    cap_init_rad    : float                  cap initial interceptor en rad
    pos_cible_m     : [float, float, float]  position initiale cible
    vel_cible_m_s   : float                  vitesse module cible en m/s
    cap_cible_rad   : float                  cap cible en rad
    guidage_fn      : callable               fonction(etat_i, etat_c) -> lat_accel_m_s2
                                             ou None (vol en ligne droite)
    alpha_rad       : float                  angle d'incidence (portance), rad
    keep_traj       : bool                   si True, construit la trajectoire sous-échantillonnée;
                                             si False (défaut), renvoie [] pour perf.

    Retourne
    --------
    dict {
        "intercept"  : bool   — True si intercept atteint
        "temps_s"    : float  — durée de l'engagement ou DUREE_MAX_S
        "trajectoire": list   — liste de {t, x, y, z} (sous-échantillonné) ou []
        "distance_min_m": float — distance minimale atteinte
    }
    """
    etat_i = etat_initial(pos_init_m, vel_init_m_s, cap_init_rad)

    # État de la cible (rectiligne uniforme) — bound as locals
    vcx = vel_cible_m_s * math.cos(cap_cible_rad)
    vcy = vel_cible_m_s * math.sin(cap_cible_rad)
    pos_cx = pos_cible_m[0]
    pos_cy = pos_cible_m[1]
    pos_cz = pos_cible_m[2]

    temps = 0.0
    traj  = [] if keep_traj else None          # alloc only when needed
    dist_min_sq = float("inf")
    intercept = False

    while temps < _DUREE_MAX:

        # Sous-échantillonnage pour la trajectoire (tous les 0.1 s)
        if traj is not None:
            if len(traj) == 0 or (temps - traj[-1]["t"]) >= 0.1:
                traj.append({
                    "t": round(temps, 3),
                    "x": round(etat_i["position"][0], 1),
                    "y": round(etat_i["position"][1], 1),
                    "z": round(etat_i["position"][2], 1),
                })

        # Distance interceptor / cible — compare squared to avoid sqrt
        dx = etat_i["position"][0] - pos_cx
        dy = etat_i["position"][1] - pos_cy
        dz = etat_i["position"][2] - pos_cz
        dist_sq = dx*dx + dy*dy + dz*dz

        if dist_sq < dist_min_sq:
            dist_min_sq = dist_sq

        # Test d'interception via squared threshold
        if dist_sq < _SEUIL_SQ:
            intercept = True
            break

        # Commande de guidage (ou zéro si pas de loi)
        lat_accel = 0.0
        if guidage_fn is not None:
            lat_accel = guidage_fn(etat_i, {"position": [pos_cx, pos_cy, pos_cz],
                                             "vitesse": [vcx, vcy, 0.0]})
            # Saturation en accélération latérale
            if lat_accel > _ACCEL_MAX:
                lat_accel = _ACCEL_MAX
            elif lat_accel < -_ACCEL_MAX:
                lat_accel = -_ACCEL_MAX

        # Intégration interceptor
        integrer(etat_i, alpha_rad, lat_accel, _DT)

        # Avance cible
        pos_cx += vcx * _DT
        pos_cy += vcy * _DT

        temps += _DT

    return {
        "intercept"     : intercept,
        "temps_s"      : round(temps, 3),
        "trajectoire"  : traj if traj is not None else [],
        "distance_min_m": round(math.sqrt(dist_min_sq), 2),
    }


# =============================================================================
# AUTO-TEST
# =============================================================================
if __name__ == "__main__":
    res = simulate_engagement(
        pos_init_m    = [0.0, 0.0, 500.0],
        vel_init_m_s  = 300.0,
        cap_init_rad  = 0.0,
        pos_cible_m   = [3000.0, 0.0, 500.0],
        vel_cible_m_s = 300.0,
        cap_cible_rad = math.pi,
        guidage_fn    = None,
        alpha_rad     = 0.0,
    )
    print(f"[sim_6dof] Test sans guidage → intercept={res['intercept']}, "
          f"dist_min={res['distance_min_m']} m, t={res['temps_s']} s")
    print("[sim_6dof] OK — le module s'exécute sans erreur.")
