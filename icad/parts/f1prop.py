"""
F1-PROP — F1 Propeller Hub (Refined L3 - FPV Performance)
Material : 7075-T6 Aluminium / Carbon
Revision : v3.0-L3 (Dynamic Balance Features)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_f1prop(params: dict = None):
    params = params or {}
    hub_D = params.get("hub_diameter", 16.0)
    hub_H = params.get("hub_height", 10.0)

    m2_5 = Fasteners.METRIC["M2.5"]

    with BuildPart() as p:
        # 1. Tapered Hub with Rounded Nose
        Cylinder(hub_D / 2, hub_H - 2.0)
        with Locations((0, 0, hub_H - 2.0)):
            Sphere(hub_D / 2) # Aerodynamic nose cap

        # 2. Central Shaft Bore (Precision fit)
        Cylinder(2.5, hub_H + 5.0, mode=Mode.SUBTRACT)

        # 3. Dynamic Balance Pockets
        # (Weight reduction pockets that also allow for fine-balancing)
        for ang in range(45, 360, 90):
            rad = math.radians(ang)
            with Locations(( (hub_D/2 - 2.0)*math.cos(rad), (hub_D/2 - 2.0)*math.sin(rad), 2.0 )):
                Cylinder(1.5, hub_H, mode=Mode.SUBTRACT)

        # 4. Blade Mounting (M2.5 Tapped - Triple screw for security)
        for ang in [0, 120, 240]:
            rad = math.radians(ang)
            with Locations(( (hub_D/3)*math.cos(rad), (hub_D/3)*math.sin(rad), 0 )):
                Cylinder(m2_5["tap_drill"] / 2, 10.0, mode=Mode.SUBTRACT)

    return p.part
