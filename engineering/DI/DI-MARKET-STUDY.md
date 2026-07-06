---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# DI-MARKET-STUDY — Interceptor_M Product Line: Defense Interceptor (DI)
## Market Study & Derived Requirements | v1.0 | June 2026

> **Context:** Issue #19 of the Interceptor_M autonomous counter-UAS project. DI product specs are currently null. This study grounds proposed specs in real market data and sourced competitor benchmarks.

---

## 1. Executive Summary

The global C-UAS market is experiencing explosive demand driven by three converging forces: the industrial-scale drone warfare demonstrated in the Russia-Ukraine conflict (2022–present), the Iran War escalation (2026), and the proliferation of low-cost Group 1–3 drones worldwide. MarketsandMarkets values the counter-UAS market at **USD 6.6 billion in 2025** growing at **25.1% CAGR to USD 20.3 billion by 2030**. Fortune Business Insights projects even faster growth to **USD 55.25 billion by 2034 at 22.4% CAGR**. The U.S. alone approved a **USD 1.98 billion counter-drone deal for Kuwait** — the largest single interceptor procurement in history — in Q2 2026.

The market bifurcates into two dominant segments: (1) **kinetic interceptors** (Anduril Anvil/Roadrunner-M, Raytheon Coyote, AeroVironment Freedom Eagle-1, MARSS Interceptor-MR) priced USD 30k–USD 150k/unit and designed for military-grade air defense; and (2) **commercial intercept drones** (Ukrainian systems, Yolka) priced USD 500–USD 2,500/unit where Ukraine is producing **tens of thousands per month**. No system currently dominates the middle market: a reusable, autonomous interceptor drone in the 5–15 kg weight class with multi-target capability and sub-USD 50k unit cost.

This gap — and the operational lessons from Ukraine — are the primary rationale for the DI product line. The DI must be a **ground-launched, autonomous or semi-autonomous interceptor drone** targeting the gap between cheap expendable FPV interceptors and expensive traditional air defense missiles.

---

## 2. Market Landscape & Competitor Benchmark

### 2.1 Competitive Systems

| System | Vendor | Origin | Type | Top Speed | Range / Endurance | Intercept Altitude | Payload / Kill | Seeker / Guidance | Weight Class | Unit Cost (approx.) |
|--------|--------|--------|------|-----------|-------------------|--------------------|----------------|-------------------|--------------|---------------------|
| **Anvil** | Anduril | USA | Rotary-wing kinetic interceptor | ≤320 km/h | Close-range, box-launched, reusable | Low–mid altitude | Kinetic impact (ram) — destroys both aircraft | EO/AI autonomous tracking + human operator ID | ~a few kg | ~USD 10k–30k (est.) |
| **Anvil-M** | Anduril | USA | Munitions variant of Anvil | ≤320 km/h | Close-range | Low–mid | Fire control + explosive warhead (lethal variant) | EO/AI + fire control module | ~a few kg | Higher than Anvil |
| **Roadrunner-M** | Anduril | USA | Jet-powered VTOL loitering interceptor | High subsonic (~1,235 km/h by analogy with Block 2 turbojet) | 10× range vs. competition; loiter-capable; reusable | Up to Group 3 altitude | HE warhead | Lattice C2 / integrated with existing radar + operator command | ~2 m airframe, twin-turbojet | Higher than Anvil; reusable offsets cost |
| **DroneHunter F700** | Fortem Technologies | USA | Net-capture autonomous interceptor | Medium | Perimeter defense; autonomous patrol | Low–mid altitude | Net entanglement (patented Drape Net); recoverable | Fortem TrueView radar + onboard autopilot; dual cameras (5.0) | <7.3 kg (<16 lbs) | USD 10k–50k range |
| **DroneHunter 5.0** | Fortem Technologies | USA | Net-capture + autonomous swarming | Medium | 5×5 simultaneous engagement; 4-net-gun option | Low–mid | Net (up to 4 nets) | TrueView radar + dual cameras + expanded computing; SkyDome C2 | <7.3 kg | USD 10k–50k range |
| **Interceptor-MR** | MARSS (EOS since 2026) | Monaco/UK | Kinetic ram interceptor | 80 m/s (288 km/h / 155 kts) | 5 km; up to >2 km altitude; 4g maneuver | >2 km (MR capable) | Hit-to-kill kinetic ram (no explosive warhead); can hit up to 3 Class 1 or 1 Class 2 per sortie | Imaging IR sensor + NiDAR AI; autonomous engagement, 90% hit rate claimed; re-engage on miss | 8 kg (updated 2024 design); wingspan 90 cm | USD 30k–40k (MR); production 2026 at <USD 50k |
| **Coyote Block 2** | Raytheon (RTX) | USA | Jet-powered loitering interceptor | Faster than Block 1; turbojet | km range with re-engage capability; up to 4 min loiter | Higher altitude than comparable systems | Fragmenting warhead (shrapnel field); rocket booster + turbine sustainment | Autonomous swarming; can re-attack if first pass misses | Expendable, ~sonobuoy-canister-sized | USD 10k–50k (expendable); under LIDS program |
| **Coyote Block 3 NK** | Raytheon (RTX) | USA | Non-kinetic loitering interceptor (recoverable) | Similar to Block 2 | Longer range and higher altitude than comparable effectors | Higher altitude | Non-kinetic (electronic/soft); recoverable for reuse | Autonomous AI | Expendable but recoverable | Lower per-engagement cost vs. kinetic |
| **Freedom Eagle-1 (FE-1)** | AeroVironment (BlueHalo) | USA | Surface-to-air kinetic missile | Subsonic | Long-range (LRKI program); loitering capable | Long-range air defense | Kinetic hit-to-kill | Dual-thrust solid rocket motor; ~15 cm diameter; NGCM winner | Missile (not a drone) | USD 95.9M LRKI contract Oct 2025 (multinational program) |
| **Sting / FPV interceptor** | Ukrainian industry | Ukraine | FPV-based kinetic interceptor | High (FPV speeds ~110–120 km/h) | Short-range tactical; expendable | Low (tens of meters) | Fragmentation charge or ram | EO + AI thermal imaging (Octopus-100); fiber-optic control (P1-SUN) | FPV frame | USD 2,500–5,000 |
| **Tytan (T716A)** | T716A Technologies | Ukraine | FPV interceptor drone | ~160 km/h est. | Short-range tactical | Low | Kinetic impact | Operator cueing | FPV frame | ~USD 500–1,000 |
| **Wild Hornet Wing-S** | Ukrainian industry | Ukraine | FPV interceptor | ~160 km/h est. | Short-range tactical | Low | Kinetic / fragmentation | EO/operator | FPV frame | ~USD 500–2,000 |
| **Yolka** | Russian MoD | Russia | Man-portable kinetic interceptor | Not disclosed | Short-range point defense | Low | Fire-and-forget kinetic ram | EO/AI autonomous | Man-portable | ~USD 500 (2026) |
| **Skydio (Defense)** | Skydio | USA | ISR + limited counter-UAS | ~100 km/h | Long endurance | Various | Non-kinetic / ISR | Autonomous flight + AI | ~2 kg | Moderate |

### 2.2 Market Size & Procurement Trends

| Metric | Value | Source |
|--------|-------|--------|
| C-UAS Market 2025 | USD 6.64 billion (M&M) / USD 5.99B (Fortune) | [MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/counter-cuas-systems-market-4197284.html), [Fortune Business Insights](https://www.fortunebusinessinsights.com/counter-uas-market-111906) |
| C-UAS Market 2030 | USD 20.31 billion | MarketsandMarkets |
| C-UAS Market 2034 | USD 55.25 billion | Fortune Business Insights |
| CAGR | 22.4%–25.1% (2025–2034) | Both sources |
| US DoD Counter-C-UAS Procurement (Kuwait deal) | USD 1.98 billion | [RBC Ukraine News](https://newsukraine.rbc.ua/news/us-approves-1-98-billion-counter-drone-deal-1781177815.html) |
| Ukraine interceptor production rate | Tens of thousands per month | [Defence Blog / Covert Shores](https://defence-blog.com/anduril-founder-calls-ukraines-drone-interceptor-output-extraordinary/) |
| Replicator-2 selection (Fortem) | DroneHunter selected | [Unmanned Airspace](https://www.unmannedairspace.info/counter-uas-systems-and-policies/fortem-begins-fifth-generation-dronehunter-deliveries/) |
| EU-Ukraine Drone Alliance | Active (battlefield learning → procurement) | [MarketsandMarkets ResearchInsight](https://www.marketsandmarkets.com/ResearchInsight/counter-cuas-systems-outlook-2030.asp) |
| EOS/MARSS new orders | ~EUR 102 million (May 2026) | [AeroTime](https://www.aerotime.aero/articles/eos-marss-counter-drone-eurosatory-2026) |
| AeroVironment LRKI/FE-1 contract | USD 95.9 million (Oct 2025) | [BusinessWire](https://www.businesswire.com/news/home/20251022561562/en/AV-Selected-for-U.S.-Army-Next-Generation-C-UAS-Missile-Program-Awarded-95.9M-Contract-to-Deliver-Fe-1-for-U.S.-Army) |

---

## 3. Threat Envelope: What the DI Must Counter

The DI must be designed to defeat the following current and near-term threat categories, drawn from operational experience in Ukraine, the Middle East, and published DoD threat assessments.

### 3.1 DoD UAS Group Classification

| Group | Weight | Typical Altitude | Typical Speed | Examples | DI Relevance |
|-------|--------|-----------------|--------------|----------|--------------|
| Group 1 | 0–20 lbs (0–9 kg) | <1,200 ft AGL | <250 kt (~460 km/h) | Commercial quadcopters, FPV drones, Raven | **Primary threat** |
| Group 2 | 20–55 lbs (9–25 kg) | <3,500 ft AGL | <250 kt | ScanEagle, MQ-27, fixed-wing tactical | **Key threat** |
| Group 3 | 55–1,320 lbs (25–600 kg) | <18,000 ft AGL | <250 kt | Shahed-136/236, Coyote, HERO, Silver Fox | **Relevant (Group 3 loitering munitions)** |

*Source: [Congress CRS IF12797](https://www.congress.gov/crs-product/IF12797); [Wikipedia UAS Groups](https://en.wikipedia.org/wiki/UAS_groups_of_the_United_States_military)*

### 3.2 Threat Profiles by Type

#### FPV Drones (Group 1 — Primary Threat)
- **Speed:** 110–120 km/h sustained; bursts up to 160 km/h
- **Altitude:** 1–3 m AGL (intentionally below radar detection threshold)
- **RCS:** Extremely low (<0.01 m²); composite/aircraft-grade plastics and carbon fiber scatter radar poorly; frequently masked by ground clutter
- **Guidance:** Manual operator control (highly erratic, stochastic trajectories) or semi-autonomous with fiber-optic data link
- **Payload:** 0.5–1.5 kg RPG-class or shaped charge; grenade
- **Operational note:** FPVs are cheap (USD 500–2,500), expendable, and human capital-intensive. Ukraine deploys them by the thousands per month. They are the primary short-range point-defense threat.

#### Loitering Munitions / Kamikaze Drones (Group 3 — Key Threat)
- **Speed:** 120–180 km/h (Shahed-136: ~180 km/h; Shahed-236: faster)
- **Altitude:** 200–4,000 m AGL; Shahed-type flies pre-programmed routes at ~800–2,000 m
- **RCS:** Low-to-moderate (0.1–1 m²); composite delta-wing but larger than FPV
- **Navigation:** GPS/GLONASS + inertial; some with satellite comms for mid-course update; fiber-optic in P1-SUN variants to counter EW
- **Payload:** 40–50 kg warhead (Shahed-136: ~40 kg); can devastate infrastructure, airfields, logistics nodes
- **Operational note:** Shahed-type drones are the most operationally significant threat in air defense. Russia has fired thousands in Ukraine. The 2026 Iran War triggered massive Shahed-class swarms against Gulf states, exposing gaps in current air defense architecture.

#### Fixed-Wing Tactical UAS (Group 2–3)
- **Speed:** 100–300 km/h
- **Altitude:** 1,000–6,000 m AGL
- **RCS:** 0.1–1 m²
- **Examples:** ScanEagle, Silver Fox, HERO series, TERMIT
- **Role:** ISR, targeted strikes, relay communications

### 3.3 Threat Summary Table for DI Design

| Threat | Speed (km/h) | Altitude (m AGL) | RCS (m²) | Guidance | DI Requirement |
|--------|-------------|-----------------|----------|----------|----------------|
| FPV drone | 110–160 | 1–50 | <0.01 | Manual/EO+AI | Short-range, high agility, low-RCS tracking |
| Loitering munition (Shahed-class) | 120–200 | 200–4,000 | 0.1–1.0 | GPS+INS, semi-autonomous | Medium-range, area defense, loiter + intercept |
| Tactical fixed-wing UAS | 100–300 | 1,000–6,000 | 0.1–1.0 | Pre-programmed/ISR relay | Medium-to-long range, higher ceiling |
| Drone swarm (5–10+) | 110–180 (heterogeneous) | 1–3,000 | <0.01 | Mixed | Multi-target autonomous engagement |

---

## 4. Derived DI Target Requirements

The following proposed specs are grounded in the competitive benchmark (Section 2), threat analysis (Section 3), and identified market gap: a reusable, autonomous, mid-tier interceptor drone at unit cost USD 30k–80k, targeting Group 1–3 threats from point defense to area protection.

### 4.1 Proposed DI Specification

| Parameter | Proposed Target | Rationale |
|-----------|---------------|-----------|
| **Role** | Ground-launched autonomous interceptor drone — point and area defense | Consistent with Anvil, Roadrunner-M, MARSS Interceptor-MR positioning |
| **Weight Class** | 8–12 kg (MTOW) | Slightly heavier than DroneHunter F700 (<7.3 kg) and MARSS Interceptor-MR (8 kg) to allow dualpayload and extended endurance; still man-transportable in 2-person teams |
| **Airframe** | Carbon fiber / thermoset composite; delta-wing or quad-rotor with VTOL | Delta-wing: higher speed (MARSS approach); Quad-rotor with VTOL: more maneuverable at low altitude (Anvil approach). **Recommendation: modular — offer both variants** |
| **Propulsion** | Dual electric pusher prop + 4 steering motors OR twin micro-turbojet | Turboprop/micro-turbojet preferred for speed >200 km/h to match loitering munitions; electric acceptable for net-capture variant |
| **Top Speed** | ≥350 km/h (high subsonic) | Exceeds FPV threat (≤160 km/h) and loitering munitions (≤200 km/h); comparable to MARSS Interceptor-MR (288 km/h) with margin; Anduril Anvil reaches 320 km/h |
| **Operating Ceiling** | 0–3,500 m AGL | Covers FPV threats (1–50 m) + Group 2–3 tactical UAS (up to 3,500 m); matches DoD Group 2 ceiling |
| **Endurance / Loiter Time** | ≥20 min loiter / ≥15 min intercept envelope | Comparable to Coyote Block 2 (4 min loiter is a limitation); market gap is longer loiter. 20 min enables area patrol and multi-pass engagement |
| **Range (one-way)** | 5–8 km (base variant) / 15 km (extended variant) | MARSS Interceptor-MR: 5 km — DI should exceed this. Anduril Roadrunner-M claims 10× range vs competition. 8 km base range with relay-optional datalink for 15 km |
| **Guidance / Seeker** | Imaging IR (uncooled) + EO visible + AI onboard processing (NiDAR-class) | MARSS Interceptor-MR uses imaging IR; autonomous AI engagement; dual-band sensor (EO+IR) needed for day/night operation and low-RCS targets |
| **Autonomy Level** | Semi-autonomous (human-in-the-loop for engagement authorization) + autonomous tracking/capture | DroneHunter 5.0, Anvil, MARSS all use human operator for engagement; full autonomy raises policy/LOi issues |
| **Kill Mechanism** | **Dual-payload bay (modular):** (A) Kinetic ram — hit-to-kill no explosive (MARSS approach; low collateral); (B) Net entanglement — for sensitive-area / low-collateral ops (DroneHunter approach) | Market is splitting between kinetic and net; modular payload solves both use cases. Weight budget allows ~1 kg additional payload at 8 kg class |
| **Multi-Target** | Up to 3–5 simultaneous engagements per sortie | DroneHunter 5.0: 5×5; DI should target minimum 3 simultaneous engagements (1 Class 2 or 3 Class 1) per sortie |
| **Reusability** | ≥80% recovery rate; ground-recoverable | Anvil, Roadrunner-M, MARSS, Coyote Block 3NK all emphasize reusability. Net variant fully recoverable. Kinetic variant recoverable at 80%+ if non-catastrophic intercept |
| **Unit Cost Target** | USD 30,000–60,000 | MARSS Interceptor-MR: USD 30k–40k; one-fifth the cost of traditional SAM ($150k–200k). DI must hit USD 30k–60k range to be procurement-attractive. Ukraine produces at USD 500–2,500 but without autonomous seeker |
| **Launch System** | Box launcher (ground-mobile); man-portable variant for point defense | Consistent with Anvil Launch Box, MARSS box launcher, Coyote canister launch |
| **Datalink / C2** | Ku-band tactical datalink; compatible with NATO C2 standards; Lattice-class AI C2 optional | Must integrate into layered C-UAS architecture; Ku-band balances range, data rate, SWaP. NATO interoperability required for export |
| **ECCM / EW Resilience** | Anti-jam GPS, inertial backup, optional fiber-optic data link | Ukraine's P1-SUN uses fiber-optic to counter EW; DI baseline should at minimum have anti-jam GPS + INS backup |
| **SWaP** | Size: ≤1 m wingspan (folded); Weight: ≤12 kg; Power: internal battery or fuel cell | Man-transportable and vehicle-mountable; must fit standard interceptor launch box |
| **Compliance** | MIL-STD-810H (environmental); NATO STANAG 4586 (UAV C2 interface) | Standard requirements for defense procurement |

### 4.2 DI Variants (Proposed)

| Variant | Role | Payload | Speed | Range | Unit Cost Est. |
|---------|------|---------|-------|-------|----------------|
| **DI-V1 "Sting"** | Short-range point defense; kinetic | Kinetic ram only | ≥300 km/h | 5 km | ~USD 30k |
| **DI-V2 "Shielder"** | Short-range point defense; net capture | Net gun (2–4 nets) | ≥200 km/h | 3 km | ~USD 25k |
| **DI-V3 "Sentinel"** | Area defense; loitering interceptor | Kinetic + extended fuel | ≥350 km/h | 12 km | ~USD 55k |

### 4.3 Differentiation vs. Existing Systems

The DI fills a specific market gap:

- **vs. Anvil/Roadrunner-M:** Neither Anvil nor Roadrunner-M is available at unit cost <USD 60k in the 8–12 kg class; DI targets organic company/small-unit procurement
- **vs. MARSS Interceptor-MR:** MARSS is priced USD 30k–40k and targets Group 2–3; DI must add multi-target capability (MARSS: 1 Class 2 or 3 Class 1 per sortie) and longer loiter time (MARSS: not disclosed, likely <10 min) to differentiate
- **vs. Coyote Block 3 NK:** Coyote is recoverable but primarily canister-launched from ships; DI is ground-mobile with VTOL for frontline troops
- **vs. Ukrainian FPV interceptors:** These are cheap but operator-dependent and require manual targeting; DI adds autonomous seeker and multi-engagement capability

---

## 5. Recommendations & Open Questions

### 5.1 Immediate Recommendations (Next 90 Days)

1. **Commission physical benchmark of MARSS Interceptor-MR and DroneHunter F700** to validate the proposed weight, speed, and cost targets against actual procurement quotes.
2. **Select DI kill mechanism priority:** Kinetic (ram) vs. net capture vs. dual-payload. This decision drives sensor suite (EO/IR priority vs. radar), airframe design (delta-wing vs. quad-rotor), and unit cost. Recommend kinetic as primary, net as secondary variant.
3. **Define DI deployment concept:** Point defense (static base protection) vs. mobile (vehicle-mounted) vs. front-line man-portable. Each implies different SWaP constraints and quantities.
4. **Initiate customer discovery:** Issue #19 is blocked pending market study — now unblocked. Recommend direct outreach to 2–3 potential DoD/international customers for early requirements validation before detailed design.
5. **Open a DI requirements GitHub issue** (linked to #19) to capture and track derived specs with team input.

### 5.2 Open Questions

| Question | Why It Matters |
|----------|---------------|
| **Autonomy level:** Does the DI require a human operator in the engagement loop for all variants, or can a high-KPI autonomous mode be authorized? | Drives export licensing (ITAR), policy, and insurance. See RF3 mitigations in project governance. |
| **Solo vs. swarm deployment:** Should the DI be designed to operate in coordinated swarms of 3–5 units (synergistic with the E2/D3 Swarm RL workstream)? | Swarm coordination adds C2 complexity but dramatically increases intercept probability and reduces per-engagement cost. Could be a key differentiator vs. MARSS/Coyote. |
| **Recovery rate target:** What is the acceptable mission abort / non-recovery rate? | Drives airframe structural design, landing system (VTOL parachute vs. ground recovery), and unit cost. |
| **Datalink range:** Is 15 km one-way sufficient, or is relay-based BVLOS required? | Drives antenna design, power budget, and potential need for mesh networking. |
| **IR vs. RF seeker for low-RCS targets:** FPV drones with composite bodies are nearly invisible to radar and IR. What is the primary cueing sensor? | Fortem TrueView radar + EO/IR dual is the current best practice. A dedicated RF seeker may be needed for Group 1 FPVs. |
| **Unit cost vs. production rate trade:** At what production volume does the USD 30k–60k target become achievable? (Ukrainian interceptors reach USD 500–2,500 at tens of thousands/month.) | Scale drives supplier selection, manufacturing approach, and export market positioning. |

---

## 6. Sources

1. MarketsandMarkets — *Counter-Unmanned Aircraft System (C-UAS) Market Report 2025*, https://www.marketsandmarkets.com/Market-Reports/counter-cuas-systems-market-4197284.html
2. Fortune Business Insights — *Counter-UAS Market*, https://www.fortunebusinessinsights.com/counter-uas-market-111906
3. MarketsandMarkets ResearchInsight — *Counter-C-UAS Systems Outlook 2030*, https://www.marketsandmarkets.com/ResearchInsight/counter-cuas-systems-outlook-2030.asp
4. RBC Ukraine News — "US Approves $1.98 Billion Counter-Drone Deal for Kuwait", June 2026, https://newsukraine.rbc.ua/news/us-approves-1-98-billion-counter-drone-deal-1781177815.html
5. Defence Blog — "Anduril Founder Calls Ukraine's Drone Interceptor Output Extraordinary", June 2026, https://defence-blog.com/anduril-founder-calls-ukraines-drone-interceptor-output-extraordinary/
6. Drones World Magazine — "Anduril Announces Anvil-M Munition Variant", https://www.dronesworldmag.com/anduril-announces-anvil-m-munition-variant-of-interceptor-platform/
7. Anduril — Roadrunner / Roadrunner-M press materials, https://www.dronesworldmag.com/anduril-unveils-roadrunner-roadrunner-m/ and https://www.defenceconnect.com.au/joint-capabilities/14727-anduril-unveils-roadrunner-interceptor-at-land-forces-2024
8. Designation-Systems.net — "Anduril Roadrunner", https://www.designation-systems.net/dusrm/app4/roadrunner.html
9. Fortem Technologies — DroneHunter F700 product page, https://tinex.no/products_category/dronehunter-f700/
10. Fortem Technologies — DroneHunter 5.0 press release (Jan 2026), https://fortemtech.com/press-releases/2026-01-20-fortem-technologies-begins-deliveries-of-next-generation-dronehunter-5-0-advancing-counter-swarm-defense/
11. Fortem Technologies — DroneHunter initial announcement (2018), https://fortemtech.com/press-releases/2018-02-15-fortem-announces-dronehunter/
12. Unmanned Airspace — "Fortem Begins Fifth-Generation DroneHunter Deliveries", 2026, https://www.unmannedairspace.info/counter-uas-systems-and-policies/fortem-begins-fifth-generation-dronehunter-deliveries/
13. Wikipedia — "MARSS Interceptor", https://en.wikipedia.org/wiki/MARSS_Interceptor
14. AeroTime — "EOS/MARSS Counter-Drone at Eurosatory 2026", June 2026, https://www.aerotime.aero/articles/eos-marss-counter-drone-eurosatory-2026
15. SpaceWar — "Raytheon Demonstrates Recoverable Coyote System Against Drone Swarms", Feb 2026, https://www.spacewar.com/reports/Raytheon_demonstrates_recoverable_Coyote_system_against_drone_swarms_999.html
16. ASDNews — "Raytheon's Non-Kinetic Coyote Variant Defeats Multiple Drone Swarms", Feb 2026, https://www.asdnews.com/news/defense/2026/02/11/raytheons-nonkinetic-coyote-variant-defeats-multiple-drone-swarms
17. Wikipedia — "Raytheon Coyote", https://en.wikipedia.org/wiki/Raytheon_Coyote
18. Aviation Week — "Raytheon Demonstrates Non-Kinetic Variant of Drone Interceptor", Feb 2026, https://aviationweek.com/defense/sensors-electronic-warfare/raytheon-demonstrates-non-kinetic-variant-drone-interceptor
19. Designation-Systems.net — "AeroVironment Freedom Eagle-1 (FE-1)", https://www.designation-systems.net/dusrm/app4/fe-1.html
20. BusinessWire — "AeroVironment Awarded $95.9M for FE-1 / LRKI", Oct 2025, https://www.businesswire.com/news/home/20251022561562/en/AV-Selected-for-U.S.-Army-Next-Generation-C-UAS-Missile-Program-Awarded-95.9M-Contract-to-Deliver-Fe-1-for-U.S.-Army
21. Congress CRS — "UAS: Background and Oversight Issues for Congress" (IF12797), https://www.congress.gov/crs-product/IF12797
22. Wikipedia — "UAS Groups of the United States Military", https://en.wikipedia.org/wiki/UAS_groups_of_the_United_States_military
23. Wikipedia — "Interceptor Drone", https://en.wikipedia.org/wiki/Interceptor_drone
24. Wikipedia — "Yolka Drone Interceptor", https://en.wikipedia.org/wiki/Yolka_(drone_interceptor)
25. Endoacustica — "FPV Drone Tactics", https://www.endoacustica.com/fpv-drone-tactics.php
26. SkyShile — "FPV Drone Defense System", https://www.skyshile.com/blog/company-news/fpv-drone-defense-system

---

*DI-MARKET-STUDY.md — Generated June 2026 | Interceptor_M Project | For internal engineering and procurement planning. All vendor specs sourced from public domain; internal specs are proposed targets pending validation.*