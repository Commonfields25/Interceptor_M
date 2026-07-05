import pytest
import os
import tempfile
import json
from scripts.param_sync_check import main

def test_sync_success(monkeypatch):
    params = {
        "lines": {
            "DD": {
                "mtow_g": 400.0,
                "segments": {"fuselage": {"L_mm": 380.0}}
            }
        }
    }
    constants = "MASSE_INTERCEPTOR_KG = 0.400\nLONGUEUR_INTERCEPTOR_MM = 380"

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        with open('PARAMETERS.json', 'w') as f:
            json.dump(params, f)
        os.makedirs('simulation')
        with open('simulation/constants.py', 'w') as f:
            f.write(constants)

        try:
            main()
        except SystemExit as e:
            assert e.code == 0
