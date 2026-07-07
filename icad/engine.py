import os
import json
import yaml
from build123d import *

class CADEngine:
    def __init__(self, output_dir="exports"):
        self.output_dir = output_dir
        self.drawing_dir = os.path.join(output_dir, "drawings")
        self.report_dir = os.path.join(output_dir, "reports")
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(self.drawing_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)

    def export(self, part, name, formats=None):
        if formats is None:
            formats = ["step", "stl"]
        results = {}
        for fmt in formats:
            path = os.path.join(self.output_dir, f"{name}.{fmt}")
            try:
                if fmt == "step":
                    export_step(part, path)
                elif fmt == "stl":
                    export_stl(part, path)
                results[fmt] = path
            except Exception as e:
                print(f"[CADEngine] Failed to export {fmt}: {e}")
        return results

    def generate_drawings(self, part, name):
        svg_dir = os.path.join(self.drawing_dir, name)
        os.makedirs(svg_dir, exist_ok=True)
        paths = {}

        # Camera positions for orthographic projections
        views = {
            "front": (0.0, -1000.0, 0.0),
            "back":  (0.0,  1000.0, 0.0),
            "top":   (0.0,    0.0, 1000.0),
            "bottom":(0.0,    0.0, -1000.0),
            "right": (1000.0, 0.0, 0.0),
            "left":  (-1000.0,0.0, 0.0),
        }

        for view_name, cam_pos in views.items():
            svg_path = os.path.join(svg_dir, f"{name}_{view_name}.svg")
            try:
                exporter = ExportSVG()
                exporter.add_builder(
                    Sketcher().add(
                        ShapeIterator(part, topology_type=TopologyType.FACE)
                    )
                )
                exporter.write(svg_path)
                paths[view_name] = svg_path
            except Exception as e:
                print(f"[CADEngine] Failed to generate {view_name} view: {e}")

        return paths

    def generate_report(self, part, name, metadata=None):
        if metadata is None:
            metadata = {}
        report_path = os.path.join(self.report_dir, f"{name}_report.md")

        with open(report_path, "w") as f:
            f.write(f"# CAD Report — {name}\n\n")

            f.write("## Part Metadata\n")
            f.write("| Property | Value |\n")
            f.write("| :--- | :--- |\n")
            for k, v in metadata.items():
                f.write(f"| **{k}** | {v} |\n")

            f.write("\n## Physical Properties\n")
            try:
                volume = part.volume
                bbox = part.bounding_box()
                f.write(f"| Property | Value |\n")
                f.write(f"| :--- | :--- |\n")
                f.write(f"| Volume | {volume:.4f} mm³ |\n")
                f.write(f"| Bounding Box | {bbox.XLen:.2f} × {bbox.YLen:.2f} × {bbox.ZLen:.2f} mm |\n")
                if "density" in metadata:
                    mass = volume * metadata["density"] / 1e3
                    f.write(f"| Mass (est.) | {mass:.4f} g |\n")
            except Exception as e:
                f.write(f"| Error | {e} |\n")

            f.write("\n## Manufacturing Files\n")
            f.write(f"- [STEP Model](./{name}.step)\n")
            f.write(f"- [STL Model](./{name}.stl)\n")

        return report_path

    def generate_pdf_drawing(self, part, name, scale=1.0):
        try:
            from svglib.svglib import svg2rlg
            from reportlab.graphics import renderPDF
            from reportlab.pdfgen import canvas
        except ImportError:
            print("[CADEngine] svglib/reportlab not installed, skipping PDF drawing.")
            return None

        svg_dir = os.path.join(self.drawing_dir, name)
        pdf_path = os.path.join(self.drawing_dir, f"{name}_drawing.pdf")

        c = canvas.Canvas(pdf_path)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, f"Drawing — {name}")

        views = ["top", "front", "right"]
        y_pos = 720
        for view in views:
            svg_file = os.path.join(svg_dir, f"{name}_{view}.svg")
            if os.path.exists(svg_file):
                try:
                    drawing = svg2rlg(svg_file)
                    if drawing:
                        drawing.width *= scale
                        drawing.height *= scale
                        drawing.scale(scale, scale)
                        renderPDF.draw(drawing, c, 50, y_pos)
                        y_pos -= (drawing.height + 60)
                except Exception as e:
                    print(f"[CADEngine] Failed to render {view} SVG to PDF: {e}")

        c.save()
        return pdf_path
