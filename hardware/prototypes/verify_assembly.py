import json, math
def verify():
    with open("PARAMETERS.json", "r") as f: p = json.load(f)
    g = p["geometry"]
    if g["sabot"]["tube_od_mm"] == p["platform"]["DD"]["launcher_bore_mm"]: print("PASS: Launcher Fit")
    if g["sabot"]["fuselage_id_mm"] >= g["fuselage"]["od_mm"]: print("PASS: Fuselage Fit")
if __name__ == "__main__": verify()
