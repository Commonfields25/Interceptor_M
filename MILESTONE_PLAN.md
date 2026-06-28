# Milestone Plan — Interceptor_M
**Version :** 1.0
**Date :** 2026-06-28
**Contexte :** audit autonome phase 1, repo restructuré (ruleset actif, README OK, workflows neutralisés)

---

## Objectif Global

> Tous les milestones actifs (M5 à M9) doivent être **CLOSED** avant le **2026-07-29**.

---

## État des Milestones Actifs

| MS | Titre | Due Date | Open | Closed | Jalon Cible |
|----|-------|----------|------|--------|-------------|
| M5 | Branch Cleanup & Archive | 2026-07-09 | 1 | 0 | J2 |
| M6 | CI Migration Node24 & Workflow Activation | 2026-07-16 | 1 | 1 | J3 |
| M7 | DI Product Specs Lock & BOM | 2026-07-23 | 1 | 0 | J4 |
| M8 | RL Environment Hardening & Agent Rebalancing | 2026-08-13 | 1 | 0 | J6 |
| M9 | Recrutement Ingénieur Conception | 2026-07-29 | 1 | 1 | J5 |

## Jalons Intermédiaires (SMART)

| Jalon | Date | Critère Mesurable |
|-------|------|-------------------|
| J1 | 2026-07-02 | 0 issue orpheline, #43 traitée (doublon) |
| J2 | 2026-07-09 | MS5 CLOSED — 0 branche archived avec ahead=0 |
| J3 | 2026-07-16 | MS6 CLOSED — python-ci.yml + node24-validation.yml GREEN |
| J4 | 2026-07-23 | MS7 CLOSED — BOM.json locked, PRODUCT-FAMILY.md updated |
| J5 | 2026-07-29 | MS9 CLOSED — offre émise ou contrat signé |
| J6 | 2026-08-13 | MS8 CLOSED — P(intercept) random < 15%, MAPPO > 60% |

---

## Actions en Attente de Validation DG

Les actions suivantes sont **proposées** (non appliquées) — nécessitent confirmation :

1. **Réassigner issues 52-59** des milestones fantômes (10-13) vers les bons milestones (6-9)
2. **Fermer #43** comme doublon de #52
3. **Mettre à jour les descriptions MS6-MS9** avec critères mesurables (métriques)
4. **Fermer/supprimer les milestones fantômes 10-13** (doublons, pas d'issue assignée)

---

## Notes

- MS4 (MAPPO Training) est en retard — due 2026-09-28 sans issue ouverte, suggère que le travail est en cours dans des branches/PR non mergées
- MS8 est le jalon le plus exigeant techniquement (RL hardening) — recommander un point DG avant J6
