---
agent: agent_worker
action: Create
timestamp: 2026-07-05T13:54:00Z
status: PRELIMINARY
related_gate: G2
---

# Plan Qualité — Prototype Interceptor M (DD-400)

> **Version** : PRELIMINARY 1.0
> **Date** : 2026-07-05
> **Statut** : 🟡 En cours — Squelette initial, à compléter
> **Référence** : Cahier_Charges_Prototype.md §CM02
> **Classification** : Interne confidentiel

---

## 1. Objet & Périmètre

Ce Plan Qualité (QA Plan) définit les contrôles, essais et critères d'acceptation pour la fabrication et la validation du prototype **Interceptor M** (DD-400). Il est issu des contraintes de fabrication documentées dans le Cahier des Charges Prototype §CM01–CM02.

**Documents de référence :**
- `docs/Cahier_Charges_Prototype.md` v1.1 PRELIMINARY
- `manufacturing/BOM_consolidee.md` v1.2.0
- `manufacturing/*_notes.md` (gammes usinage)
- `PARAMETERS.json` v1.2.0

---

## 2. Sous-ensembles & Critères d'Acceptation

### 2.1 BRK-001 — Coque + Ailes (AlSi10Mg DMLS)

| Critère | Spécification | Méthode | Tolérance | Statut |
|---------|--------------|---------|-----------|--------|
| Longueur fuselage | 380,0 mm | Métrologie 3D | ±0,5 mm | 🟡 À vérifier |
| Largeur (W) | 200,0 mm | Métrologie 3D | ±0,5 mm | 🟡 À vérifier |
| Hauteur (H) | 100,0 mm | Métrologie 3D | ±0,5 mm | 🟡 À vérifier |
| Diamètre ext. fuselage | 35,0 mm | CMU / micromètre | IT10 ±0,05 mm | 🟡 À vérifier |
| Épaisseur paroi | 2,0 mm | CND / ultrason | ±0,1 mm | 🟡 À vérifier |
| Tolérance dimensionnelle | IT10 | CMU contrôle qualité | ±0,05 mm | 🟡 À faire |
| Finition de surface | Ra 1,6 μm | Rugosimètre | — | 🟡 À faire |
| Alésage moteur Ø9 H8 @r32 | Ø9,0 mm | Tampon / CMU | H8 | 🟡 À faire |
| Alésage bras Ø5 H8 @r20 | Ø5,0 mm | Tampon / CMU | H8 | 🟡 À faire |

**Gamme usinage de référence :** `manufacturing/BRK-001_gamme_usinage.md`

### 2.2 ACT-001 — Vérin Tubulaire (AlSi10Mg DMLS + CNC)

| Critère | Spécification | Méthode | Tolérance | Statut |
|---------|--------------|---------|-----------|--------|
| Tolérance dimensionnelle | IT7 | CMU contrôle qualité | ±0,015 mm | 🟡 À faire |
| Finition de surface | Ra 0,8 μm | Rugosimètre | — | 🟡 À faire |
| Volume réservation FC | 30,5 × 30,5 × 8,5 mm | Vérification 3D | — | 🟡 À faire |
| Volume réservation ESC | 30,5 × 15,5 × 8,5 mm | Vérification 3D | — | 🟡 À faire |
| Fixation 3× M3 @ entraxe 9/12 mm | Perçages M3 | Gabarit / CMU | — | 🟡 À faire |

**Notes de fabrication :** `manufacturing/ACT-001_notes.md`

### 2.3 NCR-001 — Bague/Ogive (316L SS, Tournage CNC)

| Critère | Spécification | Méthode | Tolérance | Statut |
|---------|--------------|---------|-----------|--------|
| Gorge joint torique | Ø36,5 × 2,8 mm | CMU | IT10 | 🟡 À faire |
| Alésage central | Ø35 H7 mm | Tampon H7 | IT10 ±0,05 mm | 🟡 À faire |
| 4× perçages M3 @r20 | M3, entraxe 20 mm | Gabarit | — | 🟡 À faire |
| Tolérance globale | IT10 | CMU contrôle qualité | ±0,05 mm | 🟡 À faire |

**Notes de fabrication :** `manufacturing/NCR-001_notes.md`

### 2.4 SABOT-001 — Sabot Interface (ASA, FDM)

| Critère | Spécification | Méthode | Tolérance | Statut |
|---------|--------------|---------|-----------|--------|
| Compatibilité tube bore 40 mm | Fit fluide | Test insertion | — | 🟡 À faire |
| Étanchéité pneumatique | Zero fuite @ 5 bar | Test pression | — | 🟡 À faire |
| Tolérance prototype | IT12 | Contrôle visuel | — | 🟡 À faire |

---

## 3. Contrôles Communs

| Contrôle | Fréquence | Méthode | Critère | Responsable |
|---------|-----------|---------|---------|-------------|
| Pesée complète assemblé | Chaque prototype | Balance ±0,01 g | ≤ 475 g (MTOW DG) | Atelier |
| Contrôle dimensionnel global | Chaque prototype | Bras métrologique | 380 × 200 × 100 mm ±0,5 | QC |
| Test insertion lanceur | Chaque prototype | Insertion manuelle | Fit fluide, zero bind | Atelier |
| Test étanchéité pneumatique | Chaque prototype | Pression 5 bar / 30 s | Zero fuite détectable | QC |
| Vérification volume allocation interne | Chaque prototype | Revue 3D | Zones 0–380 mm respectées | Ingénierie |
| Inspection surface DMLS | Chaque pièce | Visuel + rugosimètre | Ra ≤ valeur spec | QC |

---

## 4. Équipements de Contrôle

| Équipement | Usage | Référence |
|-----------|-------|-----------|
| Balance analytique ±0,01 g | Pesée masse | Atelier |
| CMU 0–150 mm / lecture 0,01 mm | Contrôle dimensionnel | QC |
| Tampons lisse/alésoir Ø35 H7 | Alésage NCR-001 | QC |
| Rugosimètre portable | Ra surfaces DMLS | QC |
| Banc de pression pneumatique | Test étanchéité SABOT-001 | Atelier |

---

## 5. Non-Conformités & Actions Correctives

Toute non-conformité fait l'objet d'un **Rapport de Non-Conformité (NCR)** selon le modèle `templates/NON_CONFORMITY_REPORT.md`.

| Situations possibles | Action |
|--------------------|--------|
| MTOW > 475 g | NCR → réduction masse (alésage, allègement structurel) |
| IT non respectée | NCR → retouche ou refabrication |
| Fuite pneumatique | NCR → reprise SABOT-001 ou NCR-001 |
| Fit lanceur non fluide | NCR → ajustement géométrique |

---

## 6. Statut & Jalons

| Jalon | Date Cible | Critère |
|-------|-----------|---------|
| Révision initiale squelette | 2026-07-05 | Squelette créé ✅ (ce document) |
| Validation Ingénierie | [à confirmer] | Revue équipe Ingénierie |
| Gate G2 — Approbation Prototype | [à confirmer] | Tous critères d'acceptation verts ✅ |

---

## 7. Références

| Réf. | Document |
|------|----------|
| CM01 | Cahier §CM01 — Tolérances & Procédés |
| CM02 | Cahier §CM02 — Gammes Usinage |
| E1 | PARAMETERS.json §E1 (BRK-001) |
| E2 | PARAMETERS.json §E2 (NCR-001) |
| E3 | PARAMETERS.json §E3 (ACT-001) |
| BOM | manufacturing/BOM_consolidee.md |
| NCR | templates/NON_CONFORMITY_REPORT.md |

---
*PRELIMINARY — Plan Qualité en attente de validation Ingénierie.*
*Ce document est un squelette initial (PRELIMINARY) — compléter avant Gate G2.*
