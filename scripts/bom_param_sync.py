import json
import os
import sys

def main():
    try:
        with open('PARAMETERS.json', 'r') as f:
            params = json.load(f)
        with open('manufacturing/BOM_consolidee.md', 'r') as f:
            bom_content = f.read()
    except Exception as e:
        print(f"Error reading files: {e}")
        sys.exit(1)

    param_parts = params.get('parts', {}).keys()
    mismatches = []

    for part in param_parts:
        if part not in bom_content:
            mismatches.append(f"Part {part} defined in PARAMETERS.json but missing from BOM_consolidee.md")

    if mismatches:
        print("🔴 BOM-to-Parameter Discrepancy Found!")
        for m in mismatches:
            print(f"  - {m}")
        print("\nPlease update manufacturing/BOM_consolidee.md to match the engineering parameters.")
        sys.exit(1)
    else:
        print("✅ BOM and Parameters are synchronized.")
        sys.exit(0)

if __name__ == "__main__":
    main()
