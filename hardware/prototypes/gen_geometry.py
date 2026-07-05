"""
hardware/prototypes/gen_geometry.py
====================================
High-Fidelity Parametric Geometry Generator for Interceptor_M (DD-400).
"""

import json
import math
import os

def load_params():
    with open("PARAMETERS.json", "r") as f:
        return json.load(f)

def generate_fuselage(g):
    od, t, l = g["od_mm"], g["wall_thickness_mm"], g["length_mm"]
    vol = math.pi * ((od/2)**2 - (od/2 - t)**2) * l
    return {"id": "FUS-001", "name": "Fuselage Tube", "material": "Al-7075 T6", "mass_g": round(vol * 2.71e-3, 1)}

def generate_bracket(g):
    id_tube = g["od_mm"] - 2*g["wall_thickness_mm"]
    l = 30.0 # Reduced from 40 to save mass
    vol = math.pi * (id_tube/2)**2 * 0.3 * l # 30% density
    return {"id": "BRK-001", "name": "Structural Bracket", "material": "AlSi10Mg", "mass_g": round(vol * 2.68e-3, 1)}

def generate_actuator_mount():
    vol = 25 * 50 * 2.5 # Reduced size
    return {"id": "ACT-001", "name": "Actuator Mount", "material": "AlSi10Mg", "mass_g": round(vol * 2.68e-3, 1)}

def generate_wings(g):
    span, chord, thick = g["span_mm"], g["root_chord_mm"], g["thickness_mm"]
    vol = 0.5 * (span/2) * chord * thick * 4
    return {"id": "WNG-001", "name": "Delta Wings (x4)", "material": "CFRP", "mass_g": round(vol * 1.6e-3, 1)}

def generate_fins(g):
    span, chord, thick = g["span_mm"], g["root_chord_mm"], g["thickness_mm"]
    vol = 0.5 * (span/2) * chord * thick * 4
    return {"id": "FIN-001", "name": "Tail Fins (x4)", "material": "Al-7075", "mass_g": round(vol * 2.71e-3, 1)}

def generate_sabot(g):
    od, id_fuse, l = g["tube_od_mm"], g["fuselage_id_mm"], g["length_mm"]
    vol = math.pi * ((od/2)**2 - (id_fuse/2)**2) * l
    return {"id": "SAB-001", "name": "Launcher Sabot", "material": "PETG", "mass_g": round(vol * 1.1e-3, 1)}

def main():
    params = load_params()
    geom = params["geometry"]

    parts = [
        generate_fuselage(geom["fuselage"]),
        generate_bracket(geom["fuselage"]),
        generate_actuator_mount(),
        generate_wings(geom["wings"]),
        generate_fins(geom["fins"]),
        generate_sabot(geom["sabot"]),
        {"id": "BATT-01", "name": "50kJ Battery Pack", "material": "LiPo", "mass_g": 90.0},
        {"id": "MOT-01", "name": "8N Dash Motor", "material": "BLDC", "mass_g": 40.0},
        {"id": "SEEK-01", "name": "Ka-band Seeker", "material": "Sub-system", "mass_g": 35.0},
        {"id": "WHD-01", "name": "Kinetic Warhead", "material": "Tungsten/Steel", "mass_g": 30.0}
    ]

    output = {
        "project": "Interceptor_M",
        "baseline": "DD-400 Electric",
        "parts": parts,
        "mtow_actual_g": round(sum(p["mass_g"] for p in parts), 1)
    }

    with open("hardware/prototypes/parts_summary.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Parts generated for Wave 17 (MTOW: {output['mtow_actual_g']}g / 400.0g target):")
    for p in parts:
        print(f" [{p['id']}] {p['name']} ({p['material']}): {p['mass_g']}g")

if __name__ == "__main__":
    main()
