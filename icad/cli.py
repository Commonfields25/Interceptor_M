import argparse
import yaml
import sys
import os
from icad.engine import CADEngine
import icad.parts as parts

PART_MAP = {
    "BRK-001": parts.build_brk001,
    "ACT-001": parts.build_act001,
    "NCR-001": parts.build_ncr001,
    "SABOT-001": parts.build_sabot001,
    "CHS-001": parts.build_chs001,
    "WING-001": parts.build_wing001,
    "AV-MNT-01": parts.build_avmnt01,
    "BAT-CASE-01": parts.build_batcase01,
    "MOT-MNT-01": parts.build_motmnt01,
    "F1-BODY-01": parts.build_f1body01,
    "F1-MOT-01": parts.build_f1mot01,
    "F1-PROP-01": parts.build_f1prop01,
    "F1-AV-01": parts.build_f1av01,
    "F1-BAT-01": parts.build_f1bat01,
    "LNCH-001": parts.build_lnch001,
    "LNCH-002": parts.build_lnch002,
    "LNCH-003": parts.build_lnch003,
    "LNCH-004": parts.build_lnch004,
    "LNCH-005": parts.build_lnch005,
    "LNCH-006": parts.build_lnch006,
    "SEEKER-01": parts.build_seeker01,
    "PAYLOAD-01": parts.build_payload01,
    "F1-SEEK-01": parts.build_f1seek01,
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

            # Export PDF Drawing
            try:
                engine.generate_pdf_drawing(part_id)
            except Exception as e:
                print(f"  [WARN] PDF drawing failed for {part_id}: {e}")

            # Report
            engine.generate_report(shape, part_id, metadata)
            print(f"  [OK] {part_id} complete.")
        else:
            print(f"Unknown part ID: {part_id}")

if __name__ == "__main__":
    main()
