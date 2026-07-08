import os
import sys
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF


def convert_svg_to_pdf(svg_path, pdf_path):
    try:
        drawing = svg2rlg(svg_path)
        renderPDF.drawToFile(drawing, pdf_path)
        return True
    except Exception as e:
        print(f"Error converting {svg_path}: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="SVG file or directory")
    parser.add_argument("--output", "-o", help="Output PDF file or directory")
    args = parser.parse_args()

    if os.path.isfile(args.input):
        out = args.output if args.output else args.input.replace(".svg", ".pdf")
        convert_svg_to_pdf(args.input, out)
    elif os.path.isdir(args.input):
        out_dir = args.output if args.output else args.input
        os.makedirs(out_dir, exist_ok=True)
        for f in os.listdir(args.input):
            if f.endswith(".svg"):
                convert_svg_to_pdf(
                    os.path.join(args.input, f),
                    os.path.join(out_dir, f.replace(".svg", ".pdf")),
                )
