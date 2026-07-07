"""
F1-BODY-01 — F1 Drone Body Shell (Refined L3 - FPV Performance)
Material : Carbon Fiber / 7075-T6 | Process : CNC / SLS
Revision : v3.0-L3 (Standard Stack & Antenna Mount)
"""
from build123d import *
import math
from icad.standards import Fasteners

def build_f1body01(params: dict = None):
    params = params or {}
    L = params.get("length", 120.0)
    W = params.get("width", 80.0)
    H = params.get("height", 35.0)
    T = params.get("wall_thickness", 2.0)

    m3 = Fasteners.METRIC["M3"]
    m2 = Fasteners.METRIC["M2"]

    with BuildPart() as p:
        # 1. Aerodynamic Elliptical Body (Wider for stacks)
        with BuildSketch() as sk:
            Ellipse(L/2, W/2)
        extrude(amount=H)

        # 2. Hollow Shell
        with Locations((0, 0, T)):
            with BuildSketch() as sk2:
                Ellipse(L/2 - T, W/2 - T)
            extrude(amount=H, mode=Mode.SUBTRACT)

        # 3. Standard Mounting Stacks (Integrated into base)
        # 30.5 x 30.5 mm Stack
        for sx in [-1, 1]:
            for sy in [-1, 1]:
                with Locations((sx * 30.5 / 2, sy * 30.5 / 2, 0)):
                    Cylinder(3.5, T + 2.0, mode=Mode.ADD) # Small boss
                    Cylinder(m3["clearance"] / 2, T + 4.0, mode=Mode.SUBTRACT)

        # 20 x 20 mm Stack (Auxiliary)
        for sx in [-1, 1]:
            for sy in [-1, 1]:
                with Locations((sx * 20.0 / 2, sy * 20.0 / 2, 0)):
                    Cylinder(2.5, T + 2.0, mode=Mode.ADD)
                    Cylinder(m2["clearance"] / 2, T + 4.0, mode=Mode.SUBTRACT)

        # 4. Aerodynamic VTX Antenna Mount (Tail section)
        with Locations((L/2 - 5.0, 0, H - 5.0)):
            # Tilted antenna tube
            Cylinder(3.0, 15.0, rotation=Rot(0, 45, 0))
            # SMA/U.FL connector pass-through
            Cylinder(1.5, 20.0, rotation=Rot(0, 45, 0), mode=Mode.SUBTRACT)

        # 5. Camera Mounting Bracket (Nose section)
        with Locations((-L/2 + 10.0, 0, H/2)):
            Box(2.0, 19.0, 20.0, mode=Mode.SUBTRACT) # Standard 19mm micro cam slot

    return p.part
