---
title: OPERATIONS_WORKFLOW
version: 2.0
author: Agent Manager
validator: DG
last_updated: 2026-06-22
type: SOP
---

# 🛡️ OPERATIONS_WORKFLOW.md — Opération Drone Interception

> **CHANGELOG V2.0:**
> - ✅ Added Section 0: "OÙ LE DG DOIT INTERVENIR" with decision tree
> - ✅ Added Section 2.5: Designer↔Engineer Shared Work Table
> - ✅ Added Section 5.5: DG Intervention Decision Tree
> - ✅ Added Section 8: KPI Dashboard + Fine-Tuning Levers
> - ✅ Added Section 9: Agent Interaction Map (Mermaid)
> - ✅ Enhanced escalation matrix with more detail
> - ✅ All existing content preserved and improved

---

## Table des matières

0. [OÙ LE DG DOIT INTERVENIR](#0-où-le-dg-doit-intervenir)
1. [TEAM ROLES — Fiches Agents Complètes](#1-team-roles--fiches-agents-complètes)
2. [COLLABORATION MAP — Designers ↔ Engineers](#2-collaboration-map--designers--engineers)
3. [WORKFLOW PHASES — Par Ligne de Produit](#3-workflow-phases--par-ligne-de-produit)
4. [GO/NO-GO GATES — DG Validation Points](#4-gono-go-gates--dg-validation-points)
5. [PROBLEM RESOLUTION PROTOCOL](#5-problem-resolution-protocol)
6. [DAILY / WEEKLY RHYTHM](#6-daily--weekly-rhythm)
7. [AI/ML INTEGRATION POINTS WITH DESIGN & ENGINEERING](#7-aiml-integration-points-with-design--engineering)
8. [KPI DASHBOARD + FINE-TUNING LEVERS](#8-kpi-dashboard--fine-tuning-levers)
9. [AGENT INTERACTION MAP](#9-agent-interaction-map)

---

## 0. OÙ LE DG DOIT INTERVENIR / WHERE DG MUST ACT

### 0.1 Decision Tree — DG Intervention

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    OÙ INTERVIENT LE DG ?                                        │
│                    WHERE DOES DG NEED TO ACT ?                                  │
│                                                                                 │
│    Start: "Which phase is the project in?"                                      │
└─────────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │  PHASE 0 Start  │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │   G0 + G10      │
                              │  INITIATION     │
                              │  + COMMERCIAL   │
                              └────────┬────────┘
                                       │
              ┌────────────────────────┼────────────────────────┐
              │                        │                        │
              ▼                        ▼                        ▼
     ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
     │   PHASE 1      │      │   PHASE 2      │      │  PHASES 3-7    │
     │   CONCEPT      │      │   ENGINEERING  │      │ CAD/SIM/PROTOTYPE
     └───────┬────────┘      └───────┬────────┘      └───────┬────────┘
             │                       │                       │
             ▼                       ▼                       ▼
     ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
     │ G1 (Brief)    │       │ G3 (NDC)      │       │ G4 (CAO)      │
     │ G2 (Concept)  │       │ G5 (Sim GO)   │       │ G5 (Sim GO)   │
     └───────────────┘       └───────────────┘       │ G6 (Sim Res)  │
                                                       │ G7 (Proto GO) │
                                                       │ G8 (Test Res) │
                                                       │ G9 (Prod GO)  │
                                                       └───────────────┘

═══════════════════════════════════════════════════════════════════════════════

                         "What type of decision?"
                                      │
       ┌────────────────┬──────────────┼──────────────┬──────────────────┐
       │                │              │              │                  │
       ▼                ▼              ▼              ▼                  ▼
  STRATEGIC        TECHNICAL       COMMERCIAL     RESOURCE           SAFETY
  (direction)      (design/        (proposal      (conflict)        (urgent)
                    engineering)   quote)
       │                │              │              │                  │
       ▼                ▼              ▼              ▼                  ▼
  DG ALWAYS      DG @ G2/G3    DG @ G10      AC → DG       DG IMMEDIATE
  (briefing)     (if >3 loops   ALWAYS        (escalate)    (≤1h SLA)
                 before DG)                                       │
                                                                 ▼
                                                           ┌────────────┐
                                                           │ G11 (2h)   │
                                                           │ Emergency  │
                                                           └────────────┘

═══════════════════════════════════════════════════════════════════════════════

                         "Is there a blocker?"
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                         ▼                         ▼
                    YES — BLOCKER             NO — NO BLOCKER
                         │                         │
                         ▼                         ▼
              ┌──────────────────┐      ┌─────────────────────┐
              │ Agent Manager     │      │ DG receives daily    │
              │ reports to DG    │      │ digest but no        │
              │ immediately      │      │ action required      │
              └──────────────────┘      └─────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

                         QUICK REFERENCE MATRIX
                         (for daily use — print this)

    ┌─────────────────────────────────────────────────────────────────────┐
    │ QUESTION                                    →   CONTACT              │
    ├─────────────────────────────────────────────────────────────────────┤
    │ "Is this gate ready for DG decision?"       →   Check this doc      │
    │ "What phase are we in?"                    →   Agent Manager       │
    │ "Is there a blocker?"                      →   Agent Manager       │
    │ "Who should do this task?"                  →   Agent Manager       │
    │ "Design question (structural)"              →   D1                  │
    │ "Design question (industrial)"              →   D2                  │
    │ "Design question (defense)"                  →   D3                  │
    │ "Engineering question (systems)"            →   E1                  │
    │ "Engineering question (propulsion)"         →   E3                  │
    │ "Process question"                          →   AC                   │
    │ "Commercial question"                       →   Commercial           │
    │ "I need a decision NOW"                     →   DG (call)            │
    │ "I need DG input but it's not urgent"        →   Agent Manager (route)│
    └─────────────────────────────────────────────────────────────────────┘
```

### 0.2 OÙ LE DG DOIT INTERVENIR — Résumé (WHERE DG MUST ACT — Summary)

| Type de situation | Quand DG intervient | SLA | Qui contacter en premier |
|---|---|---|---|
| **Nouvelle opportunité commerciale** | G0 + G10 | 24h | Agent Manager → DG package |
| **Nouveau brief client** | G1 | 24h | Agent Manager → DG approval |
| **Sélection concept** | G2 | 48h | D1 → Agent Manager → DG package |
| **Validation calculs (NDC)** | G3 | 48h | E1 → Agent Manager → DG package |
| **Validation CAO** | G4 | 48h | D1 → Agent Manager → DG package |
| **GO Simulation** | G5 | 48h | E1 → Agent Manager → DG package |
| **Résultats simulation** | G6 | 48h | E1 → Agent Manager → DG package |
| **GO Prototype** | G7 | 72h | E1+E2+E3 → Agent Manager → DG package |
| **Résultats tests** | G8 | 48h | E1 → Agent Manager → DG package |
| **GO Production** | G9 | 72h | DG (direct) | DG (direct) |
| **Problème design (>3 itérations)** | Si Steps 3↔4 dépassent 3 itérations | 48h | D1 → Agent Manager → DG |
| **Problème engineering (blocage)** | Si E1 ne peut pas résoudre | 24h | E1 → Agent Manager → DG |
| **Conflit ressources** | Si Agent Manager ne peut pas résoudre | 48h | Agent Manager → DG |
| **Urgence sécurité** | Toujours | 2h (G11) | E1 → DG (appel direct) |

---

## 1. TEAM ROLES — Fiches Agents Complètes

### 🎨 AGENT MANAGER — Orchestrateur IA

#### Description du rôle

| | EN | FR |
|---|---|---|
| **Fonction principale** | AI Orchestrator — coordonne tous les agents, route le travail, applique les règles | Orchestrateur IA — coordonne tous les agents, route le travail, applique les règles |
| **Responsabilités clés** | Maintenir OPERATIONS_WORKFLOW.md, détecter les blocages, préparer les GO/NO-GO pour DG | Maintenir OPERATIONS_WORKFLOW.md, détecter les blocages, préparer les GO/NO-GO pour DG |
| **Contrainte** | Ne peut pas outrepasser les décisions DG ; doit router toutes les approbations via DG | Ne peut pas outrepasser les décisions DG ; doit router toutes les approbations via DG |
| **Supervision** | Supervise tous les agents (D1/D2/D3, E1/E2/E3, Commercial, Marketing, AC) | Supervise tous les agents (D1/D2/D3, E1/E2/E3, Commercial, Marketing, AC) |

#### Outils principaux

| Outil | Usage | Licence |
|---|---|---|
| **OPERATIONS_WORKFLOW.md** | Document central de référence | Internal |
| **DECISION_LOG.md** | Journal de toutes les décisions | Internal |
| **Daily Digest Template** | Résumé quotidien pour DG + agents | Internal |
| **GO/NO-GO Template** | Package de décision pour DG | Internal |
| **Slack/Email** | Communication agent | SaaS |

#### Ce qu'il produit

- **Résumés quotidiens** (daily digest)
- **Packages GO/NO-GO** pour validation DG
- **Alertes blockers** à DG
- **Mises à jour OPERATIONS_WORKFLOW.md**
- **Rapports KPI hebdomadaires**

#### Avec qui il travaille

| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| DG | Prépare décisions, reçoit directives | Quotidien |
| D1 | Coordination design, peer review | Quotidien |
| E1 | Coordination engineering, handoffs | Quotidien |
| E2/E3 | Coordination technique | Hebdomadaire |
| AC | Revue processus, KPIs | Hebdomadaire |
| Commercial | Briefs clients | Par projet |
| Marketing | Alignement messaging | Hebdomadaire |

#### KPIs

| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Gate packages submitted on time | 100% | Par gate | <100% → escalade AC |
| Daily digest delivered by 09:00 | 100% | Quotidien | <100% → escalade AC |
| Active blockers resolved within SLA | >80% | Hebdomadaire | <80% → escalade DG |
| Team utilization | 60-80% | Hebdomadaire | <50% ou >90% → escalade DG |

---

### 🎨 AGENT DESIGNER D1 — Lead Mechanical Design

#### Description du rôle

| | EN | FR |
|---|---|---|
| **Fonction principale** | Lead Mechanical Design — Drone Civil concepts | Lead Design Mécanique — Concepts Drone Civil |
| **Domaines** | Photo, Delivery, Agriculture drones | Drones photo, livraison, agriculture |
| **Responsabilités clés** | Concept design, CAD management, peer review D2/D3 | Design conceptuel, gestion CAO, peer review D2/D3 |
| **Outils** | Fusion 360 | Fusion 360 |

#### Outils principaux

| Outil | Usage | Licence |
|---|---|---|
| **Fusion 360** | CAD, renders, concepts | Autodesk subscription |
| **Adobe Creative Suite** | Renders, présentations | Creative Cloud |
| **Slides** | Présentations client | Google Slides |

#### Ce qu'il produit

- **Concepts 3D** (photo, delivery, agriculture drones)
- **Renders** pour présentations client
- **CAO** pour validation engineering
- **Assemblies** (D2/D3 review)
- **Specifications** pour NDC

#### Avec qui il travaille

| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| D2 | Peer review, coordination industrielle | Hebdomadaire |
| D3 | Peer review, coordination défense | Hebdomadaire |
| E1 | Handoff 7-step, feedback loop | Par handoff |
| Agent Manager | Status, gate packages | Quotidien |

#### KPIs

| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Concept delivery on time | >85% | Par projet | <75% → escalade AM |
| Peer reviews completed | >80% | Hebdomadaire | <70% → escalade AM |
| Handoff packages ready | 100% | Par handoff | <100% → escalade AM |
| Revision iterations (Steps 3↔4) | <3 per phase | Par phase | >3 → escalade DG |

---

### 🎨 AGENT DESIGNER D2 — Industrial Design Specialist

#### Description du rôle

| | EN | FR |
|---|---|---|
| **Fonction principale** | Industrial Design Specialist | Spécialiste Design Industriel |
| **Domaines** | Industrial drone concepts (inspection, surveillance) | Concepts drones industriels (inspection, surveillance) |
| **Responsabilités clés** | Industrial aesthetics, ergonomics, user experience | Esthétique industrielle, ergonomie, expérience utilisateur |

#### Outils principaux

| Outil | Usage | Licence |
|---|---|---|
| **Inventor** | CAD, assemblies industrielles | Autodesk subscription |
| **Adobe Creative Suite** | Visuels, renders | Creative Cloud |

#### Ce qu'il produit

- **Concepts industriels** (inspection, surveillance)
- **Ergonomics studies**
- **Industrial aesthetics renders**
- **Payload integration concepts** (with D1)

#### Avec qui il travaille

| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| D1 | Peer review, assembly coordination | Hebdomadaire |
| Marketing | Visual identity alignment | Hebdomadaire |
| E3 | Payload integration | Par projet |

#### KPIs

| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Concept delivery on time | >85% | Par projet | <75% → escalade AM |
| Marketing alignment score | >80% | Hebdomadaire | <70% → escalade AM |

---

### 🎨 AGENT DESIGNER D3 — Defense Design Specialist

#### Description du rôle

| | EN | FR |
|---|---|---|
| **Fonction principale** | Defense Design Specialist | Spécialiste Design Défense |
| **Domaines** | Micro-interceptor drone, launcher system | Micro-drone intercepteur, système lanceur |
| **Responsabilités clés** | Defense aesthetics, rapid-deployment form factor, Swiss defense positioning | Esthétique défense, facteur de forme déploiement rapide, positionnement défense suisse |
| **Outils** | SolidWorks | SolidWorks |

#### Outils principaux

| Outil | Usage | Licence |
|---|---|---|
| **SolidWorks** | CAD, défense | Dassault Systèmes |
| **Adobe Creative Suite** | Renders, présentations | Creative Cloud |

#### Ce qu'il produit

- **Micro-interceptor drone design**
- **Compressed air launcher design**
- **Defense renders** (classified-appropriate)
- **Swarm visual coordination concepts**
- **Ergonomics for field deployment**

#### Avec qui il travaille

| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| D1 | Peer review | Hebdomadaire |
| E3 | Launcher integration | Par projet |
| Commercial | Swiss defense requirements | Par projet |
| Marketing | Swiss defense messaging | Hebdomadaire |

#### KPIs

| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Concept delivery on time | >85% | Par projet | <75% → escalade AM |
| Launcher integration specs ready | 100% | Par projet | <100% → escalade AM |

---

### 🔧 AGENT INGÉNIEUR E1 — Responsable Systèmes & Embarqué

#### Description du rôle

| | EN | FR |
|---|---|---|
| **Fonction principale** | Systems & Embedded Engineering Lead | Lead Ingénierie Systèmes & Embarqué |
| **Domaines** | Architecture système, embarqué, FEA, CFD | Architecture système, embarqué, FEA, CFD |
| **Responsabilités clés** | NDC, FEA, coordination E2/E3, interface design↔engineering | NDC, FEA, coordination E2/E3, interface design↔engineering |
| **Outils** | Python, Ansys, simulation | Python, Ansys, simulation |

#### Outils principaux

| Outil | Usage | Licence |
|---|---|---|
| **Python (SciPy, NumPy)** | Calculations, automation | Open source |
| **Ansys (FEA)** | Structural analysis | Academic/Commercial |
| **MATLAB/Simulink** | Systems simulation | Commercial |
| **LaTeX** | NDC documentation | Open source |

#### Ce qu'il produit

- **NDC validées** (Notes de Calcul)
- **FEA reports** (stress, deformation)
- **CFD analyses** (aerodynamics)
- **Architecture diagrams**
- **Interface specifications**
- **System integration plans**

#### Avec qui il travaille

| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| D1 | 7-step handoff, feedback loop | Par handoff |
| E2 | Peer review, structural analysis | Hebdomadaire |
| E3 | Propulsion, embedded systems | Quotidien |
| Agent Manager | Status, gate packages | Quotidien |

#### KPIs

| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| NDC delivery on time | >85% | Par projet | <75% → escalade AM |
| FEA first-pass success | >60% | Par FEA | <50% → escalade AM |
| Handoff response within SLA | 100% | Par handoff | <100% → escalade AM |
| Simulation accuracy vs test | >90% | Par test | <85% → escalade DG |

---

### 🔧 AGENT INGÉNIEUR E2 — Responsable Propulsion

#### Description du rôle

| | EN | FR |
|---|---|---|
| **Fonction principale** | Aerodynamics & Structural Engineering | Ingénierie Aérodynamique & Structures |
| **Domaines** | Portance, résistance structurelle, propulsion | Portance, résistance structurelle, propulsion |
| **Responsabilités clés** | Calculs de portance, analyse structurelle, propulsion | Calculs de portance, analyse structurelle, propulsion |

#### Outils principaux

| Outil | Usage | Licence |
|---|---|---|
| **Python (AeroPython)** | Aerodynamics calculations | Open source |
| **OpenFOAM** | CFD simulation | Open source |
| **Calculix** | FEA | Open source |

#### Ce qu'il produit

- **Calculs de portance** (lift calculations)
- **Analyse résistance** (structural analysis)
- **Specs propulsion**
- **FEA support** pour E1
- **Rapports de test moteur** (si prototype disponible)

#### Avec qui il travaille

| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| E1 | NDC support, FEA peer review | Hebdomadaire |
| E3 | Propulsion specs | Hebdomadaire |
| D1/D2 | Design feedback | Par handoff |

#### KPIs

| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Propulsion specs delivery | >85% | Par projet | <75% → escalade AM |
| FEA support response | <48h | Par demande | >48h → escalade AM |

---

### 🔧 AGENT INGÉNIEUR E3 — Responsable Électronique & Intégration

#### Description du rôle

| | EN | FR |
|---|---|---|
| **Fonction principale** | Propulsion & Integration Engineering | Ingénierie Propulsion & Intégration |
| **Domaines** | Propulsion, intégration système, electronics | Propulsion, intégration système, électronique |
| **Responsabilités clés** | Moteurs, lanceur air comprimé, intégration | Moteurs, lanceur air comprimé, intégration |

#### Outils principaux

| Outil | Usage | Licence |
|---|---|---|
| **Python** | Simulation, data analysis | Open source |
| **KiCad** | PCB design | Open source |
| **LaTeX** | Specs documentation | Open source |

#### Ce qu'il produit

- **Specifications moteur** (motor specs)
- **Specs lanceur air comprimé** (compressed air launcher)
- **Routage PCB** (si développement interne)
- **Spécifications câbles et connectique**
- **Integration verification reports**

#### Avec qui il travaille

| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| E1 | Systems integration | Quotidien |
| E2 | Propulsion coordination | Hebdomadaire |
| D3 | Launcher design feedback | Par handoff |

#### KPIs

| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Integration specs on time | >85% | Par projet | <75% → escalade AM |
| Test bench data analysis | <24h après test | Par test | >24h → escalade AM |

---

### 📈 AGENT AMÉLIORATION CONTINUE (AC)

#### Description du rôle

| | EN | FR |
|---|---|---|
| **Fonction principale** | Continuous Improvement Agent | Agent Amélioration Continue |
| **Domaines** | Processus, règles, guidelines, qualité | Processus, règles, guidelines, qualité |
| **Responsabilités clés** | Process monitoring, rule updates, quality assurance, KPI analysis | Surveillance processus, mises à jour règles, assurance qualité, analyse KPI |

#### Outils principaux

| Outil | Usage | Licence |
|---|---|---|
| **DECISION_LOG.md** | Process documentation | Internal |
| **KPI Dashboard** | Metrics tracking | Internal |
| **PROPOSAL templates** | Rule change submissions | Internal |
| **RULES_ARCHIVE/** | Archive of old rule versions | Internal |

#### Ce qu'il produit

- **Rapports de processus** (process reports)
- **Analyse KPI** (KPI analysis)
- **Recommandations d'amélioration** (improvement recommendations)
- **Mises à jour rules.md/guidelines.md** (avec approbation DG)
- **Alertes de seuil** (threshold alerts)

#### Avec qui il travaille

| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| DG | Process approvals, escalations | Hebdomadaire |
| Agent Manager | KPI reports, process issues | Quotidien |
| Tous les agents | Propositions d'amélioration | Par proposition |

#### KPIs

| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Proposals reviewed within SLA | 100% (48h) | Par proposition | <100% → escalade DG |
| KPI reports delivered on time | 100% | Hebdomadaire | <100% → escalade DG |
| Rule effectiveness score | >80% | Post-implementation | <70% → revue AC |

---

## 2. COLLABORATION MAP — Designers ↔ Engineers

### 2.1 Vue d'ensemble des handoffs

```
┌────────────────────────────────────────────────────────────────────────────┐
│            DESIGNER ↔ ENGINEER COLLABORATION MAP                             │
│            CARTE DE COLLABORATION DESIGNER ↔ INGÉNIEUR                       │
│                                                                            │
│  DG / Agent Manager                                                         │
│       │                                                                      │
│       ▼                                                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 1: BRIEF RECEPTION                                                │   │
│  │ De / From: DG/AM → Vers / To: D1/D2/D3                               │   │
│  │ Fichier / File: #BRIEF_ProjectName_Date.md                            │   │
│  │ Contenu / Content: Objectifs, contraintes, timeline                     │   │
│  └───────────────────────────────────────┬──────────────────────────────┘   │
│                                          │                                  │
│                                          ▼                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 2: CONCEPT DESIGN              ──────────────────────────────── │   │
│  │ De / From: D1/D2/D3 → Vers / To: D1/D2/D3                           │   │
│  │ Fichier / File: PROJECT-CONCEPT-P1-vX.X.[fmt]                         │   │
│  │ Contenu / Content: 3D renders, dimensions, materials                   │   │
│  └───────────────────────────────────────┬──────────────────────────────┘   │
│                                          │                                  │
│                                          ▼                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 3: NDC CREATION              ◀──────────────────────────────── │   │
│  │ De / From: E1 (+E2/E3) → Vers / To: D1/D2/D3                        │   │
│  │ Fichier / File: PROJECT-NDC-P2-vX.X.pdf                             │   │
│  │ Contenu / Content: Notes calculées, safety factors, specs             │   │
│  │ Note: Must reference D concept version                                │   │
│  └───────────────────────────────────────┬──────────────────────────────┘   │
│                                          │                                  │
│       ┌──────────────────────────────────┘                                  │
│       │  (FEEDBACK LOOP / BOUCLE DE FEEDBACK)                              │
│       ▼                                                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 4: CAD REVISION                                                  │   │
│  │ De / From: D1 ↔ Vers / To: E1 (feedback loop)                        │   │
│  │ Fichier / File: PROJECT-CAD-P3-vX.X.[fmt]                             │   │
│  │ Contenu / Content: CAO mis à jour selon NDC / CAD updated from NDC   │   │
│  │ ⚠️ Max 3 iterations avant escalade DG / before DG escalation          │   │
│  └───────────────────────────────────────┬──────────────────────────────┘   │
│                                          │                                  │
│                                          ▼                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 5: SIMULATION MODEL PREP                                        │   │
│  │ De / From: D1 → Vers / To: E1                                        │   │
│  │ Fichier / File: PROJECT-SIM-P4-vX.X.[fmt]                              │   │
│  │ Contenu / Content: Géométrie nettoyée pour FEA / Clean geometry for FEA│   │
│  └───────────────────────────────────────┬──────────────────────────────┘   │
│                                          │                                  │
│                                          ▼                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 6: FEA / SIMULATION EXECUTION                                    │   │
│  │ De / From: E1 → Vers / To: D1 + DG                                    │   │
│  │ Fichier / File: PROJECT-FEA-P4-vX.X.pdf                               │   │
│  │ Contenu / Content: Résultats FEA validés / Validated FEA results       │   │
│  └───────────────────────────────────────┬──────────────────────────────┘   │
│                                          │                                  │
│                                          ▼                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 7: DESIGN FREEZE OR ITERATE                                       │   │
│  │ De / From: D1 + E1 (joint) → Vers / To: DG                            │   │
│  │ G4: CAO Validation     → GO/NO-GO Gate G4                             │   │
│  │ G5: Simulation GO      → GO/NO-GO Gate G5                             │   │
│  │ G6: Simulation Results → GO/NO-GO Gate G6                             │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Handoff Details — Fichier par fichier

| Étape | De | Vers | Fichier type | Contenu clé | SLA | Règle GO/NO-GO |
|---|---|---|---|---|---|---|
| **1** | DG/AM | D1/D2/D3 | `#BRIEF_ProjectName_Date.md` | Objectifs, contraintes, timeline | 2h ack | G1 (Brief) |
| **2** | D1/D2/D3 | D1/D2/D3 | `PROJECT-CONCEPT-P1-vX.X.[fmt]` | Renders 3D, dimensions | 5j ouvrables | G2 (Concept) |
| **3** | E1 | D1 | `PROJECT-NDC-P2-vX.X.pdf` | Dimensions calculées, safety factors | 3j ouvrables | G3 (NDC) |
| **4** | D1 | E1 (loop) | `PROJECT-CAD-P3-vX.X.[fmt]` | CAO mise à jour | 2j par itération | G4 (CAO) |
| **5** | D1 | E1 | `PROJECT-SIM-P4-vX.X.[fmt]` | Géométrie FEA | 2j ouvrables | G5 (Sim GO) |
| **6** | E1 | D1 + DG | `PROJECT-FEA-P4-vX.X.pdf` | Stress, déformation, safety factor | 5j ouvrables | G6 (Sim Res) |
| **7** | D1+E1 | DG | Gate package | GO/NO-GO decision | SLA gate | G7 (Proto GO) |

### 2.3 Peer Review Matrix

```
┌────────────────────────────────────────────────────────────────┐
│                    PEER REVIEW MATRIX                           │
│            MATRICE DE PEER REVIEW PAR PAIRE                      │
├──────────┬──────────┬──────────┬──────────┬──────────┬─────────┤
│  FROM →  │   D1    │   D2    │   D3    │   E1    │   E2   │
│  TO ↓    │          │          │          │          │         │
├──────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│   D1     │    —     │    ◦     │    ◦     │    ●     │    ◦    │
├──────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│   D2     │    ◦     │    —     │    ◦     │    ●     │    ◦    │
├──────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│   D3     │    ◦     │    ◦     │    —     │    ●     │    ◦    │
├──────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│   E1     │    ●     │    ●     │    ●     │    —     │    ●    │
├──────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│   E2     │    ◦     │    ◦     │    ◦     │    ●     │    —    │
├──────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│   E3     │    ◦     │    ◦     │    ●     │    ●     │    ◦    │
└──────────┴──────────┴──────────┴──────────┴──────────┴─────────┘

● = Peer review OBLIGATOIRE (blocker si non fait)
◦ = Peer review RECOMMANDÉE (pas blocker)
— = Pas de peer review (soit même)

Règle : 
- ● = Review obligatoire (requis pour avancer)
- ◦ = Review recommandée mais pas blocker
- D1 revoit TOUJOURS les assemblies de D2/D3
- Agent Manager revoit TOUS les livrables DG-facing
- E1 revoit TOUS les NDC avant envoi à DG
```

### 2.4 File Naming Convention (standardisée)

```
[PROJECT]-[TYPE]-[PHASE]-[VERSION].[EXT]

PROJECT codes:
  DC  = Drone Civil
  DI  = Drone Industriel  
  DD  = Drone Défense

TYPE codes:
  CONCEPT  = Concept design
  NDC      = Notes de Calcul / Engineering Notes
  CAD      = CAD file
  SIM      = Simulation model
  FEA      = FEA report
  TEST     = Test results
  BRIEF    = Client brief
  REPORT   = Engineering report

PHASE codes:
  P0       = Phase 0 (Initiation)
  P1       = Phase 1 (Concept)
  P2       = Phase 2 (Engineering)
  P3       = Phase 3 (CAD)
  P4       = Phase 4 (Simulation)
  P5       = Phase 5 (Prototype)
  P6       = Phase 6 (Test)
  P7       = Phase 7 (Production)

VERSION:
  v1.0, v1.1, ... v2.3, vFINAL
  _v1.0 = Première version
  _vFINAL = Version finale validée DG

EXEMPLES:
  DC-CONCEPT-P1-v2.1.F3D        (Drone Civil, Concept, Phase 1, v2.1)
  DD-NDC-P2-v1.0.pdf           (Drone Défense, NDC, Phase 2, v1.0)
  DC-CAD-P3-v3.0.SLDPRT        (Drone Civil, CAD, Phase 3, v3.0)
  DD-FEA-P4-v1.2.pdf           (Drone Défense, FEA report, Phase 4, v1.2)
  DC-TEST-P6-vFINAL.pdf       (Drone Civil, Test results, final)
```

### 2.5 Designer↔Engineer Shared Work Table (NOUVEAU V2)

> **This table maps EXACTLY who does what at each phase, so you know where to intervene.**

| Phase | Design Activity (D) | Engineering Activity (E) | Shared Decision | DG Intervention? |
|---|---|---|---|---|
| **P0** | — | — | Project scope, team allocation | **G0 + G10** (DG always) |
| **P1** | D1: Concepts 3D (DC), D2: Industrial concepts (DI), D3: Micro-interceptor (DD) | E1: Constraint analysis | Which concept to proceed with | **G2** (Concept selection) |
| **P2** | D1: Design specs for NDC, D2: Payload specs, D3: Launcher specs | E1: NDC creation, E2: Lift/structural calcs, E3: Propulsion specs | NDC validated? | **G3** (NDC validation) |
| **P3** | D1: CAD revision (DC), D2: Industrial CAD, D3: Launcher CAD | E1: Integration review, E2: Structural check, E3: Prop integration | CAD frozen? | **G4** (CAO validation) |
| **P4** | D1: Geometry prep for FEA, D2: Payload FEA model, D3: Launcher FEA model | E1: FEA execution, E2: CFD/aero analysis, E3: Launch dynamics | FEA results acceptable? | **G5 + G6** (Simulation GO + Results) |
| **P5** | D1: Prototype design review, D2: Ergonomic review, D3: Field test design | E1: Prototype build plan, E2: Test plan, E3: Test bench | Build prototype? | **G7** (Prototype GO) |
| **P6** | D1: Post-test design assessment, D2: Field feedback, D3: Combat assessment | E1: Test execution, E2: Structural validation, E3: Propulsion validation | Test results acceptable? | **G8** (Test Results) |
| **P7** | D1: Production design, D2: Manufacturing specs, D3: Deployment specs | E1: Production engineering, E2: QC specs, E3: Integration QC | Go to production? | **G9** (Production GO) |

---

## 3. WORKFLOW PHASES — Par Ligne de Produit

### 3.1 DRONE CIVIL (Photo, Delivery, Agriculture)

```
PHASE 0: BRIEF CLIENT
───────────────────────────────────────────────────────────────
 QUI      : Commercial Agent + DG
 INPUT    : Brief client / appel d'offre
 OUTPUT   : Client_Requirements_vX.X.docx
 VALIDATION: DG GO obligatoire (G0)
───────────────────────────────────────────────────────────────

PHASE 1: CONCEPT DESIGN
───────────────────────────────────────────────────────────────
 QUI      : D1
 INPUT    : Client requirements
 OUTPUT   : DC-CONCEPT-P1-vX.X.[fmt] (3-5 alternatives)
 DELIVERABLE: Renders 3D, dimensions, materials, manufacturing notes
 SLA      : 5 business days
 VALIDATION: DG GO (G2) — select concept
───────────────────────────────────────────────────────────────

PHASE 2: NDC & CALCULATIONS
───────────────────────────────────────────────────────────────
 QUI      : E1 + E2 (support)
 INPUT    : D1 concept + engineering flags
 OUTPUT   : DC-NDC-P2-vX.X.pdf
 DELIVERABLE: Calculated dimensions, safety factors, material specs
 SLA      : 3 business days
 VALIDATION: DG GO (G3)
───────────────────────────────────────────────────────────────

PHASE 3: CAD REVISION
───────────────────────────────────────────────────────────────
 QUI      : D1 (with E1 feedback)
 INPUT    : NDC from E1
 OUTPUT   : DC-CAD-P3-vX.X.[fmt]
 DELIVERABLE: Updated CAD based on NDC
 ITERATION: Max 3 loops with E1
 SLA      : 2 days per iteration
 VALIDATION: DG GO (G4)
───────────────────────────────────────────────────────────────

PHASE 4: SIMULATION
───────────────────────────────────────────────────────────────
 QUI      : D1 (geometry) → E1 (FEA)
 INPUT    : Clean CAD from D1
 OUTPUT   : DC-SIM-P4-vX.X, DC-FEA-P4-vX.X.pdf
 DELIVERABLE: Stress analysis, deformation, safety factor check
 SLA      : 5 business days
 VALIDATION: DG GO (G5 for simulation start, G6 for results)
───────────────────────────────────────────────────────────────

PHASE 5: PROTOTYPE (si applicable)
───────────────────────────────────────────────────────────────
 QUI      : E1 + E2 + E3
 INPUT    : Validated FEA results
 OUTPUT   : Physical prototype + test plan
 DELIVERABLE: Prototype build, test protocol
 SLA      : Per project
 VALIDATION: DG GO (G7)
───────────────────────────────────────────────────────────────

PHASE 6: TESTING
───────────────────────────────────────────────────────────────
 QUI      : E1 + E2 + E3
 INPUT    : Prototype + test plan
 OUTPUT   : DC-TEST-P6-vX.X.pdf
 DELIVERABLE: Test results, validation data
 SLA      : Per test protocol
 VALIDATION: DG GO (G8)
───────────────────────────────────────────────────────────────

PHASE 7: PRODUCTION
───────────────────────────────────────────────────────────────
 QUI      : D1 + E1 + E2 + E3 + External manufacturers
 INPUT    : Validated test results
 OUTPUT   : Production files + QC specs
 DELIVERABLE: Manufacturing package
 VALIDATION: DG GO (G9)
───────────────────────────────────────────────────────────────
```

### 3.2 DRONE INDUSTRIEL (Inspection, Surveillance)

| Phase | Agent lead | Input | Output | DG Gate |
|---|---|---|---|---|
| **P0** | Commercial + DG | Client brief | Client requirements | G0 |
| **P1** | D2 | Requirements | Industrial concept renders | G2 |
| **P2** | E1 + E3 | D2 concept | NDC + payload specs | G3 |
| **P3** | D2 + E3 | NDC | Industrial CAD + payload integration | G4 |
| **P4** | E1 + E3 | CAD | FEA + computer vision validation | G5/G6 |
| **P5** | E3 | FEA results | Prototype + computer vision test | G7 |
| **P6** | E3 | Prototype | Test results + anomaly detection accuracy | G8 |
| **P7** | D2 + E3 | Test results | Production + deployment package | G9 |

### 3.3 DRONE DÉFENSE (Micro-interceptor)

| Phase | Agent lead | Input | Output | DG Gate |
|---|---|---|---|---|
| **P0** | Commercial + DG + Swiss req | Client brief | Swiss defense requirements | G0 |
| **P1** | D3 | Requirements | Micro-interceptor + launcher concepts | G2 |
| **P2** | E1 + E3 | D3 concept | NDC + propulsion specs + swarm architecture | G3 |
| **P3** | D3 + E3 | NDC | Micro-drone CAD + launcher CAD | G4 |
| **P4** | E1 + E2 + E3 | CAD | FEA + CFD + swarm simulation | G5/G6 |
| **P5** | E3 | FEA results | Prototype launcher + test protocol | G7 |
| **P6** | E1 + E3 | Prototype | Test results + swarm behavior validation | G8 |
| **P7** | D3 + E3 | Test results | Production + field deployment package | G9 |

---

## 4. GO/NO-GO GATES — DG VALIDATION POINTS

### 4.1 Tableau récapitulatif — Tous les GO/NO-GO

| Gate # | EN Name | FR Nom | Phase | Who triggers | Validator & SLA | Auto-action if no response |
|---|---|---|---|---|---|---|
| **G0** | Project Initiation | Lancement Projet | 0 | DG/Commercial | DG (24h) | NO-GO — project cannot start |
| **G1** | Brief Validation | Validation du Brief | Brief | Agent Manager | AM/AC* or DG (24h) | Auto-proceed if no objection |
| **G2** | Concept Selection | Sélection du Concept | 1 | D1/D2/D3 | DG (48h) | Concept frozen at last approved version |
| **G3** | NDC Validation | Validation NDC | 2 | E1 | DG (48h) | NDC frozen at last version |
| **G4** | CAO Validation | Validation CAO | 3 | D1 | DG (48h) | CAO frozen |
| **G5** | Simulation GO | GO Simulation | 4 | E1 | AM/AC* or DG (48h) | Simulation delayed 1 week |
| **G6** | Simulation Results | Résultats Simulation | 4 | E1 | DG (48h) | Results logged as preliminary |
| **G7** | Prototype GO | GO Prototype | 5 | E1+E2+E3 | DG (72h) | Prototype phase skipped (jump to test) |
| **G8** | Test Results Validation | Validation Résultats Tests | 6 | E1 | AM/AC* or DG (48h) | Test results logged as preliminary |
| **G9** | Production GO | GO Production | 7 | DG | DG (72h) | Production on hold |
| **G10** | Commercial Offer | Offre Commerciale | Commercial | Commercial | DG (24h) | Offer at client's risk |
| **G11** | Emergency Response | Réponse Urgence | Emergency | Agent Manager | DG (2h) | Emergency protocol activated |

*\*Note sur la délégation (Seuils de Performance v1.2) :* La validation des Gates G1, G5 et G8 est déléguée par défaut à l'Agent Manager (AM) ou à l'Agent Amélioration Continue (AC) tant que le taux de livraison dans les délais (On-time rate) >= 85% et le taux de complétion des peer reviews >= 80%. Si les KPIs chutent en dessous de ces seuils, l'autorité de validation de ces Gates revient immédiatement et exclusivement au DG.

### 4.2 Format d'information reçu par DG à chaque GO

```
═══════════════════════════════════════════════════════════════
AGENT MANAGER : ___________    GO # : ___/11
PROJECT       : ___________   DATE : _______
═══════════════════════════════════════════════════════════════

📋 RÉSUMÉ EXÉCUTIF (max 10 lignes) :
[Ce que l'équipe a fait, en une phrase]

✅ CE QUI EST BON :
[Liste des points validés, forces du design]

⚠️ CE QUI EST INCERTAIN :
[Liste des risques ouverts, questions en suspens]

🎯 RECOMMANDATION ÉQUIPE :
[Ce que l'équipe recommande et pourquoi]

📊 KPIs À CETTE ÉTAPE :
- Taux livrables dans les délais : ___%
- Peer reviews réalisées : ___/___
- Blocker actifs : ___

📁 FICHIERS JOINTS :
- [Fichier 1] : [chemin]
- [Fichier 2] : [chemin]
- [Fichier 3] : [chemin]

⏱️ DÉLAI DE DÉCISION DG :
- SLA : __h
- Deadline : __/__/__ __h__
- Si pas de réponse → Auto-___

🔗 OU CONTACTER :
- Pour question design → D1 (Slack : @D1)
- Pour question engineering → E1 (Slack : @E1)
- Pour question processus → AC (Slack : @AC)

═══════════════════════════════════════════════════════════════
DG DECISION:  ☐ GO    ☐ NO-GO    ☐ NEED MORE INFO
DG COMMENTS: ___________________________________________________
DG SIGNATURE: ___________________  DATE: _______
═══════════════════════════════════════════════════════════════
```

---

## 5. PROBLEM RESOLUTION PROTOCOL

### 5.1 Comment un problème est détecté

| Méthode | Détection | Qui détecte | Channel |
|---|---|---|---|
| **Daily digest** | Agent Manager identifies blockers | Agent Manager | Daily digest → DG |
| **Agent report** | Agent reports issue to Agent Manager | Individual agent | Slack/Email → AM |
| **Peer review** | Reviewer identifies non-conformance | Peer reviewer | Slack → AM |
| **DG observation** | DG notices something | DG | Direct → AM |
| **AC monitoring** | KPI threshold violation | AC Agent | Alert → DG |
| **External** | Client complaint or market feedback | Commercial/Marketing | Alert → AM |

### 5.2 Chemin de résolution standard

```
Problème détecté
     │
     ▼
[1] Est-ce urgent? (sécurité / blocker critique)
     │
     ├── OUI → [2a] Contacter responsable immédiatement
     │             (≤1h pour sécurité, ≤4h pour blocker)
     │             Contacter Agent Manager en parallèle
     │
     └── NON → [2b] Contacter agent responsable
                   via Slack ou email
                   (SLA: 2-4h pendant heures travail)
     │
     ▼
[3] L'agent responsable peut-il résoudre seul?
     │
     ├── OUI → Résoudre + documenter dans DECISION_LOG
     │         → Informer Agent Manager
     │
     └── NON → [4] Contacter second contact (peer review)
                (SLA: 24h)
     │
     ▼
[5] Still unresolved?
     │
     ├── OUI → [6] Escalade vers Agent Manager
     │           Agent Manager coordonne résolution
     │           (SLA: 48h max)
     │
     └── NON → Résolu → Documenter dans DECISION_LOG
                     → Informer Agent Manager
     │
     ▼
[7] Agent Manager ne peut pas résoudre?
     │
     ├── OUI → [8] Escalade vers DG
     │           Agent Manager prépare package de décision
     │           (SLA: selon gate — 24h à 72h)
     │
     └── NON → Résolu → Documenter dans DECISION_LOG
                     → AC review si approprié
```

### 5.3 Chemins d'escalade par type de problème

#### 🔴 Escalade DESIGN (D1/D2/D3)

```
Problème détecté
      │
      ▼
[1] DG contacte D1 directement (Slack @D1 ou email)
      │
      │         │
      │         ▼
      │    [2] Si D1 a besoin de D2 ou D3
      │         D1 les contacte directement
      │         │
      │         ▼
      │    D1 + D2 (+ E1 si涉及结构)
      │    dans les 48h
      │
      ▼
[3] Si problème persiste après 48h
      │
      ▼
[4] D1 soumet à DG pour validation
      │
      ▼
[5] GO si OK / Redesk si needed
```

#### 🔴 Escalade ENGINEERING (E1/E2/E3)

```
Problème détecté
      │
      ▼
[1] E1 évalue si涉及结构
      │
      │         │
      │         ▼
      │    [2] E1 coordonne avec E2/E3 si nécessaire
      │         │
      │         ▼
      │    E1+E2+E3 dans les 48h
      │
      ▼
[3] E1 produit rapport de résolution
      │
      ▼
[4] Peer review par E2 ou E3
      │
      ▼
[5] E1 soumet à DG pour validation
      │
      ▼
[6] GO si OK / Redesign si needed
```

#### 🔴 Escalade COMMERCIAL (Agent Commercial)

```
Problème détecté
      │
      ▼
[1] DG contacte Agent Commercial
      │
      │         │
      │         ▼
      │    [2] Agent Commercial investigate
      │         │
      │         ▼
      │    [3] Preparation de réponse / solution
      │         │
      │         ▼
      │    [4] DG valide avant envoi
```

### 5.4 Protocole de réunion d'urgence

| Élément | Détail |
|---|---|
| **Durée** | Max 1h |
| **Participants** | DG + agents concernés |
| **Format** | Video call ou présentiel |
| **Output** | Decision + DECISION_LOG update |

### 5.5 DG Intervention Decision Tree (NOUVEAU V2)

```
QUESTION: "Does this situation require DG intervention?"

│
├── "Is it a safety issue?"
│     └── YES → DG MUST ACT IMMEDIATELY (G11, 2h SLA)
│
├── "Is it a commercial decision (new client/offer)?"
│     └── YES → DG MUST ACT (G0 + G10)
│
├── "Is it a GO/NO-GO gate (G1-G9)?"
│     └── YES → DG MUST ACT within gate SLA
│
├── "Is there a blocker that Agent Manager can't resolve?"
│     └── YES → DG MUST ACT within 48h
│
├── "Is it a resource conflict between agents?"
│     └── YES → AC tries first (24h) → DG if unresolved (48h)
│
└── "Is it a design/engineering issue with ≤3 iterations?"
      └── NO → Agents handle internally
      └── YES (>3 iterations) → DG MUST ACT (48h)
```

---

## 6. DAILY / WEEKLY RHYTHM

### 6.1 Daily Digest (format standard)

```
═══════════════════════════════════════════════════════════════
📅 QUOTIDIEN — [DATE] — Drone Interception Project
═══════════════════════════════════════════════════════════════

🎯 PROJETS ACTIFS

   Drone Civil (DC) — Phase [X] (Jour X/Y)
   Avancement : [██████░░░░] ___%
   Blocker : ⚠️ [OUI/NON]
   Prochaine milestone : [GO X] — [Date]
   Agent lead : [D1+E1]
   
   Drone Industriel (DI) — Phase [X] (Jour X/Y)
   Avancement : [████████░░] ___%
   Blocker : ✅ Aucun
   Prochaine milestone : [GO X] — [Date]
   Agent lead : [D2+E3]
   
   Drone Défense (DD) — Phase [X] (Jour X/Y)
   Avancement : [████░░░░░░] ___%
   Blocker : ⚠️ [OUI/NON]
   Prochaine milestone : [GO X] — [Date]
   Agent lead : [D3+E3]

🔴 BLOCKERS ACTIFS
| Blocker | Projet | Impact | Depuis | Action en cours |
|---|---|---|---|---|
| None | — | — | — | — |

⚡ ACTION REQUISE DU DG AUJOURD'HUI
| Action | Gate | SLA | Deadlines |
|---|---|---|---|
| [None] | — | — | — |

📊 KPI SNAPSHOT (cette semaine)
- Taux livrables dans les délais : ___%
- Peer reviews réalisées : ___/___
- Blocker actifs : ___

📁 DERNIERS LIVRABLES
[22.06 09:15] ✅ FEA Report Drone Civil v2.1 — E1
[22.06 08:30] ✅ CAD Assembly Drone Civil v3.0 — D1
[21.06 17:45] ✅ Concept Swarm Defense renders — D3
[21.06 16:00] ✅ Specs Propulsion Micro-drone — E2

⏰ PROCHAINES MILESTONES
[26.06] GO Simulation — Drone Civil
[28.06] GO CAO — Drone Défense
[01.07] Weekly Sync — Tous agents + DG
═══════════════════════════════════════════════════════════════
```

### 6.2 Weekly Sync — Rituel hebdomadaire

| Timing | Quoi | Durée | Participants | Output |
|---|---|---|---|---|
| **Mardi 09:30** | Engineering Sync | 60 min | E1+E2+E3 + AM | WEEKLY_ENGINEERING_YYYYMMDD.md |
| **Jeudi 10:00** | Designer Sync | 60 min | D1+D2+D3 + AM | WEEKLY_DESIGN_YYYYMMDD.md |
| **Vendredi 14:00** | Full Team Sync | 60 min | ALL + DG | WEEKLY_FULLTEAM_YYYYMMDD.md |
| **Vendredi 15:00** | KPI Review | 30 min | AM + AC + DG | KPI report |

#### Format Full Team Sync (Vendredi 14h)

```
ORDRE DU JOUR — FULL TEAM SYNC (60 minutes)
═══════════════════════════════════════════════════════════════
1. [5 min] Rétrospective semaine : qui a fait quoi
2. [10 min] KPI snapshot
3. [15 min] Problèmes ouverts : discussion collective
4. [10 min] Points DG : décisions nécessaires
5. [10 min] Actions & follow-ups
6. [10 min] Célébration des wins
═══════════════════════════════════════════════════════════════
```

### 6.3 Ce qui déclenche une réunion d'urgence

| Trigger | Condition | Timing | Participants |
|---|---|---|---|
| **Safety issue** | Any safety concern | ≤1h | DG + E1 + relevant agents |
| **Critical blocker** | Blocker blocks >2 agents | ≤4h | AM + affected agents |
| **Client escalation** | Client threatening to leave | ≤24h | DG + Commercial + AM |
| **GO/NO-GO emergency** | Gate requires DG decision in <4h | ≤2h | DG + AM |

---

## 7. AI/ML INTEGRATION POINTS WITH DESIGN & ENGINEERING

### 7.1 Vue d'ensemble des modules ML

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AI/ML INTEGRATION MAP                             │
│               CARTE D'INTÉGRATION IA/ML                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🧠 ML-1 : Topology Optimization                                    │
│  Owner: D1 + E1                                                     │
│  Tool: Fusion 360 + Ansys                                           │
│  Phase: P1-P2 (Concept → Engineering)                              │
│  Output: 3-5 design alternatives optimized                          │
│  Validation: E1 FEA on each topology → DG GO                        │
│                                                                     │
│  🧠 ML-2 : Aerodynamics / CFD ROM                                   │
│  Owner: E1 + E2                                                     │
│  Tool: Python + OpenFOAM                                            │
│  Phase: P4 (Simulation)                                             │
│  Output: 100x faster CFD computation (ROM vs full CFD)             │
│  Validation: Comparison vs full CFD and wind tunnel                 │
│                                                                     │
│  🧠 ML-3 : Propulsion Optimization                                  │
│  Owner: E3                                                          │
│  Tool: Python + simulation                                          │
│  Phase: P2-P4 (Engineering → Simulation)                            │
│  Output: Optimized motor + propeller selection                      │
│  Validation: Test bench results                                     │
│                                                                     │
│  🧠 ML-4 : Swarm Behavior Simulation                                │
│  Owner: E1 + D3                                                     │
│  Tool: Isaac Gym (NVIDIA) + PyTorch MARL                           │
│  Phase: P4-P6 (Simulation → Testing)                              │
│  Output: Swarm tactics + coordination algorithms                   │
│  Validation: Flight tests in controlled environment                 │
│                                                                     │
│  🧠 ML-5 : Launch System Optimization                               │
│  Owner: E3 + D3                                                     │
│  Tool: Python + simulation                                          │
│  Phase: P2-P4 (Engineering → Simulation)                           │
│  Output: Optimized launcher pressure + geometry                     │
│  Validation: Launch tests                                           │
│                                                                     │
│  🧠 ML-6 : Payload / Computer Vision                                │
│  Owner: D2 + E3                                                     │
│  Tool: PyTorch CNN / Vision Transformer                             │
│  Phase: P2-P6 (Engineering → Testing)                             │
│  Output: Anomaly detection + localization for inspection drones     │
│  Validation: Real-world inspection tests                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 Tableau récapitulatif AI/ML

| Module | EN | FR | Owner | Phase | Tool | Output |
|---|---|---|---|---|---|---|
| **ML-1** | Topology Optimization | Optimisation Topologique | D1 + E1 | P1-P2 | Fusion 360 + Ansys | 3-5 design alternatives |
| **ML-2** | CFD Reduced-Order Model | Modèle Réduit CFD | E1 + E2 | P4 | Python + OpenFOAM | Fast aerodynamics |
| **ML-3** | Propulsion Optimization | Optimisation Propulsion | E3 | P2-P4 | Python | Motor + propeller |
| **ML-4** | Swarm Simulation | Simulation Essaim | E1 + D3 | P4-P6 | Isaac Gym + PyTorch | Swarm tactics |
| **ML-5** | Launch Optimization | Optimisation Lancement | E3 + D3 | P2-P4 | Python | Launcher params |
| **ML-6** | Computer Vision | Vision par Ordinateur | D2 + E3 | P2-P6 | PyTorch | Anomaly detection |

---

## 8. KPI DASHBOARD + FINE-TUNING LEVERS (NOUVEAU V2)

### 8.1 KPI Dashboard — Full View

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    KPI DASHBOARD — Drone Interception                      │
│                    Version: 22/06/2026                                     │
├───────────────┬──────────┬─────────┬─────────┬─────────┬────────────────────┤
│ KPI           │ Current  │ Target  │Warning  │ Alert   │ Trend             │
├───────────────┼──────────┼─────────┼─────────┼─────────┼────────────────────┤
│ On-time rate  │   85%    │  >90%   │  <85%   │  <70%   │ ↗️ +5% this week │
│ Peer reviews  │   80%    │  >80%   │  <70%   │  <60%   │ → Stable          │
│ FEA 1st pass  │   65%    │  >60%   │  <50%   │  <40%   │ ↗️ +10% vs last  │
│ Active blkrs  │    1     │    0    │   >1    │   >3    │ ↘️ -2 resolved    │
│ Phase delay   │  +3 days │ ±5 days │  +1 wk  │  +2 wk  │ → On track        │
│ Agent util.   │   72%    │ 60-80%  │ <50%/>90%│ <40%/>95%│ → Optimal range  │
│ Cross-team    │   75%    │  >70%   │  <60%   │  <50%   │ ↗️ +8%            │
│ Cost vs bud.  │   +3%    │   ±5%   │  ±10%   │  ±20%   │ → Within target   │
│ Client sat.   │   8.5/10 │  >8/10  │  <7/10  │  <5/10  │ ↗️ +0.5 vs last  │
│ Sim accuracy  │   92%    │  >95%   │  <90%   │  <85%   │ → Good correlation│
└───────────────┴──────────┴─────────┴─────────┴─────────┴────────────────────┘

LEGEND:
🟢 Green  = On target
🟡 Yellow = Warning (action recommended)
🔴 Red    = Alert (immediate action required)
↗️ = Improving
↘️ = Declining
→ = Stable
```

### 8.2 Fine-Tuning Levers — Threshold Adjustment Matrix (NOUVEAU V2)

| KPI | Alert Threshold | Warning Threshold | Target | Who Can Adjust | DG Approval Required | Adjustment Impact |
|---|---|---|---|---|---|---|
| **On-time delivery rate** | <70% | <85% | >90% | Agent Manager | Yes (>5% change) | Reallocates work, may extend deadlines |
| **Peer review completion** | <60% | <70% | >80% | AC | Yes | Adjusts quality check frequency |
| **FEA first-pass success** | <40% | <50% | >60% | E1 | Yes | May need more design iterations |
| **Active blockers** | >3 | >1 | 0 | Agent Manager | No (within 48h) | Escalates or resolves blockers |
| **Phase delay** | +2 weeks | +1 week | ±5 days | DG | Yes | Adjusts project timeline or scope |
| **Agent utilization** | <40% or >95% | <50% or >90% | 60-80% | Agent Manager + DG | Yes | Redistributes tasks or hires |
| **Cross-team collaboration** | <50% | <60% | >70% | AC | Yes | Adjusts sync frequency, adds facilitation |
| **Cost vs budget** | >±20% | >±10% | >±5% | DG | Yes | Reduces scope or finds savings |
| **Client satisfaction** | <5/10 | <7/10 | >8/10 | Commercial + DG | Yes | Improves service, communication |
| **Simulation accuracy** | <85% | <90% | >95% | E1 + E2 | Yes | May need more test data for calibration |

### 8.3 Fine-Tuning Process

```
STEP 1: THRESHOLD EXCEEDED
────────────────────────────────────────────────────────────
  Who: KPI monitoring (AC or Agent Manager)
  Action: Push alert to responsible agent + DG
  
  Alert format:
  ┌─────────────────────────────────────────┐
  │ ⚠️ KPI ALERT                            │
  │ KPI: [Name]                             │
  │ Current: [Value]                        │
  │ Threshold: [Alert/Warning]               │
  │ Impact: [What's at risk]                │
  │ Recommended action: [What to do]        │
  └─────────────────────────────────────────┘

STEP 2: DIAGNOSIS (24h)
────────────────────────────────────────────────────────────
  Who: Responsible agent
  Action: Identify root cause of threshold breach
  
  Questions:
  - Is this a one-time anomaly or a trend?
  - Who/what is affected?
  - What are the options to bring back to target?

STEP 3: PROPOSE ADJUSTMENT (48h)
────────────────────────────────────────────────────────────
  Who: Responsible agent
  Action: Propose adjustment to AC or Agent Manager
  
  Format:
  ┌─────────────────────────────────────────┐
  │ ADJUSTMENT PROPOSAL                     │
  │ KPI: [Name]                            │
  │ Proposed change: [New threshold]       │
  │ Justification: [Why this helps]        │
  │ Impact on other KPIs: [Cross-effects]  │
  │ Duration: [How long until review]     │
  └─────────────────────────────────────────┘

STEP 4: APPROVAL (per approval matrix)
────────────────────────────────────────────────────────────
  If Agent Manager can adjust:
  → Agent Manager approves, notifies DG
  
  If DG approval required:
  → Agent Manager routes to DG
  → DG decides within SLA (24-48h)
  → Agent Manager implements + announces

STEP 5: MONITOR (2 weeks)
────────────────────────────────────────────────────────────
  Who: AC
  Action: Monitor adjusted KPI for 2 weeks
  Output: Effectiveness report to DG
```

---

## 9. AGENT INTERACTION MAP (NOUVEAU V2)

### 9.1 Mermaid Diagram

```
graph TD
    DG["DG<br/>(Direction Générale)"]
    AM["Agent Manager<br/>(Orchestrateur IA)"]
    AC["AC<br/>(Amélioration Continue)"]
    
    D1["D1<br/>(Lead Design Mécanique)"]
    D2["D2<br/>(Design Industriel)"]
    D3["D3<br/>(Design Défense)"]
    
    E1["E1<br/>(Systèmes & Embarqué)"]
    E2["E2<br/>(Propulsion & Structures)"]
    E3["E3<br/>(Électronique & Intégration)"]
    
    COMM["Commercial"]
    MKT["Marketing"]
    
    AM --> DG
    AC --> DG
    AC --> AM
    
    D1 -->|7-step handoff| E1
    D2 -->|Peer review| D1
    D3 -->|Peer review| D1
    
    E1 -->|NDC, FEA| D1
    E1 -->|Peer review| E2
    E1 -->|Peer review| E3
    
    E2 -->|Propulsion specs| E3
    E3 -->|Integration| D3
    
    COMM -->|Client briefs| DG
    MKT -->|Market insights| DG
    
    D1 -->|Status reports| AM
    E1 -->|Status reports| AM
    COMM -->|Market data| AM
    MKT -->|Campaign data| AM
    
    D2 -->|Visual identity| MKT
    D3 -->|Swiss defense| COMM
    D3 -->|Launcher design| E3
    
    subgraph "DESIGN TEAM / ÉQUIPE DESIGN"
        D1
        D2
        D3
    end
    
    subgraph "ENGINEERING TEAM / ÉQUIPE INGÉNIERIE"
        E1
        E2
        E3
    end
    
    subgraph "SUPPORT / SUPPORT"
        COMM
        MKT
        AC
    end
    
    DG -.->|"GO/NO-GO gates<br/>All 11 gates"| AM
    AM -.->|"Daily digest<br/>Weekly sync"| D1
    AM -.->|"Daily digest<br/>Weekly sync"| E1
    
    style DG fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style AM fill:#51cf66,stroke:#2b8a3e,color:#fff
    style AC fill:#94d82d,stroke:#5c940d,color:#000
    style D1 fill:#74c0fc,stroke:#1c7ed6,color:#000
    style D2 fill:#a9d4ff,stroke:#1c7ed6,color:#000
    style D3 fill:#63e6be,stroke:#0ca678,color:#000
    style E1 fill:#ffc078,stroke:#e8590c,color:#000
    style E2 fill:#ffd43b,stroke:#f08c00,color:#000
    style E3 fill:#ff922b,stroke:#e8590c,color:#000
    style COMM fill:#e599f7,stroke:#be4bdb,color:#000
    style MKT fill:#f783ac,stroke:#c2255c,color:#000
```

### 9.2 Interaction Frequency Matrix

| FROM ↓ / TO → | DG | AM | AC | D1 | D2 | D3 | E1 | E2 | E3 | COMM | MKT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **DG** | — | Daily | Weekly | Per gate | Per gate | Per gate | Per gate | Rare | Per gate | Per project | Rare |
| **AM** | Daily | — | Daily | Daily | Weekly | Weekly | Daily | Weekly | Daily | Per project | Weekly |
| **AC** | Weekly | Daily | — | Rare | Rare | Rare | Rare | Rare | Rare | Rare | Rare |
| **D1** | Per gate | Daily | Rare | — | Weekly | Weekly | Per handoff | Rare | Rare | Rare | Rare |
| **D2** | Rare | Weekly | Rare | Weekly | — | Rare | Rare | Rare | Rare | Rare | Weekly |
| **D3** | Per gate | Weekly | Rare | Weekly | Rare | — | Rare | Rare | Per handoff | Per project | Weekly |
| **E1** | Per gate | Daily | Rare | Per handoff | Rare | Rare | — | Weekly | Daily | Rare | Rare |
| **E2** | Rare | Weekly | Rare | Rare | Rare | Rare | Weekly | — | Weekly | Rare | Rare |
| **E3** | Per gate | Daily | Rare | Rare | Rare | Per handoff | Daily | Weekly | — | Rare | Rare |
| **COMM** | Per project | Per project | Rare | Rare | Rare | Per project | Rare | Rare | Rare | — | Weekly |
| **MKT** | Rare | Weekly | Rare | Rare | Weekly | Weekly | Rare | Rare | Rare | Weekly | — |

**Legend:**
- Daily = Every workday
- Weekly = Once per week minimum
- Per handoff = Every design-engineering handoff (Steps 1-7)
- Per gate = When a GO/NO-GO gate is triggered
- Per project = At project start, milestones, and end
- Rare = Only when specific need arises

---

## ANNEXE — Contact rapide

| Agent | Nom | Channel | Pour |
|---|---|---|---|
| **DG** | Direction Générale | Signal / Email: dg@project.internal | Toutes décisions stratégiques |
| **D1** | Lead Design Mécanique | Slack: @D1 | Design civil, CAO, concept, peer review |
| **D2** | Design Industriel | Slack: @D2 | Design industriel, esthétique, ergonomie |
| **D3** | Design Défense | Slack: @D3 | Design défense, micro-interceptor, lanceur |
| **E1** | Systèmes & Embarqué | Slack: @E1 | NDC, FEA, CFD, architecture, embedded |
| **E2** | Propulsion & Structures | Slack: @E2 | Propulsion, calculs portance, structure |
| **E3** | Électronique & Intégration | Slack: @E3 | Électronique, intégration, PCB, lanceur |
| **Commercial** | Agent Commercial | Slack: @Commercial | Clients, proposals, quotes |
| **Marketing** | Agent Marketing | Slack: @Marketing | Content, positioning, Swiss defense |
| **AC** | Amélioration Continue | Slack: @AC | Processus, règles, qualité, KPIs |
| **Agent Manager** | Orchestrateur IA | Slack: @AgentManager | Coordination, routage, GO/NO-GO |

---

*End of OPERATIONS_WORKFLOW.md v2.0 — Updated 22/06/2026 — Validated by DG*
