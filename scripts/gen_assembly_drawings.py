from build123d import *
from icad.engine import CADEngine
from icad.parts.lnch001 import build_lnch001
from icad.parts.lnch002 import build_lnch002
from icad.parts.lnch003 import build_lnch003
import os


def create_launcher_assembly():
    engine = CADEngine(output_dir="exports/assemblies")

    # Simple assembly: Base + Rail + Bracket
    chassis = build_lnch001({})
    rail = build_lnch002({})
    bracket = build_lnch003({})

    assembly = Compound(
        label="Launcher_Assembly",
        children=[
            chassis,
            rail.moved(Location((0, 0, 50))),
            bracket.moved(Location((500, 0, 80))),
        ],
    )

    engine.export_part(assembly, "LAUNCHER-ASSY-001")
    engine.generate_drawings(assembly, "LAUNCHER-ASSY-001")
    print("Launcher assembly generated.")


if __name__ == "__main__":
    create_launcher_assembly()
