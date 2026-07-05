import json, math, os
def load_params():
    with open("PARAMETERS.json", "r") as f: return json.load(f)
def generate_parts(g):
    od, t, l = g["fuselage"]["od_mm"], g["fuselage"]["wall_thickness_mm"], g["fuselage"]["length_mm"]
    fus = {"id": "FUS-001", "mass_g": round(math.pi * ((od/2)**2 - (od/2-t)**2) * l * 2.71e-3, 1)}
    w = g["wings"]; vol_w = 0.5 * (w["span_mm"]/2) * w["root_chord_mm"] * w["thickness_mm"] * 4
    wng = {"id": "WNG-001", "mass_g": round(vol_w * 1.6e-3, 1)}
    s = g["sabot"]; vol_s = math.pi * ((s["tube_od_mm"]/2)**2 - (s["fuselage_id_mm"]/2)**2) * s["length_mm"]
    sab = {"id": "SAB-001", "mass_g": round(vol_s * 1.1e-3, 1)}
    return [fus, wng, sab, {"id":"BATT-01", "mass_g":100.0}, {"id":"MOT-01", "mass_g":45.0}, {"id":"SEEK-01", "mass_g":35.0}]
def main():
    p = load_params(); parts = generate_parts(p["geometry"])
    output = {"project": "Interceptor_M", "mtow": round(sum(i["mass_g"] for i in parts), 1), "parts": parts}
    with open("hardware/prototypes/parts_summary.json", "w") as f: json.dump(output, f, indent=2)
    print(f"MTOW: {output['mtow']}g")
if __name__ == "__main__": main()
