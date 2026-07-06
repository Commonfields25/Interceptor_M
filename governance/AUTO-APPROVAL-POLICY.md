---
action: Create
agent: AC / Agent Manager
related_gate: G1 / G2
status: Validated
timestamp: 2026-06-27 16:10:00+00:00
---

# Threshold-Based Auto-Approval Policy

**Version:** 1.0 | **Date:** 2026-06-27
**Authors:** AC (Amelioration Continue) + Agent Manager
**Validated by:** DG (DEC-009)

---

## 1. PURPOSE

The Director General (DG) is the sole validation authority for all 11 project gates. If the DG becomes unavailable or overloaded, project progress stalls. This policy defines conditions under which the Agent Manager may autonomously approve minor gates, reducing single-point-of-failure risk without bypassing governance oversight.

---

## 2. SCOPE

Applies to all gate decisions (G0–G11) in the Interceptor_M project. Does not supersede DG decisions; it creates a conditional delegation mechanism.

---

## 3. KPI THRESHOLD DEFINITIONS

Auto-approval eligibility is evaluated per gate cycle using the following KPIs:

| KPI | Target | Alert Threshold | Auto-Approval Threshold |
|---|---|---|---|
| On-time delivery | >= 90% of tasks delivered by deadline | < 75% | > 90% |
| Peer review coverage | >= 80% of deliverables peer-reviewed | < 60% | > 80% |
| Blocker resolution time | <= 48 h per blocker | > 96 h | <= 24 h |
| Agent utilization | >= 70% active utilization | < 50% | > 70% |

**Evaluation frequency:** Every gate cycle (roughly weekly during active phases).

**Source:** OPERATIONS_WORKFLOW.md §KPIs; tracked in TEAM_UPDATE and Daily Digest.

---

## 4. GATE CLASSIFICATION — MAJOR vs. MINOR

### 4.1 MINOR Gates — Auto-Approval Eligible

The Agent Manager may sign off on these gates without DG involvement, provided KPI thresholds are met:

| Gate | Name | Reason it is Minor |
|---|---|---|
| G1 | Brief | Validation of plan vs. requirements — routine checkpoint |
| G5 | Simulation GO | Milestone for internal sim completion — technical review |
| G8 | Test Results | Validation of hardware test outcomes — data-driven |
| G3 | Preliminary Design Review | Internal review, no external commitment |
| G6 | Critical Design Review | Internal review, design is already baselined |

### 4.2 MAJOR Gates — DG Required Always

No auto-approval. DG must personally validate:

| Gate | Name | Reason it is Major |
|---|---|---|
| G0 | Programme Launch | Strategic commitment, budget authorization |
| G2 | Concept Selection | Technology choice with long-term impact |
| G4 | Programme Baseline | External commitment, customer milestone |
| G7 | Pre-Production Review | Manufacturing investment decision |
| G9 | First Article Test | Major hardware validation |
| G10 | Qualification Complete | Regulatory / certification milestone |
| G11 | Initial Operational Capability | Programme delivery milestone |

---

## 5. AUTO-APPROVAL MECHANISM

### 5.1 Trigger Conditions (ALL must be true)

1. All 4 KPIs above their Auto-Approval Threshold (see §3)
2. No open DECISION_LOG blockers flagged with 🔴 BLOCKER
3. Gate is classified MINOR (see §4.1)
4. Gate package has been produced and is complete
5. Agent Manager has received no DG objection within 24 h of notification

### 5.2 Procedure

```
1. Agent Manager prepares gate package (standard process)
2. Agent Manager checks KPI dashboard — verify all 4 thresholds met
3. Agent Manager checks for open blockers
4. If conditions met: Agent Manager signs gate as "AUTO-APPROVED"
   - Label: "AUTO-APPROVED (KPI > 90%, AM signature)"
   - Gate outcome: GO / CONDITIONAL GO / NO-GO
5. Agent Manager notifies DG within 2 h of approval (async)
6. Decision logged in DECISION_LOG.md with "AUTO-APPROVED" label
7. DG may override within 48 h — override logged as DEC-XXX override
```

### 5.3 Audit Trail

Every auto-approved gate must log:
- KPI snapshot at time of approval (actual values)
- AM signature and timestamp
- Any DG override (retroactive or proactive)
- Link to gate package in `agents/agent_manager/gate_packages/`

---

## 6. ESCALATION RULES

| Situation | Action |
|---|---|
| DG unavailable > 72 h during active gate cycle | AC escalates to human oversight |
| Any KPI falls below Alert Threshold | Auto-approval suspended; full DG review required |
| MAJOR gate due | No delegation — DG must engage or formally delegate |
| Auto-approval disputed by any agent | AM escalates to DG; gate decision paused until resolved |
| More than 2 consecutive auto-approvals | AC performs mandatory process review; DG briefed |

---

## 7. REVIEW SCHEDULE

- **Monthly:** AC reviews auto-approval usage stats and reports to DG
- **Per gate cycle:** KPI thresholds validated against actual performance data
- **Quarterly:** Policy reviewed and updated if needed

---

## 8. REFERENCES

- DECISION_LOG.md — gate history and audit trail
- OPERATIONS_WORKFLOW.md — KPI definitions and tracking
- AGENT_MANAGER_RULES.md — AM authority boundaries
- DEC-009 — this policy adoption decision
