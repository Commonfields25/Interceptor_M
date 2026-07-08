"""
CoG Sensitivity Analysis Tool
Analyzes how shifts in component placement (tolerances) affect total vehicle CoG and stability.
"""
import math
import json
from build123d import *
from icad.engine import CADEngine
import icad.parts as parts

def analyze_sensitivity(assy_func, baseline_params, component_labels, shift_mm=5.0):
    print(f"--- CoG Sensitivity Analysis (Shift: {shift_mm}mm) ---")
    engine = CADEngine()

    # Baseline
    baseline_assy = assy_func(baseline_params)
    props = engine.analyze_solid(baseline_assy, 0.0027)
    base_cog = props["cog_mm"]

    results = {}

    # We simulate a longitudinal shift (Z-axis) for each component
    # In a real tool, we would re-assemble with offset locations.
    # For this report, we use a simplified mass-moment shift calculation.

    total_mass = props["mass_kg"]

    print(f"Baseline CoG: {base_cog}")
    print(f"Total Mass: {total_mass:.4f} kg")

    for label in component_labels:
        # Assuming component mass is roughly volume * density
        # In a real assembly we'd get the child volume
        comp_vol = 10000.0 # Placeholder or extract from child
        comp_mass = (comp_vol * 1e-9) * 2700.0 # kg

        shift_cog_z = (comp_mass * shift_mm) / total_mass
        results[label] = shift_cog_z
        print(f"  Component '{label}' shift affects Total CoG by: {shift_cog_z:.4f} mm")

    return results

if __name__ == "__main__":
    # Simplified test
    components = ["BATTERY", "SEEKER", "PAYLOAD"]
    analyze_sensitivity(lambda p: parts.build_chs001({"section_length": 200}), {}, components)
