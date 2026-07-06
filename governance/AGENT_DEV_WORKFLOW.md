---
action: Create
agent: AC
related_gate: G2
status: Validated
timestamp: 2026-06-29 23:03:24+00:00
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
