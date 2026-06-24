"""
simulation/constants.py
=======================
Constantes partagées pour la chaîne de simulation E3 :
  - Enveloppe d'engagement (E1)
  - Paramètres interceptor
  - Coefficients aérodynamiques (D2)
  - Constantes physiques et atmosphériques
  - Paramètres numériques (PN, pas de temps, Monte Carlo)

Toutes les valeurs sont en unités SI sauf indication explicite.
"""

# =============================================================================
# ENVELOPPE D'ENGAGEMENT (E1)
# =============================================================================
PORTEE_MIN_KM = 1.0          # km — borne inférieure de la zone d'engagement
PORTEE_MAX_KM = 12.0         # km — borne supérieure
PORTEE_MIN_M  = PORTEE_MIN_KM * 1e3    # m
PORTEE_MAX_M  = PORTEE_MAX_KM * 1e3    # m

ALTITUDE_MIN_M = 0.0         # m
ALTITUDE_MAX_M = 5000.0      # m

MACH_CIBLE_MAX = 2.5         # vitesse cible max (adimensionné)
V_SON_NIVEAU_MER = 340.294   # m/s à 15 °C (ISA niveau mer)
V_CIBLE_MAX_M_S  = MACH_CIBLE_MAX * V_SON_NIVEAU_MER   # m/s


# =============================================================================
# INTERCEPTOR — MASSE ET GÉOMÉTRIE
# =============================================================================
MASSE_INTERCEPTOR_KG = 2.340            # kg (= 2340 g)
ACCELERATION_LATERALE_MAX_G = 25.0      # g — effort latéral max admissible
ACCELERATION_LATERALE_MAX_M_S2 = ACCELERATION_LATERALE_MAX_G * G0  # m/s²


# =============================================================================
# AÉRODYNAMIQUE — COEFFICIENTS (D2)
# =============================================================================
# Traînée —Cz = Cx  (coefficient de traînée, profil classique ogive)
COEFF_TRAITEE_Cx = 0.35                 # adimensionné — значение Cx для типовой острой головки

# Portance — C_L = C_L_alpha * alpha
COEFF_PORTANCE_CL_ALPHA = 2.0 * 0.1 * (180.0 / 3.14159)  # 1/rad — производная подъёмной силы par угол атаки

# Surface de référence (maître-couple)
SURFACE_REF_M2 = 0.01                   # m² (maître-couple, ogive ~10 cm ø)


# =============================================================================
# ATMOSPHÈRE ET PHYSIQUE
# =============================================================================
G0 = 9.80665                # m/s² — pesanteur standard (ISA)
MASSE_VOLUME_AIR_SLP = 1.225       # kg/m³ — masse volumique de l'air au niveau mer (ISA)
VITESSE_SON_SLP   = V_SON_NIVEAU_MER  # m/s — vitesse du son au niveau mer


# =============================================================================
# GUIDAGE — LOI PROPORTIONNELLE (PN)
# =============================================================================
# Gain de navigation PN  (typique : 3 – 5 pour un interceptor actif)
GAIN_PN = 4.0                # adimensionné


# =============================================================================
# SIMULATION NUMÉRIQUE
# =============================================================================
PAS_DE_TEMPS_S = 0.01       # s  — pas d'intégration (Euler explicite)
DUREE_MAX_S    = 60.0       # s  — au-delà on considère l'engagement comme raté


# =============================================================================
# MONTE CARLO
# =============================================================================
NB_TIRAGES    = 10000       # nombre d'échantillons pour le calcul de P(intercept)
GRAIN_ALEA    = None        # None = aléatoire ; int = graine reproductible
