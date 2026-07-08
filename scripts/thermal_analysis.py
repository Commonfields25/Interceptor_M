"""
Thermal Surface Area Analysis
Calculates the total radiating surface area of improved cooling fins.
"""
from build123d import *
import icad.parts as parts

def calculate_surface_area(part_id):
    if part_id == "ACT-001":
        part = parts.build_act001({})
    elif part_id == "MMT-001":
        part = parts.build_mmt001({})
    else:
        return 0.0

    area = sum(f.area for f in part.faces())
    print(f"--- Thermal Surface Area Report: {part_id} ---")
    print(f"Total Surface Area: {area:.2f} mm²")

    # Comparison to primitive block
    bbox = part.bounding_box()
    primitive_area = 2 * (bbox.size.X * bbox.size.Y + bbox.size.X * bbox.size.Z + bbox.size.Y * bbox.size.Z)
    improvement = (area / primitive_area - 1) * 100
    print(f"Surface Area Increase via Fins: +{improvement:.1f}%")

    return area

if __name__ == "__main__":
    calculate_surface_area("ACT-001")
    calculate_surface_area("MMT-001")
