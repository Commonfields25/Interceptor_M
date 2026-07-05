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

PART_MAP = {
    "BRK-001": build_brk001,
    "ACT-001": build_act001,
    "NCR-001": build_ncr001,
    "SABOT-001": build_sabot001,
    "CHS-001": build_chs001
}

def main():
    parser = argparse.ArgumentParser(description="Interceptor CAD (ICAD) CLI Engine")
    parser.add_argument("config", help="Path to YAML/JSON configuration file")
    parser.add_argument("--output", "-o", default="exports", help="Output directory")
    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f"Error: Config file {args.config} not found.")
        sys.exit(1)

    try:
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

    engine = CADEngine(output_dir=args.output)
    print(f"ICAD Engine started. Output: {args.output}")

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
