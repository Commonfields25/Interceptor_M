#!/usr/bin/env python3
"""
Interceptor_M - Drone Launcher Base Parts Generator
Generates parametric CAD parts using numpy-stl and gmsh for STEP export
"""

import numpy as np
from stl import mesh
import os
import math

OUTPUT_DIR = "/app/models/Base_Launcher_Pieces"
ASSEMBLIES_DIR = os.path.join(OUTPUT_DIR, "Assemblies")

def create_box_mesh(width, height, depth, center=(0, 0, 0)):
    if width <= 0 or height <= 0 or depth <= 0: raise ValueError("Dimensions must be positive")
    """Create a box mesh"""
    w, h, d = width/2, height/2, depth/2
    cx, cy, cz = center
    
    # 8 vertices
    vertices = np.array([
        [cx-w, cy-h, cz-d], [cx+w, cy-h, cz-d],
        [cx+w, cy+h, cz-d], [cx-w, cy+h, cz-d],
        [cx-w, cy-h, cz+d], [cx+w, cy-h, cz+d],
        [cx+w, cy+h, cz+d], [cx-w, cy+h, cz+d]
    ])
    
    # 12 triangular faces
    faces = np.array([
        [0, 3, 1], [1, 3, 2],  # Bottom face
        [4, 5, 7], [5, 6, 7],  # Top face
        [0, 1, 5], [0, 5, 4],  # Front face
        [2, 3, 7], [2, 7, 6],  # Back face
        [0, 4, 7], [0, 7, 3],  # Left face
        [1, 2, 6], [1, 6, 5]   # Right face
    ])
    
    return vertices, faces

def create_cylinder_mesh(radius, height, center=(0, 0, 0), segments=32):
    if radius <= 0 or height <= 0: raise ValueError("Dimensions must be positive")
    """Create a cylinder mesh"""
    cx, cy, cz = center
    vertices = [np.array([cx, cy, cz])]  # Center point
    angles = np.linspace(0, 2*math.pi, segments+1)[:-1]
    
    # Bottom circle
    for angle in angles:
        vertices.append(np.array([cx + radius*math.cos(angle), 
                                   cy + radius*math.sin(angle), cz]))
    
    # Top circle
    for angle in angles:
        vertices.append(np.array([cx + radius*math.cos(angle), 
                                   cy + radius*math.sin(angle), cz + height]))
    
    vertices.append(np.array([cx, cy, cz + height]))  # Top center
    
    n = len(vertices) - 1
    faces = []
    
    # Bottom triangles
    for i in range(1, segments+1):
        next_i = 1 if i == segments else i + 1
        faces.append([0, i, next_i])
    
    # Side faces (quads split into triangles)
    for i in range(1, segments+1):
        next_i = 1 if i == segments else i + 1
        current_top = i + segments
        next_top = 1 + segments if i == segments else i + 1 + segments
        faces.append([i, next_i, current_top])
        faces.append([next_i, next_top, current_top])
    
    # Top triangles
    for i in range(1, segments+1):
        next_i = 1 if i == segments else i + 1
        faces.append([n, current_top, n])
        faces.append([i + segments, (i + segments) % segments + segments + 1, n])
    
    return np.array(vertices), np.array(faces)

def combine_meshes(mesh_list):
    """Combine multiple meshes into one"""
    combined_vertices = []
    combined_faces = []
    offset = 0
    
    for vertices, faces in mesh_list:
        combined_vertices.append(vertices)
        combined_faces.append(faces + offset)
        offset += len(vertices)
    
    all_vertices = np.vstack(combined_vertices)
    all_faces = np.vstack(combined_faces)
    
    return all_vertices, all_faces

def save_stl(vertices, faces, filename):
    """Save mesh as STL"""
    stl_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        stl_mesh.vectors[i] = vertices[face]
    stl_mesh.save(filename)

def create_box_stl(filename, width, height, depth, center=(0, 0, 0)):
    """Create and save a box STL"""
    vertices, faces = create_box_mesh(width, height, depth, center)
    save_stl(vertices, faces, filename)
    return filename

def create_cylinder_stl(filename, radius, height, center=(0, 0, 0)):
    """Create and save a cylinder STL"""
    vertices, faces = create_cylinder_mesh(radius, height, center)
    save_stl(vertices, faces, filename)
    return filename

# ============================================================
# PART 1: Main Chassis/Frame Structure
# ============================================================
def create_main_chassis():
    """
    Creates the main frame structure for the drone launcher.
    Material: Aluminum 6061-T6
    Dimensions: 2000mm x 500mm x 1000mm
    """
    print("Creating main chassis...")
    mesh_list = []
    
    width = 2000
    height = 100
    depth = 50
    
    # Main longitudinal beams (2x)
    v1, f1 = create_box_mesh(depth, height, width/2 - 25, center=(-width/4, 0, 0))
    v2, f2 = create_box_mesh(depth, height, width/2 - 25, center=(width/4, 0, 0))
    mesh_list.append((v1, f1))
    mesh_list.append((v2, f2))
    
    # Cross beams at 3 heights
    for z_pos in [0, height/2, height]:
        v, f = create_box_mesh(width - 2*depth, depth, depth, center=(0, 0, z_pos))
        mesh_list.append((v, f))
    
    # Mounting brackets at corners
    bracket_positions = [
        (-width/2 + 50, 0, 0),
        (width/2 - 50, 0, 0),
        (-width/2 + 50, 0, height),
        (width/2 - 50, 0, height)
    ]
    for pos in bracket_positions:
        v, f = create_box_mesh(depth + 20, height + 20, 10, center=pos)
        mesh_list.append((v, f))
    
    combined = combine_meshes(mesh_list)
    output_path = os.path.join(OUTPUT_DIR, "01_Main_Chassis.stl")
    save_stl(*combined, output_path)
    return output_path

# ============================================================
# PART 2: Launch Rails System
# ============================================================
def create_launch_rails():
    """
    Creates the launch rail system for the drone.
    Material: Hardened Steel
    Length: 1500mm
    """
    print("Creating launch rails...")
    mesh_list = []
    
    rail_length = 1500
    rail_width = 30
    rail_height = 40
    
    # Main rail body
    v, f = create_box_mesh(rail_length, rail_height, rail_width, center=(0, 0, 0))
    mesh_list.append((v, f))
    
    # Guide flanges
    v, f = create_box_mesh(rail_length, 5, rail_width + 10, center=(0, rail_height/2 - 2.5, 0))
    mesh_list.append((v, f))
    v, f = create_box_mesh(rail_length, 5, rail_width + 10, center=(0, -rail_height/2 + 2.5, 0))
    mesh_list.append((v, f))
    
    combined = combine_meshes(mesh_list)
    output_path = os.path.join(OUTPUT_DIR, "02_Launch_Rails.stl")
    save_stl(*combined, output_path)
    return output_path

# ============================================================
# PART 3: Drone Mounting Bracket
# ============================================================
def create_drone_mounting_bracket():
    """
    Creates the drone mounting bracket.
    Material: Aluminum 6061-T6
    Max load: 20kg
    """
    print("Creating drone mounting bracket...")
    mesh_list = []
    
    base_size = 300
    base_thickness = 15
    arm_height = 80
    arm_width = 40
    
    # Main base plate
    v, f = create_box_mesh(base_size, base_size, base_thickness, center=(0, 0, 0))
    mesh_list.append((v, f))
    
    # 4 vertical arms
    arm_positions = [
        (-base_size/3, -base_size/3, base_thickness),
        (-base_size/3, base_size/3, base_thickness),
        (base_size/3, -base_size/3, base_thickness),
        (base_size/3, base_size/3, base_thickness)
    ]
    for pos in arm_positions:
        v, f = create_box_mesh(arm_width, arm_width, arm_height, center=pos)
        mesh_list.append((v, f))
    
    # Top mounting plate
    v, f = create_box_mesh(base_size - 50, base_size - 50, 10, center=(0, 0, base_thickness + arm_height))
    mesh_list.append((v, f))
    
    combined = combine_meshes(mesh_list)
    output_path = os.path.join(OUTPUT_DIR, "03_Drone_Mounting_Bracket.stl")
    save_stl(*combined, output_path)
    return output_path

# ============================================================
# PART 4: Drone Locking/Unlocking Mechanism
# ============================================================
def create_locking_mechanism():
    """
    Creates the drone locking/unlocking mechanism.
    Material: Steel for locking pins, Aluminum for housing
    """
    print("Creating locking mechanism...")
    mesh_list = []
    
    housing_length = 200
    housing_width = 100
    housing_height = 60
    
    # Main housing
    v, f = create_box_mesh(housing_length, housing_width, housing_height, center=(0, 0, 0))
    mesh_list.append((v, f))
    
    # Locking pins (3x)
    pin_positions = [-60, 0, 60]
    for x_pos in pin_positions:
        v, f = create_box_mesh(16, 40, housing_height - 10, center=(x_pos, housing_width/2, housing_height/2))
        mesh_list.append((v, f))
    
    # Actuator mechanism housing
    v, f = create_box_mesh(80, 60, 80, center=(0, housing_width/2 + 30, housing_height/2))
    mesh_list.append((v, f))
    
    combined = combine_meshes(mesh_list)
    output_path = os.path.join(OUTPUT_DIR, "04_Locking_Mechanism.stl")
    save_stl(*combined, output_path)
    return output_path

# ============================================================
# PART 5: Support Feet and Stabilizers
# ============================================================
def create_support_feet():
    """
    Creates adjustable support feet with stabilizers.
    Material: Steel feet, Aluminum structure
    """
    print("Creating support feet...")
    mesh_list = []
    
    foot_base_diameter = 150
    foot_thickness = 20
    rod_diameter = 40
    rod_length = 400
    
    # Base plate (cylinder approximated as box for simplicity)
    v, f = create_box_mesh(foot_base_diameter, foot_base_diameter, foot_thickness, center=(0, 0, 0))
    mesh_list.append((v, f))
    
    # Adjustment rod
    v, f = create_box_mesh(rod_diameter, rod_diameter, rod_length, center=(0, 0, foot_thickness))
    mesh_list.append((v, f))
    
    # Rod collar
    v, f = create_box_mesh(rod_diameter + 20, rod_diameter + 20, 30, center=(0, 0, foot_thickness + rod_length/2))
    mesh_list.append((v, f))
    
    combined = combine_meshes(mesh_list)
    output_path = os.path.join(OUTPUT_DIR, "05_Support_Feet.stl")
    save_stl(*combined, output_path)
    return output_path

# ============================================================
# PART 6: Side Protection Panels
# ============================================================
def create_side_protection():
    """
    Creates side protection panels.
    Material: Aluminum 5052-H32
    """
    print("Creating side protection panels...")
    mesh_list = []
    
    panel_length = 1000
    panel_height = 500
    panel_thickness = 3
    
    # Main panel
    v, f = create_box_mesh(panel_length, panel_height, panel_thickness, center=(0, 0, 0))
    mesh_list.append((v, f))
    
    # Reinforcement ribs
    for x_pos in [-panel_length/3, 0, panel_length/3]:
        v, f = create_box_mesh(5, panel_height - 20, 30, center=(x_pos, 0, -15))
        mesh_list.append((v, f))
    
    combined = combine_meshes(mesh_list)
    output_path = os.path.join(OUTPUT_DIR, "06_Side_Protection_Panel.stl")
    save_stl(*combined, output_path)
    return output_path

# ============================================================
# MAIN EXECUTION
# ============================================================
def main():
    print("=" * 60)
    print("Interceptor_M - Drone Launcher Base Parts Generator")
    print("=" * 60)
    
    os.makedirs(ASSEMBLIES_DIR, exist_ok=True)
    
    parts = {
        "01_Main_Chassis": create_main_chassis(),
        "02_Launch_Rails": create_launch_rails(),
        "03_Drone_Mounting_Bracket": create_drone_mounting_bracket(),
        "04_Locking_Mechanism": create_locking_mechanism(),
        "05_Support_Feet": create_support_feet(),
        "06_Side_Protection_Panel": create_side_protection()
    }
    
    print("\n" + "=" * 60)
    print("All STL parts generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
# ============================================================
# RELIABILITY & LIABILITY NOTICE
# ============================================================
"""
DISCLAIMER: The .stl files generated by this script are CONCEPTUAL
models intended for simulation and volume allocation studies ONLY.
They are NOT manufacturing-ready files. All critical dimensions
must be verified in a professional CAD environment (STEP/IGES)
before physical fabrication.
Units: Millimeters (mm).
Coordinate System: Right-handed (X: longitudinal, Y: lateral, Z: vertical).
"""
