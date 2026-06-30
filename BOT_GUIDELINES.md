---
title: Bot Interaction Guidelines (IAMD)
version: 1.0
target_audience: AI Agents (LLMs, Autonomous Agents)
last_updated: 2026-06-22
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

- **Namespace Isolation:** Only edit files within your assigned scope (e.g., E1 only edits `engineering/systems/`).
- **Shared Files:** Use "APPEND-ONLY" mode for logs (e.g., `DECISION_LOG.md`). Do not rewrite history.
- **Locking:** Before starting a long task on a shared file, create a `.lock` file (e.g., `CAD_ASSEMBLY.SLDPRT.lock`) with your Agent ID and expected duration.

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
1. **Flag:** Immediately add a 🔴 BLOCKER entry to the `Daily Digest`.
2. **Rollback:** If you corrupted a shared file, restore it immediately.
3. **Escalate:** Notify the `Agent Manager` with a specific error dump.

---
> **Note to Agents:** This file is a living document. Propose updates via the `AC Agent` (Amélioration Continue).
