"""
Script pour générer des pièces FreeCAD à partir d'un fichier JSON.
Utilisation :
    1. Ouvrir FreeCAD
    2. Ouvrir la console Python (Macro -> Python Console)
    3. Exécuter : exec(open("scripts/generate_part.py").read())
    4. Appeler la fonction : generate_part_from_json("parts/BRK001/params_BRK001.json")
"""

import json
import FreeCAD as App
import Part
import PartDesign
import os
import sys


def generate_part_from_json(json_path):
    """
    Génère une pièce FreeCAD à partir d'un fichier JSON contenant les paramètres.
    
    Args:
        json_path (str): Chemin vers le fichier JSON de paramètres.
    """
    try:
        # Charge les paramètres depuis le JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            params = json.load(f)
        
        # Crée un nouveau document FreeCAD
        doc = App.newDocument(params["name"])
        body = doc.addObject('PartDesign::Body', f'Body_{params["name"]}')
        
        # Crée une esquisse
        sketch = body.newObject('Sketcher::SketchObject', 'Sketch')
        sketch.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0))
        body.addObject(sketch)
        
        # Ajoute une géométrie de rectangle (base de la pièce)
        geo = []
        length = params["dimensions"]["length"]
        width = params["dimensions"]["width"]
        
        geo.append(Part.LineSegment(App.Vector(0, 0, 0), App.Vector(length, 0, 0)))
        geo.append(Part.LineSegment(App.Vector(length, 0, 0), App.Vector(length, width, 0)))
        geo.append(Part.LineSegment(App.Vector(length, width, 0), App.Vector(0, width, 0)))
        geo.append(Part.LineSegment(App.Vector(0, width, 0), App.Vector(0, 0, 0)))
        
        # Ajoute un trou si spécifié
        if "hole_diameter" in params["dimensions"]:
            hole_center = App.Vector(
                params["dimensions"]["hole_position"][0],
                params["dimensions"]["hole_position"][1],
                0
            )
            geo.append(Part.Circle(hole_center, App.Vector(0, 0, 1), params["dimensions"]["hole_diameter"] / 2))
        
        # Crée l'esquisse
        sketch.addGeometry(geo)
        doc.recompute()
        
        # Extrude le rectangle
        pad = body.newObject('PartDesign::Pad', 'Pad')
        pad.Profile = sketch
        pad.Length = params["dimensions"]["height"]
        doc.recompute()
        
        # Soustrais le trou si présent
        if "hole_diameter" in params["dimensions"]:
            pocket = body.newObject('PartDesign::Pocket', 'Pocket')
            pocket.Profile = sketch
            pocket.Length = params["dimensions"]["height"]
            doc.recompute()
        
        # Exporte en STEP
        output_dir = os.path.dirname(json_path)
        step_path = os.path.join(output_dir, f'{params["name"]}.step')
        Part.export([body], step_path)
        print(f"✅ Pièce exportée en STEP : {step_path}")
        
        # Sauvegarde le fichier FreeCAD
        fcstd_path = os.path.join(output_dir, f'{params["name"]}.FCStd')
        doc.saveAs(fcstd_path)
        print(f"✅ Pièce sauvegardée en FCStd : {fcstd_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération de la pièce : {e}")
        return False


# Exemple d'utilisation (à exécuter dans FreeCAD)
if __name__ == "__main__":
    print("⚠️  Ce script doit être exécuté dans FreeCAD (Console Python).")
    print("Exemple d'utilisation : generate_part_from_json('parts/BRK001/params_BRK001.json')")
