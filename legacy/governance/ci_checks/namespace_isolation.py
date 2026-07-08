#!/usr/bin/env python3
"""
Namespace Isolation CI Check
Validates that all files changed in a PR belong to the author's allowed namespace.

Usage (local):
    python3 governance/ci_checks/namespace_isolation.py --changed-files "file1.md agents/D1/file2.md" --author-agent D1

Usage (GitHub Actions — via governance.yml):
    python3 governance/ci_checks/namespace_isolation.py

Exit codes:
    0 = compliant (all files within allowed namespace)
    1 = violation detected
    2 = invalid input / unknown agent
"""

import sys
import os
import argparse
import json
import re
from pathlib import Path
from typing import Optional

# ─── Namespace Map ────────────────────────────────────────────────────────────

NAMESPACE_MAP: dict[str, list[str]] = {
    "agent_manager": [
        "agents/agent_manager/",
        "deliverables/",
    ],
    "D1": [
        "agents/D1/",
        "models/DC/",
    ],
    "D2": [
        "agents/D2/",
        "models/DI/",
    ],
    "D3": [
        "agents/D3/",
        "models/DD/",
    ],
    "E1": [
        "agents/E1/",
        "engineering/NDC/",
        "engineering/FEA/",
        "engineering/simulation/",
    ],
    "E2": [
        "agents/E2/",
        "engineering/ML/",
        "engineering/CFD/",
    ],
    "E3": [
        "agents/E3/",
        "engineering/simulation/",
    ],
    "AC": [
        "agents/AC/",
        "governance/",
    ],
    "commercial": [
        "agents/commercial/",
    ],
    "marketing": [
        "agents/marketing/",
    ],
}

# Shared read-only paths that any agent may touch lightly
SHARED_ALLOWED: list[str] = [
    "governance/BOT_GUIDELINES.md",
    "governance/AGENT_MANAGER_RULES.md",
    "governance/guidelines.md",
    "governance/rules.md",
    "governance/NAMESPACE-ISOLATION.md",
    "governance/AUTO-APPROVAL-POLICY.md",
    ".github/workflows/",
    "README.md",
    "PARAMETERS.json",
]

# Agent Manager may write to these additional shared files
AM_EXTRA_SHARED: list[str] = [
    "agents/agent_manager/DECISION_LOG.md",
    "deliverables/GATE_G",
    "agents/agent_manager/gate_packages/",
    "agents/agent_manager/daily_digest/",
]


def is_in_namespace(file_path: str, allowed_prefixes: list[str]) -> bool:
    """Return True if file_path starts with one of the allowed path prefixes."""
    fp = file_path.strip().lstrip("/")
    for prefix in allowed_prefixes:
        if fp.startswith(prefix.rstrip("/")):
            return True
    return False


def is_shared_readonly(file_path: str) -> bool:
    """Return True if file is a shared read-only file that any agent may touch."""
    fp = file_path.strip().lstrip("/")
    for entry in SHARED_ALLOWED:
        if fp.startswith(entry.rstrip("/")) or fp == entry.rstrip("/"):
            return True
    return False


def is_am_extra_shared(file_path: str, agent: str) -> bool:
    """Additional files the Agent Manager may write."""
    if agent != "agent_manager":
        return False
    fp = file_path.strip().lstrip("/")
    for entry in AM_EXTRA_SHARED:
        if fp.startswith(entry.rstrip("/")):
            return True
    return False


def validate_pr_files(files: list[str], author_agent: str) -> tuple[bool, list[str]]:
    """
    Validate a list of changed file paths against the author's namespace.
    Returns (is_compliant, list_of_violations).
    """
    if author_agent not in NAMESPACE_MAP:
        return False, [
            f"Unknown agent '{author_agent}'. Valid agents: {list(NAMESPACE_MAP.keys())}"
        ]

    allowed = NAMESPACE_MAP[author_agent]
    violations = []

    for f in files:
        fp = f.strip()
        if not fp:
            continue
        in_ns = is_in_namespace(fp, allowed)
        is_shared = is_shared_readonly(fp)
        is_am_extra = is_am_extra_shared(fp, author_agent)

        if not in_ns and not is_shared and not is_am_extra:
            violations.append(
                f"  ✗ {fp} — outside namespace of agent '{author_agent}' "
                f"(allowed: {', '.join(allowed)})"
            )

    return len(violations) == 0, violations


def extract_agent_from_branch(branch_name: str) -> Optional[str]:
    """
    Extract agent ID from branch name following feat/<AgentID>/... convention.
    Returns None if no match.
    """
    m = re.match(r"^(?:feat|fix|docs|refactor|chore)/([A-Za-z_]+)/", branch_name)
    if m:
        return m.group(1)
    return None


def main():
    parser = argparse.ArgumentParser(description="Namespace Isolation CI Check")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--changed-files", help="Space-separated list of changed file paths"
    )
    group.add_argument(
        "--json-input", help="JSON array of changed files (for GitHub Actions)"
    )
    group.add_argument(
        "--branch-name", help="Branch name to auto-derive agent from --changed-files"
    )
    parser.add_argument("--author-agent", help="Override agent ID (e.g. D1, E2)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    # Determine files list
    if args.json_input:
        try:
            files = json.loads(args.json_input)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON input: {e}", file=sys.stderr)
            sys.exit(2)
    elif args.changed_files:
        files = args.changed_files.split()
    else:
        print("ERROR: No input provided", file=sys.stderr)
        sys.exit(2)

    # Determine agent
    if args.author_agent:
        author = args.author_agent.lower()
    elif args.branch_name:
        author = extract_agent_from_branch(args.branch_name)
        if author is None:
            print(
                f"WARNING: Could not extract agent from branch '{args.branch_name}'. "
                "Assuming 'agent_manager' as fallback.",
                file=sys.stderr,
            )
            author = "agent_manager"
    else:
        print("ERROR: Must provide --author-agent or --branch-name", file=sys.stderr)
        sys.exit(2)

    if args.verbose:
        print(f"Author agent : {author}")
        print(f"Changed files: {files}")

    compliant, violations = validate_pr_files(files, author)

    print(f"\n{'=' * 60}")
    print(f"Namespace Isolation Check — Agent: {author}")
    print(f"{'=' * 60}")
    print(f"Changed files  : {len(files)}")
    print(
        f"Status        : {'✅ COMPLIANT — no violations' if compliant else '❌ VIOLATION(S) DETECTED'}"
    )

    if violations:
        for v in violations:
            print(v)
        print(f"\nTotal violations: {len(violations)}")
        print("🔴 Fix these files before merging.")
    else:
        print("All changed files are within the allowed namespace(s).")

    print(f"{'=' * 60}\n")
    sys.exit(0 if compliant else 1)


if __name__ == "__main__":
    main()
