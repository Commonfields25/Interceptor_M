---
agent: Jules
action: Update
timestamp: 2026-06-30T17:30:00Z
status: PRELIMINARY
---

# Cahier des Charges Technique — Prototype Interceptor M

> **Version** : PRELIMINARY 0.2
> **Date** : 2026-06-30
> **Statut** : 🟡 En cours — Basé sur Baseline v1.5
> **Classification** : Interne confidentiel

---

## 1. Contexte & Objet

Ce document définit les exigences techniques mécaniques du prototype **Interceptor M** (Ligne DD - Defense). Il consolide les données issues de la Baseline v1.5 et du fichier `PARAMETERS.json`.

L'Interceptor M est un drone intercepteur modulaire. Le prototype vise à valider la structure primaire et les interfaces critiques avant le passage en production.

---

## 2. Énoncés Fonctionnels (FF)

| ID | Fonction | Critère d'acceptation |
|---|---|---|
| **FF01** | Validation Physique | Le prototype permet de vérifier l'encombrement et l'assemblage manuel. |
| **FF02** | Configuration | Géométrie cruciforme avec ailes delta (envergure 150mm repliée / 1754mm déployée). |
| **FF03** | Intégration Propulsion | Baie moteur compatible avec le module SC-02 (Propulsion Brick). |
| **FF04** | Interface Lanceur | Insertion fluide dans un tube de 40mm avec le sabot SABOT-001. |
| **FF05** | Modularité | Utilisation des modules SC-01 à SC-06 sans modification structurelle. |
| **FF06** | Manutention | Démontable et transportable en mallette standard. |

---

## 3. Exigences Mécaniques (EM)

### EM01 — Masse (Ligne DD)

| Sous-ensemble | Masse Cible (g) | Matériau | Source |
|--------------|-----------------|----------|--------|
| **BRK-001** (Coque + Ailes) | 130,74 | AlSi10Mg | BOM v1.5 |
| **ACT-001** (Vérin) | 55,49 | AlSi10Mg | BOM v1.5 |
| **NCR-001** (Bague/Ogive) | 104,48 | 316L SS | BOM v1.5 |
| **SABOT-001** (Interface) | 15,00 | FDM ASA | BOM v1.5 |
| **Masse Sèche Totale** | **305,71** | — | Calculé |
| **MTOW (Vol)** | **321,21** | — | DG Decision |
| **Plafond MTOW** | **400,00** | — | Spec E1 |

### EM02 — Dimensions (Ligne DD)

| Paramètre | Valeur | Tolérance | Source |
|-----------|--------|-----------|--------|
| Longueur Fuselage | 380,0 mm | ±0,5 mm | PARAMETERS.json |
| Largeur (W) | 200,0 mm | ±0,5 mm | PARAMETERS.json |
| Hauteur (H) | 100,0 mm | ±0,5 mm | PARAMETERS.json |
| Diamètre Ext. Fuselage | 35,0 mm | IT10 | PARAMETERS.json |
| Épaisseur Coque | 2,0 mm | ±0,1 mm | PARAMETERS.json |

### EM03 — Résistance & Environnement

| ID | Exigence | Valeur | Note |
|---|---|---|---|
| **EM03.1** | Facteur de charge | 25 g | Manœuvre limite |
| **EM03.2** | Facteur de sécurité | 1,5 | Charge ultime |
| **EM03.3** | Température | -40°C à +60°C | Opérationnel |

---

## 4. Contraintes d'Interface (CE)

### CE01 — Interface Lanceur
- **Diamètre Tube** : 40,0 mm (Bore).
- **Sabot** : SABOT-001 requis pour centrage et étanchéité pneumatique.

### CE02 — Électronique (SC-01)
- **Volume** : < 30 × 30 × 10 mm.
- **Fixation** : Rail ou entretoises M2.

### CE03 — Propulsion (SC-02)
- **Interface** : 3 vis M3, entraxe standard 9/12mm.

---

## 5. Contraintes de Fabrication (CM)

| Pièce | Procédé | Matériau | Tolérance | Finition (Ra) |
|-------|---------|----------|-----------|---------------|
| **BRK-001** | DMLS (SLM) | AlSi10Mg T6 | IT10 | 1,6 μm |
| **ACT-001** | DMLS + CNC | AlSi10Mg T6 | IT7 | 0,8 μm |
| **NCR-001** | Tournage CNC | 316L SS | IT10 | 3,2 μm |
| **SABOT-001**| Impression 3D| ASA | IT12 | N/A |

---

## 6. Matrice de Conformité

| ID Req | Description | Méthode | Statut |
|---|---|---|---|
| EM01 | Masse DD < 400g | Pesée | ✅ (321g target) |
| EM02 | Dimensions L/W/H | Métrologie | 🟡 À vérifier |
| EM03 | Résistance 25g | Simulation FEA | ✅ (D3_structure) |
| CE01 | Passage tube 40mm | Test Fit | 🟡 À vérifier |
| CM01 | Tolérance IT7 (ACT) | Contrôle Qualité| 🔴 À faire |

---
*Fin du document.*
