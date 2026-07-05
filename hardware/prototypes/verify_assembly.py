import json
import math

def verify():
    with open("PARAMETERS.json", "r") as f:
        p = json.load(f)

    g = p["geometry"]

    # 1. Launcher Fit
    sabot_od = g["sabot"]["tube_od_mm"]
    launcher_bore = p["platform"]["DD"]["launcher_bore_mm"]
    if sabot_od != launcher_bore:
        print(f"FAIL: Sabot OD ({sabot_od}mm) does not match Launcher Bore ({launcher_bore}mm)")
    else:
        print("PASS: Sabot fits launcher bore.")

    # 2. Fuselage Interface
    fuse_od = g["fuselage"]["od_mm"]
    sabot_id = g["sabot"]["fuselage_id_mm"]
    if sabot_id < fuse_od:
        print(f"FAIL: Sabot ID ({sabot_id}mm) too small for Fuselage OD ({fuse_od}mm)")
    else:
        print(f"PASS: Sabot interfaces with fuselage (Gap: {round(sabot_id - fuse_od, 2)}mm).")

    # 3. Volume Check (Simplifié)
    fuse_l = g["fuselage"]["length_mm"]
    if fuse_l != 380.0:
        print(f"FAIL: Fuselage length ({fuse_l}mm) misaligned with 380mm baseline.")
    else:
        print("PASS: Fuselage length correct.")

if __name__ == "__main__":
    verify()
