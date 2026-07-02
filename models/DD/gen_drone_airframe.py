#!/usr/bin/env python3
"""
Interceptor_M - Professional Aerospace-Grade Airframe & Propeller Generator
Version: 2.0 (High-Fidelity)
Authors: D1/D2/D3 Composite
Features:
- Tangent Ogive Nose Cone
- NACA 0012 Airfoil Wings/Fins
- High-Poly Twisted Propellers
- Mass-Optimized Hollow Shells
"""

import numpy as np
from stl import mesh
import os
import math

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_naca_4digit(m, p, t, c, n=32):
    x = np.linspace(0, c, n)
    yt = 5 * t * c * (0.2969 * np.sqrt(x/c) - 0.1260 * (x/c) - 0.3516 * (x/c)**2 + 0.2843 * (x/c)**3 - 0.1015 * (x/c)**4)
    yc = np.zeros_like(x)
    if m > 0:
        yc[x <= p*c] = m * (x[x <= p*c] / p**2) * (2*p - (x[x <= p*c]/c))
        yc[x > p*c] = m * ((c - x[x > p*c]) / (1-p)**2) * (1 + (x[x > p*c]/c) - 2*p)
    return x, yc, yt

def create_aero_surface(span, root_chord, tip_chord, sweep_deg, center=(0,0,0), vertical=False):
    cx, cy, cz = center
    n_points = 24
    sweep_rad = math.radians(sweep_deg)

    # Airfoil (NACA 0012)
    m, p, t = 0, 0, 0.12

    vertices = []
    faces = []

    # 1. Root Section
    x, yc, yt = get_naca_4digit(m, p, t, root_chord, n_points)
    for i in range(n_points):
        vertices.append([cx + x[i], cy, cz + yc[i] + yt[i]])
    for i in range(n_points-1, -1, -1):
        vertices.append([cx + x[i], cy, cz + yc[i] - yt[i]])

    # 2. Tip Section
    dx_tip = abs(span) * math.tan(sweep_rad)
    x_t, yc_t, yt_t = get_naca_4digit(m, p, t, tip_chord, n_points)
    for i in range(n_points):
        vertices.append([cx + dx_tip + x_t[i], cy + span, cz + yc_t[i] + yt_t[i]])
    for i in range(n_points-1, -1, -1):
        vertices.append([cx + dx_tip + x_t[i], cy + span, cz + yc_t[i] - yt_t[i]])

    v = np.array(vertices)
    if vertical:
        temp_y = v[:, 1] - cy
        temp_z = v[:, 2] - cz
        v[:, 1] = cy - temp_z
        v[:, 2] = cz + temp_y

    n = n_points * 2
    for i in range(n):
        next_i = (i + 1) % n
        faces.append([i, next_i, i + n])
        faces.append([next_i, next_i + n, i + n])
    for i in range(1, n-1):
        faces.append([0, i, i+1])
        faces.append([n, n+i+1, n+i])
    return v, np.array(faces)

def create_ogive_nose(radius, length, center=(0,0,0), segments=32):
    cx, cy, cz = center
    v, f = [], []
    # Tangent Ogive Rho calculation
    rho = (radius**2 + length**2) / (2 * radius)

    x_vals = np.linspace(0, length, 20)
    for i, x in enumerate(x_vals):
        # y = sqrt(rho^2 - (L-x)^2) + R - rho
        r_curr = math.sqrt(rho**2 - (length - x)**2) + radius - rho
        for s in range(segments):
            theta = 2 * math.pi * s / segments
            v.append([cx + x, cy + r_curr * math.cos(theta), cz + r_curr * math.sin(theta)])

    v = np.array(v)
    for i in range(len(x_vals)-1):
        for s in range(segments):
            s1, s2 = i * segments + s, i * segments + (s + 1) % segments
            s3, s4 = (i + 1) * segments + s, (i + 1) * segments + (s + 1) % segments
            f.append([s1, s2, s3]); f.append([s2, s4, s3])
    # Nose tip cap
    for s in range(1, segments-1):
        f.append([0, s, s+1])
    return v, np.array(f)

def create_hollow_fuselage(radius, thickness, length, center=(0, 0, 0), segments=32):
    cx, cy, cz = center
    v, f = [], []
    x_steps = 20
    for i, x_off in enumerate(np.linspace(0, length, x_steps)):
        r_curr = radius
        r_inner = r_curr - thickness
        for r in [r_curr, r_inner]:
            for s in range(segments):
                theta = 2 * math.pi * s / segments
                v.append([cx + x_off, cy + r * math.cos(theta), cz + r * math.sin(theta)])
    v = np.array(v)
    for i in range(x_steps-1):
        for s in range(segments):
            c_s = i * segments * 2
            n_s = (i + 1) * segments * 2
            # Outer
            f.append([c_s + s, c_s + (s+1)%segments, n_s + s])
            f.append([c_s + (s+1)%segments, n_s + (s+1)%segments, n_s + s])
            # Inner
            f.append([c_s + s + segments, n_s + s + segments, c_s + (s+1)%segments + segments])
            f.append([c_s + (s+1)%segments + segments, n_s + s + segments, n_s + (s+1)%segments + segments])
    return v, np.array(f)

def create_propeller(radius, chord, pitch_deg, center=(0, 0, 0), rotation_rad=0):
    cx, cy, cz = center
    v, f = [], []
    sections = 15
    n_pts = 16
    for b in [0, math.pi]: # 2 blades
        blade_rot = rotation_rad + b
        for i in range(sections):
            r_l = (i / (sections-1)) * radius
            if r_l < 2: r_l = 2 # Hub clearance
            c_l = chord * math.sqrt(1 - (r_l/radius)**2) + 0.5
            p_l = math.radians(pitch_deg * (1 - 0.3 * (r_l/radius)))
            x_a, yc_a, yt_a = get_naca_4digit(0, 0, 0.12, c_l, n_pts)
            for j in range(n_pts):
                px, pz = x_a[j] - c_l/2, yc_a[j] + yt_a[j]
                rx = px * math.cos(p_l) - pz * math.sin(p_l)
                rz = px * math.sin(p_l) + pz * math.cos(p_l)
                gx = r_l * math.cos(blade_rot) - rx * math.sin(blade_rot)
                gy = r_l * math.sin(blade_rot) + rx * math.cos(blade_rot)
                v.append([cx + gx, cy + gy, cz + rz])
            for j in range(n_pts-1, -1, -1):
                px, pz = x_a[j] - c_l/2, yc_a[j] - yt_a[j]
                rx = px * math.cos(p_l) - pz * math.sin(p_l)
                rz = px * math.sin(p_l) + pz * math.cos(p_l)
                gx = r_l * math.cos(blade_rot) - rx * math.sin(blade_rot)
                gy = r_l * math.sin(blade_rot) + rx * math.cos(blade_rot)
                v.append([cx + gx, cy + gy, cz + rz])
    v = np.array(v)
    n = n_pts * 2
    for b in range(2):
        b_off = b * sections * n
        for i in range(sections - 1):
            for j in range(n):
                s1, s2 = b_off + i * n + j, b_off + i * n + (j + 1) % n
                s3, s4 = b_off + (i + 1) * n + j, b_off + (i + 1) * n + (j + 1) % n
                f.append([s1, s2, s3]); f.append([s2, s4, s3])
    return v, np.array(f)

def combine_meshes(mesh_list):
    cv, cf = [], []
    offset = 0
    for v, f in mesh_list:
        cv.append(v)
        cf.append(f + offset)
        offset += len(v)
    return np.vstack(cv), np.vstack(cf)

def main():
    print("🚀 Generating Professional High-Fidelity Drone Airframe (v2.0)...")
    m_list = []
    # 1. Nose (Tangent Ogive)
    m_list.append(create_ogive_nose(17.5, 60, center=(0,0,0)))
    # 2. Fuselage
    m_list.append(create_hollow_fuselage(17.5, 1.5, 320, center=(60,0,0)))
    # 3. Wings (NACA 0012)
    m_list.append(create_aero_surface(120, 80, 30, 35, center=(80, 17.5, 0)))
    m_list.append(create_aero_surface(-120, 80, 30, 35, center=(80, -17.5, 0)))
    # 4. Tail Fins
    m_list.append(create_aero_surface(60, 50, 20, 20, center=(320, 0, 15), vertical=True))
    m_list.append(create_aero_surface(-60, 50, 20, 20, center=(320, 0, -15), vertical=True))
    # 5. Propellers (4x Professional Grade)
    # Positions corresponding to motor mounts in concept
    for x, y, z, r in [(140, 60, 0, 0), (140, -60, 0, 0), (340, 0, 40, math.pi/2), (340, 0, -40, -math.pi/2)]:
        m_list.append(create_propeller(35, 8, 25, center=(x, y, z), rotation_rad=r))

    cv, cf = combine_meshes(m_list)
    out = os.path.join(OUTPUT_DIR, "INTERCEPTOR_DD_PRO_V2.stl")
    m = mesh.Mesh(np.zeros(len(cf), dtype=mesh.Mesh.dtype))
    for i, face in enumerate(cf): m.vectors[i] = cv[face]
    m.save(out)
    print(f"✅ Baseline v2.0 Generated: {out}")

if __name__ == "__main__":
    main()
