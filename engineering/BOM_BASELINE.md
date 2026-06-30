# BOM Baseline — Interceptor_M

> **Status:** Baseline Active | **Version:** 1.0 | **Date:** 2026-06-30
> **Owner:** Direction Générale | **Classification:** Interne

---

## 1. Objet

Ce document constitue la **Bill of Materials (BOM) verrouillée** du projet Interceptor_M.
Il référence la BOM opérationnelle dans `manufacturing/BOM_consolidee.md` et ajouter les
références croisées vers les spécifications DI verrouillées.

---

## 2. BOM Consolidée — Référence

> Voir : `manufacturing/BOM_consolidee.md` — Source primaire

| Ligne | Référence | Masse (DC) | Masse (DD) | Masse (DI) |
|-------|-----------|-----------|-----------|-----------|
| Structure primaire | BRK-001 | 111.78g | 130.74g | 118.78g |
| Actionneur | ACT-001 | 55.49g | 55.49g | 55.49g |
| Carénage aero | NCR-001 | 89.33g | 104.48g | 95.71g |
| **TOTAL STRUCTURE** | | **256.60g** | **290.71g** | **269.98g** |

**Cible DRF:** Ratio structure/MTOW < 3% ✅ (DC: 2.57%)

---

## 3. Paramètres Critiques

| Paramètre | Valeur | Unité |
|-----------|-------|-------|
| MTOW DC | 250 | g |
| Masse structure DC | 256.60 | g |
| Charge utile residualle DC | ≤ 0 (à optimiser) | g |
| Ratio structure/MTOW DC | 2.57 | % |

---

## 4. Chaîne de Traçabilité

```
MILESTONE_PLAN.md (M7)
  → engineering/DI_SPEC_LOCK.md (v1.0, locked)
  → engineering/BOM_BASELINE.md (this file)
    → manufacturing/BOM_consolidee.md (operational BOM)
      → engineering/DI/NDC/MTOW-RECOMMENDATION.md
        → engineering/DI/D1_specifications.json
```

---

*Généré automatiquement — aligns with DI_SPEC_LOCK.md v1.0*
