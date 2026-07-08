import json
import re
import sys


def get_python_constant(content, name):
    match = re.search(rf"{name}\s*=\s*([\d\.]+)", content)
    return float(match.group(1)) if match else None


def main():
    try:
        with open("PARAMETERS.json", "r") as f:
            params = json.load(f)
        with open("simulation/constants.py", "r") as f:
            constants_py = f.read()
    except Exception as e:
        print(f"Error reading files: {e}")
        sys.exit(1)

    # 1. Check MTOW (DD baseline)
    json_mtow_kg = params["lines"]["DD"]["mtow_g"] / 1000.0
    py_mtow_kg = get_python_constant(constants_py, "MASSE_INTERCEPTOR_KG")

    # 2. Check Length
    json_l_mm = params["lines"]["DD"]["segments"]["fuselage"]["L_mm"]
    py_l_mm = get_python_constant(constants_py, "LONGUEUR_INTERCEPTOR_MM")

    mismatches = []
    if json_mtow_kg != py_mtow_kg:
        mismatches.append(
            f"MTOW Mismatch: PARAMETERS.json={json_mtow_kg}kg, constants.py={py_mtow_kg}kg"
        )
    if json_l_mm != py_l_mm:
        mismatches.append(
            f"Length Mismatch: PARAMETERS.json={json_l_mm}mm, constants.py={py_l_mm}mm"
        )

    if mismatches:
        print("🔴 Parameter Synchronization Error!")
        for m in mismatches:
            print(f"  - {m}")
        print("\nPlease ensure simulation/constants.py matches PARAMETERS.json (SSoT).")
        sys.exit(1)
    else:
        print("✅ Parameter Synchronization Verified (DD Baseline).")
        sys.exit(0)


if __name__ == "__main__":
    main()
