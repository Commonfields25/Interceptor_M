"""
simulation/constants.py
=======================
Unified Physics & Engineering Constants — DD-400 Baseline
Corrected for Electric Propulsion & Pneumatic Launch.
"""

# 1. PHYSICAL CONSTANTS (ISA)
G0 = 9.80665                  # m/s²
T0_ISA = 288.15               # K
P0_ISA = 101325.0             # Pa
RHO0_ISA = 1.225              # kg/m³
L_ISA = 0.0065                # K/m
R_AIR = 287.05                # J/(kg·K)
V_SON_NIVEAU_MER = 340.294    # m/s

# 2. PLATFORM: DD-400 (Baseline v1.2.0)
MASSE_INTERCEPTOR_KG = 0.400  # kg (MTOW)
MASSE_PROPELLANT_KG = 0.000   # kg (Electric Dash = Constant Mass)
LONGUEUR_INTERCEPTOR_MM = 380
DIAMETRE_FUSELAGE_MM = 35
SURFACE_REF_M2 = 0.001        # pi * (0.035/2)^2 approx 0.001

# 3. AERODYNAMICS
COEFF_TRAITEE_Cx_BASE = 0.35
COEFF_PORTANCE_CL_ALPHA = 2.0
ACCELERATION_LATERALE_MAX_G = 15.11 # P95 Envelope from Physics Report
ACCELERATION_LATERALE_MAX_M_S2 = ACCELERATION_LATERALE_MAX_G * G0

# 4. PROPULSION (Electric Dash)
POUSSEE_MAX_N = 8.0           # 8N sustained electric thrust (ref SITUATION_REPORT)
DUREE_COMBUSTION_S = 60.0     # 60s dash capacity (ref Consolidated Def)
ISP_S = 0.0                   # Not applicable for Electric
TWR_DD = POUSSEE_MAX_N / (MASSE_INTERCEPTOR_KG * G0)

# 5. GUIDAGE
GAIN_PN = 4.0

# 6. NUMERICAL
PAS_DE_TEMPS_S = 0.01
DUREE_MAX_S = 60.0

# 7. ENGAGEMENT
RL_INTERCEPT_RADIUS_M = 2.0
RL_START_DISTANCE_M = 3000.0

# 8. ENVELOPPE E1
PORTEE_MIN_M = 500.0
PORTEE_MAX_M = 5000.0
PORTEE_MIN_KM = PORTEE_MIN_M / 1000.0
PORTEE_MAX_KM = PORTEE_MAX_M / 1000.0
ALTITUDE_MIN_M = 100.0
ALTITUDE_MAX_M = 2000.0
V_CIBLE_MAX_M_S = 150.0

# 9. DIVERS
GRAIN_ALEA = 42
