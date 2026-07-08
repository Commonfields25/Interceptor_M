#!/usr/bin/env python3
"""
Interceptor_M — Project Quality Scanner (AC Tool)
Audits files for IAMD compliance, header presence, and formatting.
"""

import os
import re
import sys


def check_iamd_header(file_path):
    """Checks if a markdown file starts with the required YAML header."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read(500)  # Read first 500 chars
        if content.strip().startswith("---"):
            # Check for mandatory fields
            if "agent:" in content and "action:" in content and "timestamp:" in content:
                return True
    return False


def scan_project(root_dir="."):
    print(f"--- 🔍 AC Quality Scan: {root_dir} ---")
    violations = 0
    scanned = 0

    # Files to exclude from IAMD check
    exclude_dirs = {".git", "node_modules", "venv", "__pycache__"}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file.endswith(".md"):
                scanned += 1
                path = os.path.join(root, file)
                if not check_iamd_header(path):
                    print(f"  ❌ Missing/Invalid IAMD Header: {path}")
                    violations += 1

    print(f"\n--- Scan Summary ---")
    print(f"  Markdown Files Scanned: {scanned}")
    print(f"  IAMD Violations: {violations}")

    return violations == 0


if __name__ == "__main__":
    success = scan_project()
    sys.exit(0 if success else 1)
