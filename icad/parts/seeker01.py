"""
SEEKER-01 — Seeker Head Assembly (L3 Manufacturing)
"""
from build123d import *
import math

def build_seeker01(params: dict = None):
    params = params or {}
    D = params.get("diameter", 30.0)
    H = params.get("height", 25.0)

    with BuildPart() as p:
        Cylinder(D/2, H)
        with Locations((0, 0, H/2)):
            Sphere(D/2, mode=Mode.INTERSECT)
        Cylinder(D/2 - 2.0, H + 2, mode=Mode.SUBTRACT)
    return p.part
