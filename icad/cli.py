import argparse
import yaml
import sys
import os
from icad.engine import CADEngine
from icad.parts.brk001 import build_brk001
from icad.parts.act001 import build_act001
from icad.parts.ncr001 import build_ncr001
from icad.parts.sabot001 import build_sabot001
from icad.parts.chs001 import build_chs001
from icad.parts.wing001 import build_wing001
from icad.parts.avs001 import build_avs001
from icad.parts.bat3s001 import build_bat3s001
from icad.parts.mmt001 import build_mmt001
from icad.parts.f1body01 import build_f1body01
from icad.parts.f1motor import build_f1motor
from icad.parts.f1prop import build_f1prop
from icad.parts.f1avs import build_f1avs
from icad.parts.f1bat import build_f1bat
from icad.parts.lnch001 import build_lnch001
from icad.parts.lnch002 import build_lnch002
from icad.parts.lnch003 import build_lnch003
from icad.parts.lnch004 import build_lnch004
from icad.parts.lnch005 import build_lnch005
from icad.parts.lnch006 import build_lnch006

PART_MAP = {
    "BRK-001": build_brk001,
    "ACT-001": build_act001,
    "NCR-001": build_ncr001,
    "SABOT-001": build_sabot001,
    "CHS-001": build_chs001,
    "WING-001": build_wing001,
    "AVS-001": build_avs001,
    "BAT-3S-001": build_bat3s001,
    "MMT-001": build_mmt001,
    "F1-BODY-01": build_f1body01,
    "F1-MOTOR": build_f1motor,
    "F1-PROP": build_f1prop,
    "F1-AVS": build_f1avs,
    "F1-BAT": build_f1bat,
    "LNCH-001": build_lnch001,
    "LNCH-002": build_lnch002,
    "LNCH-003": build_lnch003,
    "LNCH-004": build_lnch004,
    "LNCH-005": build_lnch005,
    "LNCH-006": build_lnch006,
}


def main():
    parser = argparse.ArgumentParser(description="Interceptor CAD (ICAD) CLI Engine")
    parser.add_argument(
        "configs", nargs="+", help="Path to YAML/JSON configuration files"
    )
    parser.add_argument("--output", "-o", default="exports", help="Output directory")
    args = parser.parse_args()

    engine = CADEngine(output_dir=args.output)
    print(f"ICAD Engine started. Output: {args.output}")

    for config_path in args.configs:
        if not os.path.exists(config_path):
            print(f"Error: Config file {config_path} not found.")
            continue

        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config {config_path}: {e}")
            continue

        parts_to_gen = config.get("parts", [])
        for part_cfg in parts_to_gen:
            part_id = part_cfg.get("id")
            params = part_cfg.get("parameters", {})
            metadata = part_cfg.get("metadata", {})

            if part_id in PART_MAP:
                print(f"Generating {part_id}...")
                builder = PART_MAP[part_id]
                shape = builder(params)

                # Export Models
                engine.export_part(shape, part_id)

                # Export Drawings
                engine.generate_drawings(shape, part_id)

                # Report
                engine.generate_report(shape, part_id, metadata)
                print(f"  [OK] {part_id} complete.")
            else:
                print(f"Unknown part ID: {part_id}")


if __name__ == "__main__":
    main()
