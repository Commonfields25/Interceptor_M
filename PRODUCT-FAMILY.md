# Interceptor_M — Product Family Overview

**Strategy:** Common-platform modular product family
**Version:** 1.3 — All Line Specs Locked
**Date:** 2026-06-29

---

## 1. Product Lines

| Line | Market | Priority | MTOW (g) | Fuselage (mm) | Wing Span (m) | Status |
|------|--------|----------|----------|---------------|---------------|--------|
| **DD** | Defense | High | 400 | 380x200x100 | 0.150 | **LOCKED** |
| **DI** | Industrial | High | 300 | 365x180x90 | 0.135 | **LOCKED** |
| **DC** | Civil | Medium | 250 | 350x160x80 | 0.120 | **LOCKED** |

---

## 2. Shared Platform Modules (SC Registry)

All lines utilize the **SC-Series** shared components to minimize NRE and maximize supply chain efficiency.

- **SC-01**: Autopilot / FC Board
- **SC-02**: Propulsion Brick (Motor + ESC)
- **SC-03**: Datalink / RF Modem
- **SC-04**: Mission Software Stack
- **SC-05**: Ground Control Station
- **SC-06**: Launcher Interface (DD/DI only)

---

## 3. Governance Rule: SPEC LOCK
As of version 1.3, the MTOW and Fuselage dimensions for all three lines (DD, DI, DC) are **locked**. Any changes require a formal ECR (Engineering Change Request) and DG approval.

---

## 4. Engineering Performance Baseline (MATLAB Verified)

Analytical performance metrics for the **DD-400** platform at Sea Level.

| Parameter | Value | Condition |
|-----------|-------|-----------|
| **Intercept Speed** | 300 m/s (Mach 0.88) | Full Thrust |
| **Max Load Factor** | 5.9 g | Aero-limited @ 12° AoA |
| **Min Turn Radius** | 1,559 m | @ 300 m/s |
| **Steady Drag** | 19.3 N | @ 300 m/s |
| **Thrust-to-Weight** | 3.06 | @ Max Thrust (12N) |

Verified via [`matlab/interceptor_performance.m`](./matlab/interceptor_performance.m)

## 5. Milestone Alignment

| MS | Title | DI BOM relevance |
|----|-------|-----------------|
| M5 | Branch Cleanup & Archive | - |
| M6 | CI Migration Node24 & Workflow Activation | Infrastructure only |
| **M7** | **DI Product Specifications Lock & BOM** | **Primary owner - BOM locked** |
| M8 | RL Environment Hardening & Agent Rebalancing | - |
| M9 | Recrutement Ingenieur Conception & Design Industriel | Personnel |

---

*Authorized by Jules (Physics Expert) for the Engineering Group.*
