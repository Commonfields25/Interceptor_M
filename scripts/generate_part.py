"""
Interceptor_M — Agent CAD Tooling
Generates 3D part descriptions compatible with the Agent Production Protocol.
Outputs: .stl (via Trimesh/OpenSCAD logic) or geometric metadata.
"""

import json
import os


def generate_component_metadata(component_name, params_path, output_dir):
    """
    Génère une pièce FreeCAD à partir d'un fichier JSON contenant les paramètres.

    Args:
        json_path (str): Chemin vers le fichier JSON de paramètres.
    """
    try:
        # Charge les paramètres depuis le JSON
        with open(json_path, "r", encoding="utf-8") as f:
            params = json.load(f)

        # Crée un nouveau document FreeCAD
        doc = App.newDocument(params["name"])
        body = doc.addObject("PartDesign::Body", f"Body_{params['name']}")

        # Crée une esquisse
        sketch = body.newObject("Sketcher::SketchObject", "Sketch")
        sketch.Placement = App.Placement(
            App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0)
        )
        body.addObject(sketch)

        # Ajoute une géométrie de rectangle (base de la pièce)
        geo = []
        length = params["dimensions"]["length"]
        width = params["dimensions"]["width"]

        geo.append(Part.LineSegment(App.Vector(0, 0, 0), App.Vector(length, 0, 0)))
        geo.append(
            Part.LineSegment(App.Vector(length, 0, 0), App.Vector(length, width, 0))
        )
        geo.append(
            Part.LineSegment(App.Vector(length, width, 0), App.Vector(0, width, 0))
        )
        geo.append(Part.LineSegment(App.Vector(0, width, 0), App.Vector(0, 0, 0)))

        # Ajoute un trou si spécifié
        if "hole_diameter" in params["dimensions"]:
            hole_center = App.Vector(
                params["dimensions"]["hole_position"][0],
                params["dimensions"]["hole_position"][1],
                0,
            )
            geo.append(
                Part.Circle(
                    hole_center,
                    App.Vector(0, 0, 1),
                    params["dimensions"]["hole_diameter"] / 2,
                )
            )

        # Crée l'esquisse
        sketch.addGeometry(geo)
        doc.recompute()

        # Extrude le rectangle
        pad = body.newObject("PartDesign::Pad", "Pad")
        pad.Profile = sketch
        pad.Length = params["dimensions"]["height"]
        doc.recompute()

        # Soustrais le trou si présent
        if "hole_diameter" in params["dimensions"]:
            pocket = body.newObject("PartDesign::Pocket", "Pocket")
            pocket.Profile = sketch
            pocket.Length = params["dimensions"]["height"]
            doc.recompute()

        # Exporte en STEP
        output_dir = os.path.dirname(json_path)
        step_path = os.path.join(output_dir, f"{params['name']}.step")
        Part.export([body], step_path)
        print(f"✅ Pièce exportée en STEP : {step_path}")

        # Sauvegarde le fichier FreeCAD
        fcstd_path = os.path.join(output_dir, f"{params['name']}.FCStd")
        doc.saveAs(fcstd_path)
        print(f"✅ Pièce sauvegardée en FCStd : {fcstd_path}")

        return True

    except Exception as e:
        print(f"❌ Erreur lors de la génération de la pièce : {e}")
        return False

    # Save JSON Metadata
    json_out = os.path.join(output_dir, f"{component_name}_plan.json")
    with open(json_out, "w") as f:
        json.dump(metadata, f, indent=2)

    # Generate Python Geometry Script (Placeholder for actual CAD logic)
    py_out = os.path.join(output_dir, f"gen_{component_name}.py")
    with open(py_out, "w") as f:
        f.write(f"import json\n")
        f.write(f"# Geometry generation for {component_name}\n")
        f.write(
            f"with open('{component_name}_plan.json', 'r') as f: metadata = json.load(f)\n"
        )
        f.write(
            f'print(f\'Generating {component_name} with length {{metadata["parameters"]["result_L_lanceur"]}}mm\')\n'
        )
        f.write(f"# CAD logic goes here...\n")

    return json_out, py_out


if __name__ == "__main__":
    # Test generation for D1 mission
    generate_component_metadata(
        "SAB-02_Launcher", "PARAMETERS.json", "agents/D1/workspace/SAB-02/"
    )
