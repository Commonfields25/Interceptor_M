# DI_SPEC_LOCK — Interceptor_M — Specification Lock Baseline

> **Status:** LOCKED | **Lock Version:** 1.0 | **Lock Date:** 2026-06-30
> **Owner:** Direction Générale | **Classification:** Interne — Protégé

---

## 1. Objet du Verrouillage

Ce document fige la **Design Interface (DI) specifications** du projet Interceptor_M
à la date du lock. Tout écart par rapport à ces spécifications doit suivre le
processus NCR (Non-Conformance Report) défini dans `templates/NON_CONFORMANCE_REPORT.md`.

---

## 2. Paramètres Structurels Verrouillés

| Paramètre | Valeur Lockée | Unité | Référence |
|-----------|--------------|-------|-----------|
| MTOW (DC) | 250 | g | engineering/DI/NDC/MTOW-RECOMMENDATION.md |
| MTOW (DD) | 300 | g | engineering/DI/NDC/MTOW-RECOMMENDATION.md |
| MTOW (DI) | 285 | g | engineering/DI/NDC/MTOW-RECOMMENDATION.md |
| Envergure | 200 | mm | DRF airframe analysis |
| Longueur fuselage | 350 | mm | DRF airframe analysis |
| Surface alaire | 0.02 | m² | DRF airframe analysis |
| Ratio structure/MTOW (DC) | < 3.0 | % | manufacturing/BOM_consolidee.md |
| Masse totale structure (DC) | 256.60 | g | manufacturing/BOM_consolidee.md |

---

## 3. Spécifications Électroniques Verrouillées

| Sous-système | Composant | Spécification | Source |
|-------------|-----------|--------------|--------|
| ESC | Type | Brushless sensorless | docs/E2_electronics.md |
| FC | Protocol | MAVLink v2.0 | docs/E2_electronics.md |
| Battery | Chemistry | LiPo 3S / Li-Ion 18650 | docs/E2_electronics.md |
| Battery | Zone exclusion | Volume réservé — ne pas implanter ESC/FC | engineering/DI/NDC/ |
| Remote ID | Standard | ASTM F3411-24 | engineering/ISO_UAS_BASELINE.md |

---

## 4. Spécifications Propulsion Verrouillées

| Paramètre | Valeur | Tolérance |
|-----------|-------|----------|
| Poussée statique max | TBD (en attente essais DI) | — |
| rapport masse/puissance | ≥ 2:1 (W/kg) | DRF target |
| Temps de vol estimé | ≥ 15 min | Avec payload standart |

---

## 5. Artefacts DI Valides (Référence)

| Fichier | Description | Statut |
|---------|------------|--------|
| engineering/DI/D1_specifications.json | Spécifications détaillées D1 | ✅ Actif |
| engineering/DI/DI-MARKET-STUDY.md | Étude de marché | ✅ Actif |
| engineering/DI/NDC/NDC-INTERCEPTOR-DD.md | Modèle airframe DD | ✅ Actif |
| engineering/DI/NDC/MTOW-RECOMMENDATION.md | Recommandation MTOW | ✅ Actif |
| engineering/DI/ML/SWARM-RL-PLAN.md | Plan RL Isaac Gym | ✅ Actif |
| engineering/DI/ML/isaac_gym/scenarios.yaml | Scénarios simulation | ✅ Actif |
| engineering/DI/simulation/E3-AVIONICS-PLAN.md | Plan avionics | ✅ Actif |

---

## 6. Procédure de Déverrouillage (Change Request)

Pour modifier une spécification verrouillée :

1. **Déposer NCR** via `manufacturing/NCR-001_notes.md`
2. **Révision DG** — justification technique obligatoire
3. **Mise à jour DI_SPEC_LOCK.md** — nouvelle version
4. **Propagation** vers BOM_consolidee.md + MILESTONE_PLAN.md
5. **Validation CI** — `.github/workflows/iso-compliance.yml` doit passer

---

## 7. Version History

| Version | Date | Auteur | Changement |
|---------|------|--------|-----------|
| 1.0 | 2026-06-30 | DG-AUTO | Initial lock — baseline established |

---

*Document généré automatiquement — Toute modification requiert l'approbation de la DG.*
