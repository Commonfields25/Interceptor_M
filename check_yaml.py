#!/usr/bin/env python3
"""
check_yaml.py — Validate f1_parts.yaml syntax before commit.
Usage: python check_yaml.py [--fix]
Exit code 0 = valid, 1 = invalid, 2 = usage error.
"""
import sys
import yaml
import argparse
from pathlib import Path

DEFAULT_FILE = "f1_parts.yaml"


def load_yaml(path: Path):
    """Load and parse a YAML file, returning (data, errors)."""
    errors = []
    try:
        with path.open() as fh:
            data = yaml.safe_load(fh)
    except yaml.YAMLError as e:
        errors.append(str(e))
        return None, errors

    # Recursive schema check for f1_parts.yaml
    if path.name == "f1_parts.yaml":
        errors.extend(_validate_f1_schema(data, path))
        errors.extend(_validate_f1_refs(data))

    return data, errors


def _validate_f1_schema(data, path):
    errs = []
    if not isinstance(data, dict):
        errs.append(f"Root of {path} must be a dict (mapping), got {type(data).__name__}")
        return errs
    for key, val in data.items():
        if not isinstance(key, str):
            errs.append(f"Non-string key: {key!r} (type {type(key).__name__})")
        if isinstance(val, dict):
            for sub, sv in val.items():
                if not isinstance(sub, str):
                    errs.append(f"Non-string sub-key in '{key}': {sub!r}")
        elif not isinstance(val, (str, int, float, bool, list, type(None))):
            errs.append(f"Unrecognised value type for '{key}': {type(val).__name__}")
    return errs


def _validate_f1_refs(data):
    """Cross-check that every part-number reference resolves."""
    errs = []
    # Collect all known part numbers
    known = set()
    for group in data.values():
        if isinstance(group, dict):
            for part in group.values():
                if isinstance(part, dict) and "part_number" in part:
                    known.add(part["part_number"])
    # Check cross-references if _crossref field exists
    for group_key, group in data.items():
        if not isinstance(group, dict):
            continue
        for part_name, part in group.items():
            if not isinstance(part, dict):
                continue
            refs = part.get("_crossref", [])
            if isinstance(refs, str):
                refs = [refs]
            for ref in refs:
                if ref not in known:
                    errs.append(
                        f"Part '{part_name}' in group '{group_key}': "
                        f"cross-reference '{ref}' not found in any group."
                    )
    return errs


def main():
    parser = argparse.ArgumentParser(description="Validate YAML files.")
    parser.add_argument("file", nargs="?", default=DEFAULT_FILE,
                        help=f"YAML file to validate (default: {DEFAULT_FILE})")
    parser.add_argument("--fix", action="store_true",
                        help="Auto-fix fixable issues if supported")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    _, errors = load_yaml(path)

    if errors:
        print(f"❌ {path}: {len(errors)} error(s)")
        for e in errors:
            print(f"   • {e}")
        sys.exit(1)
    else:
        print(f"✅ {path}: valid")
        sys.exit(0)


if __name__ == "__main__":
    main()
