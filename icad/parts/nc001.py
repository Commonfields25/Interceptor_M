"""
NC-001 — Nose Cone (L3 Manufacturing)
Shape: Tangent Ogive
"""
from build123d import *
import math

def build_nc001(params: dict = None):
    params = params or {}
    L = params.get("length", 80.0)
    D = params.get("diameter", 35.0)
    wall = params.get("wall_thickness", 1.5)

    with BuildPart() as p:
        Cylinder(D/2, L)
        # Intersection with a larger sphere to approximate ogive/cone
        with Locations((0, 0, -L)):
             Sphere(math.sqrt(L**2 + (D/2)**2), mode=Mode.INTERSECT)
        Cylinder(D/2 - wall, L + 2, mode=Mode.SUBTRACT)
    return p.part
