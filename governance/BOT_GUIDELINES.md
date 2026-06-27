---
title: Bot Interaction Guidelines (IAMD)
version: 1.1
target_audience: AI Agents (LLMs, Autonomous Agents)
last_updated: 2026-06-24
original_location: /BOT_GUIDELINES.md
---

# 🤖 BOT INTERACTION GUIDELINES

This document provides structured instructions for AI agents working on the Interceptor_M project. Adhere to these formats to ensure seamless parallel execution and minimize human intervention.

## 1. META-COMMUNICATION PROTOCOL

Every modification to the codebase or documentation MUST be accompanied by a structured log entry.

### 1.1 Documentation Header
All Markdown files should start with a YAML block:
```yaml
---
agent: [AgentID, e.g., D1]
action: [Update/Create/Refactor]
timestamp: 2026-06-22THH:MM:SSZ
related_gate: [G1-G11 or N/A]
status: [Draft/Review/Validated]
---
```

## 2. PARALLEL WORKFLOW RULES

To avoid concurrency issues (stepping on toes):

- **Namespace Isolation:** Each agent operates within their assigned directory scope:
  - **Agent Manager:** `agents/agent_manager/`, `deliverables/`
  - **D1:** `agents/D1/`, `models/DC/`
  - **D2:** `agents/D2/`, `models/DI/`
  - **D3:** `agents/D3/`, `models/DD/`
  - **E1:** `agents/E1/`, `engineering/NDC/`, `engineering/FEA/`, `engineering/simulation/`
  - **E2:** `agents/E2/`, `engineering/CFD/`
  - **E3:** `agents/E3/`, `engineering/simulation/`
  - **AC:** `agents/AC/`, `governance/` (proposals only, DG validates)
  - **Commercial:** `agents/commercial/`
  - **Marketing:** `agents/marketing/`
- **Shared Files:** Use "APPEND-ONLY" mode for logs (e.g., `agents/agent_manager/DECISION_LOG.md`). Do not rewrite history.
- **Locking:** Before starting a long task on a shared file, create a `.lock` file (e.g., `ROOT_ASSEMBLY.iam.lock`) with your Agent ID and expected duration.
- **PARAMETERS.json:** Located at project root. READ by all agents. WRITE only via a validated proposal (agent → AM → DG).

## 3. IAMD FORMATTING (Information Augmented Markdown)

### 3.1 Data Blocks
When providing parameters or specs, use fenced code blocks with specific labels for parsing:

```json:parameters
{
  "propulsion": {
    "thrust_required_n": 15.5,
    "battery_v": 22.2
  }
}
```

### 3.2 Task Lists for Bots
Use the following syntax for task tracking:
- [ ] `TASK_ID_001`: Pending task description.
- [/] `TASK_ID_002`: Task in progress by @AgentID.
- [x] `TASK_ID_003`: Completed task (linked to commit/PR).

## 4. ERROR & EXCEPTION HANDLING

If an agent encounters a conflict or a logic error:
1. **Flag:** Immediately add a 🔴 BLOCKER entry to the `agents/agent_manager/DECISION_LOG.md`.
2. **Rollback:** If you corrupted a shared file, restore it immediately.
3. **Escalate:** Notify the `Agent Manager` with a specific error dump.

## 5. FOLDER STRUCTURE QUICK REFERENCE

```
Interceptor_M/
├── governance/          # Rules, guidelines, SOPs (read by all, edit by AC+DG)
├── agents/              # Per-agent instructions & workspaces
│   ├── agent_manager/   # Daily digests, gate packages, decision log
│   ├── D1/ ... D3/      # Designer workspaces
│   ├── E1/ ... E3/      # Engineer workspaces
│   ├── AC/              # Improvement proposals, KPI reports
│   ├── commercial/      # Sales workspace
│   └── marketing/       # Marketing workspace
├── models/              # CAD files by product line (DC, DI, DD)
├── engineering/         # NDC, FEA, CFD, simulation deliverables
├── deliverables/        # Final validated outputs per gate (G0–G11)
├── references/          # Archived concepts, analyses, PDFs
├── templates/           # Reusable report/digest/package templates
├── PARAMETERS.json      # Shared global parameters
└── README.md            # Project overview & navigation index
```

---
> **Note to Agents:** This file is a living document. Propose updates via the `AC Agent` (Amélioration Continue). All proposals go through `governance/` update process.
