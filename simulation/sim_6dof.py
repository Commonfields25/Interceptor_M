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
def densite(altitude_m):
    """
    Masse volumique de l'air en fonction de l'altitude (modèle isotherme simple).
    Retourne kg/m³.
    """
    h_scale = 8500.0           # m — hauteur d'échelle de l'atmosphère
    rho_0   = C.MASSE_VOLUME_AIR_SLP
    return rho_0 * math.exp(-altitude_m / h_scale)


# =============================================================================
# ACTIONS AÉRODYNAMIQUES
# =============================================================================
def trainee(vitesse_m_s, altitude_m):
    """
    Module de la force de traînée (N).
    D = 0.5 * rho * v² * S_ref * Cx
    """
    rho = densite(altitude_m)
    return 0.5 * rho * (vitesse_m_s ** 2.0) * C.SURFACE_REF_M2 * C.COEFF_TRAITEE_Cx


def portance(vitesse_m_s, incidence_rad, altitude_m):
    """
    Module de la force de portance (N).
    L = 0.5 * rho * v² * S_ref * C_L_alpha * alpha
    """
    rho = densite(altitude_m)
    c_l = C.COEFF_PORTANCE_CL_ALPHA * incidence_rad
    return 0.5 * rho * (vitesse_m_s ** 2.0) * C.SURFACE_REF_M2 * c_l


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
    # Vitesse dans le repère ENG (x = Nord, y = Est, z = Haut)
    vx = vitesse_m_s * math.cos(cap_rad)
    vy = vitesse_m_s * math.sin(cap_rad)
    vz = 0.0  # vol planar (pas de pente initiale)

    return {
        "position": list(position_m),    # [x, y, z]
        "vitesse" : [vx, vy, vz],        # [vx, vy, vz]
        "masse"   : C.MASSE_INTERCEPTOR_KG,
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

    # Modules
    vx, vy, vz = vel
    vitesse_module = math.sqrt(vx**2 + vy**2 + vz**2)

    # Sécurité : si vitesse quasi-nulle, on garde le cap
    if vitesse_module < 0.1:
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # Direction unitaire de la vitesse
    ux = vx / vitesse_module
    uy = vy / vitesse_module
    uz = vz / vitesse_module

    # Repère local (T, N, B) — tangent, normal (vertical), binormal (lateral)
    # Plan de vol : T = [ux, uy, uz]
    # N (vertical dans le plan) : projection de la gravité + portance
    grav_z = -C.G0
    portance_z = portance(vitesse_module, alpha_rad, pos[2]) / C.MASSE_INTERCEPTOR_KG
    accel_verticale = grav_z + portance_z

    # Normalisé dans le plan
    norm_plan = math.sqrt(ux**2 + uy**2 + 0.0001)
    nx = 0.0
    ny = 0.0
    nz = (accel_verticale / abs(accel_verticale + 0.001)) if abs(accel_verticale) > 0.001 else 0.0

    # Binormal (perpendiculaire au plan) = direction de la commande latérale
    bx = -uy
    by =  ux
    bz = 0.0
    norm_b = math.sqrt(bx**2 + by**2 + bz**2) + 1e-9
    bx /= norm_b
    by /= norm_b
    bz /= norm_b

    # Traînée (opposée à la vitesse)
    d_tr = trainee(vitesse_module, pos[2]) / C.MASSE_INTERCEPTOR_KG

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
   derivees(etat, alpha_rad, lat_accel_m_s2)
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
                        guidage_fn=None, alpha_rad=0.0):
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

    Retourne
    --------
    dict {
        "intercept"  : bool   — True si intercept atteint
        "temps_s"    : float  — durée de l'engagement ou DUREE_MAX_S
        "trajectoire": list   — liste de {t, x, y, z} (sous-échantillonné)
        "distance_min_m": float — distance minimale atteinte
    }
    """
    etat_i = etat_initial(pos_init_m, vel_init_m_s, cap_init_rad)

    # État de la cible (rectiligne uniforme)
    vcx = vel_cible_m_s * math.cos(cap_cible_rad)
    vcy = vel_cible_m_s * math.sin(cap_cible_rad)
    pos_c = list(pos_cible_m)

    temps   = 0.0
    dt      = C.PAS_DE_TEMPS_S
    traj    = []
    dist_min = float("inf")
    intercept = False

    # Seuil d'interception (distance < seuil → intercept)
    SEUIL_INTERCEPT_M = 5.0     # m — distance à partir de laquelle on considère l'interception

    while temps < C.DUREE_MAX_S:

        # Sous-échantillonnage pour la trajectoire (tous les 0.1 s)
        if len(traj) == 0 or (temps - traj[-1]["t"]) >= 0.1:
            traj.append({
                "t": round(temps, 3),
                "x": round(etat_i["position"][0], 1),
                "y": round(etat_i["position"][1], 1),
                "z": round(etat_i["position"][2], 1),
            })

        # Distance interceptor / cible
        dx = etat_i["position"][0] - pos_c[0]
        dy = etat_i["position"][1] - pos_c[1]
        dz = etat_i["position"][2] - pos_c[2]
        dist = math.sqrt(dx**2 + dy**2 + dz**2)

        if dist < dist_min:
            dist_min = dist

        # Test d'interception
        if dist < SEUIL_INTERCEPT_M:
            intercept = True
            break

        # Commande de guidage (ou zéro si pas de loi)
        lat_accel = 0.0
        if guidage_fn is not None:
            lat_accel = guidage_fn(etat_i, {"position": pos_c, "vitesse": [vcx, vcy, 0.0]})
            # Saturation en accélération latérale
            lat_accel = max(-C.ACCELERATION_LATERALE_MAX_M_S2,
                            min(C.ACCELERATION_LATERALE_MAX_M_S2, lat_accel))

        # Intégration interceptor
        integrer(etat_i, alpha_rad, lat_accel, dt)

        # Avance cible
        pos_c[0] += vcx * dt
        pos_c[1] += vcy * dt

        temps += dt

    return {
        "intercept"     : intercept,
        "temps_s"       : round(temps, 3),
        "trajectoire"   : traj,
        "distance_min_m": round(dist_min, 2),
    }


# =============================================================================
# AUTO-TEST
# =============================================================================
if __name__ == "__main__":
    # Scénario simple : interceptor en (0,0,500), cible en (3000,0,500)
    # Vitesse égale → intercept impossible sans guidage
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