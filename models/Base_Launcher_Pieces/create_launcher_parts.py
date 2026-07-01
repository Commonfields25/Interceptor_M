#!/usr/bin/env python3
"""
Interceptor_M - Drone Launcher Base Parts Generator (High-Fidelity Edition)
Generates parametric CAD parts using numpy-stl with integrated assembly points and tolerances.
"""

import numpy as np
from stl import mesh
import os
import math

# Use relative paths for portability
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = SCRIPT_DIR
ASSEMBLIES_DIR = os.path.join(OUTPUT_DIR, "Assemblies")

def create_box_mesh(width, height, depth, center=(0, 0, 0)):
    if width <= 0 or height <= 0 or depth <= 0: raise ValueError("Dimensions must be positive")
    w, h, d = width/2, height/2, depth/2
    cx, cy, cz = center
    vertices = np.array([
        [cx-w, cy-h, cz-d], [cx+w, cy-h, cz-d],
        [cx+w, cy+h, cz-d], [cx-w, cy+h, cz-d],
        [cx-w, cy-h, cz+d], [cx+w, cy-h, cz+d],
        [cx+w, cy+h, cz+d], [cx-w, cy+h, cz+d]
    ])
    faces = np.array([
        [0,3,1], [1,3,2], [0,4,7], [0,7,3],
        [4,5,6], [4,6,7], [1,2,6], [1,6,5],
        [0,1,5], [0,5,4], [2,3,7], [2,7,6]
    ])
    return vertices, faces

def create_cylinder_mesh(radius, height, center=(0, 0, 0), segments=32):
    if radius <= 0 or height <= 0: raise ValueError("Dimensions must be positive")
    cx, cy, cz = center
    vertices = [[cx, cy, cz - height/2]]
    for i in range(segments):
        theta = 2.0 * math.pi * i / segments
        vertices.append([cx + radius * math.cos(theta), cy + radius * math.sin(theta), cz - height/2])
    vertices.append([cx, cy, cz + height/2])
    for i in range(segments):
        theta = 2.0 * math.pi * i / segments
        vertices.append([cx + radius * math.cos(theta), cy + radius * math.sin(theta), cz + height/2])
    vertices = np.array(vertices)
    n = segments
    faces = []
    for i in range(1, n + 1):
        next_i = 1 if i == n else i + 1
        faces.append([0, next_i, i])
    top_center = n + 1
    for i in range(1, n + 1):
        next_i = 1 if i == n else i + 1
        faces.append([top_center, i + n + 1, next_i + n + 1])
    for i in range(1, n + 1):
        next_i = 1 if i == n else i + 1
        faces.append([i, next_i, i + n + 1])
        faces.append([next_i, next_i + n + 1, i + n + 1])
    return vertices, np.array(faces)

def create_hollow_cylinder_mesh(outer_radius, inner_radius, height, center=(0, 0, 0), segments=32):
    cx, cy, cz = center
    vertices = []
    for z_off in [-height/2, height/2]:
        for r in [inner_radius, outer_radius]:
            for i in range(segments):
                theta = 2.0 * math.pi * i / segments
                vertices.append([cx + r * math.cos(theta), cy + r * math.sin(theta), cz + z_off])
    vertices = np.array(vertices)
    n = segments
    faces = []
    for i in range(n):
        next_i = (i + 1) % n
        faces.append([i, i + n, next_i])
        faces.append([next_i, i + n, next_i + n])
    for i in range(n):
        next_i = (i + 1) % n
        faces.append([i + 2*n, next_i + 2*n, i + 3*n])
        faces.append([next_i + 2*n, next_i + 3*n, i + 3*n])
    for i in range(n):
        next_i = (i + 1) % n
        faces.append([i + n, next_i + n, i + 3*n])
        faces.append([next_i + n, next_i + 3*n, i + 3*n])
    for i in range(n):
        next_i = (i + 1) % n
        faces.append([i, i + 2*n, next_i])
        faces.append([next_i, i + 2*n, next_i + 2*n])
    return vertices, np.array(faces)

def combine_meshes(mesh_list):
    combined_vertices = []
    combined_faces = []
    offset = 0
    for vertices, faces in mesh_list:
        combined_vertices.append(vertices)
        combined_faces.append(faces + offset)
        offset += len(vertices)
    return np.vstack(combined_vertices), np.vstack(combined_faces)

def save_stl(vertices, faces, filename):
    stl_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        stl_mesh.vectors[i] = vertices[face]
    stl_mesh.save(filename)

# --- Refactored Part Generators ---

def create_main_chassis():
    print("Creating main chassis (v2.3)...")
    mesh_list = []
    for y_pos in [-100, 100]:
        v, f = create_box_mesh(2000, 50, 10, center=(0, y_pos, 0))
        mesh_list.append((v, f))
        v, f = create_box_mesh(2000, 10, 50, center=(0, y_pos + 20, 25))
        mesh_list.append((v, f))
    for x_pos in [-900, 0, 900]:
        v, f = create_box_mesh(10, 250, 50, center=(x_pos, 0, 25))
        mesh_list.append((v, f))
    combined = combine_meshes(mesh_list)
    save_stl(*combined, os.path.join(OUTPUT_DIR, "01_Main_Chassis.stl"))

def create_launch_rails():
    print("Creating launch rails (v2.3)...")
    mesh_list = []
    v, f = create_box_mesh(1500, 60, 20, center=(0, 0, 0))
    mesh_list.append((v, f))
    for pos_y in [-20, 20]:
        v, f = create_box_mesh(1500, 10, 40, center=(0, pos_y, 15))
        mesh_list.append((v, f))
    combined = combine_meshes(mesh_list)
    save_stl(*combined, os.path.join(OUTPUT_DIR, "02_Launch_Rails.stl"))

def create_drone_mounting_bracket():
    """Refactored Mounting Bracket with light-weighting and M3 holes"""
    print("Creating drone mounting bracket (v2.3)...")
    mesh_list = []
    # Main structural ring (approximated as hollow cylinder)
    v, f = create_hollow_cylinder_mesh(60, 40, 15, center=(0, 0, 0))
    mesh_list.append((v, f))
    # 4 Mounting arms with M3 holes
    for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
        cx, cy = 80 * math.cos(angle), 80 * math.sin(angle)
        # Arm
        v, f = create_box_mesh(30, 30, 10, center=(cx, cy, 0))
        mesh_list.append((v, f))
        # M3 Hole (represented as small additive cylinder for boundary)
        v, f = create_cylinder_mesh(1.6, 12, center=(cx, cy, 0))
        mesh_list.append((v, f))
    combined = combine_meshes(mesh_list)
    save_stl(*combined, os.path.join(OUTPUT_DIR, "03_Drone_Mounting_Bracket.stl"))

def create_sabot():
    v, f = create_hollow_cylinder_mesh(20, 17.5, 60, center=(0, 0, 0))
    save_stl(v, f, os.path.join(OUTPUT_DIR, "SABOT-001.stl"))

def main():
    os.makedirs(ASSEMBLIES_DIR, exist_ok=True)
    create_main_chassis()
    create_launch_rails()
    create_drone_mounting_bracket()
    create_sabot()
    print("All parts generated.")

if __name__ == "__main__":
    main()
