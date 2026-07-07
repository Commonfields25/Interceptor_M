"""
Assembly Verification Script
Checks tolerances and interference between DD-400 fuselage and launcher.
Baseline: DD-400 (35mm Fuselage, 40mm Launcher Bore)
"""
import json
import os

def check_fit():
    try:
        with open("PARAMETERS.json", "r") as f:
            params = json.load(f)
    except Exception as e:
        print(f"Error loading PARAMETERS.json: {e}")
        return

    fuselage_dia = params["shared_geometry"]["fuselage_outer_diameter_mm"]
    launcher_bore = params["shared_geometry"]["launcher_tube_bore_mm"]

    print(f"--- Assembly Verification Report ---")
    print(f"Fuselage Outer Diameter: {fuselage_dia} mm")
    print(f"Launcher Tube Bore: {launcher_bore} mm")

    # 1. Radial Clearance (Sabot Gap)
    # Sabot fits between fuselage and launcher.
    # We modeled sabot ID=35.2 and OD=39.8 in sabot001.py
    # Let's verify if that matches the parameters.

    sabot_id = 35.2
    sabot_od = 39.8

    fit_inner = sabot_id - fuselage_dia
    fit_outer = launcher_bore - sabot_od

    print(f"\nSabot Clearance Check:")
    print(f"  Inner Gap (Sabot ID - Fuselage OD): {fit_inner:.2f} mm")
    if fit_inner >= 0.1:
        print("  [PASS] Inner clearance sufficient for sliding.")
    else:
        print("  [FAIL] Inner clearance too tight!")

    print(f"  Outer Gap (Launcher Bore - Sabot OD): {fit_outer:.2f} mm")
    if fit_outer >= 0.1:
        print("  [PASS] Outer clearance sufficient for launch.")
    else:
        print("  [FAIL] Outer clearance too tight!")

    # 2. Design Margin check
    total_margin = fit_inner + fit_outer
    print(f"\nTotal Design Margin: {total_margin:.2f} mm")

    if 0.2 <= total_margin <= 1.0:
        print("  [PASS] Margin within aerospace standards for counter-UAS.")
    else:
        print("  [WARNING] Margin out of nominal range (Expected 0.2-1.0mm).")

if __name__ == "__main__":
    check_fit()
