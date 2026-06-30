#!/usr/bin/env python3
"""MTOW-driven geometry generator for Interceptor M product line.
Scaling rules:
  - Linear dimensions  : L × (MTOW/250)^(1/3)   (cube-root — geometric similarity)
  - Wall thickness     : t × (MTOW/250)^0.5      (sqrt — stress conservation σ=F/A)
  - ACT-001            : driven by spec E3 (MTOW-insensitive) — structural actuator
"""

import json, math, os, sys

BASE_MTOW = 250  # kg → DC baseline
BASE_PARAMS = {
    "fuselage": {"L_mm": 380.0, "W_mm": 180.0, "H_mm": 95.0},
    "wing_span_m": 1.50,
    "wall_mm": 2.0,
}
PARTS_BASE = {
    "BRK-001": {"description": "Structure primaire — Coque fuselage + 支翼",
                "material": "AlSi10Mg (DMLS)", "mass_g": 111.78},
    "ACT-001": {"description": "Vérin tubulaire 3 axes",
                "material": "AlSi10Mg (DMLS)", "mass_g": 55.49},
    "NCR-001": {"description": "Carénage aero — Coque complexe",
                "material": "Nomex honeycomb + CF skins", "mass_g": 89.33},
}

def scale(mtow_g, base=250):
    r = mtow_g / base
    return {
        "fuselage": {k: round(v * r**(1/3), 2) for k, v in BASE_PARAMS["fuselage"].items()},
        "wing_span_m": round(BASE_PARAMS["wing_span_m"] * r**(1/3), 3),
        "wall_mm": round(BASE_PARAMS["wall_mm"] * r**0.5, 3),
    }

def gen(mtow_g, key, mtow_src):
    sc = scale(mtow_g)
    parts = {}
    # Scale mass for scaled parts
    r = mtow_g / BASE_MTOW
    for pid, pb in PARTS_BASE.items():
        if pid == "ACT-001":
            parts[pid] = {**pb, "mass_g": pb["mass_g"],
                          "note": "MTOW-insensitive — spec E3 drives geometry"}
        else:
            parts[pid] = {**pb, "mass_g": round(pb["mass_g"] * r, 2)}
    return {"project": "Interceptor M", "version": "1.0.0", "line": key,
            "mtow_g": mtow_g, "mtow_source": mtow_src,
            "segments": sc, "parts": parts}

OUT = os.path.dirname(os.path.abspath(__file__))
configs = [
    (250, "DC", "spec E1 nominal"),
    (400, "DD", "spec E1 nominal"),
    (300, "DI", "provisional midpoint DC/DD"),
]
for mtow, key, src in configs:
    out = os.path.join(OUT, f"params_{key}.json")
    with open(out, "w") as f:
        json.dump(gen(mtow, key, src), f, indent=2)
    print(f"Generated {out}")

# Assertions — verify per-line masses differ
dc = json.loads(open(os.path.join(OUT, "params_DC.json")).read())
dd = json.loads(open(os.path.join(OUT, "params_DD.json")).read())
di = json.loads(open(os.path.join(OUT, "params_DI.json")).read())

for pid in ["BRK-001", "NCR-001"]:
    m = {k: v["parts"][pid]["mass_g"] for k, v in [("DC", dc), ("DD", dd), ("DI", di)]}
    assert m["DC"] != m["DD"], f"{pid}: DC==DD"
    assert m["DC"] != m["DI"], f"{pid}: DC==DI"
    print(f"ASSERT PASS {pid}: DC={m['DC']}g  DD={m['DD']}g  DI={m['DI']}g")

m_act = {k: v["parts"]["ACT-001"]["mass_g"] for k, v in [("DC", dc), ("DD", dd), ("DI", di)]}
assert m_act["DC"] == m_act["DI"] == m_act["DD"], f"ACT-001 should be MTOW-insensitive"
print(f"ASSERT PASS ACT-001: all {m_act['DC']}g (MTOW-insensitive, spec E3)")

print("\nAll assertions passed.")
