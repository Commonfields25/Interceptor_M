"""
simulation/constants.py
=======================
Unified Physics & Engineering Constants — DD-400 Baseline
"""

# 1. PHYSICAL CONSTANTS
G0 = 9.80665                  # m/s²
MASSE_VOLUME_AIR_SLP = 1.225  # kg/m³
V_SON_NIVEAU_MER = 340.294    # m/s
H_SCALE = 8500.0              # m

# 2. PLATFORM: DD-400 (Locked 2026-06-29)
MASSE_INTERCEPTOR_KG = 0.400  # kg
LONGUEUR_INTERCEPTOR_MM = 380 # mm
DIAMETRE_FUSELAGE_MM = 35     # mm
SURFACE_REF_M2 = 0.001        # m² (approx 35mm dia)

# 3. AERODYNAMICS (D2)
COEFF_TRAITEE_Cx = 0.35       # Cd
COEFF_PORTANCE_CL_ALPHA = 2.0 # per rad
ACCELERATION_LATERALE_MAX_G = 25.0

# 4. PROPULSION (SC-02)
POUSSEE_MAX_N = 12.0          # N
TWR_DD = POUSSEE_MAX_N / (MASSE_INTERCEPTOR_KG * G0) # ~3.06

# 5. NUMERICAL
PAS_DE_TEMPS_S = 0.01         # s
DUREE_MAX_S = 60.0            # s

# 6. RL MEDIAN
RL_INTERCEPT_RADIUS_M = 2.0   # m
RL_START_DISTANCE_M = 3000.0  # m
