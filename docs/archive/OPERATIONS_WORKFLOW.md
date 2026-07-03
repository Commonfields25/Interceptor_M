---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# OPERATIONS_WORKFLOW.md — Cadre Opérationnel AIML UAV Startup
**Version :** 1.0 | **Date :** 22.06.2026 | **Classification :** INTERNE CONFIDENTIEL
**Rédigé par :** Agent Manager | **Validé par :** DG

---

## Table des matières

1. [TEAM ROLES — Fiches Agents Complètes](#1-team-roles--fiches-agents-complètes)
2. [COLLABORATION MAP — Designers ↔ Engineers](#2-collaboration-map--designers--engineers)
3. [WORKFLOW PHASES — Par Ligne de Produit](#3-workflow-phases--par-ligne-de-produit)
4. [WHERE THE DG MUST INTERVIDE — Points de Décision Critiques](#4-where-the-dg-must-intervene--points-de-décision-critiques)
5. [PROBLEM RESOLUTION PROTOCOL](#5-problem-resolution-protocol)
6. [DAILY / WEEKLY RHYTHM](#6-daily--weekly-rhythm)
7. [AIML INTEGRATION POINTS](#7-aiml-integration-points-with-design--engineering)

---

## 1. TEAM ROLES — Fiches Agents Complètes

> **Règle universelle** : Chaque agent produit un livrable nommé selon la convention `PRODUIT_SECTION_CODE_DATE_vX.X` (ex: `CIVIL_A320_Concept_D1_220626_v1.0.SLDPRT`). Tous les livrables sont stockés dans `/workspace/deliverables/` avec sous-dossiers par ligne de produit.

---

### 🔧 AGENT INGÉNIEUR E1 — Responsable Mécanique Structures

#### Description du rôle
E1 est l'expert en **mécanique des structures**, en **CAE (Computer-Aided Engineering)** et en **simulation mécanique** (statique, fatigue, vibration). Il Dimensionne chaque composant structural du drone (bras, fuselage, supports moteur, tray) et garantit que les designs survive aux charges de vol et aux contraintes environnementales. Il est le premier interlocuteur technique lors de la traduction CAO → modèle physique.

#### Outils principaux
| Outil | Usage | Licence |
|---|---|---|
| SolidWorks Simulation / Simulation Premium | Analyse éléments finis (FEA) | D1 partage le siège SolidWorks |
| Fusion 360 Simulation workspace | Validation secondaire / collaboration | Sousscription Fusion 360 |
| ANSYS Mechanical (si disponible) | FEA avancée, non-linéaire | Lab interne |
| Python + NumPy/SciPy | post-processing données de simulation | Libre |
| MLflow | versioning des résultats de simulation | DVC/MLflow pipeline |
| Excel / Google Sheets | Tableaux de dimensionnement | Libre |

#### Ce qu'il produit
- **Notes de calcul** (NDC) signées par élément structurel
- **Rapports FEA** : contrainte Von Mises, facteur de sécurité, déformation, modes propres (fréquence propre)
- **Modèles CAO simplifiés** pour simulation (clean geometry, volume mesh-ready)
- **BOM validée** (Bill of Materials) — masses, matériaux, fournisseurs
- **Fichiers de validation géométrique** (STEP / IGES export check)
- **Topologie optimisation outputs** (via integration AIML, cf. Section 7)

#### Avec qui il travaille
| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| D1 | Reçoit le concept 3D, renvoie le dimensionnement structural | Quotidienne |
| D2 | Valide les conmemations et interference checks | Hebdomadaire |
| D3 | Coordination sur le design système d'emport (payload) | Sur besoin |
| E2 | Transmission des charges pour dimensionnement moteur | Quotidienne |
| E3 | Transmission des contraintes thermiques et vibration pour fatigue | Hebdomadaire |
| Agent Manager | Rapports KPI, escalade technique | Quotidienne |

#### KPIs
| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Taux de NDC livrées dans les délais | ≥ 90% | Hebdomadaire | < 80% → escalade |
| Nombre d'itérations de redesign | ≤ 3 par composant | Par projet | > 5 → revue |
| Temps moyen de simulation par composant | ≤ 4h | Mensuelle | > 6h → optimisation |
| Taux de validation FEA au premier passage | ≥ 85% | Par livrable | < 70% → peer review |
| Fichiers CAO transmis à E2 dans les 24h | ≥ 95% | Quotidienne | < 90% → Agent Manager |

---

### 🔧 AGENT INGÉNIEUR E2 — Responsable Propulsion
#### Description du rôle
E2 est l'expert en **propulsion drone** — moteurs brushless, ESC, hélices, batteries et gestion thermique de la chaîne de propulsion. Il Dimensionne la motorisation pour chaque configuration de vol (poids total, autonomie requise, plafond de vol) et produit les spécifications techniques de chaque composant buy-or-build. Il est responsable de la sélection fournisseurs et de l'intégration propulsion-structure.

#### Outils principaux
| Outil | Usage | Licence |
|---|---|---|
| SolidWorks (partagé) | Modélisation composants propulsion | D1 partage |
| Excel / Google Sheets | Tableaux de sélection moteur, courbe thrust/poids | Libre |
| Python (matplotlib, pandas) | Modélisation performance, analyse données vol | Libre |
| eCalc ou Motor Calculator | Pré-dimensionnement rapide moteur/hélice | Version gratuite |
| LMS Amesim ou Simscape (option) | Simulation système de propulsion | Lab interne |
| TensorRT (inférence) | Modèles de prédiction performance | NVIDIA |
| Isaac Gym (RL propulsion) | Optimisation politique de contrôle moteur | NVIDIA |

#### Ce qu'il produit
- **Dossiers de sélection propulsion** : moteur + ESC + hélice + batterie validés
- **Courbes de performance** : thrust vs RPM, puissance absorbée vs thrust, autonomie vs charge utile
- **BOM propulsion** détaillée avec références fournisseurs et prix unitaires
- **Fichiers de configuration ESC** (params Betaflight/iNav)
- **Spécifications batteries** : C-rate, capacité, tension, connectique, BMS
- **Rapports de test moteur** (si prototype disponible)

#### Avec qui il travaille
| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| D1 | Reçoit spécifications contraintes structurelles et Emport | Quotidienne |
| E1 | Transmet charges et masses pour calcul thrust needed | Quotidienne |
| E3 | Intégration thermique moteur/batterie | Hebdomadaire |
| D2 | Design système de refroidissement moteur | Sur besoin |
| Agent Manager | Pipeline européen, specs armasuisse | Hebdomadaire |

#### KPIs
| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Temps de sélection propulsion par configuration | ≤ 2 jours | Par projet | > 3 jours → escalade |
| Taux de specs propulsion validées au premier passage | ≥ 90% | Par livrable | < 80% → peer review |
| Nombre de fournisseurs identifiés par composant | ≥ 2 | Par composant | 0 → blocker |
| Fichiers ESC transmis à D1 dans les 48h | ≥ 95% | Par livrable | < 90% → Agent Manager |
| Précision prédiction autonomie (réel vs calculé) | ±10% | Tests vol | > 20% → recalibration |

---

### 🔧 AGENT INGÉNIEUR E3 — Responsable Électronique & Firmware

#### Description du rôle
E3 est l'expert en **électronique embarquée**, en **firmware** et en **intégration système**. Il Dimensionne et conçoit (ou spécifie) toute l'électronique du drone : contrôleurs de vol (FC), capteurs, distribution power, LEDs, buzzers, radio links. Il écrit et maintient le firmware des contrôleurs de vol (Betaflight, INAV ou custom) et garantit l'intégration électrique de tous les sous-systèmes. Il est le garant de la compatibilité électromagnétique et de la fiablité électrique.

#### Outils principaux
| Outil | Usage | Licence |
|---|---|---|
| KiCad | Schémas électroniques et PCB design | Libre |
| SolidWorks Electrical 3D | Routing câbles dans CAO | Si disponible |
| Arduino IDE / PlatformIO | Prototypage firmware | Libre |
| Betaflight / INAV Configurator | Configuration firmware drone | Libre |
| Python (pymavlink, DroneKit) | Scripts de test et analyse logs vol | Libre |
| DVC | Versioning firmware et datasets de vol | Libre |
| PyTorch | Modèles de prédiction défaillance composants | Libre |
| TensorRT | Déploiement modèles inference embarqué | NVIDIA |

#### Ce qu'il produit
- **Schémas électroniques** : FC, Power Distribution, capteurs
- **Routage PCB** (si développement interne)
- **Firmware Betaflight/INAV configuré** : PID, rates, OSD, modes de vol, failsafes
- **Spécifications câbles et connectique**
- **Protocoles de test électronique** : checklists pré-vol, tests EMI
- **Logs de vol analysés** : extraction de données de performance
- **Modèles de maintenance prédictive** : prédiction défaillance ESC/moteur (cf. Section 7)

#### Avec qui il travaille
| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| D2 | Design enclosure électronique (caisson IP67) | Quotidienne |
| D3 | Intégration payload électronique (caméra, capteurs) | Sur besoin |
| E1 | Contraintes de masse et размещения pour electronics bays | Hebdomadaire |
| E2 | Interface power entre batterie, ESC, FC | Quotidienne |
| Agent Manager | Rapports intégration, risques blockers | Hebdomadaire |

#### KPIs
| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Firmware validé avant vol inaugural | 100% | Par projet | fail → no flight |
| Temps de résolution bug firmware | ≤ 48h | Par incident | > 72h → escalade |
| Taux de composants électroniques sourcés | ≥ 95% | Hebdomadaire | < 90% → blocker |
| Logs de vol analysés dans les 24h | ≥ 90% | Par vol | > 48h → Agent Manager |
| Score prédiction défaillance (accuracy) | ≥ 80% | Mensuelle | < 75% → retraining |

---

### 🎨 AGENT DESIGNER D1 — Lead Mechanical Design

#### Description du rôle
D1 est le **Lead Mechanical Designer**. Il est responsable de l'architecture 3D complète du drone et de la coordination CAO multi-produit. Il Traduit les briefs clients et les contraintes engineering en géométries 3D CAD détaillées, performantes et manufacturing-ready. Il Est le gardien de la cohérence CAO à travers toutes les lignes de produit et le principal interlocuteur CAO des ingénieurs.

#### Outils principaux
| Outil | Usage | Licence |
|---|---|---|
| SolidWorks Premium 3DExperience | Design CAO principal, Assembly, Drawings | Siège principal |
| Fusion 360 | Collaboration, design secondaire | Sousscription |
| Autodesk Inventor | Interopérabilité clients, validation IGES STEP | Si disponible |
| 3DExperience (on-cloud) | Sharing et review avec équipe | Si actif |
| Python + Swig | Automation CAO (scripting de répétitions) | Libre |
| PyTorch (topology optimization) | ML-driven design exploration | Libre |

#### Ce qu'il produit
- **Assemblies complets** de chaque drone (root assembly + sub-assemblies)
- **Parts detailées** : bras, fuselage, tray, supports, hardware
- **Drawings** (plan 2D pour fabrication) : vues, côtes, tolérances
- **BOM structurée** : every part, qty, material, supplier, cost
- **STLs pour impression 3D** : prototypes et outillages
- **Exploded views** pour documentation technique et marketing
- **Design studies** : comparaisons géométriques (design alternatives)

#### Avec qui il travaille
| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| E1 | Transmission CAO pour FEA, réception notes de calcul | Quotidienne |
| E2 | Intégration composants propulsion dans CAO | Quotidienne |
| E3 | Coordination enclosure électronique | Quotidienne |
| D2 | Peer review design, partage d'approches | Quotidienne |
| D3 | Revue design payload et intégration caméra | Hebdomadaire |
| Agent Manager | Reporting KPI, blockers design | Quotidienne |

#### KPIs
| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Assemblies complets livrés dans les délais | ≥ 90% | Par phase projet | < 80% → escalade |
| Fichiers CAO transmis à E1 dans les 24h | ≥ 95% | Par livrable | < 90% → peer review |
| Peer reviews réalisées par D2 | ≥ 1/semaine | Hebdomadaire | 0 → manquement |
| Iterations de redesign CAO | ≤ 3 par composant | Par projet | > 5 → revue design |
| Temps de compilation BOM finale | ≤ 4h | Par projet | > 6h → optimisation |

---

### 🎨 AGENT DESIGNER D2 — Systems Design & Payload Integration

#### Description du rôle
D2 est le **Systems Designer**. Il est responsable de l'intégration des subsystems dans le design global (électronique, propulsion, payload) et de la gestion des interfaces mécaniques. Il Est l'expert en conception de systèmes d'emport (payloads) pour les drones industriels et civils et le garant de la modularité du design.

#### Outils principaux
| Outil | Usage | Licence |
|---|---|---|
| SolidWorks (partagé avec D1) | Design subsystems, payload integration | D1 partage |
| Fusion 360 | Collaboration, design alternatif | Sousscription |
| Python (numpy, scipy) | Calculs d'interface, études d'intégration | Libre |
| SolidWorks Tolerance Analysis (si dispo) | Analyse de tolérances | Lab interne |

#### Ce qu'il produit
- **Design des subsystems** : electronics bays, payload mounts, cooling channels
- **Interface control drawings** : documents d'interface entre sous-systèmes
- **Design modulaire** : standardized payload rails, quick-release mechanisms
- **Design de système de refroidissement** actif et passif
- **Études d'emport** : centrage de gravité, inertie, stabilité au vol
- **Design waterproofing** : joints, presses, systèmes IP67 (inspection drones)

#### Avec qui il travaille
| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| E1 | Validation structural payload integration | Quotidienne |
| E2 | Interface refroidissement moteur | Hebdomadaire |
| E3 | Design enclosure électronique (co-design) | Quotidienne |
| D1 | Peer review, cohérence architecturale | Quotidienne |
| D3 | Design payload spécialisé (inspection, agriculture) | Sur besoin |
| Agent Manager | Rapports intégration, planning | Hebdomadaire |

#### KPIs
| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Interface control documents livrés | ≥ 90% | Par projet | < 80% → escalade |
| Designs d'emport validés (CG within spec) | 100% | Par configuration | fail → redesign |
| Temps de résolution problème d'interface | ≤ 2 jours | Par problème | > 3 jours → escalade |
| Designs modulaires réutilisés | ≥ 3 projets | Trimestrielle | < 2 → revue modularité |
| Peer reviews D1 ← D2 | ≥ 1/semaine | Hebdomadaire | 0 → manquement |

---

### 🎨 AGENT DESIGNER D3 — Defense & Concept Design Specialist

#### Description du rôle
D3 est le **spécialiste Concept & Défense**. Il Est le gardien du concept défense (intercepteurs essaim, lanceurs air comprimé) et le lead designer de toutes les nouvelles architectures conceptuelles. Il Produit les concepts avancés, les designs déposés (patentable) et les proposals techniques pour armasuisse et les appels d'offres défense. Il Est le lien design avec le pipeline commercial défense.

#### Outils principaux
| Outil | Usage | Licence |
|---|---|---|
| SolidWorks (partagé) | Concept design, early-stage 3D | D1 partage |
| Fusion 360 | Rapid concepting, design sketching 3D | Sousscription |
| Autodesk sketchbook | Conceptual sketching, storyboarding | Optionnel |
| Python (matplotlib, PIL) | Visualisation, rendu rapide de concepts | Libre |
| Blender (si disponible) | Rendu visuel conceptuel, animation | Libre |
| PyTorch / Isaac Gym | ML-driven topology optimization défensive | NVIDIA |

#### Ce qu'il produit
- **Concepts avancés** : early-stage 3D, sketches, designs déposables
- **Proposals défense** : réponses techniques aux appels d'offres armasuisse
- **Design essaim micro-drones** : architecture lanceur, cellule drone miniaturisée
- **Design lanceur air comprimé** : système de lancement, tubes, station de contrôle
- **Renderings et visualisations** pour pitch deck et présentations commerciales
- **Design patents** : documentation technique pour dépôt
- **Dossiers de faisabilité** : études de concept rapide (feasibility studies)

#### Avec qui il travaille
| Agent | Nature de la collaboration | Fréquence |
|---|---|---|
| E1 | Dimensionnement structurel lanceur | Quotidienne |
| E2 | Spécifications propulsion micro-drones | Sur besoin |
| E3 | Électronique miniaturisée pour intercepteurs | Sur besoin |
| D1 | Peer review, cohérence avec designs existants | Quotidienne |
| Agent Manager | Pipeline défense armasuisse, planning stratégique | Hebdomadaire |
| Commercial Agent | Préparation offers commerciales défense | Sur besoin |

#### KPIs
| KPI | Cible | Fréquence mesure | Seuil alerte |
|---|---|---|---|
| Concepts livrés dans les délais proposal | ≥ 90% | Par appel d'offre | < 80% → DG alert |
| Renders visuels livrés pour pitch deck | ≥ 1/semaine | Hebdomadaire | missed → DG alert |
| Concepts défense validés DG avant soumission | 100% | Par soumission | fail → no submission |
| Designs dépofts nouveaux par trimestre | ≥ 1 | Trimestrielle | 0 → revue stratégique |
| Temps moyen concept → proposal | ≤ 5 jours | Par proposal | > 7 jours → escalade |

---

## 2. COLLABORATION MAP — Designers ↔ Engineers

### 2.1 Vue d'ensemble des handoffs

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          COLLABORATION MAP — D ↔ E                          │
│                      Flux principal : Brief → CAO → Sim → Proto             │
└─────────────────────────────────────────────────────────────────────────────┘

  BRIEF                          CONCEPT                     CAO DÉTAILLÉ
  CLIENT                        EXPLORATION                   (E1→D1)
    │                              │                            │
    ▼                              ▼                            ▼
 ┌──────┐  ┌────────────────────────────────────────────────────────────┐
 │  DG  │  │         PHASE 1 : CONCEPT SHARING (D1+D2+D3 ↔ E1+E2+E3)     │
 └──────┘  └────────────────────────────────────────────────────────────┘
                                     │
                                     │ D1 produit : Concept 3D raw
                                     │ D2 produit : Interface studies
                                     │ D3 produit : Concept défense
                                     ▼
                       ┌─────────────────────────────────┐
                       │  HANDLE N°1 : BRIEF CONCEPT      │
                       │  De : D1/D2/D3  →  Vers : E1/E2   │
                       │  Fichier : BRIEF_vX.X.pdf        │
                       │  Contenu : Design brief + goals  │
                       └─────────────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
             ┌──────────┐    ┌───────────┐   ┌───────────┐
             │    E1    │    │    E2     │   │    E3     │
             │Structures│    │Propulsion │   │ Électroniq│
             └────┬─────┘    └─────┬─────┘   └─────┬─────┘
                  │                │               │
                  │                │               │
                  │                │               │
                  ▼                ▼               ▼
          ┌────────────┐  ┌─────────────┐  ┌─────────────┐
          │ NDC + FEA  │  │  Specs      │  │  Schémas    │
          │ Reports    │  │  Propulsion │  │  Électroniq │
          └─────┬──────┘  └──────┬──────┘  └──────┬──────┘
                │               │               │
                └───────────┬───┘───────────────┘
                            ▼
               ┌───────────────────────────┐
               │  HANDLE N°2 : VALIDATION │
               │  De : E1+E2+E3 → Vers : D1│
               │  Fichier : NDC_VALIDATED  │
               │  Contenu : Notes calculées│
               └─────────────┬─────────────┘
                             │
                             ▼
            ┌────────────────────────────────┐
            │  HANDLE N°3 : CAO REVISED       │
            │  De : D1  →  Vers : E1 (loop)   │
            │  Fichier : CAD_vX.X.SLDPRT     │
            │  Contenu : CAO mis à jour E1   │
            └────────────┬───────────────────┘
                         │
                         ▼
            ┌────────────────────────────────┐
            │  HANDLE N°4 : SIMULATION       │
            │  De : D1  →  Vers : E1 (FEA)    │
            │  Fichier : SIM_MODEL.SLDPRT    │
            │  Contenu : Géométrie nettoyée   │
            └────────────┬───────────────────┘
                         │
                         ▼
            ┌────────────────────────────────┐
            │  HANDLE N°5 : SIM RESULTS      │
            │  De : E1  →  Vers : D1 + DG     │
            │  Fichier : FEA_REPORT.pdf      │
            │  Contenu : Résultats FEA validés│
            └────────────┬───────────────────┘
                         │
                         ▼
         ┌─────────────────────────────────────────┐
         │  HANDLE N°6 : FINAL CAD RELEASE         │
         │  De : D1  →  Vers : E1+E2+E3 + DG        │
         │  Fichier : CAD_RELEASE_vX.X.SLDDRW      │
         │  Contenu : CAO final + BOM validée       │
         └─────────────┬───────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────────────────────┐
         │  HANDLE N°7 : PROTOTYPE PACKAGE          │
         │  De : D1+E1+E2+E3 → Vers : Proto Team    │
         │  Contenu : Files + BOM + Instructions    │
         └─────────────────────────────────────────┘
```

### 2.2 Handoff Details — Fichier par fichier

| Handoff | De | Vers | Fichier | Contenu | Délai max | Review requis |
|---|---|---|---|---|---|---|
| H1 | D1/D2/D3 | E1/E2/E3 | BRIEF_CONCEPT_vX.X.pdf | Brief design + contraintes | Jour 1 | Agent Manager |
| H2 | E1 | D1 | NDC_STRUCT_vX.X.xlsx | Notes de calcul | Jour 3 | Peer E2 check |
| H2b | E2 | D1 | SPECS_PROPULSION_vX.X.xlsx | Specs moteur/hélice | Jour 3 | E1 sign-off |
| H2c | E3 | D2 | SCHEMATIC_ELEC_vX.X.pdf | Schémas électroniques | Jour 3 | D2 sign-off |
| H3 | D1 | E1 | CAD_REVISED_vX.X.SLDPRT | CAO intégrant NDC | Jour 5 | E1 approval |
| H4 | D1 | E1 | SIM_GEOMETRY_vX.X.SLDPRT | Géométrie nettoyée pour FEA | Jour 5 | E1 QC check |
| H5 | E1 | D1 + DG | FEA_REPORT_vX.X.pdf | Résultats FEA validés | Jour 8 | DG review |
| H6 | D1 | ALL + DG | CAD_RELEASE_vX.X | CAO final + BOM | Jour 10 | DG GO required |
| H7 | ALL | Proto | PROTOTYPE_PKG_vX.X.zip | Package complet fabrication | Jour 10 | Agent Manager |

### 2.3 Peer Review Matrix

> **Règle** : Tout livrable entre agents passe par au moins 1 peer review avant transmission au suivant dans la chaîne.

```
  Légende : ★ = Peer Review obligatoire   ◦ = Peer Review recommandé   — = Pas de relation directe

               REVIEWER →                                                             
               D1    D2    D3    E1    E2    E3    Agent Mgr   DG
  AUTHOR ↓                                                         
  D1     [—]   ★     ★     ★     ★     ◦      ★        ★
  D2     ★    [—]    ◦     ★     ★     ★      ★        ★
  D3     ★     ◦    [—]    ★     ◦     ◦      ★        ★
  E1     ★     ★    ★    [—]    ★     ★      ★        ★
  E2     ★     ★    ◦     ★    [—]    ★      ★        ★
  E3     ◦     ★    ◦     ★     ★    [—]     ★        ★
  Mgr    ★     ★    ★     ★     ★     ★     [—]       ★
  DG     ★     ★    ★     ★     ★     ★      ★       [—]

  Règle : 
  - ★ = Review obligatoire AVANT transmission au validateur suivant
  - ◦ = Review encouraged mais pas blocker
  - D1 revoit TOUJOURS les assemblies de D2/D3
  - E1 revoit TOUJOURS les NDC de E2/E3 (cohérence structurale)
  - Agent Manager revoit TOUS les livrables DG-facing
```

### 2.4 File Naming Convention (standardisée)

```
Format : {PRODUIT}_{PHASE}_{SECTION}_{AGENT}_{DATE}_v{VERSION}.{EXT}

Exemples :
  CIVIL_Concept_Bras_D1_220626_v1.0.SLDPRT      → D1, bras drone civil, phase concept
  DEFENSE_CAO_Lanceur_D3_220626_v2.1.SLDPRT     → D3, lanceur défense, phase CAO
  INDUSTRIAL_Sim_FEA_E1_220626_v1.0.pdf         → E1, simulation FEA drone industriel
  CIVIL_BOM_Final_D1+E1+E2+E3_220626_v1.0.xlsx  → BOM validée multi-agent
  DEFENSE_Propulsion_ micro_E2_220626_v1.0.pdf  → E2, specs propulsion micro-drone

Convention de versioning :
  _v1.0 = Première version
  _v1.1 = Révision mineure (correction orthographe, adjustment léger)
  _v2.0 = Changement majeur (nouvelle géométrie, new specs)
  _vFINAL = Version finale validée DG
```

---

## 3. WORKFLOW PHASES — Par Ligne de Produit

### 3.1 DRONE CIVIL (Photo, Delivery, Agriculture)

```
PHASE 0: BRIEF CLIENT
═══════════════════════════════════════════════════════════════════════════════
 QUI : Commercial Agent + DG
 QUOI : Spécifier le besoin client (payload, autonomie, portée, budget)
 INPUT : Brief client / appel d'offre
 OUTPUT : Client_Requirements_vX.X.docx
 VALIDATION : DG GO obligatoire
═══════════════════════════════════════════════════════════════════════════════
```

| Phase | Step | Qui | Quoi | Input | Output | Validation | SLA |
|---|---|---|---|---|---|---|---|
| **1. CONCEPT** | 1.1 | DG + Commercial | Brief meeting | Client brief | Requirements document | DG sign | Jour 1 |
| **1. CONCEPT** | 1.2 | D1 + D2 | Explorations 3D (2-3 concepts) | Requirements | Concept sketches + renders | Peer review D3 | Jours 2-4 |
| **1. CONCEPT** | 1.3 | E1 + E2 | Quick structural + propulsion check | Concepts | Screening report | E1+E2 sign | Jours 3-5 |
| **1. CONCEPT** | 1.4 | ALL (débrief) | **Débrief collectif** | Screening | Debrief notes | Agent Manager | Jour 5 |
| **1. CONCEPT** | 1.5 | DG | **GO/NO-GO concept** | Screening + renders | Decision | DG | Jour 6 |
| **2. CAO** | 2.1 | D1 | CAO détaillée (assembly root) | GO concept | CAD_assembly.SLDPRT | Peer D2 | Jours 7-14 |
| **2. CAO** | 2.2 | E1 | NDC + FEA iteration 1 | CAD_v1 | NDC + FEA_report | E1 sign | Jours 8-15 |
| **2. CAO** | 2.3 | E2 | Specs propulsion validées | CAD_v1 | SPECS_PROPULSION_v1 | E2 sign | Jours 8-15 |
| **2. CAO** | 2.4 | E3 | Schematic électronique | CAD_v1 | SCHEMATIC_ELEC_v1 | E3 sign | Jours 9-15 |
| **2. CAO** | 2.5 | D2 | Payload integration + interfaces | CAD_v1 | INTERFACE_DRAWINGS | Peer E1 | Jours 10-16 |
| **2. CAO** | 2.6 | D1 | CAO intègre retours E1+E2+E3 | NDC + specs | CAD_REVISED_v2 | Peer review | Jours 14-18 |
| **2. CAO** | 2.7 | ALL (débrief) | **Débrief collectif** | CAD_REVISED | Debrief notes | Agent Manager | Jour 18 |
| **2. CAO** | 2.8 | DG | **GO/NO-GO CAO** | CAD_REVISED | Decision | DG | Jour 19 |
| **3. SIMULATION** | 3.1 | E1 | FEA complète (stress, fatigue, vibration) | CAD_RELEASE | FEA_REPORT | Peer review E2 | Jours 19-25 |
| **3. SIMULATION** | 3.2 | E1 + E2 | Performance flight simulation | CAD_RELEASE | FLIGHT_SIM_REPORT | E2 sign | Jours 20-26 |
| **3. SIMULATION** | 3.3 | E3 | EMI + thermal simulation | CAD_RELEASE | THERMAL_EMI_REPORT | E3 sign | Jours 20-26 |
| **3. SIMULATION** | 3.4 | D3 (si applicable) | ML-driven topology optimization | CAD_RELEASE | TOPO_OPT_DESIGNS | D1 review | Jours 21-27 |
| **3. SIMULATION** | 3.5 | ALL | **Débrief collectif** | All reports | Synthesis | Agent Manager | Jour 27 |
| **3. SIMULATION** | 3.6 | DG | **GO/NO-GO Simulation** | Reports | Decision | DG | Jour 28 |
| **4. PROTOTYPE** | 4.1 | D1 + E1 | Preparation prototype package | CAD_RELEASE | PROTOTYPE_PKG | Agent Manager | Jours 28-30 |
| **4. PROTOTYPE** | 4.2 | Proto team | Fabrication | PROTOTYPE_PKG | Physical prototype | QC check | Jours 30-60 |
| **4. PROTOTYPE** | 4.3 | ALL | **Débrief collectif final** | Prototype | Lessons learned | Agent Manager | Jour 61 |
| **4. PROTOTYPE** | 4.4 | DG | **GO/NO-GO Production** | Lessons learned | Decision | DG | Jour 62 |

---

### 3.2 DRONE INDUSTRIEL (Inspection, Surveillance)

| Phase | Step | Qui | Quoi | Input | Output | Validation | SLA |
|---|---|---|---|---|---|---|---|
| **1. CONCEPT** | 1.1 | DG + Commercial | Brief inspection use case | Client brief | Requirements | DG sign | Jour 1 |
| **1. CONCEPT** | 1.2 | D2 | Design payload inspection (caméra, sensors) | Requirements | Payload concepts | Peer D3 | Jours 2-5 |
| **1. CONCEPT** | 1.3 | D1 + E1 | Structure IP67 waterproof design | Payload concepts | Structural concepts | Peer E1 | Jours 3-6 |
| **1. CONCEPT** | 1.4 | E3 | Electronic integration sensors | Requirements | Sensor integration plan | Peer D2 | Jours 3-6 |
| **1. CONCEPT** | 1.5 | ALL | **Débrief collectif** | All concepts | Debrief notes | Agent Manager | Jour 6 |
| **1. CONCEPT** | 1.6 | DG | **GO/NO-GO** | Debrief | Decision | DG | Jour 7 |
| **2. CAO** | 2.1 | D2 | CAO waterproof enclosure | GO | CAD_enclosure.SLDPRT | Peer D1 | Jours 8-14 |
| **2. CAO** | 2.2 | D1 | CAO structure principale | GO | CAD_main_structure | Peer D2 | Jours 8-14 |
| **2. CAO** | 2.3 | E1 | FEA IP67 + pressure tests | CAD | FEA_WATERPROOF | Peer review | Jours 10-16 |
| **2. CAO** | 2.4 | E3 | Wiring + connectors specs | CAD | WIRING_SPEC | Peer D2 | Jours 10-16 |
| **2. CAO** | 2.5 | ALL | **Débrief collectif** | CAD_REVISED | Debrief | Agent Manager | Jour 16 |
| **2. CAO** | 2.6 | DG | **GO/NO-GO CAO** | CAD | Decision | DG | Jour 17 |
| **3. SIMULATION** | 3.1 | E1 | FEA pressure + vibration | CAD_RELEASE | FEA_REPORT | Peer review | Jours 17-22 |
| **3. SIMULATION** | 3.2 | E3 | EMI + thermal (enclosure) | CAD_RELEASE | THERMAL_EMI | Peer review | Jours 18-23 |
| **3. SIMULATION** | 3.3 | E2 | Flight performance (heavy payload) | CAD_RELEASE | FLIGHT_SIM | E2 sign | Jours 18-23 |
| **3. SIMULATION** | 3.4 | DG | **GO/NO-GO Sim** | Reports | Decision | DG | Jour 24 |
| **4. PROTOTYPE** | 4.1 | ALL | Prototype package | CAD_RELEASE | PROTOTYPE_PKG | Agent Manager | Jours 24-26 |
| **4. PROTOTYPE** | 4.2 | Proto | Fabrication | PROTOTYPE_PKG | Prototype | QC | Jours 26-55 |
| **4. PROTOTYPE** | 4.3 | DG | **GO/NO-GO Prod** | Prototype | Decision | DG | Jour 56 |

---

### 3.3 DRONE DÉFENSE (Micro-drone Interceptor Swarm + Lanceur Air Comprimé)

> ⚠️ **Classification :** CONFIDENTIEL — Concept défense
> ⚠️ **Règle spéciale** : Zéro transmission externe sans validation DG explicite.

| Phase | Step | Qui | Quoi | Input | Output | Validation | SLA |
|---|---|---|---|---|---|---|---|
| **1. CONCEPT** | 1.1 | DG + D3 | Brief défense armasuisse | Call for tender | BRIEF_DEFENSE_v1 | DG sign | Jour 1 |
| **1. CONCEPT** | 1.2 | D3 | Concept essaim + lanceur air comprimé | BRIEF | CONCEPT_SWARM_v1 (renders + 3D) | Peer D1 | Jours 2-5 |
| **1. CONCEPT** | 1.3 | E1 | Dimensionnement lanceur (pression, structure) | CONCEPT | NDC_LANCEUR | E1 sign | Jours 3-6 |
| **1. CONCEPT** | 1.4 | E2 | Propulsion micro-drone (miniaturisation) | CONCEPT | SPECS_MICRO_PROP | E2 sign | Jours 3-6 |
| **1. CONCEPT** | 1.5 | E3 | Électronique miniaturisée (avionique) | CONCEPT | SPECS_AVIONICS | E3 sign | Jours 3-6 |
| **1. CONCEPT** | 1.6 | ALL | **Débrief collectif défense** | All specs | DEBRIEF_DEFENSE | Agent Manager | Jour 6 |
| **1. CONCEPT** | 1.7 | DG | **GO/NO-GO défense** | Debrief | Decision (obligatoire) | DG | Jour 7 |
| **2. CAO** | 2.1 | D3 | CAO lanceur air comprimé | GO | CAD_LANCEUR | Peer D1 | Jours 8-14 |
| **2. CAO** | 2.2 | D3 + D1 | CAO cellule micro-drone | GO | CAD_MICRO_DRONE | Peer D2 | Jours 8-14 |
| **2. CAO** | 2.3 | E1 | FEA lanceur (pression interne) | CAD_LANCEUR | FEA_LANCEUR | Peer review | Jours 10-16 |
| **2. CAO** | 2.4 | E1 | FEA cellule micro-drone (crash) | CAD_MICRO | FEA_MICRO | Peer review | Jours 10-16 |
| **2. CAO** | 2.5 | E2 | Integration propulsion micro | CAD_MICRO | PROP_INTEGRATION | E2 sign | Jours 11-17 |
| **2. CAO** | 2.6 | E3 | Miniature electronics packaging | CAD_MICRO | ELEC_PACKAGING | E3 sign | Jours 11-17 |
| **2. CAO** | 2.7 | ALL | **Débrief collectif** | CAD_REVISED | Debrief | Agent Manager | Jour 17 |
| **2. CAO** | 2.8 | DG | **GO/NO-GO CAO défense** | CAD | Decision (DG obligatoire) | DG | Jour 18 |
| **3. SIMULATION** | 3.1 | E1 | FEA complète lanceur + cellule | CAD_RELEASE | FEA_FULL | Peer review | Jours 18-24 |
| **3. SIMULATION** | 3.2 | E1 + E2 | Trajectoire lancement (physics-informed ML) | FEA + specs | TRAJ_SIM_REPORT | E1+E2 sign | Jours 19-25 |
| **3. SIMULATION** | 3.3 | E3 | Signal/comm micro-drone sim | CAD_RELEASE | COMMS_SIM | E3 sign | Jours 19-25 |
| **3. SIMULATION** | 3.4 | ALL | **Débrief collectif** | Reports | Synthesis | Agent Manager | Jour 25 |
| **3. SIMULATION** | 3.5 | DG | **GO/NO-GO Sim défense** | Reports | Decision (DG obligatoire) | DG | Jour 26 |
| **4. PROTOTYPE** | 4.1 | ALL | Prototype defense package | CAD_RELEASE | PROTOTYPE_DEF_PKG | Agent Manager | Jours 26-28 |
| **4. PROTOTYPE** | 4.2 | DG | **GO/NO-GO Production défense** | Prototype | Decision (DG + armasuisse) | DG | Jour 28 |

---

## 4. WHERE THE DG MUST INTERVENE — Points de Décision Critiques

### 4.1 Tableau récapitulatif — Tous les GO/NO-GO

| # | Point de décision | Phase | Timing | Information reçue par DG | Options | SLA | Si silence |
|---|---|---|---|---|---|---|---|
| **G0** | Validation brief client | 0 | Jour 1 | Brief + Requirements document | GO / NO-GO / Demande info | 24h | Auto-NO-GO après 48h |
| **G1** | GO Concept | 1 | Jour 6 | Renders + screening + debrief | GO / NO-GO / Revoir specs | 24h | Auto-NO-GO après 48h |
| **G2** | GO CAO détaillée | 2 | Jour 19 | CAD_REVISED + BOM + peer reviews | GO / NO-GO / Modifications | 48h | Auto-NO-GO après 72h |
| **G3** | GO Simulation | 3 | Jour 28 | FEA_report + flight_sim + thermal_EMI | GO / NO-GO / Additional sim | 48h | Auto-NO-GO après 72h |
| **G4** | GO Prototype | 4 | Jour 62 | Prototype + lessons learned | GO / NO-GO / Redesign | 72h | Auto-NO-GO après 96h |
| **G5** | GO Production | 5 | — | Business case + prototype + BOM cost | GO / NO-GO | 1 semaine | Auto-NO-GO après 2 semaines |
| **G6** | GO Concept Défense | 1 | Jour 7 | Concept défense + renders | GO / NO-GO / Revoir | 24h | Auto-NO-GO après 48h |
| **G7** | GO CAO Défense | 2 | Jour 18 | CAD défense + specs | GO / NO-GO | 24h | Auto-NO-GO après 48h |
| **G8** | GO Sim Défense | 3 | Jour 26 | FEA + traj_sim + comms_sim | GO / NO-GO | 24h | Auto-NO-GO après 48h |
| **G9** | GO Production Défense | 4 | Jour 28 | Prototype défense | GO / NO-GO + armasuisse approval | 72h | Auto-NO-GO après 96h |
| **G10** | GO offre armasuisse | — | — | Full proposal + commercial terms | GO / NO-GO | 1 semaine | Auto-NO-GO après 2 semaines |

### 4.2 Format d'information reçu par DG à chaque GO

```
┌─────────────────────────────────────────────────────────┐
│           FICHE GO — DG DECISION SUPPORT                │
│  Format standardisé pour TOUS les points de GO          │
└─────────────────────────────────────────────────────────┘

PROJECT : _______________    PHASE : _______    DATE : _______
AGENT MANAGER : ___________    GO # : _______

📋 RÉSUMÉ EXÉCUTIF (max 10 lignes) :
[Ce que l'équipe a fait, en une phrase]

✅ CE QUI EST BON :
[Liste des points validés, forces du design]

⚠️ CE QUI EST INCERTAIN :
[Liste des risques ouverts, questions en suspens]

🎯 RECOMMANDATION ÉQUIPE :
[GO recommandé / Non recommandé / Plus d info nécessaire]

📊 KPIs À CETTE ÉTAPE :
- Taux livrables dans les délais : ____%
- Peer reviews réalisées : ____/____
- Blocker actifs : ____

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
- Pour question process → Agent Manager (Slack : @Mgr)
```

---

## 5. PROBLEM RESOLUTION PROTOCOL

### 5.1 Comment un problème est détecté

| Méthode | Détection | Qui détecte | Channel |
|---|---|---|---|
| 📉 **KPI Alert** | KPI en dessous du seuil alerte | Agent Manager (dashboard) | Slack #ops-alerts |
| 🔴 **Agent Flag** | Agent identifie un risque blocker | N'importe quel agent | Slack #problem-escalation |
| 👥 **Peer Review Failure** | Review découvre un défaut | Peer reviewer | Email + Slack |
| 📅 **Weekly Sync** | Discussion ouverte | Agent Manager | Réunion hebdo |
| 🚨 **DG Flag** | DG identifie un problème | DG | N'importe quel canal |

### 5.2 Arbre de décision — Comment DG résout un problème

```
                    ┌─────────────────────────────┐
                    │  DG IDENTIFIE UN PROBLÈME   │
                    │  ou reçoit une alerte      │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │  TYPE DE PROBLÈME ?          │
                    │  (DG diagnostique)           │
                    └─────────────┬───────────────┘
                                  │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐         ┌───────────────┐          ┌───────────────┐
│  🎨 DESIGN    │         │  🔧 ENGINEER  │          │  📋 PROCESS   │
│  (CAO, forme, │         │  (simulation, │          │  (workflow,   │
│   aesthetics) │         │   structure,   │          │   délai,       │
│               │         │   propulsion)  │          │   delivery)    │
└───────┬───────┘         └───────┬───────┘          └───────┬───────┘
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐         ┌───────────────┐          ┌───────────────┐
│→ Contacter D1 │         │→ Contacter E1 │          │→ Contacter    │
│  (ou D2/D3 si│         │  (ou E2/E3 si │          │  Agent Mgr    │
│  spécialisé)  │         │  spécialisé)  │          │               │
└───────┬───────┘         └───────┬───────┘          └───────┬───────┘
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐         ┌───────────────┐          ┌───────────────┐
│Demander:      │         │Demander:     │          │Demander:     │
│- Screenshot   │         │- Logs sim    │          │- Dashboard   │
│  problème CAO │         │- NDC ou      │          │- KPIs actuels│
│- Cause root   │         │  specs en    │          │- Blocker list│
│- Solution     │         │  cause       │          │- Plan action │
│  suggérée     │         │- Solution    │          │              │
│- Impact coût  │         │  suggérée    │          │              │
│  + délais     │         │- Impact coût │          │              │
│               │         │  + délais    │          │              │
└───────┬───────┘         └───────┬───────┘          └───────┬───────┘
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐         ┌───────────────┐          ┌───────────────┐
│Si solveable:  │         │Si solveable:  │          │Si solveable:  │
│DG valide +    │         │DG valide +    │          │DG valide +    │
│redémarrer     │         │redémarrer     │          │redémarrer     │
│étape          │         │étape          │          │étape          │
└───────┬───────┘         └───────┬───────┘          └───────┬───────┘
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐         ┌───────────────┐          ┌───────────────┐
│Si NON         │         │Si NON         │          │Si NON         │
│solveable:     │         │solveable:     │          │solveable:     │
│→ Escalade     │         │→ Escalade     │          │→ Escalade     │
│  réunion      │         │  réunion      │          │  réunion      │
│  d'urgence    │         │  d'urgence    │          │  d'urgence    │
│  (DG+Mgr+     │         │  (DG+Mgr+     │          │  (DG+Mgr+     │
│  agent(s))     │         │  agent(s))     │          │  agent(s))     │
└───────────────┘         └───────────────┘          └───────────────┘
```

### 5.3 Chemins d'escalade par type de problème

#### 🔴 Escalade DESIGN (D1/D2/D3)

```
Problème détecté
      │
      ▼
[1] DG contacte D1 directement (Slack @D1 ou email)
      │
      ├─── D1 analyse + propose solution dans les 24h
      │         │
      │         ▼
      │    [2] Si D1 a besoin de D2 ou D3
      │         D1 les contacte directement
      │         │
      │         ▼
      │    [3] D1 produit CAO révisée + peer review D2
      │         │
      │         ▼
      │    [4] D1 soumet à DG pour validation
      │         │
      │         ▼
      │    GO si OK / Redesk si needed
      │
      └─── Si D1 ne peut pas résoudre seul → réunion d'urgence
                D1 + D2 (+ E1 siinvolving structural analysis)
                dans les 48h
```

#### 🔴 Escalade ENGINEERING (E1/E2/E3)

```
Problème détecté
      │
      ▼
[1] DG contacte E1 directement (ou E2/E3 si spécialisé)
      │
      ├─── E1 analyse + produit diagnostic technique
      │         │
      │         ▼
      │    [2] E1 coordonne avec E2/E3 si nécessaire
      │         │
      │         ▼
      │    [3] E1 produit rapport de résolution
      │         (NDC révisée, specs mises à jour)
      │         │
      │         ▼
      │    [4] Peer review par E2 ou E3
      │         │
      │         ▼
      │    [5] E1 soumet à DG pour validation
      │         │
      │         ▼
      │    GO si OK / Redesign si needed
      │
      └─── Si problème système-wide → réunion d'urgence
                E1+E2+E3 + DG dans les 48h
```

#### 🔴 Escalade COMMERCIAL (Agent Commercial)

```
Problème détecté
      │
      ▼
[1] DG contacte Agent Commercial
      │
      ├─── Agent Commercial analyse + propose réponse
      │         │
      │         ▼
      │    [2] Coordiné avec D3 (siconcept défense) ou D1/D2 (si civilian)
      │         │
      │         ▼
      │    [3] Agent Commercial produit réponse clients/armasuisse
      │         │
      │         ▼
      │    [4] DG valide avant envoi
      │
      └─── Si problème juridique ou contractuel → consultation juridique
```

### 5.4 Protocole de réunion d'urgence

| Élément | Détail |
|---|---|
| **Timing** | Réunion convoquée dans les 24-48h après escalade |
| **Participants** | DG + Agent(s) impliqué(s) + Agent Manager |
| **Durée** | Max 1h |
| **Prérequis** | Chaque participant prépare : problème décrit + solution suggérée + impact |
| **Output** | Decision record : décidé quoi + qui + quand |
| **Follow-up** | Agent Manager envoie compte-rendu sous 24h |

---

## 6. DAILY / WEEKLY RHYTHM

### 6.1 Dashboard quotidien — Ce que le DG voit chaque matin

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              🚀 OPERATIONS DASHBOARD — AIML UAV STARTUP                  │
│                          DATE : [JOUR] | HEURE : [HH:MM]                │
│                       Dashboard généré par Agent Manager                 │
└─────────────────────────────────────────────────────────────────────────────┘

📅 AUJOURD'HUI — Points ouverts
─────────────────────────────────────────────────────────────────────────────
[ ] 0 blockers actifs        [ ] 1 projet en cours         [ ] 3 agents en alerte
─────────────────────────────────────────────────────────────────────────────

🎯 PROJETS ACTIFS

🏷️ [Nom Projet 1] — [Civil / Industrial / Defense]
   Phase : [Phase] (Jour X/Y)
   Avancement : [██████░░░░] 60%
   Blocker : ⚠️ [OUI/NON]
   Prochaine milestone : [GO CAO] — [Date]
   Agent lead : [D1+E1]
   
🏷️ [Nom Projet 2] — [Civil / Industrial / Defense]
   Phase : [Phase] (Jour X/Y)
   Avancement : [████████░░] 80%
   Blocker : ✅ Aucun
   Prochaine milestone : [GO Simulation] — [Date]
   Agent lead : [D2+E2]
   
🔴 BLOCKERS ACTIFS
─────────────────────────────────────────────────────────────────────────────
|ID | Projet       | Blocker                     | Owner   | SLA restant |
|---|---|---|---|
|B01| Drone Civil  | Validation BOM incomplete   | E1      | 24h         |
|B02| Défense      | Données armasuisse manquantes| Agent Mgr| 48h        |
─────────────────────────────────────────────────────────────────────────────
⚡ ACTION REQUISE DU DG AUJOURD'HUI
─────────────────────────────────────────────────────────────────────────────
[1] 🚨 Urgent : GO CAO Drone Civil — Deadline aujourd'hui 17h
[2] 📋 Review : Renders Concept Défense D3 — Merci valider
[3] ✅ Confirmer : Budget prototype agricole — 5 minutes
─────────────────────────────────────────────────────────────────────────────

📊 KPI SNAPSHOT (cette semaine)
┌──────────────────────┬─────────┬─────────┬────────────┐
│ Domaine              │ Cible   │ Actuel  │ Status     │
├──────────────────────┼─────────┼─────────┼────────────┤
│ Livrables dans délais│ ≥ 90%   │ 88%     │ 🟡 À voir  │
│ Peer reviews réalisées│ 100%    │ 95%     │ 🟡 À voir  │
│ Simulations OK 1er pass│ ≥ 85% │ 100%   │ 🟢 Bon     │
│ Contacts armasuisse   │ ≥ 2/sem│ 3       │ 🟢 Bon     │
│ Blocker résolus <48h │ 100%    │ 100%    │ 🟢 Bon     │
└──────────────────────┴─────────┴─────────┴────────────┘

📁 DERNIERS LIVRABLES
─────────────────────────────────────────────────────────────────────────────
[22.06 09:15] ✅ FEA Report Drone Civil v2.1 — E1
[22.06 08:30] ✅ CAD Assembly Drone Civil v3.0 — D1
[21.06 17:45] ✅ Concept Swarm Defense renders — D3
[21.06 16:00] ✅ Specs Propulsion Micro-drone — E2
─────────────────────────────────────────────────────────────────────────────

⏰ PROCHAINES MILESTONES
─────────────────────────────────────────────────────────────────────────────
[26.06] GO Simulation — Drone Civil
[28.06] GO CAO — Drone Défense
[01.07] Weekly Sync — Tous agents + DG
─────────────────────────────────────────────────────────────────────────────
```

### 6.2 Weekly Sync — Rituel hebdomadaire

| Timing | Quoi | Durée | Participants | Output |
|---|---|---|---|---|
| **Lundi 09h** | Kickoff semaine — Agent Manager seul | 15 min | Agent Manager | Planing semaine publié |
| **Mardi 10h** | Design sync (D1+D2+D3) | 45 min | D1+D2+D3 + Agent Mgr | blockers design listés |
| **Mardi 11h** | Engineering sync (E1+E2+E3) | 45 min | E1+E2+E3 + Agent Mgr | blockers engineering listés |
| **Mercredi 14h** | Commercial + Marketing sync | 30 min | Com + Mkt + Mgr | pipeline update |
| **Jeudi 10h** | Amélioration continue review | 30 min | AC agent + Mgr | actions processuelles |
| **Vendredi 14h** | **FULL TEAM SYNC** | 60 min | ALL + DG | dashboard final semaine |
| **Vendredi 15h** | **DG SYNC** (optionnel) | 30 min | DG + Mgr | Décisions ouvertes |

#### Format Full Team Sync (Vendredi 14h)

```
ORDRE DU JOUR — FULL TEAM SYNC (60 minutes)
═══════════════════════════════════════════════════════════════════════════════
1. [5 min] Rétrospective semaine : qui a fait quoi
2. [10 min] Dashboard review : KPIs, blockers, avancements
3. [15 min] Problèmes ouverts : discussion collective
4. [10 min] Planning semaine prochaine : кто fait quoi
5. [10 min] Points DG : décisions nécessaires
6. [10 min] Actions & follow-ups
═══════════════════════════════════════════════════════════════════════════════
```

### 6.3 Ce qui déclenche une réunion d'urgence

| Trigger | Condition | Timing | Participants |
|---|---|---|---|
| 🚨 **Blocker critique** | Blocker bloque > 2 jours sans resolution | Dans les 24h | DG + agent(s) + Mgr |
| 💥 **Simulation failure** | FEA ou simulation échoue sans solution | Dans les 24h | DG + E1 + Mgr |
| ⚠️ **Client/armi deadline** | Deadline externe menacé | Dans les 4h | DG + Commercial + Mgr |
| 🤝 **Conflict agents** | Conflit entre 2+ agents non résolu | Dans les 24h | DG + les 2 agents + Mgr |
| 📉 **KPI critical** | KPI < 70% pendant 2 semaines consécutives | Dans les 48h | DG + Mgr + agent(s) concerné(s) |
| 🔒 **Sécurité/Pénombre** | Toute suspicion de fuite de données défense | Immédiat | DG + tous les agents |

---

## 7. AIML INTEGRATION POINTS WITH DESIGN & ENGINEERING

### 7.1 Vue d'ensemble — Où ML entre dans le workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              AIML INTEGRATION MAP — Design ↔ Engineering ↔ ML            │
│                                                                             │
│  BRIEF ───▶ CONCEPT ───▶ CAO ───▶ SIMULATION ───▶ PROTOTYPE ───▶ PROD    │
│                            │                                                │
│    ┌───────────────────────┼──────────────────────────────────────┐       │
│    │                       │                                              │       │
│    ▼                       ▼                                              ▼       │
│ ┌──────────┐      ┌────────────────┐      ┌────────────────────────────┐   │
│ │Topology  │      │Aerodynamics    │      │Predictive Maintenance     │   │
│ │Optimiz. │      │ML (CFD)        │      │(ESC, motor, battery)      │   │
│ │(D3+E1)  │      │(E1)            │      │(E3)                        │   │
│ └──────────┘      └────────────────┘      └────────────────────────────┘   │
│                            │                                              │       │
│    ┌───────────────────────┼──────────────────────────────────────┐       │
│    │                       ▼                                              │       │
│    │              ┌────────────────┐                                    │       │
│    │              │Swarm RL        │                                    │       │
│    │              │Coordination    │                                    │       │
│    │              │(Defense only)  │                                    │       │
│    │              │(E2+D3)        │                                    │       │
│    │              └────────────────┘                                    │       │
│    │                                                                      │       │
│    ▼                                                                      │       │
│ ┌──────────┐      ┌────────────────┐      ┌────────────────────────────┐   │
│ │Trajectory│      │Payload/CV      │      │Market Intelligence        │   │
│ │Prediction│      │Integration ML  │      │(NLP pipeline)             │   │
│ │(E1)      │      │(D2+E3)         │      │(Commercial)               │   │
│ └──────────┘      └────────────────┘      └────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 AIML Modules — Propriétaire et workflow détaillé

#### 🧠 ML-1 : Topology Optimization (Topology Optimization ML-Driven)

| Élément | Détail |
|---|---|
| **Module owner** | D3 (design lead) + E1 (structural validation) |
| **Outil** | PyTorch + custom topology optimization loop |
| **Pipeline** | D3 produit design space → ML génère topologies candidates → D3 filtre → E1 valide FEA |
| **Intégration workflow** | Step 3.3 du workflow défense (après FEA initiale) |
| **Input** | CAD concept + contraintes structurales |
| **Output** | 3-5 design alternatives optimisées |
| **Comment D1/D2 interagit** | Reçoit renders + comparaison coût/fabrication |
| **Validation** | E1 FEA chaque topologie → DG GO |

#### 🧠 ML-2 : Aerodynamics / CFD Reduced-Order Model

| Élément | Détail |
|---|---|
| **Module owner** | E1 |
| **Outil** | PyTorch (PINN / Reduced Order Model) + DVC pour datasets |
| **Pipeline** | Training sur données CFD existantes → inference en < 1min vs 4h CFD complet |
| **Intégration workflow** | Remplace la simulation CFD complète en phase screening (Step 1.3 concept) |
| **Input** | Géométrie simplifiée, conditions de vol |
| **Output** | Coefficients aérodynamiques prédits (Cx, Cz, Cm) |
| **Comment designers interagissent** | D1 reçoit les coefficients pour ajustement géométrique |
| **Validation** | Comparaison vs données réelles vol (E3 logs) tous les 3 projets |

#### 🧠 ML-3 : Predictive Maintenance (ESC, Moteur, Batterie)

| Élément | Détail |
|---|---|
| **Module owner** | E3 |
| **Outil** | PyTorch LSTM / Transformer + MLflow tracking + TensorRT inference |
| **Pipeline** | Training sur logs de vol → inference embarqué (TensorRT) → alertes maintenance |
| **Intégration workflow** | Phase 4 (prototype) et production — maintenance prédictive |
| **Input** | Logs de vol (RPM, tension batterie, température, courants) |
| **Output** | Score de santé composant + prédiction défaillance J+7 |
| **Comment designers interagissent** | D2 utilise les predictions pour design du bay batterie (maintenance access) |
| **Validation** | Accuracy ≥ 80%, recalibration mensuelle |

#### 🧠 ML-4 : Swarm RL Coordination (Défense uniquement)

| Élément | Détail |
|---|---|
| **Module owner** | E2 (propulsion) + D3 (concept) |
| **Outil** | Isaac Gym (NVIDIA) + PyTorch MARL |
| **Pipeline** | Isaac Gym simulation → RL training → politique de coordination essaim |
| **Intégration workflow** | Phase 3 (simulation) défense uniquement |
| **Input** | Positions initiales drones, cibles, contraintes environnementales |
| **Output** | Politique de coordination optimisée (deployment-ready) |
| **Classification** | CONFIDENTIEL — air-gapped, zéro cloud |
| **Comment DG interagit** | Reçoit demonstration video simulé + rapport performance |

#### 🧠 ML-5 : Trajectory Prediction (Physics-Informed ML)

| Élément | Détail |
|---|---|
| **Module owner** | E1 |
| **Outil** | PyTorch + physics-informed neural networks (PINN) |
| **Pipeline** | Training sur données lancement réel/simulé → prédiction trajectoire |
| **Intégration workflow** | Phase 3 simulation défense (après FEA lanceur) |
| **Input** | Angle lancer, pression air, masse drone, vent |
| **Output** | Trajectoire prédite + enveloppe de confiance |
| **Comment D3 interagit** | Utilise pour design longueur tube lanceur |
| **Validation** | Comparaison vs launch tests |

#### 🧠 ML-6 : Payload / Computer Vision (Inspection)

| Élément | Détail |
|---|---|
| **Module owner** | D2 (design) + E3 (electronics) |
| **Outil** | PyTorch CNN / Vision Transformer |
| **Pipeline** | Training sur dataset images inspection → inference embarqué |
| **Intégration workflow** | Phase 2 CAO (payload integration) industriel |
| **Input** | Images de vol drone inspection (industries chimiques, toit solaire) |
| **Output** | Anomalies détectées + localisation |
| **Comment designers interagissent** | D2 design electronics bay pour GPU embarqué (NVIDIA Jetson) |

### 7.3 Tableau récapitulatif AIML

| ML Module | Owner principal | Owner secondaire | Phase intégrée | Drone lines | Outil principal | Status |
|---|---|---|---|---|---|---|
| ML-1 Topology Opt | D3 | E1 | 3 (Sim) | Defense | PyTorch | 🔴 À développer |
| ML-2 Aero CFD | E1 | D1 | 1 (Concept) | All | PyTorch + DVC | 🟡 En cours |
| ML-3 Pred. Maintenance | E3 | D2 | 4 (Proto) | Industrial + Civil | PyTorch + TensorRT | 🟢 En production |
| ML-4 Swarm RL | E2 | D3 | 3 (Sim) | Defense only | Isaac Gym | 🔴 À développer |
| ML-5 Trajectory PINN | E1 | D3 | 3 (Sim) | Defense only | PyTorch PINN | 🟡 Planifié |
| ML-6 CV Inspection | D2 | E3 | 2 (CAO) | Industrial | PyTorch ViT | 🟡 En cours |

---

## ANNEXE — Contact rapide

| Agent | Nom | Channel | Pour |
|---|---|---|---|
| DG | [Nom DG] | Slack @DG / email | Décisions finales, GO/NO-GO |
| Agent Manager | [Nom Mgr] | Slack @Mgr | Coordination, planning, blockers |
| D1 | Lead Mechanical | Slack @D1 | CAO, assemblies, BOM |
| D2 | Systems Design | Slack @D2 | Payloads, interfaces, waterproofing |
| D3 | Concept & Defense | Slack @D3 | Concepts, proposals défense |
| E1 | Mechanical Eng | Slack @E1 | Structures, FEA, simulation |
| E2 | Propulsion | Slack @E2 | Moteurs, batteries, performance |
| E3 | Electronics | Slack @E3 | Firmware, électronique, logs vol |
| Commercial | Agent Commercial | Slack @Com | Clients, armasuisse, pipeline |
| Marketing | Agent Marketing | Slack @Mkt | Brand, contenu, stratégie |
| AC Agent | Amélioration | Slack @AC | Processus, quality, audits |

---

*Document créé par Agent Manager — v1.0 — 22.06.2026*
*Prochaine révision prévue : 22.07.2026 (par Agent Amélioration Continue)*
*Classification : INTERNE CONFIDENTIEL — Ne pas diffuser sans accord DG*
