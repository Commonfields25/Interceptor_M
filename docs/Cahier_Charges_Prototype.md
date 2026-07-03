---
agent: Jules + agent_worker
action: Merge conflict resolution
timestamp: 2026-07-03T21:30:00Z
related_gate: G4
status: PRELIMINARY
version: 0.4
conflict_resolved: true
base_main: 3298788cf807aa196a2b5e1daa8472b0c91c624c
base_feat: 3e689f3ee7550e9492519893800ece42627077ff
---

# Cahier des Charges Technique — Prototype Interceptor M (DD-400)

> **Version** : PRELIMINARY 0.4
> **Date** : 2026-07-03
> **Statut** : 🟡 En cours — Basé sur Baseline v1.2.0 / DD-400
> **Classification** : Interne confidentiel
> **Sources** : DDC-001, D2_aerodynamics.md, D3_structure.md, PRODUCT-FAMILY.md v1.1, PARAMETERS.json, PROTOTYPE_ROADMAP.md, BOM_consolidee.md, D1_specifications.json

---

## 1. Contexte & Objet

Ce document définit les **exigences techniques mécaniques** du prototype **Interceptor M — Ligne DD (Defense)**, baseline DD-400.
Il consolide les données issues de la Baseline v1.2.0 (DG Decision, 2026-07-01) et constitue la Table 1c (Vague 6).

> ⚠️ **Alerte Masse (BOM_consolidee.md):** Total estimé = 475 g > MTOW = 400 g. Réduction requise : 75 g minimum. Cf. § EM01.

---

## 2. Énoncés Fonctionnels (FF)

Chaque énoncé fonctionnel est associé à un **critère d'acceptation** vérifiable.

| ID | Énoncé fonctionnel | Critère d'acceptation | Source |
|---|---|---|---|
| **FF01** | Le prototype permet de valider l'encombrement, l'assemblage et l'intégration des modules SC-01 à SC-06 dans le fuselage Ø35 × 900 mm | Démontage/remontage manuel < 30 min sans outillage spécial ; tous les modules s'insèrent sans modification de structure | DDC-001, D3_structure §3.6, PRODUCT-FAMILY.md §3.1 |
| **FF02** | La géométrie cruciforme est respectée : 4 ailes delta (envergure 110 mm, corde 60 mm, sweep 45°) et 4 dérives cruciformes (envergure 75 mm, corde 40 mm, sweep 40°) | Mesure métrologique des cordes, sweep et envergures dans tolérances ±5 % | D2_aerodynamics.md §2.2, D2 §2.4 |
| **FF03** | La propulsion (SC-02) est mécaniquement intégrée à la zone arrière (280–380 mm depuis le nez) et interfacée via 3 vis M3 | Le module SC-02 se monte sur l'interface prévue sans alésage supplémentaire | PRODUCT-FAMILY.md SC-02, D3_structure §3.6.3 |
| **FF04** | Le prototype est compatible avec le lanceur pneumatique (tube bore 40 mm, SABOT-001) | Passage et Centrage dans le tube sans collage ni obstruction de la conduite pneumatique | DDC-001 (40mm tube), PRODUCT-FAMILY.md SC-06, D3 §3.6.1 |
| **FF05** | Le prototype est modulaire : chaque module SC-0X est accessible, remplaçable et ne nécessite pas de modification de structure | Aucun module ne requiert découpe, perçage ou calage pour s'insérer | PRODUCT-FAMILY.md §3.1, D3 §3.6 |
| **FF06** | La structure résiste aux charges de lancement (3,5 g) et de manœuvre (25 g) sans déformation permanente | Absence de déformation plastique vérifiée par examen visuel post-vol | D2_aerodynamics.md §2.6, D3_structure.md §3.5 |
| **FF07** | Le radôme (ogive nez) permet le passage du signal seeker Ka-band | Transparent diélectrique ou fenêtre d'antenne intégrée ; ne bloque pas le faisceau radar | D2 §2.4, D3 §3.4.4 (ogive) |
| **FF08** | Le prototype est démantelable et transportable dans une mallette de dimensions ≤ 400 × 220 × 110 mm | Toutes les pièces repliables ou démontables tiennent dans le volume spécifié | D3_structure §3.6–3.7, PROTOTYPE_ROADMAP.md |

---

## 3. Exigences Mécaniques (EM)

### EM01 — Masse (Ligne DD — Baseline DD-400)

> ⚠️ Alerte : total BOM (475 g) > MTOW (400 g) → cf. note ci-dessous.

| Sous-ensemble | Description | Masse Cible (g) | Matériau | Source |
|---|---|---|---|---|
| **BRK-001** | Coque fuselage +支翼 | 135,0 | AlSi10Mg (DMLS) | BOM_consolidee.md, PARAMETERS.json |
| **ACT-001** | Vérin tubulaire 3 axes | 65,0 | AlSi10Mg (DMLS) | BOM_consolidee.md, PARAMETERS.json |
| **NCR-001** | Bague interface ogive + joint torique | 110,0 | 316L SS | BOM_consolidee.md, PARAMETERS.json |
| **Avionique** | SC-01 (autopilote) | 50,0 | — | BOM_consolidee.md |
| **Batterie** | LiPo | 115,0 | — | BOM_consolidee.md |
| **SABOT-001** | Sabot interface lanceur | 15,0 | ASA (FDM) | docs/Cahier_Charges_Prototype.md v0.2 |
| **Total estimé** | — | **475,0** | — | BOM_consolidee.md |
| **MTOW DD-400** | Masse maximale au décollage | **400,0** | — | PARAMETERS.json, DDC-001 |
| **⚠️ Excès** | Total − MTOW | **−75,0 g** | — | Calculé |

> **Action requise :** Réduction de masse de 75 g minimum avant validation prototype. Options : allègement BRK-001 (AlSi10Mg → CFRP), réduction batterie, optimisation NCR-001. Aucune exigence de performance ne doit être dégradée.

**Cible intermédiaire :** masse sèche ≤ 340 g (payload restant : 60 g pour batteries + mission).

### EM02 — Dimensions (Ligne DD — DD-400)

| Paramètre | Valeur | Tolérance | Source |
|---|---|---|---|
| Longueur fuselage | 900,0 mm | ±0,5 mm | D2_aerodynamics.md §2.2 (fuselage L = 900 mm) |
| Diamètre fuselage | 35,0 mm | ±0,2 mm | D2_aerodynamics.md §2.2, PARAMETERS.json (fuselage_outer_diameter_mm = 35.0) |
| Épaisseur paroi AV | 1,5 mm | ±0,1 mm | D3_structure.md §3.4.1 (Al-7075 T6) |
| Épaisseur paroi AR | 1,2 mm | ±0,1 mm | D3_structure.md §3.4.3 (CFRP) |
| Longueur ogive | 122,5 mm (L_n = 3,5 × Ø35) | ±0,5 mm | D2_aerodynamics.md §2.2 (ogive tangente) |
| Diamètre tube lanceur | 40,0 mm (bore) | — | DDC-001, PRODUCT-FAMILY.md (tube_diameter_mm = 40.0) |

### EM03 — Répartition Interne (Volume Allocation)

| Zone | Plage axiale (mm) | Contenu | Longueur (mm) | Source |
|---|---|---|---|---|
| Zone A — Ogive | 0 – 123 | Seeker / Radôme | 123 | D3_structure.md §3.2 |
| Zone B — Corps AV | 123 – 280 | Electronics Bay + Warhead shoulder | 157 | D3_structure.md §3.2 |
| Zone C — Corps central | 280 – 780 | Propulsion (SRM) + Warhead | 500 | D3_structure.md §3.2 |
| Zone D — Queue AV | 780 – 820 | Actuated fins + Nozzle | 40 | D3_structure.md §3.2 |
| Zone E — Dérives | 820 – 900 | Dérives cruciformes | 80 | D3_structure.md §3.2 |

### EM04 — Résistance Structurelle

| Paramètre | Valeur | Unité | Note |
|---|---|---|---|
| Facteur de charge limite | 25,0 | g | D2_aerodynamics.md §2.6.1 ; PARAMETERS.json (limite manœuvre) |
| Facteur de charge ultime | 22,7 | g | DDC-001 (Ultimate = 15.1 × 1.5) |
| Facteur de sécurité en flexion (25 g) | 1,53 | — | D3_structure.md §3.5.2 (σ_bend = 283 MPa < σ_0.2 = 434 MPa) |
| Facteur de sécurité pression SRM (50 bar) | 11,5 | — | D3_structure.md §3.5.3 (AISI 4330, σ_UTS = 930 MPa) |
| Contrainte admissible (Al-7075 T6) | 290 | MPa | D2 §2.6.1 (σ_0.2 / 1.5) |
| Pression chambre SRM nominale | 50 | bar | D3 §3.5.3 |
| Plage température opérationnelle | -40 à +60 | °C | EM03.3 (v0.2) [hors-repo — à confirmer] |
| Accélération latérale max | 245 | m/s² | D2 §2.6.2 (25 g × 9,81) |

---

## 4. Contraintes d'Interface (CE)

### CE01 — Interface Lanceur Pneumatique

| Paramètre | Valeur | Tolérance | Source |
|---|---|---|---|
| Diamètre tube (bore) | 40,0 mm | H8 | DDC-001, PRODUCT-FAMILY.md SC-06, PARAMETERS.json |
| Sabot requis | SABOT-001 | FDM ASA | PROTOTYPE_ROADMAP.md TASK_DD_004, docs/Cahier_Charges_Prototype.md v0.2 |
| Interface sabot/fuselage | Shoulder joint Ø35 × 20 mm overlap | ±0,1 mm | D3 §3.6.1 |
| Étanchéité | Joint torique NBR (section 1 mm) | — | NCR-001 (316L SS) |
| Boulons de fixation sabot | 4× M2, passo 1,4 mm, HC-90 | 0,5 N·m | D3 §3.6.1 |

### CE02 — Interface Électronique (SC-01)

| Paramètre | Valeur | Tolérance | Source |
|---|---|---|---|
| Dimensions FC board | < 30 × 30 × 10 mm | — | PRODUCT-FAMILY.md SC-01 |
| Fixation | Rail ou entretoises M2 | — | PRODUCT-FAMILY.md SC-01 |
| Consommation | ~200 mW idle | — | PRODUCT-FAMILY.md SC-01 |
| Interface | PWM / CAN / UART | — | PRODUCT-FAMILY.md SC-01 |

### CE03 — Interface Propulsion (SC-02)

| Paramètre | Valeur | Tolérance | Source |
|---|---|---|---|
| Interface mécanique | 3× vis M3 socket-head | entraxe 9/12 mm | PRODUCT-FAMILY.md SC-02 |
| Plage puissance | 50–150 W | sizing D2 CFD | PRODUCT-FAMILY.md SC-02 |
| Zone d'intégration | 280 – 380 mm (depuis nez) | — | D3_structure.md §3.2, §5 |

### CE04 — Interface Seekers & Datalink

| Paramètre | Valeur | Source |
|---|---|---|
| SC-03 (Datalink) interface UART | MAVLink ou propriétaire | PRODUCT-FAMILY.md SC-03 |
| Portée datalink DD | > 5 km LOS | PRODUCT-FAMILY.md SC-03 |
| Seeker | Ka-band radar (zone A : 0–123 mm) | D3 §3.4.4, D2 §2.4 |

---

## 5. Contraintes de Fabrication (CM)

### CM01 — Procédés et Tolérances

| Pièce | Description | Procédé | Matériau | Tolérance | Finition (Ra) | Source |
|---|---|---|---|---|---|---|
| **BRK-001** | Coque fuselage +支翼 | DMLS (SLM) | AlSi10Mg T6 | IT10 (±0,05 mm) | 1,6 μm | PARAMETERS.json, docs/manufacturing/BRK-001_machining.md |
| **ACT-001** | Vérin tubulaire 3 axes | DMLS + CNC post | AlSi10Mg T6 | IT7 (±0,015 mm) | 0,8 μm | PARAMETERS.json, docs/manufacturing/ACT-001_machining.md |
| **NCR-001** | Bague interface ogive | Tournage CNC | 316L SS | IT10 (±0,05 mm) | 3,2 μm | PARAMETERS.json, docs/manufacturing/NCR-001_machining.md |
| **SABOT-001** | Sabot lanceur | Impression 3D (FDM) | ASA | IT12 | N/A (prototype) | PROTOTYPE_ROADMAP.md |
| Fuselage AV | Corps avant | CNC turning + boring | Al-7075 T6 | IT10 | 1,6 μm | D3 §3.7 |
| Corps AR | Corps arrière | Filament winding / NC tape | CFRP | IT10 | [hors-repo] | D3 §3.7 |
| Ailes | 4× delta wings | Prepreg layup + autoclave | CFRP/PVC foam | IT10 | [hors-repo] | D3 §3.7 |
| Dérives | 4× cruciformes | Prepreg hand layup | CFRP | IT10 | [hors-repo] | D3 §3.7 |
| Motor case | Carter moteur | Deep draw + QT | AISI 4330 | IT10 | [hors-repo] | D3 §3.7 |

### CM02 — Plan d'Assurance Qualité Prototype

| Étape | Méthode | Critère | Source |
|---|---|---|---|
| Contrôle dimensionnel | Métrologie (palmer) | Conforme aux tolérances IT7/IT10 | CM01 |
| Contrôle masse | Pesée | Masse sèche ≤ 340 g (cible) / ≤ 400 g (absolue) | EM01 |
| Contrôle structure (FEA) | Simulation éléments finis | σ < 290 MPa en flexion 25 g | EM04 |
| Test pneumatique | Pressurisation 50 bar | Pas de fuite, joint NBR intact | CE01 |
| Test d'insertion tube | Montage réel | Passage tube 40 mm sans obstruction | CE01 |
| Inspection NDT | [hors-repo — protocole NDT à définir] | Non destructif pré-vol | D3 §3.7 |

---

## 6. Matrice de Conformité

| ID Req | Description | Source | Méthode de vérification | Critère | Statut |
|---|---|---|---|---|---|
| **FF01** | Démontabilité / intégration SC modules | DDC-001, D3 §3.6 | Assemblage manuel chrono | < 30 min, sans outillage spécial | 🟡 À vérifier |
| **FF02** | Géométrie cruciforme wings/fins | D2 §2.2 | Métrologie (cordes, sweep) | ±5 % sur cord/chord/sweep | 🟡 À vérifier |
| **FF03** | Intégration SC-02 propulsion | PRODUCT-FAMILY SC-02, D3 §3.6.3 | Test montage | 3× M3, sans alésage | 🟡 À vérifier |
| **FF04** | Compatibilité lanceur bore 40 mm | DDC-001, SC-06 | Test fit tube + SABOT | Centrage OK, pas d'obstruction | 🟡 À vérifier |
| **FF05** | Modularité SC-01 à SC-06 | PRODUCT-FAMILY §3.1 | Inspection visuelle | Aucun module ne requiert découpe | 🟡 À vérifier |
| **FF06** | Résistance 25 g sans déformation | D2 §2.6, D3 §3.5 | FEA + post-vol inspection | Pas de déformation plastique | ✅ D3 §3.5.2 |
| **FF07** | Transparence radôme (Ka-band) | D3 §3.4.4, D2 §2.4 | [hors-repo — test RF à définir] | Transmission signal ≥ [hors-repo] | 🔴 À faire |
| **FF08** | Transportable en mallette | D3 §3.6–3.7 | Test volume réel | ≤ 400 × 220 × 110 mm | 🟡 À vérifier |
| **EM01** | MTOW DD ≤ 400 g | PARAMETERS.json, BOM | Pesée prototype complet | ≤ 400 g (absolu) | 🔴 Non conforme (475 g) |
| **EM02** | Dimensions L=900 / Ø=35 mm | D2 §2.2 | Métrologie | ±0,5 mm | 🟡 À vérifier |
| **EM03** | Zones axiales volume allocation | D3 §3.2, §5 | Gabarit / calibre | Modules dans zones définies | 🟡 À vérifier |
| **EM04** | FS flexion ≥ 1,5 / pression ≥ 2,0 | D3 §3.5.2–3.5.3 | FEA | σ < 290 MPa (Al-7075) / FS > 2 | ✅ D3 §3.5 |
| **CE01** | Interface tube bore 40 mm + SABOT | DDC-001, SC-06, PARAMETERS.json | Test insertion réel | Passage sans obstruction | 🟡 À vérifier |
| **CE02** | Interface SC-01 (< 30×30×10 mm) | PRODUCT-FAMILY SC-01 | Contrôle dimensions | Conforme | 🟡 À vérifier |
| **CE03** | Interface SC-02 (3× M3, 9/12 mm) | PRODUCT-FAMILY SC-02 | Test montage | Montage sans alésage | 🟡 À vérifier |
| **CE04** | Interface seeker Ka-band | D3 §3.4.4 | [hors-repo — test RF] | Transparent RF | 🔴 À faire |
| **CM01** | Tolérances IT7/IT10 conformes | PARAMETERS.json, D3 §3.7 | Métrologie QC | Conforme IT7/IT10 | 🟡 À vérifier |
| **CM02** | Plan QA prototype | D3 §3.7 | NDT + pesée + FEA | Rapport QA signé | 🔴 À faire |
| — | Marque "PRELIMINARY" + statut | Ce document | Révision DG | Validation ingénieur | 🟡 En attente |

### Actions ouvertes (à répartir entre codeurs)

> Issues GitHub : #203 (FF), #204 (EM), #205 (CE), #206 (CM), #207 (Matrice de conformité + validation)

| Priority | Bloc | Actions ouvertes |
|---|---|---|
| 🔴 Haute | EM01 — Masse | Réduction 75 g : option allègement BRK-001, réduction batterie, optimisation NCR-001 |
| 🔴 Haute | CM02 — Plan QA | Définir protocole NDT ; produire rapport QA signé |
| 🔴 Haute | FF07 / CE04 | Définir protocole test RF Ka-band |
| 🟡 Moyenne | FF01–FF05 | Tests d'assemblage, intégration SC-01 à SC-06, test insertion tube |
| 🟡 Moyenne | CM01 | Vérification tolérances IT7/IT10 sur BRK-001, ACT-001, NCR-001 |
| 🟡 Moyenne | EM02–EM04 | Métrologie prototype complet + FEA validation |
| ✅ Faible | FF06, EM04 | Vérifiés par D3 §3.5 ; reste inspection post-vol |

---

## 7. Références

- DDC-001 — `docs/consolidated_definition.md`
- D2_aerodynamics.md — Baseline v1.2.0
- D3_structure.md — Baseline v1.2.0
- PRODUCT-FAMILY.md v1.1
- PARAMETERS.json v1.2.0
- PROTOTYPE_ROADMAP.md
- BOM_consolidee.md
- D1_specifications.json

---

*Document marqué PRELIMINARY — en attente de validation par Ingénierie (DG / Lead Engineer).*

*MàJ : 2026-07-03 — Jules / Agent Mammouth*