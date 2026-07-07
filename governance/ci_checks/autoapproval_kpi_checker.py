#!/usr/bin/env python3
"""
Auto-Approval KPI Checker
Reads a KPI JSON snapshot and outputs an approve/deny decision for the
Agent Manager's auto-approval authority, with an audit log entry.

Usage:
    python3 governance/ci_checks/autoapproval_kpi_checker.py --kpi-json kpi_snapshot.json

    # Or inline JSON:
    python3 governance/ci_checks/autoapproval_kpi_checker.py \
      --kpi-json '{"on_time_rate": 92, "peer_review_rate": 85, "blocker_resolution_h": 20, "agent_utilization": 78}'

Exit codes:
    0 = auto-approval GRANTED (all KPIs >= threshold)
    1 = auto-approval DENIED (one or more KPIs below threshold)
    2 = invalid input / JSON error
"""

import sys
import os
import json
import argparse
import datetime
from typing import Any


# ─── Thresholds (from governance/AUTO-APPROVAL-POLICY.md §3) ─────────────────

THRESHOLDS: dict[str, float] = {
    "on_time_rate": 90.0,  # >= 90%
    "peer_review_rate": 80.0,  # >= 80%
    "blocker_resolution_h": 24.0,  # <= 24h (lower is better)
    "agent_utilization": 70.0,  # >= 70%
}

# Alert thresholds — if ANY KPI is below this, auto-approval is SUSPENDED entirely
ALERT_THRESHOLDS: dict[str, float] = {
    "on_time_rate": 75.0,
    "peer_review_rate": 60.0,
    "blocker_resolution_h": 96.0,  # >96h = alert (worse than auto-approval threshold)
    "agent_utilization": 50.0,
}

REPORTED_KPI_NAMES = {
    "on_time_rate": "On-time Delivery Rate",
    "peer_review_rate": "Peer Review Coverage",
    "blocker_resolution_h": "Blocker Resolution Time",
    "agent_utilization": "Agent Utilization",
}


def load_kpis(source: str) -> dict[str, float]:
    """Parse KPI JSON from a file path or inline string."""
    try:
        # Try as file path first
        if os.path.isfile(source):
            with open(source) as f:
                data = json.load(f)
        else:
            # Treat as inline JSON string
            data = json.loads(source)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Could not parse KPI JSON: {e}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(data, dict):
        print("ERROR: KPI JSON must be a dictionary", file=sys.stderr)
        sys.exit(2)
    return data


def evaluate_kpis(kpis: dict[str, float]) -> dict[str, Any]:
    """
    Evaluate KPIs against thresholds.
    Returns a dict with decision, details, and audit entry.
    """
    results = {}
    alert = False
    denied_fields = []

    for field, threshold in THRESHOLDS.items():
        value = kpis.get(field)
        if value is None:
            results[field] = {
                "value": None,
                "threshold": threshold,
                "status": "MISSING",
                "approved": False,
            }
            denied_fields.append(field)
            continue

        alert_threshold = ALERT_THRESHOLDS.get(field, threshold)

        # Lower-is-better fields (blocker_resolution_h)
        if field == "blocker_resolution_h":
            approved = value <= threshold
            is_alert = value > alert_threshold
        else:
            approved = value >= threshold
            is_alert = value < alert_threshold

        if is_alert:
            alert = True
        if not approved:
            denied_fields.append(field)

        results[field] = {
            "value": value,
            "threshold": threshold,
            "alert_threshold": alert_threshold,
            "status": "ALERT" if is_alert else ("PASS" if approved else "FAIL"),
            "approved": approved,
        }

    if alert:
        decision = "DENIED_SUSPENDED"
        reason = "One or more KPIs are in ALERT zone — auto-approval SUSPENDED pending DG review."
    elif denied_fields:
        decision = "DENIED"
        reason = f"KPI(s) below auto-approval threshold: {', '.join(denied_fields)}."
    else:
        decision = "GRANTED"
        reason = "All KPIs meet auto-approval thresholds."

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    audit_entry = {
        "timestamp": timestamp,
        "decision": decision,
        "kpi_snapshot": {field: r["value"] for field, r in results.items()},
        "thresholds_applied": THRESHOLDS,
        "reason": reason,
        "alert_zone": alert,
    }

    return {
        "decision": decision,
        "reason": reason,
        "kpi_results": results,
        "alert_zone": alert,
        "audit_entry": audit_entry,
    }


def print_report(evaluation: dict[str, Any]):
    """Print a formatted human-readable report."""
    d = evaluation
    print(f"\n{'=' * 65}")
    print(
        f"  AUTO-APPROVAL KPI CHECK — {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    )
    print(f"{'=' * 65}")

    status_icon = {
        "GRANTED": "✅",
        "DENIED": "❌",
        "DENIED_SUSPENDED": "🚫",
    }.get(d["decision"], "❓")

    print(f"\n  Decision : {status_icon} {d['decision']}")
    print(f"  Reason   : {d['reason']}")
    print(f"\n  KPI Results:")
    print(f"  {'KPI':<28} {'Value':>7}  {'Threshold':>10}  {'Alert':>6}  Status")
    print(f"  {'-' * 28} {'-' * 7}  {'-' * 10}  {'-' * 6}  ------")

    for field, r in d["kpi_results"].items():
        val = f"{r['value']:.1f}%" if r["value"] is not None else "N/A"
        thr = (
            f"{THRESHOLDS.get(field, 0):.0f}%"
            if field != "blocker_resolution_h"
            else f"≤{THRESHOLDS.get(field, 0):.0f}h"
        )
        alert_str = (
            f"{r.get('alert_threshold', '?'):.0f}"
            if r.get("alert_threshold") is not None
            else "?"
        )
        status = r["status"]
        icon = {"PASS": "✅", "FAIL": "❌", "ALERT": "🚨", "MISSING": "⚠️"}.get(
            status, "❓"
        )
        print(
            f"  {REPORTED_KPI_NAMES.get(field, field):<28} {val:>7}  {thr:>10}  ≤{alert_str:>5}  {icon} {status}"
        )

    if d["alert_zone"]:
        print(f"\n  ⚠️  ALERT: One or more KPIs below alert threshold.")
        print(f"      Auto-approval SUSPENDED — escalate to DG.")
    elif d["decision"] == "DENIED":
        print(f"\n  ❌ One or more KPIs below approval threshold.")
        print(f"     Auto-approval DENIED — DG review required.")
    else:
        print(f"\n  ✅ All KPIs above auto-approval threshold.")
        print(
            f"     Agent Manager MAY exercise auto-approval authority for MINOR gates."
        )

    print(f"\n  Audit entry written to DECISION_LOG.md:")
    ae = d["audit_entry"]
    print(f"     Timestamp : {ae['timestamp']}")
    print(f"     Decision  : {ae['decision']}")
    print(f"     KPIs      : {json.dumps(ae['kpi_snapshot'], indent=False)}")

    print(f"\n{'=' * 65}\n")


def write_audit_log(
    evaluation: dict[str, Any], output_path: str = "AUTOAPPROVAL_AUDIT_LOG.md"
):
    """Append audit entry to a local markdown audit log file."""
    ae = evaluation["audit_entry"]
    entry = f"""
## Auto-Approval Audit Entry — {ae["timestamp"]}

| Field | Value |
|---|---|
| **Decision** | `{ae["decision"]}` |
| **Reason** | {ae["reason"]} |
| **On-time Rate** | {ae["kpi_snapshot"].get("on_time_rate", "N/A")}% |
| **Peer Review Rate** | {ae["kpi_snapshot"].get("peer_review_rate", "N/A")}% |
| **Blocker Resolution** | {ae["kpi_snapshot"].get("blocker_resolution_h", "N/A")}h |
| **Agent Utilization** | {ae["kpi_snapshot"].get("agent_utilization", "N/A")}% |
| **Alert Zone** | {"YES — SUSPENDED" if ae["alert_zone"] else "NO"} |
"""
    try:
        with open(output_path, "a") as f:
            f.write(entry + "\n")
        print(f"Audit log written to: {output_path}")
    except Exception as e:
        print(f"WARNING: Could not write audit log: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Auto-Approval KPI Checker")
    parser.add_argument(
        "--kpi-json", required=True, help="Path to KPI JSON file, or inline JSON string"
    )
    parser.add_argument(
        "--output-log",
        default="AUTOAPPROVAL_AUDIT_LOG.md",
        help="Path to append audit log entry",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress stdout report")
    args = parser.parse_args()

    kpis = load_kpis(args.kpi_json)
    evaluation = evaluate_kpis(kpis)

    if not args.quiet:
        print_report(evaluation)

    write_audit_log(evaluation, args.output_log)

    sys.exit(0 if evaluation["decision"] == "GRANTED" else 1)


if __name__ == "__main__":
    main()
