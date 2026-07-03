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
GAMMA_AIR = 1.4
V_SON_NIVEAU_MER = 340.294

# 2. PLATFORM: DD-400 (Electric)
MASSE_INTERCEPTOR_KG = 0.400  # Constant mass (no propellant loss)
LONGUEUR_INTERCEPTOR_MM = 380
DIAMETRE_FUSELAGE_MM = 35
SURFACE_REF_M2 = 0.001

# 3. AERODYNAMICS
COEFF_TRAITEE_Cx_BASE = 0.35
COEFF_PORTANCE_CL_ALPHA = 2.0
ACCELERATION_LATERALE_MAX_G = 15.0 # Realistic for electric airframe
ACCELERATION_LATERALE_MAX_M_S2 = ACCELERATION_LATERALE_MAX_G * G0

# 4. PROPULSION (Electric & Pneumatic)
V_LAUNCH_M_S = 70.0           # Exit velocity from compressed air launcher
POUSSEE_DASH_N = 8.0          # Electric motor max thrust (Dash mode)
BATTERY_CAPACITY_J = 50000.0  # Joules available for dash
ENERGY_EFFICIENCY = 0.7       # Motor/Propeller efficiency

# 5. GUIDAGE
GAIN_PN = 3.0

# 6. NUMERICAL
PAS_DE_TEMPS_S = 0.005
DUREE_MAX_S = 60.0

# 7. ENGAGEMENT
RL_INTERCEPT_RADIUS_M = 2.0
RL_START_DISTANCE_M = 2000.0

# 8. ENVELOPPE E1
PORTEE_MIN_M = 100.0
PORTEE_MAX_M = 3000.0
ALTITUDE_MIN_M = 50.0
ALTITUDE_MAX_M = 1000.0
V_CIBLE_MAX_M_S = 120.0

# 9. DIVERS
GRAIN_ALEA = 42
