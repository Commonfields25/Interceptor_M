#!/usr/bin/env python3
"""
Namespace Isolation CI Check (Hardened v1.2)
Validates that all files changed in a PR belong to the author's allowed namespace.
Covers all project root directories.
"""

import sys
import os
import argparse
import json
import re
from pathlib import Path
from typing import Optional

# ─── Hardened Namespace Map ───────────────────────────────────────────────────

NAMESPACE_MAP: dict[str, list[str]] = {
    "agent_manager": [
        "agents/agent_manager/",
        "deliverables/",
    ],
    "D1": [
        "agents/D1/",
        "models/DC/",
        "docs/D1/",
    ],
    "D2": [
        "agents/D2/",
        "models/DI/",
        "docs/D2/",
    ],
    "D3": [
        "agents/D3/",
        "models/DD/",
        "docs/D3/",
    ],
    "E1": [
        "agents/E1/",
        "engineering/NDC/",
        "engineering/FEA/",
        "engineering/simulation/",
        "params/",  # Systems owns the master params
    ],
    "E2": [
        "agents/E2/",
        "engineering/ML/",
        "engineering/CFD/",
        "simulation/",  # E2 owns flight dynamics simulation
    ],
    "E3": [
        "agents/E3/",
        "engineering/simulation/",
        "hardware/",  # E3 owns hardware integration
    ],
    "AC": [
        "agents/AC/",
        "governance/",
        "manufacturing/",  # AC audits manufacturing gammes
    ],
    "commercial": [
        "agents/commercial/",
    ],
    "marketing": [
        "agents/marketing/",
    ],
}

# Root-level files that are strictly protected
# Changes to these usually require DG approval or AM lead.
CRITICAL_ROOT_FILES: list[str] = [
    "PARAMETERS.json",
    "MILESTONE_PLAN.md",
    "PRODUCT-FAMILY.md",
    "rules.md",
]

# Shared read-only paths (any agent may touch for documentation)
SHARED_ALLOWED: list[str] = [
    "governance/BOT_GUIDELINES.md",
    "README.md",
    ".github/",
    ".gitignore",
]


def is_in_namespace(file_path: str, allowed_prefixes: list[str]) -> bool:
    fp = file_path.strip().lstrip("/")
    for prefix in allowed_prefixes:
        if fp.startswith(prefix.rstrip("/")):
            return True
    return False


def validate_pr_files(files: list[str], author_agent: str) -> tuple[bool, list[str]]:
    if author_agent not in NAMESPACE_MAP:
        return False, [f"Unknown agent '{author_agent}'."]

    allowed = NAMESPACE_MAP[author_agent]
    violations = []

    for f in files:
        fp = f.strip()
        if not fp:
            continue

        # Check if it's a critical root file
        if fp in CRITICAL_ROOT_FILES and author_agent != "agent_manager":
            violations.append(
                f"  ✗ {fp} — Critical root file. Requires Agent Manager approval."
            )
            continue

        in_ns = is_in_namespace(fp, allowed)
        is_shared = (
            any(fp.startswith(s) for s in SHARED_ALLOWED) or fp in SHARED_ALLOWED
        )

        if not in_ns and not is_shared:
            violations.append(f"  ✗ {fp} — Outside namespace of agent '{author_agent}'")

    return len(violations) == 0, violations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--changed-files", help="List of files")
    parser.add_argument("--author-agent", help="Agent ID")
    args = parser.parse_args()

    if not args.changed_files or not args.author_agent:
        print("Usage: --changed-files 'f1 f2' --author-agent D1")
        sys.exit(2)

    files = args.changed_files.split()
    compliant, violations = validate_pr_files(files, args.author_agent)

    if not compliant:
        for v in violations:
            print(v)
        sys.exit(1)

    print("✅ Namespace Protection: ACTIVE and COMPLIANT.")
    sys.exit(0)


if __name__ == "__main__":
    main()
