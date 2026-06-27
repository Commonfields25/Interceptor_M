"""
simulation/flight_control_poc.py
================================
Loi de guidage Proportional Navigation (PN) avec commande bang-bang
sur l'accélération latérale.

Principe
--------
On calcule la vitesse de rotation de la ligne de visée (LOS) entre
l'interceptor et la cible. La PN commande une accélération latérale
proportionnelle à cette vitesse de rotation, multipliée par le gain PN.

Commande bang-bang : la saturation en accélération latérale est appliquée
par le modèle de vol (sim_6dof.py) ; ici on возвращает le sinal brut
qui sera saturé en aval.

Fonction principale : proportional_navigation(etat_interceptor, etat_cible)
"""

import math
from . import constants as C


# =============================================================================
# PROPORTIONAL NAVIGATION (PN)
# =============================================================================
def proportional_navigation(etat_interceptor, etat_cible):
    """
    Calcule l'accélération latérale de commande selon la loi PN classique.

    a_cmd = N * |V_rel| * omega_LOS

    où :
      N      = gain de navigation (C.GAIN_PN)
      V_rel  = vitesse relative interceptor – cible
      omega_LOS = vitesse angulaire de la ligne de visée (LOS)

    Paramètres
    ----------
    etat_interceptor : dict — état de l'interceptor (doit contenir "position", "vitesse")
    etat_cible       : dict — état de la cible (doit contenir "position", "vitesse")

    Retourne
    --------
    float — accélération latérale commandée en m/s² (signe : vers la cible)
    """
    # Vecteurs position et vitesse
    pos_i = etat_interceptor["position"]
    pos_c = etat_cible["position"]
    vel_i = etat_interceptor["vitesse"]
    vel_c = etat_cible.get("vitesse", [0.0, 0.0, 0.0])

    # Ligne de visée (LOS) : interceptor → cible
    los_x = pos_c[0] - pos_i[0]
    los_y = pos_c[1] - pos_i[1]
    los_z = pos_c[2] - pos_i[2]

    norme_los = math.sqrt(los_x**2 + los_y**2 + los_z**2)
    if norme_los < 0.1:
        return 0.0   # trop près — pas de guidage significatif

    # Vitesse relative
    vrx = vel_i[0] - vel_c[0]
    vry = vel_i[1] - vel_c[1]
    vrz = vel_i[2] - vel_c[2]

    # Produit croisé LOS × V_rel  (perpendiculaire au plan LOS)
    cx = los_y * vrz - los_z * vry
    cy = los_z * vrx - los_x * vrz
    cz = los_x * vry - los_y * vrx

    # Dérivée de la LOS : (LOS × V_rel) / |LOS|²
    omega_x = cx / (norme_los ** 2.0)
    omega_y = cy / (norme_los ** 2.0)
    omega_z = cz / (norme_los ** 2.0)

    # Module de la vitesse de rotation LOS
    omega_LOS = math.sqrt(omega_x**2 + omega_y**2 + omega_z**2)

    # Vitesse relative module
    v_rel = math.sqrt(vrx**2 + vry**2 + vrz**2)

    # Commande PN : a = N * V_rel * omega_LOS
    a_cmd = C.GAIN_PN * v_rel * omega_LOS

    # Direction : on projette sur le vecteur croisé LOS × omega_LOS
    # pour déterminer le signe (gauche / droite du plan de collision)
    los_unit_x = los_x / norme_los
    los_unit_y = los_y / norme_los
    los_unit_z = los_z / norme_los

    signe = (omega_y * los_unit_x - omega_x * los_unit_y)
    if abs(signe) > 1e-9:
        direction = 1.0 if signe > 0.0 else -1.0
        a_cmd = direction * abs(a_cmd)
    else:
        a_cmd = 0.0

    return a_cmd


# =============================================================================
# INTERFACE DE GUIDAGE (compatible avec simulate_engagement)
# =============================================================================
def loi_guidage(etat_interceptor, etat_cible):
    """
    Interface dewrapper pour proportional_navigation.
    Retourne la commande d'accélération latérale en m/s².
    Compatible avec le paramètre guidage_fn de sim_6dof.simulate_engagement.
    """
    return proportional_navigation(etat_interceptor, etat_cible)


# =============================================================================
# AUTO-TEST
# =============================================================================
if __name__ == "__main__":
    print("[flight_control_poc] Test de la loi PN...")
    import math

    # Cible en approche : interceptor à (0,0,500), cible à (2000,0,500)
    etat_i = {
        "position": [0.0, 0.0, 500.0],
        "vitesse" : [300.0 * math.cos(0.0), 300.0 * math.sin(0.0), 0.0],
    }
    etat_c = {
        "position": [2000.0, 0.0, 500.0],
        "vitesse" : [-200.0, 0.0, 0.0],
    }

    a_cmd = proportional_navigation(etat_i, etat_c)
    print(f"  → Commande latérale a_cmd = {a_cmd:.2f} m/s²")

    if abs(a_cmd) > C.ACCELERATION_LATERALE_MAX_M_S2:
        print(f"  → Saturation à {C.ACCELERATION_LATERALE_MAX_M_S2:.1f} m/s² "
              f"(limite {C.ACCELERATION_LATERALE_MAX_G} g)")
    else:
        print(f"  → Commande dans la plage admissible ({C.ACCELERATION_LATERALE_MAX_G} g max)")

    print("[flight_control_poc] OK — module exécutable sans erreur.")