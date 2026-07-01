#!/usr/bin/env python3
"""
Interceptor_M - Drone Airframe Generator (DD Line)
Generates high-fidelity parametric CAD for the Interceptor drone and internal component envelopes.
"""

import numpy as np
from stl import mesh
import os
import math

# Output configuration
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

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
    # Bottom Ring
    for i in range(n):
        next_i = (i + 1) % n
        faces.append([i, i + n, next_i])
        faces.append([next_i, i + n, next_i + n])
    # Top Ring
    for i in range(n):
        next_i = (i + 1) % n
        faces.append([i + 2*n, next_i + 2*n, i + 3*n])
        faces.append([next_i + 2*n, next_i + 3*n, i + 3*n])
    # Outer wall
    for i in range(n):
        next_i = (i + 1) % n
        faces.append([i + n, next_i + n, i + 3*n])
        faces.append([next_i + n, next_i + 3*n, i + 3*n])
    # Inner wall
    for i in range(n):
        next_i = (i + 1) % n
        faces.append([i, i + 2*n, next_i])
        faces.append([next_i, i + 2*n, next_i + 2*n])
    return vertices, np.array(faces)

def create_wing_mesh(span, chord_root, chord_tip, thickness, sweep_angle_deg, center=(0, 0, 0)):
    cx, cy, cz = center
    sweep_rad = math.radians(sweep_angle_deg)
    dx_tip = span * math.tan(sweep_rad)
    t = thickness / 2
    vertices = np.array([
        [cx, cy, cz - t], [cx + chord_root, cy, cz - t],
        [cx + dx_tip + chord_tip, cy + span, cz - t], [cx + dx_tip, cy + span, cz - t],
        [cx, cy, cz + t], [cx + chord_root, cy, cz + t],
        [cx + dx_tip + chord_tip, cy + span, cz + t], [cx + dx_tip, cy + span, cz + t]
    ])
    faces = np.array([
        [0,3,1], [1,3,2], [4,5,6], [4,6,7], [0,1,5], [0,5,4], [2,3,7], [2,7,6], [0,4,7], [0,7,3], [1,2,6], [1,6,5]
    ])
    return vertices, faces

def create_box_mesh(width, height, depth, center=(0, 0, 0)):
    w, h, d = width/2, height/2, depth/2
    cx, cy, cz = center
    vertices = np.array([
        [cx-w, cy-h, cz-d], [cx+w, cy-h, cz-d], [cx+w, cy+h, cz-d], [cx-w, cy+h, cz-d],
        [cx-w, cy-h, cz+d], [cx+w, cy-h, cz+d], [cx+w, cy+h, cz+d], [cx-w, cy+h, cz+d]
    ])
    faces = np.array([
        [0,3,1], [1,3,2], [0,4,7], [0,7,3], [4,5,6], [4,6,7], [1,2,6], [1,6,5], [0,1,5], [0,5,4], [2,3,7], [2,7,6]
    ])
    return vertices, faces

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
    stl_mesh.save(os.path.join(OUTPUT_DIR, filename))

def generate_airframe():
    print("Generating Interceptor_M Airframe (DD)...")
    v_fus, f_fus = create_hollow_cylinder_mesh(17.5, 16.0, 380, center=(190, 0, 0), segments=64)
    mesh_list = [(v_fus, f_fus)]
    # Wings
    v_wl, f_wl = create_wing_mesh(75, 60, 20, 2, 30, center=(100, 17.5, 0))
    v_wr, f_wr = create_wing_mesh(-75, 60, 20, 2, 30, center=(100, -17.5, 0))
    mesh_list.append((v_wl, f_wl)); mesh_list.append((v_wr, f_wr))
    # Fins
    v_wt, f_wt = create_wing_mesh(60, 40, 15, 2, 20, center=(320, 0, 17.5))
    v_wt[:, [1, 2]] = v_wt[:, [2, 1]]
    v_wb, f_wb = create_wing_mesh(-60, 40, 15, 2, 20, center=(320, 0, -17.5))
    v_wb[:, [1, 2]] = v_wb[:, [2, 1]]
    mesh_list.append((v_wt, f_wt)); mesh_list.append((v_wb, f_wb))
    combined = combine_meshes(mesh_list)
    save_stl(*combined, "INTERCEPTOR_DD_AIRFRAME.stl")

def generate_internals():
    print("Generating Internal Envelopes (FC, Battery, Motors)...")
    mesh_list = []
    mesh_list.append(create_box_mesh(30.5, 30.5, 10, center=(150, 0, 0)))
    mesh_list.append(create_box_mesh(50, 25, 15, center=(80, 0, 0)))
    for pos_y, pos_z in [(-12, -12), (-12, 12), (12, -12), (12, 12)]:
        mesh_list.append(create_box_mesh(15, 15, 20, center=(360, pos_y, pos_z)))
    combined = combine_meshes(mesh_list)
    save_stl(*combined, "INTERCEPTOR_DD_INTERNALS.stl")

def main():
    generate_airframe()
    generate_internals()
    print("All drone models generated successfully.")

if __name__ == "__main__":
    main()
