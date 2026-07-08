#!/usr/bin/env python3
"""MTOW-driven geometry generator for Interceptor M product line.
Updated for Baseline v1.2.0.
"""

import json, os

BASE_PARAMS = {
    "DC": {
        "mtow_g": 250.0,
        "L_mm": 350.0,
        "W_mm": 160.0,
        "H_mm": 80.0,
        "wing_span_m": 0.12,
        "wall_mm": 1.5,
    },
    "DI": {
        "mtow_g": 300.0,
        "L_mm": 365.0,
        "W_mm": 180.0,
        "H_mm": 90.0,
        "wing_span_m": 0.135,
        "wall_mm": 1.8,
    },
    "DD": {
        "mtow_g": 400.0,
        "L_mm": 380.0,
        "W_mm": 200.0,
        "H_mm": 100.0,
        "wing_span_m": 0.15,
        "wall_mm": 2.0,
    },
}

PARTS_BASE = {
    "BRK-001": {
        "description": "Structure primaire — Coque fuselage + 支翼",
        "material": "AlSi10Mg (DMLS)",
    },
    "ACT-001": {"description": "Vérin tubulaire 3 axes", "material": "AlSi10Mg (DMLS)"},
    "NCR-001": {
        "description": "Bague d'interface ogive — joint torique NBR (étanchéité pneumatique)",
        "material": "316L SS",
    },
}


def gen(line_key):
    p = BASE_PARAMS[line_key]
    parts = {
        "BRK-001": {
            **PARTS_BASE["BRK-001"],
            "mass_g": round(135.0 * (p["mtow_g"] / 400.0), 2),
        },
        "ACT-001": {
            **PARTS_BASE["ACT-001"],
            "mass_g": 65.0,
            "note": "MTOW-insensitive — spec E3 drives geometry",
        },
        "NCR-001": {
            **PARTS_BASE["NCR-001"],
            "mass_g": round(110.0 * (p["mtow_g"] / 400.0), 2),
        },
    }
    return {
        "project": "Interceptor M",
        "version": "1.2.0",
        "line": line_key,
        "mtow_g": p["mtow_g"],
        "mtow_source": "Baseline v1.2.0",
        "segments": {
            "fuselage": {"L_mm": p["L_mm"], "W_mm": p["W_mm"], "H_mm": p["H_mm"]},
            "wing_span_m": p["wing_span_m"],
            "wall_mm": p["wall_mm"],
        },
        "parts": parts,
    }


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for key in BASE_PARAMS.keys():
    config = gen(key)
    # Write to multiple locations for consistency
    paths = [
        os.path.join(ROOT, f"params_{key}.json"),
        os.path.join(ROOT, "params", f"params_{key}.json"),
        os.path.join(ROOT, "hardware", "prototypes", f"params_{key}.json"),
    ]
    for p in paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            json.dump(config, f, indent=2)
        print(f"Generated {p}")

print("\nAll line parameters synchronized to Baseline v1.2.0.")
