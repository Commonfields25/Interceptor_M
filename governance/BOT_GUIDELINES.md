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
  - **E2:** `agents/E2/`, `engineering/ML/`, `engineering/CFD/`
  - **E3:** `agents/E3/`, `engineering/simulation/`
  - **AC:** `agents/AC/`, `governance/` (proposals only, DG validates)
  - **Commercial:** `agents/commercial/`
  - **Marketing:** `agents/marketing/`

### 2.1 Namespace Isolation — Operational Rules

To prevent Git merge hell when multiple agents edit documentation concurrently:

1. **Single-owner files:** Every file has exactly one owning agent. Only that agent may modify the file in a given work cycle. Exceptions require AM approval.
2. **No co-editing:** Two agents must never edit the same file in the same commit cycle. If overlap is needed, use a PR with explicit review.
3. **Shared files — integration owner only:**
   - `PARAMETERS.json`: WRITE via validated proposal (agent -> AM -> DG) only. No direct write by sub-agents.
   - `agents/agent_manager/DECISION_LOG.md`: APPEND-ONLY. Never delete or edit existing entries. New entries go at the bottom.
   - `governance/BOT_GUIDELINES.md`, `governance/AGENT_MANAGER_RULES.md`: Proposals via AC agent only; DG validates.
4. **Branch naming convention per agent:**
   - `feat/<agentID>/<short-description>` — feature work
   - `fix/<agentID>/<short-description>` — bug fixes
   - `docs/<agentID>/<short-description>` — documentation only
   - Example: `feat/E2/swarm-rl-kickoff`, `fix/D3-mass-budget`
5. **Locking for shared files:** Before starting a long task on a shared file, create a `.lock` file in the file's directory with content: `Agent: <ID> | Expected duration: <X>h | Start: <ISO timestamp>`. Remove the lock file when done.
6. **Merge conflict resolution:** If a merge conflict occurs, the owning agent resolves it. The AM is notified. Do not force-merge over unresolved conflicts.
7. **PR review requirement:** All PRs to `main` require at least one review from an agent other than the author before merge.

- **Shared Files:** Use "APPEND-ONLY" mode for logs (e.g., `agents/agent_manager/DECISION_LOG.md`). Do not rewrite history.
- **Locking:** Before starting a long task on a shared file, create a `.lock` file (e.g., `ROOT_ASSEMBLY.iam.lock`) with your Agent ID and expected duration.
- **PARAMETERS.json:** Located at project root. READ by all agents. WRITE only via a validated proposal (agent -> AM -> DG).

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

## 6. PLAN PRODUCTION PROTOCOL (Artifact Bundles)

When an agent is tasked with producing a "Plan" (Mechanical, Electronic, or Simulation), they must deliver a **Plan Artifact Bundle** consisting of three mandatory components:

### 6.1 Technical Specification (`.md`)
A human-readable document following the IAMD header protocol, containing:
- Design rationale and assumptions.
- Performance characteristics.
- Materials and manufacturing notes.

### 6.2 Geometry/Execution Script (`.py`)
A standalone, executable Python script that generates the artifact.
- For Mechanical: Uses `model_parts.py` or similar to output a 3D description or `.stl`.
- For Simulation: A scenario script compatible with the physics engine.

### 6.3 Configuration Metadata (`.json`)
A machine-readable file containing the specific parameters used for this instance, cross-referenced with `PARAMETERS.json`.

**Protocol:**
1. **DRAFT**: Agent produces the bundle in their workspace.
2. **REVIEW**: Agent Manager/Peer reviews the bundle.
3. **VALIDATE**: DG/AM approves the bundle, moving it to the `deliverables/` or `models/` directory.
