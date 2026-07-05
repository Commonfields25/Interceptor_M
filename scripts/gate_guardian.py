import os
import sys
import json

def main():
    # In a real GHA, we would get the labels from the PR context
    # For this script, we'll check an environment variable or default to G3 if not provided
    gate_label = os.environ.get('PR_GATE_LABEL')

    if not gate_label:
        print("ℹ️ No gate label detected. Skipping Gate Guardian check.")
        sys.exit(0)

    print(f"⛩️ Gate Guardian checking requirements for {gate_label}...")

    gate_pkg_dir = 'agents/agent_manager/gate_packages/'

    if not os.path.exists(gate_pkg_dir):
        print(f"🔴 Error: Gate package directory {gate_pkg_dir} missing!")
        sys.exit(1)

    # Example: gate:G4 -> check for GATE_G4_*.md
    gate_id = gate_label.replace('gate:', '')
    pattern = f"GATE_{gate_id}"

    required_files = [f for f in os.listdir(gate_pkg_dir) if f.startswith(pattern)]

    if not required_files:
        print(f"🔴 Violation: No validation package found for {gate_label} in {gate_pkg_dir}")
        print(f"Please ensure a template like 'GATE_{gate_id}_VALIDATION.md' is submitted.")
        sys.exit(1)

    print(f"✅ Found {len(required_files)} validation document(s) for {gate_label}.")
    for f in required_files:
        print(f"  - {f}")
    sys.exit(0)

if __name__ == "__main__":
    main()
