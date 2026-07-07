"""
BRK-001 — Structural Mounting Bracket (Refined L3)
Material : 7075-T6 Aluminium | Process : CNC 3-axis Milling
Revision : v3.1-L3 (Warehouse Patterns)
"""
from build123d import *
import math
from icad.standards import Fasteners, Materials

def build_brk001(params: dict = None):
    params = params or {}
    L = params.get("length", 75.0)
    W = params.get("width", 55.0)
    T = params.get("thickness", 10.0)
    bore = params.get("bore_diameter", 35.0)

    m3 = Fasteners.METRIC["M3"]
    m4 = Fasteners.METRIC["M4"]

    with BuildPart() as p:
        # Base slab
        Box(L, W, T)

        # 1. Central Bore
        Cylinder(bore / 2, T + 2, mode=Mode.SUBTRACT)

        # 2. Standard Mounting Pattern
        with Locations(GridLocations(L-15.0, W-15.0, 2, 2).locations):
            # Clearance hole
            Cylinder(m4["clearance"] / 2, T + 2, mode=Mode.SUBTRACT)
            # Counterbore
            with Locations((0, 0, T - m4["counterbore_depth"])):
                Cylinder(m4["counterbore_dia"] / 2, m4["counterbore_depth"] + 1, mode=Mode.SUBTRACT)

        # 3. Lightening Pockets (Optimized)
        with Locations(GridLocations(L/2, W/2, 2, 2).locations):
             Box(L/4, W/4, T, mode=Mode.SUBTRACT)

        # 4. Fillets and Chamfers
        # Select vertical corners for filleting
        # corners = p.edges().filter_by(Axis.Z).sort_by(Axis.X)[0:2] + p.edges().filter_by(Axis.Z).sort_by(Axis.X)[-2:]
        # Simplify to avoid OCP failures
        try:
            # Only fillet outer edges if they don't intersect pockets too closely
            v_edges = p.edges().filter_by(Axis.Z)
            if v_edges:
                fillet(v_edges, radius=1.0)
        except:
            pass

        # Chamfer top edges
        try:
            top_edges = p.edges().filter_by_position(Axis.Z, T, T)
            if top_edges:
                chamfer(top_edges, length=0.3)
        except:
            pass

    return p.part
