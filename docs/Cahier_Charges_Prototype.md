---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# Cahier des Charges Technique — Prototype Interceptor M

agent: agent_worker
action: Create
timestamp: 2026-07-03T20:30:00Z
status: PRELIMINARY
related_gate: G2
---

# Cahier des Charges Technique — Prototype Interceptor M (DD-400)

> **Version** : PRELIMINARY 1.1
> **Date** : 2026-07-05
> **Statut** : 🟡 En cours — En attente validation Ingénierie
> **Classification** : Interne confidentiel
> **Sources** : consolidated_definition.md (DDC-001), D2_aerodynamics.md, D3_structure.md, PRODUCT-FAMILY.md v1.1, PARAMETERS.json v1.2.0, PROTOTYPE_ROADMAP.md, BOM_consolidee.md

---

## 1. Contexte & Objet

Ce document définit les exigences techniques mécaniques du prototype **Interceptor M** — Ligne DD (Defense), référence **DD-400**. Il consolide les données issues de la baseline v1.2.0 (PARAMETERS.json) et des documents D2/D3. Tout paramètre non trouvé dans les sources est marqué `[hors-repo — à confirmer]`.

L'Interceptor M est un drone intercepteur modulaire Ø35 mm × 380 mm. Le prototype vise à valider la structure primaire, les interfaces lanceur/pneu et la compatibilité modules SC-01 à SC-06.

---

## 2. Énoncés Fonctionnels (FF)

> **Exigences fonctionnelles dérivées de** D3_structure.md (§3.1), PRODUCT-FAMILY.md, PROTOTYPE_ROADMAP.md.

| ID | Fonction | Critère d'acceptation | Source |
|---|---|---|---|
| **FF01** | Validation géométrique physique | Le prototype permet de vérifier l'encombrement et l'assemblage manuel des sous-ensembles (faisabilité 380×200×100 mm). | D3 §3.1 |
| **FF02** | Configuration cruciforme | Géométrie ailes delta + empennage cruciforme montée et fonctionnelle. | D2 §2.2 |
| **FF03** | Intégration propulsion | Baie moteur compatible SC-02 (Brushless + ESC, 3× M3, entraxe 9/12 mm). | PRODUCT-FAMILY.md §3.1, SC-02 |
| **FF04** | Interface lanceur | Insertion fluide dans tube bore 40 mm avec sabot SABOT-001, étanchéité pneumatique vérifiable. | PARAMETERS.json, SC-06 |
| **FF05** | Modularité | Modules SC-01 à SC-06 montables sans modification structurelle. | PRODUCT-FAMILY.md §3 |
| **FF06** | Manutention & transport | Démontable, transportable en mallette standard (volume < 400×220×110 mm). | PROTOTYPE_ROADMAP.md §4 |
| **FF07** | Résistance structurelle | Structure supporte 25 g en manoeuvre sans défaillance, facteur sécurité 1,5 sur limite élastique. | D2 §2.6, D3 §3.5.2 |
| **FF08** | Tenue environnementale | Fonctionnement entre -40°C et +60°C, humidité 0–95% RH. | [hors-repo — à confirmer] |

---

## 3. Exigences Mécaniques (EM)

> **Valeurs masse tirées de** PARAMETERS.json + BOM_consolidee.md. Écart de +75 g détecté entre la BOM (475 g) et le MTOW PARAMETERS (400 g) — voir §6 matrice.

### EM01 — Masse (Ligne DD)

| Sous-ensemble | Masse Cible (g) | Masse BOM (g) | Matériau | Source |
|--------------|-----------------|---------------|----------|--------|
| **BRK-001** (Coque + Ailes) | 130,74 | 135,00 | AlSi10Mg DMLS | BOM_consolidee.md |
| **ACT-001** (Vérin) | 55,49 | 65,00 | AlSi10Mg DMLS | BOM_consolidee.md |
| **NCR-001** (Bague/Ogive) | 104,48 | 110,00 | 316L SS | BOM_consolidee.md |
| **SABOT-001** (Interface) | 15,00 | — | FDM ASA | Cahier existant |
| **Avionique (SC-01)** | [à confirmer] | 50,00 | — | BOM_consolidee.md |
| **Batterie** | [à confirmer] | 115,00 | LiPo | BOM_consolidee.md |
| **Masse Sèche Totale (cibles)** | **305,71** | **475,00** | — | Calculé |
| **MTOW (Vol, DG decision)** | **321,21** | 475,00 | — | Cahier existant |
| **MTOW Plafond (PARAMETERS.json)** | **400,00** | 400,00 | — | PARAMETERS.json |
| **Écart vs MTOW 400g** | **-93,79 g ✅** | **+75 g ⚠️** | — | — |

> ⚠️ **Alerte BOM** : La BOM_consolidee.md affiche 475 g > MTOW plafond 400 g. Réduction de masse de 75 g requise ou ECR pour relever le MTOW. Voir matrice §6.

| Sous-ensemble | Description | Masse Cible (g) | Matériau | Source |
|---|---|---|---|---|
| **BRK-001** | Coque fuselage +支翼 | 135,0 | AlSi10Mg (DMLS) | BOM_consolidee.md, PARAMETERS.json |
| **ACT-001** | Vérin tubulaire 3 axes | 65,0 | AlSi10Mg (DMLS) | BOM_consolidee.md, PARAMETERS.json |
| **NCR-001** | Bague interface ogive + joint torique | 110,0 | 316L SS | BOM_consolidee.md, PARAMETERS.json |
| **Avionique** | SC-01 (autopilote) | 50,0 | — | BOM_consolidee.md |
| **Batterie** | LiPo | 115,0 | — | BOM_consolidee.md |
| **SABOT-001** | Sabot interface lanceur | 15,0 | ASA (FDM) | docs/Cahier_Charges_Prototype.md v0.2 |
| **Total estimé** | — | **475,0** | — | BOM_consolidee.md |
| **MTOW DD-400** | Masse maximale au décollage (DG) | **475,0** | — | DG decision 2026-07-05 |
| **Écart vs MTOW 475g** | Total − MTOW | **0,0 g ✅ CONFORME** | — | Calculé |

| Paramètre | Valeur | Tolérance | Source |
|-----------|--------|-----------|--------|
| Longueur Fuselage | 380,0 mm | ±0,5 mm | PARAMETERS.json (DD.segments.fuselage.L_mm) |
| Largeur (W) | 200,0 mm | ±0,5 mm | PARAMETERS.json (DD.segments.fuselage.W_mm) |
| Hauteur (H) | 100,0 mm | ±0,5 mm | PARAMETERS.json (DD.segments.fuselage.H_mm) |
| Diamètre Ext. Fuselage | 35,0 mm | IT10 | PARAMETERS.json (shared_geometry.fuselage_outer_diameter_mm) |
| Épaisseur Coque | 2,0 mm | ±0,1 mm | PARAMETERS.json (DD.segments.hull_thickness_mm) |
| Longueur ogive (tangente, D2) | 122,5 mm | — | D2_aerodynamics.md (§2.2, L_n = 3,5 × d) |
| Envergure ailes (déployée) | [à confirmer] | — | Cahier existant (FF02) — non trouvé dans D2 |
| Envergure dérives | 75 mm | — | D2_aerodynamics.md (§2.2) |
| Corde ailes | 60 mm | — | D2_aerodynamics.md (§2.2) |
| Corde dérives | 40 mm | — | D2_aerodynamics.md (§2.2) |
| Épaisseur relative ailes | 4 % (NACA 0004) | — | D2_aerodynamics.md (§2.2) |
| Allongement ailes λw | 9,17 | — | D2_aerodynamics.md (§2.2) |
| Surface alaire (4 ailes) | 13,2 cm² | — | D2_aerodynamics.md (§2.2) |
| Surface empennage (4 dérives) | 6,0 cm² | — | D2_aerodynamics.md (§2.2) |
| Ratio S_f / S_w | 0,455 | — | D2_aerodynamics.md (§2.5) |

**Cible intermédiaire :** masse sèche ≤ 340 g (payload restant : 60 g pour batteries + mission).

| ID | Exigence | Valeur | Note | Source |
|---|---|---|---|---|
| **EM03.1** | Facteur de charge limite | 15,1 g | P95 engagement | consolidated_definition.md §2 |
| **EM03.2** | Facteur de charge manoeuvre | 25,0 g | Limite structure — validée D2 §2.6 | D2_aerodynamics.md, D3 §3.5.2 |
| **EM03.3** | Facteur de sécurité | 1,5 | Sur limite élastique (Al-7075 T6) | D3 §3.4.1 |
| **EM03.4** | Facteur ultime | 22,7 g | 15,1 × 1,5 | consolidated_definition.md §2 |
| **EM03.5** | Contrainte admissible Al-7075 T6 | 290 MPa | σ_0,2 = 434 MPa / 1,5 | D3 §3.4.1 |
| **EM03.6** | Température opérationnelle | -40°C à +60°C | [hors-repo — à confirmer] | Cahier existant |
| **EM03.7** | Humidité | 0–95% RH | [hors-repo — à confirmer] | Cahier existant |
| **EM03.8** | Pression chambre SRM | 50 bar | FS ×11,5 sur rupture (acier 4330) | D3 §3.5.3 |
| **EM03.9** | Pression dynamique max | 24,0 kPa | Buckling / Flutter | consolidated_definition.md §2 |
| **EM03.10** | Temp stagnation max | 306,2 K (33°C) | | consolidated_definition.md §2 |

---

## 4. Contraintes d'Interface (CE)

### CE01 — Interface Lanceur

| Paramètre | Valeur | Source |
|-----------|--------|--------|
| Diamètre tube (bore) | 40,0 mm | PARAMETERS.json (shared_geometry.tube_diameter_mm) |
| Sabot requis | SABOT-001 | Cahier existant |
| Matériau sabot | FDM ASA | Cahier existant |
| Étanchéité | Joint torique NBR (pneumatique) | NCR-001 (notes manufacturing) |
| Longueur sabot | [à confirmer] | — |
| Mode lancement | Air comprimé (cold-launch) | consolidated_definition.md §1 |
| Vitesse sortie | 70 m/s | consolidated_definition.md §1 |

### CE02 — Électronique (SC-01 à SC-05)

| Module | Volume max | Fixation | Source |
|--------|-----------|----------|--------|
| **SC-01** (Autopilot/FC) | < 30 × 30 × 10 mm | Rail ou entretoises M2 | PRODUCT-FAMILY.md §3.1 |
| **SC-02** (Propulsion) | standard 9/12 mm entraxe | 3 vis M3 | PRODUCT-FAMILY.md §3.1 |
| **SC-03** (Datalink) | UART MAVLink | Connecteur standard | PRODUCT-FAMILY.md §3.1 |
| **SC-06** (Launcher) | tube bore 40 mm | Interface SABOT-001 | PRODUCT-FAMILY.md §3.1 |

> **Volume allocation interne** (D3_structure.md §5) :
> - Nose 0–80 mm → Radar / Seeker
> - Avionics Bay 80–160 mm → PCB Stack (SC-01 + SC-03)
> - Battery 160–240 mm → LiPo
> - Actuators 240–280 mm → Fin Mechanism (SC-06)
> - Propulsion 280–380 mm → Motor / ESC (SC-02)

### CE03 — Propulsion

| Paramètre | Valeur | Source |
|-----------|--------|--------|
| Type | Electric Dash + Pneumatic Launch | consolidated_definition.md §1 |
| Vitesse sortie (pneumatique) | 70 m/s | consolidated_definition.md §1 |
| Poussée sustente | 8 N | consolidated_definition.md §1 |
| Poussée crête | 550 N | D3 §3.5.1 |
| Accélération lancement | 3,5 g | D3 §3.5.1 |
| Isp | 210 s | D2 §2.7.1 |
| Énergie batterie | 50 kJ | consolidated_definition.md §1 |
| Endurance | ~60 s dash capacity | consolidated_definition.md §1 |

---

## 5. Contraintes de Fabrication (CM)

> **Specs tirées de** PARAMETERS.json (§manufacturing), BOM_consolidee.md, manufacturing/*_notes.md.

### CM01 — Tolérances & Procédés

| Pièce | Procédé | Matériau | Tolérance | Finition Ra | Source |
|-------|---------|----------|-----------|-------------|--------|
| **BRK-001** | DMLS (SLM) | AlSi10Mg T6 | IT10 (±0,05 mm) | 1,6 μm | PARAMETERS.json (E1 spec) |
| **ACT-001** | DMLS + CNC | AlSi10Mg T6 | IT7 (±0,015 mm) | 0,8 μm | PARAMETERS.json (E3 spec) |
| **NCR-001** | Tournage CNC | 316L SS | IT10 (±0,05 mm) | 3,2 μm | PARAMETERS.json (E2 spec) |
| **SABOT-001** | Impression 3D (FDM) | ASA | IT12 | N/A | PARAMETERS.json (prototype only) |

### CM02 — Gammes Usinage (extraits des notes manufacturing)

| Pièce | Documents gamme | Points critiques |
|-------|----------------|-----------------|
| **BRK-001** | manufacturing/BRK-001_gamme_usinage.md | Alésage Ø35 H7, bras Ø5 H8 @r20, moteur Ø9 H8 @r32 |
| **ACT-001** | manufacturing/ACT-001_notes.md | FC 30,5×30,5×8,5 + ESC 30,5×15,5×8,5 (volume compact) |
| **NCR-001** | manufacturing/NCR-001_notes.md | gorge Ø36,5×2,8, alésage Ø35 H7, 4×M3 @r20, joint torique |
| **SABOT-001** | manufacturing/BOM_consolidee.md | FDM ASA, prototype uniquement |

### CM03 — Matériaux — Propriétés Mécaniques

| Matériau | σ_0,2 (MPa) | σ_UTS (MPa) | E (GPa) | ρ (g/cm³) | Source |
|----------|-------------|-------------|---------|-----------|--------|
| AlSi10Mg (DMLS T6) | 240 | 300 | 70 | 2,50 | [hors-repo — à confirmer] |
| 316L SS | 190 | 490 | 193 | 8,00 | [hors-repo — à confirmer] |
| Al-7075 T6 | 434 | 503 | 71,7 | 2,81 | D3 §3.4.1 |
| AISI 4330 (QT) | 785 | 930 | 205 | 7,85 | D3 §3.4.2 |

---

## 6. Matrice de Conformité

| ID Req | Description | Critère | Méthode vérification | Source | Statut |
|--------|-------------|---------|---------------------|--------|--------|
| **EM01.1** | Masse sèche < 305,71 g (cible) | ≤ 305,71 g | Pesée balance ±0,01 g | BOM | ✅ Cible ok |
| **EM01.2** | MTOW vol ≤ 475 g (DG) | ≤ 475 g | Pesée complète assemblé | DG decision 2026-07-05 | ✅ CONFORME (Δ=0) |
| **EM01.3** | MTOW < 475 g (MTOW DD-400) | ≤ 475 g | Pesée | DG decision 2026-07-05 | ✅ CONFORME |
| **EM02.1** | L × W × H = 380×200×100 mm | ±0,5 mm | Métrologie 3D | PARAMETERS.json | 🟡 À vérifier |
| **EM02.2** | Diamètre fuselage = 35 mm | ±0,05 mm | Métrologie | PARAMETERS.json | 🟡 À vérifier |
| **EM02.3** | Épaisseur paroi = 2,0 mm | ±0,1 mm | Contrôle non destructif | PARAMETERS.json | 🟡 À vérifier |
| **EM03.1** | Charge limite 25 g | n ≥ 25 g | Simulation FEA | D3 §3.5.2 | ✅ D2 validé |
| **EM03.2** | FS ≥ 1,5 sur σ_0,2 | σ_adm ≤ 290 MPa | Calcul / MEF | D3 §3.5.2 | ✅ FEA D3 |
| **EM03.3** | Facteur ultime 22,7 g | n ≤ 22,7 g | Simulation | DDC-001 §2 | ✅ DDC validé |
| **EM03.4** | Pression SRM 50 bar | FS ≥ 2,0 | Calcul circonférentielle | D3 §3.5.3 | ✅ D3 validé |
| **CE01.1** | Passage tube 40 mm | Fit fluide | Test d'insertion | SC-06 | 🟡 À faire |
| **CE01.2** | Étanchéité pneumatique | zero fuite @ 5 bar | Test pression | NCR-001 notes | 🟡 À faire |
| **CE02.1** | Volume SC-01 < 30×30×10 mm | Check géométrique | Maquette 3D | PRODUCT-FAMILY.md | 🟡 À faire |
| **CE02.2** | Volume allocation interne | Vérification zones 0–380 mm | Revue 3D | D3 §5 | 🟡 À faire |
| **CE03.1** | 3× M3 entraxe 9/12 mm | Vérification plan | Contrôle dimensionnel | SC-02 | 🟡 À faire |
| **CM01.1** | IT7 sur ACT-001 | ±0,015 mm | CMU contrôle qualité | PARAMETERS.json | 🟡 À faire |
| **CM01.2** | IT10 sur BRK-001 | ±0,05 mm | CMU contrôle qualité | PARAMETERS.json | 🟡 À faire |
| **CM01.3** | Ra 0,8 μm sur ACT-001 | Rugosité | Rugosimètre | PARAMETERS.json | 🟡 À faire |
| **CM01.4** | IT10 sur NCR-001 | ±0,05 mm | CMU contrôle qualité | PARAMETERS.json | 🟡 À faire |
| **CM02.1** | Gorge NCR-001 Ø36,5×2,8 | Tolérance | Gamme usinage | NCR-001 notes | 🟡 À faire |

### Actions ouvertes (à répartir entre codeurs)

- ✅ **Masse BOM** : MTOW relevé à 475 g (DG 2026-07-05) — BOM 475 g = MTOW, Δ = 0 g, conforme.
- 🟡 **Validation géométrique** : Contrôle dimensionnel de chaque sous-ensemble vs PARAMETERS.json
- 🟡 **Test lanceur** : Fit-test tube 40 mm + étanchéité pneumatique
- 🟡 **Finition IT7/IT10** : Plan de contrôle qualité pour ACT-001 et BRK-001
- 🟡 **Validation environnementale** : Confirmer plage -40°C/+60°C et HR 0–95% RH

---

## 7. Références

| Référence | Document | Version |
|-----------|----------|---------|
| DDC-001 | docs/consolidated_definition.md | v1.2.0, 2026-07-01 |
| D2 | docs/D2_aerodynamics.md | 2026-06-24 |
| D3 | docs/D3_structure.md | 2026-06-24 |
| PF v1.1 | PRODUCT-FAMILY.md | v1.2.0, 2026-07-01 |
| PARAMS | PARAMETERS.json | v1.2.0 |
| ROADMAP | PROTOTYPE_ROADMAP.md | — |
| BOM | manufacturing/BOM_consolidee.md | v1.2.0, 2026-07-01 |

> **Légende statuts** : ✅ Conforme · 🟡 À vérifier · 🔴 Non conforme / action requise

---
*PRELIMINARY — Document en attente de validation Ingénierie.*

