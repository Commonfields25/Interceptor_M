import os
import json
import yaml
import trimesh
import numpy as np
from build123d import *

class CADEngine:
    def __init__(self, output_dir="exports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def analyze_solid(self, part: Solid, density_g_mm3: float):
        """
        Performs high-fidelity physical analysis of the B-Rep solid.
        Uses Trimesh for watertightness and inertia tensor calculation.
        Converts results to standard SI units (kg, m, kg.m2).
        """
        # 1. Tessellate the solid with fine chordal tolerance (0.01mm)
        tmp_stl = "tmp_analysis.stl"
        export_stl(part, tmp_stl, tolerance=0.01, angular_tolerance=0.1)

        # 2. Load into Trimesh
        mesh = trimesh.load(tmp_stl)
        os.remove(tmp_stl)

        # 3. Validation: Watertightness
        if not mesh.is_watertight:
            mesh.fill_holes()
            if not mesh.is_watertight:
                # Fallback to build123d built-in properties if trimesh fails watertightness
                # though we prefer watertight meshes for flight sim.
                print("Warning: Mesh is not watertight, attempting recovery...")

        # 4. Physical Calculations (Units SI: kg, m, kg.m2)
        # density_g_mm3 -> kg/m3: 1 g/mm3 = 1e6 kg/m3
        density_kg_m3 = density_g_mm3 * 1e6

        volume_mm3 = mesh.volume
        volume_m3 = volume_mm3 * 1e-9
        mass_kg = volume_m3 * density_kg_m3

        # COG in mm
        cog = mesh.centroid

        # Inertia Tensor: mm^5 -> m^5 (1e-15) * density (kg/m3) = kg.m2
        # PyCad Physics Calibration: 1e-15 factor for mm^5 to SI
        inertia_tensor_kg_m2 = mesh.moment_inertia * density_kg_m3 * 1e-15

        return {
            "watertight": mesh.is_watertight,
            "volume_mm3": volume_mm3,
            "mass_kg": mass_kg,
            "cog_mm": tuple(cog),
            "inertia_tensor_si": inertia_tensor_kg_m2.tolist(),
            "density_kg_m3": density_kg_m3
        }

    def export_part(self, part, name, formats=["step", "stl"]):
        results = {}
        if "step" in formats:
            path = os.path.join(self.output_dir, f"{name}.step")
            export_step(part, path)
            results["step"] = path
        if "stl" in formats:
            path = os.path.join(self.output_dir, f"{name}.stl")
            export_stl(part, path, tolerance=1e-4, angular_tolerance=0.01)
            results["stl"] = path
        return results

    def generate_drawings(self, part, name):
        drawing_dir = os.path.join(self.output_dir, "drawings")
        os.makedirs(drawing_dir, exist_ok=True)

        views = {
            "top": (0.01, 0.01, 1000),
            "front": (0.01, -1000, 0.01),
            "side": (1000, 0.01, 0.01)
        }

        paths = {}
        for view_name, cam_pos in views.items():
            path = os.path.join(drawing_dir, f"{name}_{view_name}.svg")
            try:
                visible, hidden = part.project_to_viewport(cam_pos)
                exporter = ExportSVG()
                exporter.add_layer("visible", line_color=Color("black"), line_weight=0.3)
                exporter.add_layer("hidden", line_color=Color("gray"), line_weight=0.1)
                for edge in visible: exporter.add_shape(edge, layer="visible")
                for edge in hidden: exporter.add_shape(edge, layer="hidden")
                exporter.write(path)
                paths[view_name] = path
            except Exception as e:
                print(f"Warning: Could not export SVG for {view_name} of {name}: {e}")
        return paths

    def generate_report(self, part, name, metadata):
        density = float(metadata.get("density", 0.0027))
        analysis = self.analyze_solid(part, density)

        report_path = os.path.join(self.output_dir, f"{name}_report.md")
        with open(report_path, "w") as f:
            f.write(f"# PyCad Technical Data Sheet: {name}\n\n")
            f.write(f"## Engineering Metadata\n")
            f.write(f"| Property | Value |\n")
            f.write(f"| :--- | :--- |\n")
            for k, v in metadata.items():
                f.write(f"| **{k}** | {v} |\n")
            f.write(f"| **Watertight Integrity** | {'PASSED' if analysis['watertight'] else 'FAILED'} |\n")

            f.write(f"\n## Physical Properties (SI Units)\n")
            f.write(f"- **Mass**: {analysis['mass_kg']:.4f} kg ({analysis['mass_kg']*1000:.2f} g)\n")
            f.write(f"- **Volume**: {analysis['volume_mm3']:.2f} mm³\n")
            f.write(f"- **Center of Gravity (mm)**: X={analysis['cog_mm'][0]:.2f}, Y={analysis['cog_mm'][1]:.2f}, Z={analysis['cog_mm'][2]:.2f}\n")

            f.write(f"\n## Inertia Tensor (kg.m²)\n")
            f.write(f"```json\n{json.dumps(analysis['inertia_tensor_si'], indent=2)}\n```\n")

            f.write(f"\n## Manufacturing Files\n")
            f.write(f"- [STEP Model](./{name}.step)\n")
            f.write(f"- [STL Model](./{name}.stl)\n")

            f.write(f"\n## Technical Drawings\n")
            f.write(f"### Projections\n")
            f.write(f"![Top](./drawings/{name}_top.svg) ![Front](./drawings/{name}_front.svg) ![Side](./drawings/{name}_side.svg)\n")

        return report_path
