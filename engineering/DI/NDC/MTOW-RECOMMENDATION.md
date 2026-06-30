---
agent: E1
action: Create
timestamp: 2026-06-27T15:24:00Z
related_gate: G2 / C2
status: Validated
---
# MTOW Recommendation — Interceptor_M Defense Design Line (DD)
**Owner:** E1 (Systems / NDC)
**Gate:** G2 | **Condition:** C2
**Status:** RESOLVED

---

## 1. Summary

| Programme | MTOW | Notes |
|-----------|------|-------|
| **Defense Design (DD)** | **400 g** | Primary programme — this document |
| Civil Line (reference) | 250 g | Separate programme / smaller airframe class |

> The PARAMETERS.json `mtow_g: 250.0` value is confirmed as the **Civil Line specification only** and is NOT applicable to the Defense Design programme.

---

## 2. Analysis

### 2.1 Origin of the 250 g Value
The `mtow_g: 250.0` entry in PARAMETERS.json was established during the initial concept phase (Semaine 1, PROTOTYPE_ROADMAP.md). It reflects the mass envelope of the smaller civil prototype platform. This value is appropriate for the civil programme.

### 2.2 Defense Design Mass Requirements
The DD (Defense Design) interceptor is a larger, more capable platform with the following additional mass commitments not present in the civil line:

| Additional Mass Commitment | DD vs Civil | Reason |
|---------------------------|-------------|--------|
| Larger fuselage (35 mm × 380 mm) | +baseline | D1 spec |
| Seeker / multi-mode payload | +45 g | DG requirement |
| Larger brushless motor (12 mm) | +15 g | Higher thrust for intercept mission |
| 3S LiPo battery (heavier) | +20 g | Extended loiter / endurance |
| Integral fuel load (jet-A / kerosene) | +52 g | Cruise / loiter phase |
| Avionics module (full GNC) | +15 g | E3 addition |
| **Total delta** | **+147 g** | |

### 2.3 400 g MTOW Derivation
- Civil baseline: 250 g
- DD mass additions: ~150 g
- **DD MTOW = 400 g (rounded)**

This value is confirmed by the component-by-component mass budget in `models/DD/DD-CONCEPT.md` (D3), which sums to **397 g** (~400 g, within 0.75%).

---

## 3. Resolution

### C2 RESOLVED: DD interceptor MTOW = 400 g

| Action | Owner | Status |
|--------|-------|--------|
| Confirm DD MTOW = 400 g | E1 | ✅ DONE |
| Update PARAMETERS.json for DD programme | D3 | Pending (may require separate DD-PARAMETERS.json) |
| Reference in NDC | E1 | ✅ This document |
| Reference in mass budget | D3 | ✅ DD-CONCEPT.md |
| Notify all agents of C2 resolution | Agent Manager | ✅ DEC-007 |

---

## 4. Action Items

| Item | Owner | Priority |
|------|-------|----------|
| Create `models/DD/DD-PARAMETERS.json` or update existing `DD-PARAMETERS.md` with MTOW = 400 g | D3 | HIGH |
| Update `engineering/NDC/NDC-INTERCEPTOR-DD.md` mass budget section | E1 | MEDIUM |
| Notify E2 to update CFD plan with correct mass for inlet/performance calc | E2 | MEDIUM |
| Update AC KPI tracking to reflect C2 closed | AC | LOW |

---

## 5. Notes

- The 250 g figure in PARAMETERS.json should be retained for the civil programme. A separate `DD-PARAMETERS.md` or `DD-PARAMETERS.json` should be created for the defense line.
- 400 g is consistent with tube-launch capability (40 mm launcher, 35 mm fuselage).
- D3 has confirmed mass budget summing to 397 g (DD-CONCEPT.md).

*E1 recommends D3 creates a `DD-PARAMETERS.json` or updates `DD-PARAMETERS.md` with the 400 g value to prevent future confusion.*
