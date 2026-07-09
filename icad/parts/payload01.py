"""
PAYLOAD-01 — Kinetic Payload (L3 Manufacturing)
"""
from build123d import *
import math

def build_payload01(params: dict = None):
    params = params or {}
    D = params.get("diameter", 25.0)
    L = params.get("length", 40.0)

    with BuildPart() as p:
        # Heavy core
        Cylinder(D/2, L)
        # Fragmentation grooves
        for z in [L*0.25, L*0.5, L*0.75]:
            with Locations((0, 0, z - L/2)):
                Torus(D/2, 1.5, mode=Mode.SUBTRACT)
    return p.part
