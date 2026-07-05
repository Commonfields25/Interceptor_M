---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# BOM Préliminaire — Interceptor M (Vague 6)
**Issue:** #68  
**Parent:** #34  
**Version:** 1.0  
**Classification:** Interne  
**Source:** `manufacturing/BOM_consolidee.md` + `PARAMETERS.json` (v1.0.1)

---

## 1. Nomenclature — Pièces Mécaniques

| Réf. | Désignation | Matériau | Tech. Primaire | Tech. Secondaire | Qté/APU | TRL |
|------|-------------|----------|---------------|-----------------|---------|-----|
| BRK-001 | Coque fuselage +支翼 | AlSi10Mg (DMLS) | DMLS (SLM) | CNC IT10 | 1 | **7** — prototype usiné validé |
| ACT-001 | Vérin tubulaire 3 axes | AlSi10Mg (DMLS) | DMLS (SLM) | CNC IT7 | 1 | **7** |
| NCR-001 | Carénage aero complexe | Nomex honeycomb + CF skins | Layup manual | FDM (proto) | 1 | **6** |
| OR-112-NBR | Joint torique NBR AS568-112 | NBR 70 Shore A | Acheté | — | ≥2 | **9** |
| FAST-01 | Visserie M2/M2.5 Inox A2 | A2-70 stainless | Acheté | — | ~12 | **9** |

## 2. Nomenclature — Électronique / Chaîne de Propulsion

*(issues #83+ — en cours d'estimation par E3)*

## 3. Masse Estimée vs MTOW par Ligne

| Réf. | Masse DC (250g) | Masse DI (300g) | Masse DD (400g) | Δ vs MTOW |
|------|----------------|----------------|----------------|-----------|
| BRK-001 | 111.78g | 118.78g | 130.74g | — |
| ACT-001 | 55.49g | 55.49g | 55.49g | — |
| NCR-001 | 89.33g | 95.71g | 104.48g | — |
| OR-112-NBR | ~3g | ~3g | ~3g | — |
| FAST-01 | ~5g | ~5g | ~5g | — |
| **TOTAL** | **265g** | **278g** | **299g** | |
| **MTOW** | 250g | 300g | 400g | |
| **Ratio** | **106% ⚠️** | **92.7% ✅** | **74.7% ✅** | ⚠️ DC hors cible |

> **Note :** Le ratio structure/MTOW pour DC dépasse 100% — une optimisation (alvéolaire BRK-001, réduction NCR-001) est nécessaire avant la proto-batch. Voir `engineering/DI_SPEC_LOCK.md`.

## 4. Statut TRL par Pièce

| Réf. | TRL actuel | Bilan | Gate cible |
|------|-----------|-------|-----------|
| BRK-001 | 7 | Prototype usiné; validation E2/E1 en attente | G2 |
| ACT-001 | 7 | Prototype usiné; validation E2 en attente | G2 |
| NCR-001 | 6 | Layup manuel validé; qualification DMLS en cours | G2 |
| OR-112-NBR | 9 | Composant commercial — prête à l'achat | G1 |
| FAST-01 | 9 | Visserie standard — prête à l'achat | G1 |

## 5. Propositions Technologie — Analyse Build/Make

| Réf. | Tech. actuelle | Tech. proposée (optimisation) | Gain masse estimé |
|------|---------------|-------------------------------|------------------|
| BRK-001 | DMLS AlSi10Mg plein | DMLS AlSi10Mg alvéolaire (lattice) | −15 à −20g |
| ACT-001 | DMLS AlSi10Mg plein | DMLS AlSi10Mg alvéolaire ou CNC 7075-T6 | −5 à −10g |
| NCR-001 | Layup Nomex CF | DMLS Nomex ou formage复合材料 | À évaluer |

> **Recommandation :** Lancer étude d'optimisation topologique BRK-001 (SLM lattice) avant la proto-batch DC.

## 6. Delta BOM Préliminaire vs BOM Consolidée

| Réf. | BOM consol. | BOM prélim. | Δ | Commentaire |
|------|-----------|------------|---|-------------|
| BRK-001 | ✅ présent | ✅ présent | 0 | Conforme |
| ACT-001 | ✅ présent | ✅ présent | 0 | Conforme |
| NCR-001 | ✅ présent | ✅ présent | 0 | Conforme |
| OR-112-NBR | ❌ absent | ✅ ajouté | +1 | Joint de bride — ajout E3 |
| FAST-01 | ❌ absent | ✅ ajouté | +1 | Visserie忽略了 |

---

*Document généré — Closes #68*