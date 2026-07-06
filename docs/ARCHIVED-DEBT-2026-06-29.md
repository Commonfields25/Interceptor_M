---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# ARCHIVED — README Debt Section (2026-06-29)

> Ce fichier conserve l'historique de la section "Éléments en attente de revue" supprimée du README le 2026-06-29.
> Toutes les actions listées ci-dessous ont été traitée via les PRs #80–#85.

## Contenu archivé

| Élément | Action effectuée |
|---------|-----------------|
| `params/` | Inventaire créé : `params/INVENTORY.md` (PR #80) |
| `gen_geometry.py` (racine) | Vérifié : déjà canonical dans `scripts/`, no-op (PR #81 fermée) |
| `governance/` vs `docs/governance/` | `docs/governance/` → `governance/` promu à la racine, canonical établi (PR #82) |
| `ci-templates/workflows/` vs `.github/workflows/` | 9 workflows consolidés via `legacy/ci-templates-workflows/` (PR #83 + #85) |
| `OPERATIONS_WORKFLOW.md` V1 | V1 archivé dans `legacy/operations/`, V2 conservé (PR #84) |
| `Base_Launcher_Pieces/` | Hors périmètre этих PRs — laissé tel quel (décision différée) |