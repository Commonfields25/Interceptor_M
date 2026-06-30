---
agent: Agent Manager
action: Create
timestamp: 2026-06-27T16:30:00Z
related_gate: N/A
status: Validated
---

# Namespace Isolation — Specification & Enforcement

**Version:** 1.0 | **Date:** 2026-06-27
**Owner:** Agent Manager
**References:** governance/BOT_GUIDELINES.md §2.1 (DEC-009)
**Red Flag:** RF2 — Git Merge Hell risk with multiple agents

---

## 1. PURPOSE

Each AI agent operates within a defined directory scope to prevent concurrent edits to the same file, which causes git merge conflicts and blocks parallel work. This document formalises the namespace convention from BOT_GUIDELINES.md §2.1 and adds an automated CI check.

---

## 2. NAMESPACES PER AGENT

| Agent | Primary Namespace(s) | Shared Files (Read-Only) |
|---|---|---|
| Agent Manager | `agents/agent_manager/` | All |
| D1 | `agents/D1/`, `models/DC/` | `governance/`, `PARAMETERS.json` |
| D2 | `agents/D2/`, `models/DI/` | `governance/`, `PARAMETERS.json` |
| D3 | `agents/D3/`, `models/DD/` | `governance/`, `PARAMETERS.json` |
| E1 | `agents/E1/`, `engineering/NDC/`, `engineering/FEA/`, `engineering/simulation/` | `governance/`, `PARAMETERS.json` |
| E2 | `agents/E2/`, `engineering/ML/`, `engineering/CFD/` | `governance/`, `PARAMETERS.json` |
| E3 | `agents/E3/`, `engineering/simulation/` | `governance/`, `PARAMETERS.json` |
| AC | `agents/AC/`, `governance/` (proposals only) | All except DG-confidential |
| Commercial | `agents/commercial/` | `governance/` (read) |
| Marketing | `agents/marketing/` | `governance/` (read) |

---

## 3. SHARED FILES — SPECIAL RULES

### 3.1 PARAMETERS.json (project root)
- **READ:** All agents
- **WRITE:** Proposals only — agent → AC → AM → DG validation chain. No direct write.

### 3.2 agents/agent_manager/DECISION_LOG.md
- **MODE:** APPEND-ONLY. New entries appended at the bottom. Never edit or delete existing entries.

### 3.3 governance/BOT_GUIDELINES.md, governance/AGENT_MANAGER_RULES.md
- Proposals via AC agent only; DG validates.

---

## 4. BRANCH NAMING CONVENTION

Format: `feat/<AgentID>/<short-description>`
Example: `feat/E2/6dof-dynamics`, `feat/D1/mass-budget`

Agents must name branches with their own ID to enable ownership attribution.

---

## 5. CI ENFORCEMENT

The CI check `governance/ci_checks/namespace_isolation.py` validates every PR:

1. **Extract changed files** from the PR diff (via GitHub Actions `github.event.pull_request.changed_files`)
2. **Determine the author agent** from the branch name (`feat/<AgentID>/...`)
3. **Verify** every changed file falls within the author's allowed namespace(s)
4. **Flag violations** if any file is outside the allowed scope
5. **Fail the PR** (with a clear comment) if violations are found

The CI workflow is at `.github/workflows/governance.yml`.

---

## 6. EXCEPTION PROCESS

Temporary namespace overlaps require:
1. A written proposal to the Agent Manager
2. AM approval recorded in `DECISION_LOG.md`
3. A `.lock` file created in the shared directory with Agent ID + expected duration

---

## 7. VIOLATION RESPONSE

| Violation | Response |
|---|---|
| 1st occurrence | AM comment on PR requesting correction |
| Recurring violations | AM blocks PR; agent must reconvene |
| Intentional bypass | Flagged as 🔴 BLOCKER in DECISION_LOG.md |

---

## APPENDIX A — VALIDATION SCRIPT REFERENCE

```bash
# Local test
python3 governance/ci_checks/namespace_isolation.py \
  --changed-files "agents/D1/file1.md models/DC/file2.md" \
  --author-agent D1
# Returns: 0 if compliant, 1 if violation
```
