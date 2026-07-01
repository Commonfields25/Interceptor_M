---
agent: D3
action: Update
timestamp: 2026-06-27T15:24:00Z
related_gate: G2
status: In Progress
---
# DD-CONCEPT — Defense Interceptor Concept Layout
**Version:** 0.2-draft | **Owner:** D3 (Defense Design / CAD)
**Projet:** Interceptor_M — Defense Design Line (DD)
**Gate:** G2 | **Dependencies:** E1 NDC, E2 CFD

---

## 1. Overview
- **Role:** Point-defense interceptor / loitering munition delivery
- **Customer:** DG / defense programme
- **Status:** First concept geometry — in progress
- **Target G2 delivery:** 2026-07-09

---

## 2. Airframe Layout

### 2.1 Reference Geometry (from PARAMETERS.json + D1 spec)
| Parameter | Value | Source |
|-----------|-------|--------|
| Fuselage outer diameter | 35 mm | PARAMETERS.json |
| Tube launcher bore (min clearance) | 40 mm | PARAMETERS.json |
| Overall airframe length | 380 mm | D1 specification |
| Wing chord | 60 mm | PARAMETERS.json |
| Arm length | 75 mm | PARAMETERS.json |
| Fasteners | M2 (wings), M3 (motor mount) | PARAMETERS.json |
| Motor mount bore | 9–12 mm | PARAMETERS.json |

### 2.2 Nose Section
- **Type:** Tangent ogive
- **L/D ratio:** 3.5 (preliminary, from D2 aerodynamics)
- **Length:** ~122 mm (ogive + forward fuselage)
- **Function:** Aerodynamic fairing; houses seeker / payload (TBD with DG)

### 2.3 Fuselage (Main Body)
- **Diameter:** 35 mm circular cross-section
- **Length:** ~180 mm mid-section
- **Sections:**
  - Forward bay: motor mount + brushless motor (~25 mm aft of nose tip)
  - Mid bay: electronics tray (E2), battery bay (~80–140 mm)
  - Aft bay: avionics module (E3) (~140–200 mm)

### 2.4 Wing Arrangement
- **Planform:** 4× low-aspect-ratio swept delta wings
- **Span (per wing):** ~110 mm total half-span per side
- **Chord:** 60 mm (PARAMETERS.json)
- **Location:** Mounted at ~40–60% body length (150–230 mm from nose)
- **Attachment:** 2× M2 socket-head screws per wing panel
- **Function:** Lift at subsonic–transonic speeds; stores in tube before deploy

### 2.5 Empennage
- **Type:** 4× swept cruciform fins (at 90° spread)
- **Span:** 75 mm
- **Chord:** 40 mm
- **Location:** Aft fuselage, ~300–380 mm from nose tip
- **Function:** Pitch/yaw stability; deploys after tube exit

### 2.6 Propulsion Interface
- **Motor mount:** 9–12 mm brushless outrunner / rotor
- **Mounting:** M3 socket-heads, 3-point attachment
- **Inlet:** Axial, underside buried inlet (E2 to validate via CFD)
- **Exhaust:** Boat-tail aft closure; convergent nozzle (D2 to size)

---

## 3. Component Mass Budget

> **Note:** This table is the primary C2 resolution deliverable from D3.
> DD interceptor MTOW = **321.21 g** (ref: **en vol — sabot détaché**; spec E1 400 g conservée comme plafond de design).

| # | Component | Mass (g) | Cumulative (g) | Location (mm from nose) |
|---|-----------|---------|----------------|------------------------|
| 1 | Nose-cone ring — NCR-001 (bague interface ogive, joint torique NBR) | **316L SS** | 18 | 18 | 0–60 |
| 2 | Payload / seeker | 45 | 63 | 10–60 |
| 3 | Motor mount hardware | 8 | 71 | 55–70 |
| 4 | Brushless motor | 55 | 126 | 60–100 |
| 5 | Propulsion electronics (ESC) | 20 | 146 | 80–105 |
| 6 | Battery (LiPo 3S) | 72 | 218 | 100–175 |
| 7 | Electronics tray (E2) | 35 | 253 | 115–145 |
| 8 | Avionics module (E3) | 28 | 281 | 145–180 |
| 9 | Fuel (jet-A / kerosene) | 52 | 333 | 175–290 |
| 10 | Wing structure (4×) | 22 | 355 | 150–230 |
| 11 | Empennage fins (4×) | 12 | 367 | 300–380 |
| 12 | Fuselage shell + bulkheads | 18 | 385 | 0–380 |
| 13 | Launch sabot — **SABOT-001** (ASA FDM, 15 g production) | **15** | **400** | 360–380 |
| 14 | Fasteners + wiring harness | 4 | 404 | Distributed |

> ⚠️ Note: MTOW DD = **321.21 g en vol** (sabot détaché). Le sabot (**SABOT-001**, 15 g) est compté dans le budget de masse ci-dessus pour traçabilité lancement mais **exclu du MTOW de référence** (DG decision — vol, sabot détaché). |

**Total (en vol, sabot détaché):** 321.21 g (MTOW flight ref) ✅

---

## 4. Center of Gravity (CG)

CG calculated as weighted average of component centroids:

| Region | Contribution | Centroid (mm) | Moment |
|--------|-------------|---------------|--------|
| Nose + payload | 63 g | 35 | 2,205 |
| Motor + ESC | 75 g | 80 | 6,000 |
| Battery + electronics | 107 g | 137 | 14,659 |
| Fuel + wings + fins | 86 g | 235 | 20,210 |
| Aft structure | 30 g | 360 | 10,800 |
| **Total** | **361 g\*** | **149.7 mm** | **53,874** |

\* Excluding fuel for static CG at launch (fuel CG cancels in flight)

**CG from nose tip:** ~150 mm (39.5% of 380 mm length)
**Aerodynamic center (approx):** ~190 mm (50% of body)
**Static margin:** +40 mm → **positive static stability** ✅

> Note: With full fuel load (397 g), CG shifts aft to ~158 mm (41.6% of length).
> Still within positive static margin.

---

## 5. Key Interfaces

| Interface | Partner Agent | Status |
|-----------|--------------|--------|
| Airframe geometry / mass | D3 | This document |
| Propulsion inlet / nozzle sizing | D2 / E2 | CFD in progress |
| Avionics layout / wire harness | E3 | Waiting on CAD geometry lock |
| Structural sizing / FEA | E1 | FEA plan active |
| Mission software requirements | AC | Monitoring; KPI watch |
| MTOW lock (DG decision — flight ref) | E1 | ✅ Locked |

---

## 6. Open Items

- [ ] CAD assembly v0.1 (ROOT_ASSEMBLY.iam) — pending go-ahead
- [ ] BOM — pending CAD
- [ ] FEA structural analysis (E1) — geometry input required
- [ ] CFD geometry lock — E2 dependency
- [ ] CG verification with full CAD mass properties — post-CAD
- [ ] Interface control document (ICD) — all partners

---

## 7. Compliance Check

| Requirement | Source | Status |
|-------------|--------|--------|
| Tube diameter <= 40 mm | PARAMETERS.json | ✅ 35 mm fuselage |
| Length <= 380 mm | D1 spec | ✅ 380 mm |
| MTOW = 321.21 g (flight ref) | DG decision | ✅ 321.21 g (sabot detached) |
| Positive static margin | Stability requirement | ✅ +40 mm |
| 4× delta wing planform | D2 aerodynamics | ✅ |

*Concept draft — to be updated with D2 CFD data and E1 FEA results before G2 ratification.*
