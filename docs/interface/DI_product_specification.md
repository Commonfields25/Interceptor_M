---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# DI — Product Specification v1.0
**Issue:** #54  
**Version:** 1.0.0  
**Classification:** Interne — Restricted  
**Path:** `docs/interface/`  
**Owner:** Lead Engineer (E1)

---

## 1. Objet et Périmètre

Ce document constitue le **Dossier d'Interface (DI) version 1.0 verrouillée** du projet Interceptor_M.
Il définit les interfaces mécaniques, électriques et logicielles entre sous-systèmes pour le lancement des contrats fournisseurs.

**Périmètre v1.0 :**
- Structure mécanique (BRK-001, ACT-001, NCR-001)
- Interfaces électroniques (bride moteur, câblage ESC, connectique)
- Spécifications matériaux et tolérances
- Contraintes d'intégration (espace disponible, drainage thermique)

---

## 2. References Normatives

| Réf. | Document | Version | Statut |
|------|----------|---------|--------|
| DI-BOM | `manufacturing/BOM_consolidee.md` | Draft | ⚠️ à verrouiller |
| DI-PAR | `PARAMETERS.json` | 1.0.1 | ✅ actif |
| DI-ENG | `engineering/DI_SPEC_LOCK.md` | v1.0 | ✅ verrouillé |
| DI-STR | `engineering/BOM_BASELINE.md` | 1.0 | ✅ actif |

---

## 3. Interfaces Mécaniques

### 3.1 BRK-001 — Coque Fuselage

| Paramètre | Valeur | Tolérance | Unité |
|-----------|-------|-----------|-------|
| Longueur fuselage | 350 (DC) / 365 (DI) / 380 (DD) | ±0.5 | mm |
| Diamètre extérieur | 35.0 | IT10 | mm |
| Épaisseur paroi | 1.5 (DC) / 1.8 (DI) / 2.0 (DD) | IT10 | mm |
| Encastrement bras | 75.0 | IT7 | mm |

### 3.2 ACT-001 — Vérin Tubulaire

| Paramètre | Valeur | Tolérance |
|-----------|-------|-----------|
| Diamètre tube | 40.0 | IT7 |
| Course | À définir (E3) | — |

### 3.3 NCR-001 — Carénage Aero

| Paramètre | Valeur | Tolérance |
|-----------|-------|-----------|
| Interface bride moteur | Øext à définir | IT10 |
| Interface fuselage | collé/ boulonné BRK-001 | — |

---

## 4. BOM Intégrée

> Voir : [`manufacturing/BOM_consolidee.md`](../../manufacturing/BOM_consolidee.md) (révision courante : Draft)
> et [`engineering/BOM_BASELINE.md`](../../engineering/BOM_BASELINE.md) (référence verrouillée)

**Delta DI v1.0 vs BOM actuelle :** Aucun changement majeur. Points ouverts :
- [ ] Verrouillage OR-112-NBR (Qté mini commande)
- [ ] Validation NCR-001 layup par E1

---

## 5. Chaîne de Traçabilité

```
engineering/BOM_BASELINE.md (baseline v1.0)
  → manufacturing/BOM_consolidee.md (opérationnel, Draft)
  → PARAMETERS.json (v1.0.1)
  → docs/interface/DI_product_specification.md (ce document, v1.0.0)
```

---

## 6. Revue Formelle

| Rôle | Nom | Date | Signature |
|------|-----|------|-----------|
| Lead Engineer | Commonfields25 | — | ⬜ |

> ⚠️ **Document gelé.** Toute modification nécessite une demande de déverrouillage validée par E1.

---

*Document généré — Closes #54*