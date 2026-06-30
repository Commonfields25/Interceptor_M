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
# CONSTANTES PHYSIQUES (en premier — utilisées par toutes les sections)
# =============================================================================
G0 = 9.80665                  # m/s² — pesanteur standard (ISA niveau mer)
MASSE_VOLUME_AIR_SLP = 1.225  # kg/m³ — masse volumique de l'air au niveau mer
V_SON_NIVEAU_MER = 340.294    # m/s — vitesse du son à 15 °C (ISA niveau mer)

# =============================================================================
# ENVELOPPE D'ENGAGEMENT (E1)
# =============================================================================
PORTEE_MIN_KM = 1.0            # km — borne inférieure de la zone d'engagement
PORTEE_MAX_KM = 12.0          # km — borne supérieure
PORTEE_MIN_M  = PORTEE_MIN_KM * 1e3    # m
PORTEE_MAX_M  = PORTEE_MAX_KM * 1e3    # m

ALTITUDE_MIN_M = 0.0           # m
ALTITUDE_MAX_M = 5000.0       # m

MACH_CIBLE_MAX = 2.5          # adimensionné — vitesse cible max
V_CIBLE_MAX_M_S = MACH_CIBLE_MAX * V_SON_NIVEAU_MER  # m/s

# =============================================================================
# INTERCEPTOR — MASSE ET GÉOMÉTRIE
# =============================================================================
MASSE_INTERCEPTOR_KG = 2.340               # kg (= 2340 g)
ACCELERATION_LATERALE_MAX_G = 25.0         # g — effort latéral max admissible
ACCELERATION_LATERALE_MAX_M_S2 = ACCELERATION_LATERALE_MAX_G * G0  # m/s²

# =============================================================================
# AÉRODYNAMIQUE — COEFFICIENTS (D2)
# =============================================================================
COEFF_TRAITEE_Cx = 0.35        # adimensionné — coefficient de traînée (ogive classique)
COEFF_PORTANCE_CL_ALPHA = 2.0  # 1/rad — dérivée de portance par angle d'incidence
SURFACE_REF_M2 = 0.01          # m² — maître-couple (ogive ~10 cm ø)

# =============================================================================
# GUIDAGE — LOI PROPORTIONNELLE (PN)
# =============================================================================
GAIN_PN = 4.0                  # adimensionné — gain de navigation (typique 3–5)

# =============================================================================
# SIMULATION NUMÉRIQUE
# =============================================================================
PAS_DE_TEMPS_S = 0.01          # s — pas d'intégration (Euler explicite)
DUREE_MAX_S = 60.0             # s — au-delà → engagement raté

# =============================================================================
# RL ENV — MEDIAN CALIBRATION (feat/env/rebalance)
#   Signal: random ~0%  trained ~15-40%
# =============================================================================
V_CIBLE_RL_M_S = 300.0         # m/s — vitesse cible médiane (dure, pas triviale)
RL_MAX_STEPS = 120             # steps — fenêtre d'engagement réalisable
RL_INTERCEPT_RADIUS_M = 8.0    # m — rayon d'interception
RL_START_DISTANCE_M = 5000.0  # m — distance initiale cible/interceptor (calibré)
RL_FUEL_PENALTY = 0.05         # par step — coût carburant

# =============================================================================
# MONTE CARLO
# =============================================================================
NB_TIRAGES = 10000            # nombre d'échantillons pour P(intercept)
GRAIN_ALEA = None             # None = aléatoire pur ; int = graine reproductible
