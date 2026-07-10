import argparse
import yaml
import sys
import os
from icad.engine import CADEngine
import icad.parts as parts

# Mapping Canonical IDs to their builder functions
PART_MAP = {
    "BRK-001": parts.build_brk001,
    "ACT-001": parts.build_act001,
    "NCR-001": parts.build_ncr001,
    "NC-001": parts.build_nc001,
    "FIN-001": parts.build_fin001,
    "SABOT-001": parts.build_sabot001,
    "CHS-001": parts.build_chs001,
    "WING-001": parts.build_wing001,
    "AVS-001": parts.build_avs001,
    "BAT-3S-001": parts.build_bat3s001,
    "MMT-001": parts.build_mmt001,
    "F1-BODY-01": parts.build_f1body01,
    "F1-MOTOR": parts.build_f1motor,
    "F1-PROP": parts.build_f1prop,
    "F1-AV-01": parts.build_f1avs,
    "F1-BAT-01": parts.build_f1bat,
    "F1-SEEK-01": parts.build_seeker01,
    "PAYLOAD-01": parts.build_payload01,
    "PDB-001": parts.build_pdb001,
    "LNCH-001": parts.build_lnch001,
    "LNCH-002": parts.build_lnch002,
    "LNCH-003": parts.build_lnch003,
    "LNCH-004": parts.build_lnch004,
    "LNCH-005": parts.build_lnch005,
    "LNCH-006": parts.build_lnch006,
    "PROP-022": parts.build_prop022,
    "PROP-023": parts.build_prop023,
    "PROP-024": parts.build_prop024,
    "PROP-025": parts.build_prop025,
    "PROP-026": parts.build_prop026,
}

# Aliases for TICKET-05 and legacy support
ALIASES = {
    "F1-BAT": "F1-BAT-01",
    "F1-AVS": "F1-AV-01",
    "BAT-CASE-01": "F1-BAT-01",
    "AV-MNT-01": "F1-AV-01",
    "SEEKER-01": "F1-SEEK-01",
    "F1-MOT-01": "F1-MOTOR",
    "F1-PROP-01": "F1-PROP",
    "MOT-MNT-01": "MMT-001"
}

def main():
    parser = argparse.ArgumentParser(description="Interceptor CAD (ICAD) CLI Engine")
    parser.add_argument("configs", nargs="+", help="Path to YAML/JSON configuration files")
    parser.add_argument("--output", "-o", default="exports", help="Output directory")
    args = parser.parse_args()

    engine = CADEngine(output_dir=args.output)
    print(f"ICAD Engine started. Output: {args.output}")

    for config_path in args.configs:
        if not os.path.exists(config_path):
            print(f"Error: Config file {config_path} not found.")
            continue
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config {config_path}: {e}")
            continue

        parts_to_gen = config.get("parts", [])
        for part_cfg in parts_to_gen:
            part_id = part_cfg.get("id")
            params = part_cfg.get("parameters", {})
            metadata = part_cfg.get("metadata", {})

            # Resolve Alias
            target_id = ALIASES.get(part_id, part_id)

            if target_id in PART_MAP:
                print(f"Generating {part_id} (Target: {target_id})...")
                builder = PART_MAP[target_id]
                shape = builder(params)

                # TICKET-01: Ensure output filename is the canonical ID (e.g. F1-BAT-01)
                engine.export_part(shape, target_id)
                engine.generate_drawings(shape, target_id)
                engine.generate_report(shape, target_id, metadata)
                print(f"  [OK] {target_id} complete.")
            else:
                print(f"Unknown part ID: {part_id}")

if __name__ == "__main__":
    main()
