import os
import json
import yaml
from build123d import *

class CADEngine:
    def __init__(self, output_dir="exports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

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

        # Camera positions for projections
        views = {
            "top": (0.01, 0.01, 1000), # Slight offset to avoid zero norm cross product
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

                for edge in visible:
                    exporter.add_shape(edge, layer="visible")
                for edge in hidden:
                    exporter.add_shape(edge, layer="hidden")

                exporter.write(path)
                paths[view_name] = path
            except Exception as e:
                print(f"Warning: Could not export SVG for {view_name} of {name}: {e}")

        return paths

    def generate_report(self, part, name, metadata):
        report_path = os.path.join(self.output_dir, f"{name}_report.md")
        with open(report_path, "w") as f:
            f.write(f"# Technical Data Sheet: {name}\n\n")

            f.write(f"## Part Metadata\n")
            f.write(f"| Property | Value |\n")
            f.write(f"| :--- | :--- |\n")
            for k, v in metadata.items():
                f.write(f"| **{k}** | {v} |\n")

            f.write(f"\n## Physical Properties\n")
            volume = part.volume
            bbox = part.bounding_box()
            f.write(f"- **Volume**: {volume:.2f} mm³\n")
            f.write(f"- **Bounding Box**: {bbox.size.X:.2f} x {bbox.size.Y:.2f} x {bbox.size.Z:.2f} mm\n")

            if "density" in metadata:
                mass = volume * float(metadata["density"]) # g
                f.write(f"- **Calculated Mass**: {mass:.2f} g\n")

            f.write(f"\n## Manufacturing Files\n")
            f.write(f"- [STEP Model](./{name}.step)\n")
            f.write(f"- [STL Model](./{name}.stl)\n")

            f.write(f"\n## Technical Drawings (Projections)\n")
            f.write(f"### Top View\n![Top View](./drawings/{name}_top.svg)\n\n")
            f.write(f"### Front View\n![Front View](./drawings/{name}_front.svg)\n\n")
            f.write(f"### Side View\n![Side View](./drawings/{name}_side.svg)\n\n")

        return report_path

    def generate_pdf_drawing(self, name):
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPDF
        from reportlab.pdfgen import canvas

        drawing_dir = os.path.join(self.output_dir, "drawings")
        pdf_path = os.path.join(drawing_dir, f"{name}_technical_drawing.pdf")

        c = canvas.Canvas(pdf_path)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, f"Technical Drawing: {name}")
        c.setFont("Helvetica", 10)
        c.drawString(50, 785, "Part of Interceptor_M Project - L3 Manufacturing Grade")

        y_pos = 500
        views = ["top", "front", "side"]
        for view in views:
            svg_file = os.path.join(drawing_dir, f"{name}_{view}.svg")
            if os.path.exists(svg_file):
                drawing = svg2rlg(svg_file)
                # Scale drawing to fit
                scale = 400.0 / drawing.width if drawing.width > 400 else 1.0
                drawing.width *= scale
                drawing.height *= scale
                drawing.scale(scale, scale)

                c.drawString(50, y_pos + drawing.height + 10, f"View: {view.capitalize()}")
                renderPDF.draw(drawing, c, 50, y_pos)
                y_pos -= (drawing.height + 60)

        c.save()
        return pdf_path
