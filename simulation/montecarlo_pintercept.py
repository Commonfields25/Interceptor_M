import math, random, numpy as np
from . import constants as C
from .sim_6dof import simulate_engagement
from .flight_control_poc import GuidanceSystem
_P_MIN, _P_MAX, _ALT_MIN, _ALT_MAX, _V_CIBLE, _V_LAUNCH = C.PORTEE_MIN_M, C.PORTEE_MAX_M, C.ALTITUDE_MIN_M, C.ALTITUDE_MAX_M, C.V_CIBLE_MAX_M_S, C.V_LAUNCH_M_S
def tirer_config():
    a_i, p_c, a_c, ang = random.uniform(_ALT_MIN,_ALT_MAX), random.uniform(_P_MIN,_P_MAX), random.uniform(_ALT_MIN,_ALT_MAX), random.uniform(0, 2*math.pi)
    return {"p_i": [0,0,a_i], "v_i": _V_LAUNCH, "c_i": ang, "p_c": [p_c*math.cos(ang), p_c*math.sin(ang), a_c], "v_c_m": random.uniform(30,_V_CIBLE), "c_c": ang+math.pi+random.uniform(-0.5,0.5)}
def run_monte_carlo(nb=20, mode="APN"):
    s = 0
    for i in range(nb):
        c = tirer_config(); gs = GuidanceSystem(mode=mode, latency_steps=10)
        if simulate_engagement(c["p_i"], c["v_i"], c["c_i"], c["p_c"], c["v_c_m"], c["c_c"], gs=gs)["intercept"]: s += 1
    return s / nb
if __name__ == "__main__":
    for m in ["PN", "APN"]: print(f"Mode {m}: P(int) = {run_monte_carlo(20, m)*100}%")
