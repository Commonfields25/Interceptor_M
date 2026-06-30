---
agent: AC
action: Create
timestamp: 2026-06-29T23:03:24Z
status: Validated
---

# 🔄 AGENT DEVELOPMENT WORKFLOW

This guide details the iterative process for agents to develop technical plans and artifacts within the Interceptor_M project.

## Phase 1: Parameter Fetch & Alignment
Agents must never hardcode values.
1. Read **PARAMETERS.json** for the relevant product line (DD, DI, DC).
2. Cross-reference with **PRODUCT-FAMILY.md** for shared module constraints.
3. If parameters are missing, submit a proposal to the Agent Manager.

## Phase 2: Draft & Geometry Scripting
1. Use `scripts/generate_part.py` to create a baseline geometry script.
2. Iterate on the logic to meet functional requirements (e.g., strength, aerodynamics).
3. Ensure the script is standalone and reproducible.

## Phase 3: Verification Loop (The "Self-Correction" Step)
Before finalizing, agents must:
1. Run `scripts/check_constraints.py` to verify MTOW, center of gravity (CG), and dimensional limits.
2. Perform a "Peer Preview": Send the draft to a related agent (e.g., D1 sends to E1) for sanity check.
3. Document any deviations in a `VERIFICATION.md` file.

## Phase 4: Documentation & Bundle Assembly
Assemble the **Plan Artifact Bundle** as defined in `BOT_GUIDELINES.md`:
- [ ] Technical Spec (`.md`)
- [ ] Geometry Script (`.py`)
- [ ] Config Metadata (`.json`)
- [ ] **Verification Log** (`VERIFICATION.md`)

## Phase 5: Gate Submission (G4-G11)
Submit the bundle to the Agent Manager for Gate review.

---
*Authorized by Continuous Improvement Agent (AC)*

## 6. AUTONOMY LEVELS & HUMAN-IN-THE-LOOP (HITL)

The Interceptor_M production system operates on a **Semi-Autonomous** model to balance execution speed with safety and quality.

### 6.1 Level 1: Technical Autonomy (Agents)
- Agents have full autonomy to draft, iterate, and verify designs within their assigned namespaces.
- They must use automated tools (\`check_constraints.py\`, \`generate_part.py\`) to self-validate.

### 6.2 Level 2: Conditional Autonomy (Agent Manager)
- The Agent Manager can autonomously approve **MINOR GATES** (G1, G5, G8) only when KPI thresholds are met (On-time >= 85%, Peer reviews >= 80%).
- If KPIs drop, this autonomy is revoked and reverts to HITL.

### 6.3 Level 3: Human Oversight (DG - Mandatory)
- **MAJOR GATES** (G0, G2, G4, G7, G9, G10, G11) require explicit validation from the Director General.
- No design is considered "Final" or "Production-Ready" without a G9 Human sign-off.
- The DG holds the "Emergency Stop" authority (G11) over all agent activities.

---
*Status: Semi-Autonomous (HITL Guardrails Active)*
