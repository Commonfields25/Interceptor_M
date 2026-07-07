"""
SABOT-001 — Drone Sabot (Refined L3)
Material : ASA | Process : FDM / SLS
Revision : v3.1-L3 (Enhanced Reliability)
"""
from build123d import *
import math

def build_sabot001(params: dict = None):
    params = params or {}
    OD = params.get("outer_diameter", 39.8)
    ID = params.get("inner_diameter", 35.2)
    L = params.get("length", 60.0)

    with BuildPart() as p:
        # 1. Main Sabot Body (Single Shell with release line)
        Cylinder(OD / 2, L)
        Cylinder(ID / 2, L + 2, mode=Mode.SUBTRACT)

        # 2. Friction-Reducing Outer Surface (Spiral Groove)
        # Using a sweep or multiple torus for high-performance launch
        for i in range(10):
            with Locations((0, 0, (i+0.5) * L / 10)):
                Torus(OD/2, 0.5, mode=Mode.SUBTRACT)

        # 3. Structural Gussets (Reinforcing for pneumatic shock)
        for ang in range(0, 360, 60):
            rad = math.radians(ang)
            with Locations(( (ID/2 + 1.0)*math.cos(rad), (ID/2 + 1.0)*math.sin(rad), L/2 )):
                Box(1.0, 3.0, L, rotation=Rot(0, 0, math.degrees(ang)))

    return p.part
