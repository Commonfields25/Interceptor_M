# Cahier des Charges Technique — Prototype Interceptor M

> **Version** : PRELIMINARY 0.1  
> **Date** : 2026-06-29  
> **Statut** : 🟡 En cours — soumis à validation Ingénierie  
> **Milestone** : [M6 — Prototype : Plans & Conception](https://github.com/Commonfields25/Interceptor_M/milestone/14)  
> **Parent** : [#34 Mechanical prototypes for machining](https://github.com/Commonfields25/Interceptor_M/issues/34)  
> **Issue livrable** : [#67 [Ingé] Cahier des charges technique](https://github.com/Commonfields25/Interceptor_M/issues/67)  
> **Classification** : Interne confidentiel —'usage restreint

---

## 1. Contexte & Objet

Ce document constitue le **cahier des charges (CDC) technique mécanique** du prototype **Interceptor M**, dans le cadre du jalon M6 — Prototype : Plans & Conception.

L'Interceptor M est un système intercepteur anti-drone / anti-essaim short-to-medium range (SHORAD), dérivé d'une plateforme modulaire commune à trois lignes produits :

| Ligne | Marché | MTOW | Statut produit |
|-------|--------|------|----------------|
| **DD** | Défense | 400 g | Actif |
| **DI** | Industriel | 300 g | BOM verrouillé |
| **DC** | Civil | 250 g | Actif |

> ⚠️ **Ligne prioritaire pour le prototype physique** : DD (défense) — volume maximal, contraintes les plus sévères. Les dimensions DC/DI sont des Scaling reductions de la plateforme commune.

**Documents de référence** :
- DDC-001 — Dossier de Définition Consolidé (`docs/consolidated_definition.md`)
- D2_aerodynamics.md, D3_structure.md
- PRODUCT-FAMILY.md v1.1
- PARAMETERS.json (`parts.BRK-001`, `parts.ACT-001`, `parts.NCR-001`)
- BOM_consolidee.md
- PROTOTYPE_ROADMAP.md

---

## 2. Objectifs du Prototype

### 2.1 But général
Produire un **prototype physique validable** de la cellule Interceptor M (ligne DD), démontrant :
- La faisabilité de fabrication (DMLS / layup / CNC)
- La conformité aux dimensions et masses cibles
- L'intégration correcte des interfaces (lanceur, électronique, propulsion)

### 2.2 Objectifs mesurables (SMART)

| # | Objectif | Critère | Valeur cible |
|---|----------|---------|-------------|
| O1 | Masse totale prototype DD | Mesurée vs théorique | ≤ 400 g (MTOW DD) |
| O2 | Conformité géométrique fuselage | Contrôle dimensions critiques | Tolérance IT10 sur dimensions clés |
| O3 | Intégrité structurelle | Résistance acceleration 25 g | Validé FEA ou test |
| O4 | Interface lanceur | Hauteur libre tube bore | 40 mm — sabot TBD |
| O5 | Assemblage pratique | Temps d'assemblage premier article | ≤ 2 h (APPU) |

---

## 3. Exigences Fonctionnelles

### FF01 — Fonction principale
Le prototype doit permettre la **validation physique** des formes, dimensions et interfaces du système intercepteur avant investissement usinage séries.

### FF02 — Configuration géométrique
Le prototype reproduit la configuration cruciforme delta-wing + rear cruciform tail fins définie en DDC-001 §2.1.

### FF03 — Intégration propulsion
Le prototype intègre une baie électronique pour le-motor (propulsion électrique), en prévision de l'insertion du propulseur solide (SRM) en phase ultérieure.

### FF04 — Interface lanceur
Le prototype est conçu pour insertion dans un tube lanceur de Øintérieur 40 mm (ligne DD et DI). L'interface sabot (SABOT-001) est à définir.

### FF05 — Modularité
Le prototype utilise l'architecture modulaire commune (SC-01 à SC-06), permettant l'échange rapide de composants entre lignes DD/DI/DC.

### FF06 — Transport & manutention
Le prototype est transportable sans outillage spécialisé. Dismontable pour expédition et réassemblage terrain.

---

## 4. Exigences Mécaniques

### EM01 — Masse

| Sous-ensemble | Masse max (DD) | Source |
|--------------|-----------------|--------|
| Coque fuselage (BRK-001) | 130,74 g | BOM_consolidee.md |
| Vérin tubulaire (ACT-001) | 55,49 g | BOM_consolidee.md |
| Carénage aéro (NCR-001) | 104,48 g | BOM_consolidee.md |
| **Total structure** | **290,71 g** | BOM_consolidee.md |
| Marge electronics/propulsion | 109,29 g | MTOW 400 g − structure |
| **MTOW total** | **400 g** | PRODUCT-FAMILY.md |

### EM02 — Dimensions fuselage DD

| Dimension | Valeur | Tolérance |
|-----------|--------|-----------|
| Longueur totale | 480,0 mm | ±0,5 mm |
| Largeur (envergure repliée) | 228,0 mm | ±0,5 mm |
| Hauteur (envergure repliée) | 120,0 mm | ±0,5 mm |
| Diamètre extérieur fuselage | 35,0 mm | IT10 |
| Diamètre tube lanceur | 40,0 mm (int.) | IT10 |
| Envergure ailes | 1 754 mm (déployée) | ±5 mm |

### EM03 — Résistance structurelle

| Critère | Valeur | Note |
|---------|--------|------|
| Charge de manœuvre | 25 g | DDC-001 §1.1 |
| Facteur de sécurité | 1,5 | Charge ultime |
| Température opérationnelle | −40 °C à +60 °C | Stockage / transport |
| Humidité relative | jusqu'à 95 % | Milieu extérieur |

### EM04 — Finitions & surface

| Pièce | Finition Ra | Tolérance IT | Technologie |
|-------|------------|-------------|-------------|
| ACT-001 (vérin) | 0,8 μm | IT7 (±0,015 mm) | DMLS CNC secondée |
| BRK-001 (coque) | 1,6 μm | IT10 (±0,05 mm) | DMLS SLM |
| NCR-001 (carénage) | 3,2 μm | IT10 (±0,05 mm) | Nomex CF layup |

---

## 5. Contraintes de Fabrication

### CM01 — Technologie primaire

| Pièce | Technologie | Matériau | Post-traitement |
|-------|-------------|----------|----------------|
| BRK-001 | DMLS (SLM) | AlSi10Mg | T6 (heat treatment) |
| ACT-001 | DMLS (SLM) | AlSi10Mg | T6 + CNC surface critique |
| NCR-001 | Layup manuel | Nomex honeycomb + CF skins | Imprégnation résine |

### CM02 — Prototype vs production
- **Phase prototype** : FDM ASA/ABS autorisée pour formes de validation (fabrication additive grand format) —ITolerances relachées IT12
- **Phase production** : DMLS / layup / CNC uniquement — conformité IT10/IT7

### CM03 — Chaîne d'approvisionnement

| Ressource | Statut | Note |
|-----------|--------|------|
| Poudre AlSi10Mg | TODO — qualifier fournisseur | 2–3 semaines lead time |
| Nomex honeycomb | TODO — qualifier fournisseur | 1–2 semaines |
| Usinage CNC | TODO — initier contact atelier | IT7 sur ACT-001 |
| DMLS service bureau | TODO — comparer prix/lead time | AlSi10Mg T6 |
| Assemblage | TODO — definir resource | Interne / sous-traitant |

---

## 6. Interfaces & Dimensions Critiques

### IE01 — Interface lanceur

| Paramètre | Valeur |
|-----------|--------|
| Tube bore diameter | 40,0 mm |
| Sabot interface (SABOT-001) | TODO — à concevoir |
| Longueur sabot | TODO — à calculer (L_lanceur − L_drone) |
| Matériau sabot | TODO — polymère ou alu |

### IE02 — Interface électronique

| Paramètre | Valeur |
|-----------|--------|
| Carte FC (SC-01) | < 30 × 30 × 10 mm |
| Baie electronics | Volume keep-out Zone — D3/E3 à définir |
| Interface connectique | PWM / CAN / UART |
| Datalink (SC-03) | UART MAVLink |
| Consommation | ~200 mW idle |

### IE03 — Interface propulsion

| Paramètre | Valeur |
|-----------|--------|
| Motor mount | 3 × M3 socket-head screws, 9 mm / 12 mm standard |
| Moteur | Brushless sizing — E2 à calculer |
| ESC | Intégré propulsion brick (SC-02) |

### IE04 — Points de fixation

| Type | Spécification |
|------|--------------|
| Visserie principale | M3 socket-head, acier inoze A2-70 |
| Visserie secondaire | M2, acier inoze A2-70 |
| Inserts | Helicoil ou equivalent pour passages répétés |

---

## 7. Matériaux

### 7.1 Aluminium AlSi10Mg (DMLS)

| Propriété | Valeur |
|-----------|--------|
| Densité | ~2,68 g/cm³ |
| Resistance traction (T6) | ~380 MPa |
| Module young | ~70 GPa |
| Durete | ~120 HB |
| Resist. corrosion | Bonne (silicium comme barrière) |
| Traitement thermique | T6 (solubilisation + revenu) |
| Finition surface max | Ra 0,8 μm (CNC post) |

### 7.2 Nomex Honeycomb + Fiber Composite (CF skins)

| Propriété | Valeur |
|-----------|--------|
| Densité core | ~48 kg/m³ |
| Resistance compression | ~3 MPa (core) |
| Finitions | Ra 3,2 μm (surface CF) |
| Traitement | Imprégnation résine époxy |

---

## 8. Jalons & Livrables

| Jalon | Livrable | Date cible | Statut |
|-------|----------|-----------|--------|
| J1 | CDC validé (ce document) | TODO — interne | 🟡 En cours |
| J2 | BOM préliminaire validé | TODO | 🔴 À faire |
| J3 | Fiche matériaux/tolérances validée | TODO | 🔴 À faire |
| J4 | Plan interfaces validé | TODO | 🔴 À faire |
| J5 | Dossier plansstructural | TODO | 🔴 À faire |
| J6 | Prototype physique manufactured | TODO | 🔴 À faire |

---

## 9. Points Ouverts (TODO)

| # | Point ouvert | Responsable | Priorité |
|---|-------------|-------------|---------|
| T1 | Confirmer MTOW DI avec le produit (actuellement 300g provisioie) | Produit | Haute |
| T2 | Qualifier fournisseur poudre AlSi10Mg | Achats | Haute |
| T3 | Concevoir SABOT-001 (interface sabot) | Ingénierie | Haute |
| T4 | Définir baie électronique (volume keep-out) | E3 | Moyenne |
| T5 | Comparer prix/lead time DMLS service bureaus | Achats | Moyenne |
| T6 | Valider choix mousse Nomex (density grade) | Ingénierie | Moyenne |
| T7 | Plan de test résistance 25 g | Ingénierie | Basse |

---

*Document produit dans le cadre de Vague 6 — Prototype : Plans & Conception.*  
*Derniere mise a jour : 2026-06-29*