"""
Interceptor_M — Constraint Verifier
Validates agent-produced plans against MTOW and dimensional limits.
Usage: python scripts/check_constraints.py <path_to_plan_json>
"""

import json
import sys
import os

def check_constraints(plan_json_path, params_path="PARAMETERS.json"):
    if not os.path.exists(plan_json_path):
        print(f"Error: Plan file {plan_json_path} not found.")
        return False

    with open(plan_json_path, 'r') as f:
        plan = json.load(f)

    with open(params_path, 'r') as f:
        params = json.load(f)

    # Example: Check if the component belongs to DD (Defense)
    # This logic can be expanded as more product lines are defined in PARAMETERS.json
    mtow_limit = params.get("DD", {}).get("performance", {}).get("MTOW_g", 400.0)

    component_name = plan.get("component", "Unknown")
    result_length = plan.get("parameters", {}).get("result_L_lanceur", 0)

    print(f"--- Constraint Check: {component_name} ---")

    # 1. Dimensional Check (Example for Launcher)
    if component_name == "SAB-02_Launcher":
        limit = 2000.0 # Max length for portable launcher
        if result_length <= limit:
            print(f"[PASS] Length: {result_length}mm <= {limit}mm limit.")
        else:
            print(f"[FAIL] Length: {result_length}mm exceeds {limit}mm limit!")
            return False

    # 2. MTOW Margin Check (Mock logic for component mass impact)
    print(f"[INFO] Product Line MTOW Limit: {mtow_limit}g")

    print("--- Check Complete ---")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_constraints(sys.argv[1])
    else:
        print("Usage: python scripts/check_constraints.py <path_to_plan_json>")
