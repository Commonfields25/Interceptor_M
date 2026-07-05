---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# Mechanical Dev Approval Chain

## Role Assignments

| Agent | Role | Mechanical Dev Responsibility |
|-------|------|-------------------------------|
| D1 | Lead Design/Dev | CAO conception, overall architecture, integration |
| D2 | Dev Structure | Structural bonds, mechanical endurance, load paths |
| D3 | Dev Sub-systems | Actuators, electro-mechanical sub-assemblies |
| E1 | Lead Reviewer | Primary gate entry, process enforcement |
| E2 | Structural/Materials Evaluator | Calculations, material validation |
| E3 | Systems Integration Reviewer | Cross-system interfaces, coherence |

## Expert Mapping

| Domain | Primary | Secondary |
|--------|---------|-----------|
| Structural / Materials | E2 | D2 |
| Aero / Propulsion | E3 | D3 |
| Systems Integration | E3 | D1 |

## Ordered 8-Step Approval Chain

1. **D1/D2/D3** — Mechanical work completion and self-review
2. **E1** — Entry gate review; returns to D1 if blocking issues
3. **D1** — Addresses E1 blocking findings
4. **E1 + E2 + E3** — Cross-review session (structure, materials, interfaces)
5. **E1** — Consolidates cross-review output; gates forward
6. **E1 + E2 + E3** — Final validation pass (all three sign off)
7. **E1** — Final sign-off aggregation and confirmation
8. **DG / Agent Manager** — Executive signature and project release

## Auto-Approval Rule

When KPI score > 90%, the Agent Manager co-signs minor gate items under the following conditions:
- All mandatory safety checks passed
- No open blocking comments in the review thread
- Rules reference: rules.md v1.2 §1.1

This co-signature reduces redundant Agent Manager review while maintaining accountability.

## Namespace Isolation

All mechanical dev artifacts live under the top-level namespace `docs/governance/`.
Sub-namespaces per domain (e.g. `docs/governance/structural/`, `docs/governance/aero/`)
are isolated to prevent merge conflicts between concurrent development streams.
Branches must rebase against `main` before PR to avoid cross-stream coupling.
