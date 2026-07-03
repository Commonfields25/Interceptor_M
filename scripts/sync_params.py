#!/usr/bin/env python3
"""
scripts/sync_params.py
Force l'alignement des fichiers de paramètres sur PARAMETERS.json
"""
import json
import os

def sync():
    with open('PARAMETERS.json', 'r') as f:
        master = json.load(f)

    dd_specs = master['lines']['DD']

    # 1. Update params/params_DD.json
    dd_params_path = 'params/params_DD.json'
    if os.path.exists(dd_params_path):
        with open(dd_params_path, 'r') as f:
            dd_params = json.load(f)

        dd_params['mtow_g'] = dd_specs['mtow_g']
        dd_params['segments']['fuselage']['L_mm'] = dd_specs['segments']['fuselage']['L_mm']
        dd_params['segments']['wing_span_m'] = dd_specs['segments']['wing_span_m']

        with open(dd_params_path, 'w') as f:
            json.dump(dd_params, f, indent=2)
        print(f"Updated {dd_params_path}")

    # 2. Update simulation/constants.py (limited sync for now)
    constants_path = 'simulation/constants.py'
    if os.path.exists(constants_path):
        with open(constants_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if 'MASSE_INTERCEPTOR_KG =' in line:
                new_lines.append(f'MASSE_INTERCEPTOR_KG = {dd_specs["mtow_g"]/1000.0:.3f}  # Synced from PARAMETERS.json\n')
            elif 'LONGUEUR_INTERCEPTOR_MM =' in line:
                new_lines.append(f'LONGUEUR_INTERCEPTOR_MM = {dd_specs["segments"]["fuselage"]["L_mm"]}  # Synced from PARAMETERS.json\n')
            else:
                new_lines.append(line)

        with open(constants_path, 'w') as f:
            f.writelines(new_lines)
        print(f"Updated {constants_path}")

if __name__ == "__main__":
    sync()
