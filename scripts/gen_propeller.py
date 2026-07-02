import numpy as np
from stl import mesh
import math

def create_propeller_mesh(radius, chord, pitch_deg, center=(0, 0, 0), num_blades=2):
    """
    Creates a high-poly propeller model.
    """
    cx, cy, cz = center
    vertices = []
    faces = []

    segments = 20
    sections = 10

    for b in range(num_blades):
        angle_offset = 2 * math.pi * b / num_blades
        for s in range(sections):
            r = (s / (sections - 1)) * radius
            if r == 0: r = 0.1 # avoid singularity

            # Chord distribution (elliptical-ish)
            local_chord = chord * math.sqrt(1 - (r/radius)**2) if r < radius else 0.1

            # Twist (pitch)
            local_pitch = math.radians(pitch_deg * (1 - 0.5 * (r/radius)))

            # NACA 0012-ish profile points
            for i in range(segments):
                t = i / (segments - 1)
                x = t * local_chord - local_chord/2
                # Thickness
                y = 0.12 * local_chord * (0.2969*math.sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1015*t**4)

                # Rotate by pitch and angle offset
                # 1. Profile rotation (pitch)
                x_rot = x * math.cos(local_pitch) - y * math.sin(local_pitch)
                y_rot = x * math.sin(local_pitch) + y * math.cos(local_pitch)

                # 2. Blade rotation
                final_x = r * math.cos(angle_offset) + x_rot * (-math.sin(angle_offset))
                final_y = r * math.sin(angle_offset) + x_rot * (math.cos(angle_offset))
                final_z = y_rot

                vertices.append([cx + final_x, cy + final_y, cz + final_z])

    # Logic for faces between sections omitted for this step,
    # but the concept is to bridge vertices of section i and i+1.
    return np.array(vertices), np.array(faces)

if __name__ == "__main__":
    v, f = create_propeller_mesh(40, 10, 20)
    print(f"Propeller vertices: {len(v)}")
