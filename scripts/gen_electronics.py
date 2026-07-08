#!/usr/bin/env python3
"""
Interceptor_M - Electronic Schematics & Gerber Generation Script (Traceability)
Generates structured schematics and Gerber placeholders for the Flight Controller and PDB.
"""

import os
import json

# Setup directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "engineering", "electronics")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_schematic_json(name, components):
    """Generates a structured schematic in JSON format for traceability"""
    schematic = {
        "project": "Interceptor_M",
        "assembly": name,
        "version": "1.0",
        "units": "mm",
        "components": components,
    }
    file_path = os.path.join(OUTPUT_DIR, f"{name}_schematic.json")
    with open(file_path, "w") as f:
        json.dump(schematic, f, indent=4)
    print(f"Generated schematic: {file_path}")


def generate_gerber_placeholder(name):
    """Generates a placeholder for Gerber files (standard naming)"""
    layers = ["GTL", "GBL", "GTS", "GBS", "GTO", "GBO", "GKO", "TXT"]
    gerber_dir = os.path.join(OUTPUT_DIR, f"{name}_gerbers")
    os.makedirs(gerber_dir, exist_ok=True)
    for layer in layers:
        file_path = os.path.join(gerber_dir, f"{name}.{layer}")
        with open(file_path, "w") as f:
            f.write(f"Interceptor_M - {name} Gerber Placeholder Layer: {layer}\n")
    print(f"Generated gerber placeholders in: {gerber_dir}")


def main():
    # 1. Flight Controller (FC) Schematics
    fc_components = [
        {"id": "U1", "type": "MCU", "model": "STM32H743", "pins": 144},
        {"id": "U2", "type": "IMU", "model": "ICM-42688-P", "interface": "SPI"},
        {"id": "U3", "type": "Baro", "model": "BMP388", "interface": "I2C"},
        {"id": "J1", "type": "Connector", "model": "USB-C", "purpose": "Data/Config"},
        {"id": "P1", "type": "Header", "model": "GH1.25", "purpose": "Receiver/GPS"},
    ]
    generate_schematic_json("Flight_Controller", fc_components)
    generate_gerber_placeholder("Flight_Controller")

    # 2. Power Distribution Board (PDB) Schematics
    pdb_components = [
        {"id": "Q1-Q4", "type": "MOSFET", "model": "TPH1R204PL", "rating": "40V/150A"},
        {"id": "U4", "type": "Regulator", "model": "LM5164", "output": "5V/1A"},
        {"id": "J2", "type": "Power_In", "model": "XT60", "rating": "60A"},
    ]
    generate_schematic_json("PDB_ESC_Integrated", pdb_components)
    generate_gerber_placeholder("PDB_ESC_Integrated")


if __name__ == "__main__":
    main()
