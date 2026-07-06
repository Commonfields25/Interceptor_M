---
action: Update
agent: E1
related_gate: G2
status: In Progress
timestamp: 2026-06-27 15:24:00+00:00
---

# NDC — Interceptor_M Defense Design
# Cahier des Charges Fonctionnel (CdCF) — Systems Requirements
**Owner:** E1 | **Gate:** G2 | **Version:** 0.2-draft

---

## 1. Mission Profile
- **Primary role:** Point-defense interceptor / loitering munition delivery platform
- **Target environment:** Contested airspace, GPS-denied, multi-threat
- **Target customer:** DG / defense programme (ref: G1 RATIFIED)
- **Operational concept:** Rapid deploy from ground vehicle, autonomous or semi-autonomous flight to target area, terminal engagement
- **Launcher:** 40 mm tube bore, 380 mm total airframe length (see DD-CONCEPT.md)

---

## 2. Mass Budget (MTOW) — C2 RESOLVED ✅
- **DD MTOW = 400 g** (per MTOW-RECOMMENDATION.md, DEC-007)
- **Civil line MTOW = 250 g** (separate programme, PARAMETERS.json)
- Sub-system mass allocation per DD-CONCEPT.md mass budget (D3):
  - Structure / airframe: ~36 g
  - Propulsion (motor + ESC): ~75 g
  - Avionics (E3): ~28 g
  - Electronics tray (E2): ~35 g
  - Battery: ~72 g
  - Fuel: ~52 g
  - Payload / seeker: ~45 g
  - Wings + fins: ~34 g
  - Payload / seeker: ~45 g
  - Fasteners / harness: ~4 g
  - **Total: 397 g ≈ 400 g** ✅

---

## 3. Propulsion
- **Type:** Turbojet / small turbofan preferred (TBD per D2/CFD input)
- **Motor:** Brushless outrunner, 9–12 mm mount (D1 specification)
- **Thrust target:** TBD based on MTOW and endurance requirements
- **Fuel fraction:** ~30–40% of MTOW (detailed sizing pending, ~52 g jet-A)
- **Notes:** E2 to provide aero/propulsion CFD data; integration interface with D3 airframe
- **Inlet:** Underside buried inlet (E2 CFD to validate; see DD-CONCEPT.md §2.6)

---

## 4. Payload
- **Warhead:** TBD in coordination with DG user requirements
- **Guidance:** Multi-mode seeker (RF + IR dual-mode preferred)
- **Mass allocation:** ~45 g (see DD-CONCEPT.md §3 row 2)

---

## 5. Key Interfaces
| Interface | Partner Agent | Status |
|-----------|--------------|--------|
| Airframe geometry / mass | D3 | ✅ DD-CONCEPT.md v0.2 drafted |
| Propulsion inlet / nozzle sizing | D2 / E2 | CFD in progress |
| Avionics / GNC | E3 | ✅ E3-AVIONICS-PLAN.md active |
| Structural sizing / FEA | E1 | FEA plan active |
| Software / mission logic | AC | Monitoring; KPI watch active |
| MTOW lock (C2) | E1 | ✅ RESOLVED (DEC-007) |

---

## 6. Geometrical Constraints
- Fuselage: 35 mm outer diameter × 380 mm length
- Launcher bore: 40 mm (minimum clearance 2.5 mm per side)
- Wing chord: 60 mm | Arm length: 75 mm
- Fasteners: M2 (wings), M3 (motor mount)
- See DD-CONCEPT.md §2 for full dimensional layout

---

## 7. Open Items / Tracked by E1
- [x] C2 resolution (MTOW = 400 g) — CLOSED per DEC-007
- [ ] Propulsion selection trade — OPEN, owner D2/E2
- [ ] Avionics architecture — OPEN, owner E3
- [ ] FEA structural analysis — OPEN, owner E1 (waiting on geometry)
- [ ] ICD with all partners — OPEN, owner E1

*To be updated with D2 CFD data before G2 ratification (2026-07-09).*
