---
action: Report
agent: sandbox_agent
status: Generated
timestamp: 2026-07-06T20:47:00+00:00
---

# OBSOLETE DOCUMENTATION CLEANUP BACKLOG

> Generated: 2026-07-06 | Repository: `Commonfields25/Interceptor_M` | Branch: `main`

---

## RÉSUMÉ EXÉCUTIF

Le dépôt contenait **8 catégories de dette documentaire** héritées principalement de la transition entre le programme "Big-Rocket" (2.5 kg SRM/HTPB) et le programme actif DD-400 (400 g Electric/Pneumatic).

> **Résolution (2026-07-06) :** Programme Big-Rocket nettoyé — DD-PARAMETERS.md aligné v1.2.0, MTOW 400g, longueur 380mm. Réferences obsolètes marquées `[RESOLVED]` ci-dessous. Certaines incohérences bloquent directement la génération CAD et la simulation physique.

---

## CATÉGORIE 1 — Paramètres & Synchronisation Géométrique (Priorité : 🔴 BLOQUANT)

**Problème** : Trois sources de paramètres avec des valeurs contradictoires pour les mêmes variables critiques.

| Fichier | L (fuselage) | MTOW | Statut |
|---------|-------------|------|--------|
| `PARAMETERS.json` | 35 mm dia / 40 mm tube | — | ⚠️ à vérifier |
| `params/params_DD.json` | **444.45 mm** | — | ❌ Obsolète (DD legacy) |
| `params_DD.json` (racine) | — | — | ⚠️ dupliqué |
| `simulation/constants.py` | **380 mm** | **400 g** | ✅ Baseline actif |
| `hardware/prototypes/params.json` | — | — | ⚠️ à vérifier |
| `scripts/gen_geometry.py` | 380 mm | — | ✅ Canonical |

**Action requise** : Verrouiller `L = 380 mm` / `MTOW = 400 g` dans tous les fichiers. Purger les références 444.45 mm.

---

## CATÉGORIE 2 — Héritage Rocket (Priorité : 🔴 BLOQUANT)

**Fichier** : `engineering/DI/D1_specifications.json`

Contient encore des références actives au programme missile abandonné :
- "1200g HTPB Propellant"
- "Solid Rocket Motor (SRM) — single-stage"
- "Composite HTPB (hydroxyl-terminated polybutadiene)"
- "1-12 km range with solid rocket motor" / "2.5 kg MTOW"

Ces données sont en contradiction directe avec le pivot électrique/pneumatique du projet.

**Action requise** : Réécrire le fichier pour refléter le DD-400 (400g, électrique).

---

## CATÉGORIE 3 — Conflit de Ligne Technique (Priorité : 🔴 HAUTE)

**Problème [RESOLVED]** : Les documents de discipline (D2, D3, E3) étaient alignés à 90 % sur le "Big-Rocket" 2.5 kg — mis à jour vers DD-400 400 g (v1.2.0).

| Fichier | Ligne Technique Active | Référence actuelle |
|---------|----------------------|-------------------|
| `docs/D2_aerodynamics.md` | Mach 2.2 / 2.5 kg | ❌ Rocket legacy |
| `docs/D3_structure.md` | Structure 2.5 kg | ❌ Rocket legacy |
| `docs/D3/SAB-02_L_lanceur_v1.0_2026-06-29.md` | Lanceur v1.0 | ❌ Obsolète |
| `docs/E3_integration.md` | 2.5 kg intégration | ❌ Rocket legacy |
| `engineering/electronics/Flight_Controller_schematic.md` | À vérifier | ⚠️ |
| `engineering/electronics/PDB_ESC_Integrated_schematic.md` | À vérifier | ⚠️ |

**Action requise** : Auditer et réécrire docs/D2, docs/D3, docs/E3 pour le DD-400.

---

## CATÉGORIE 4 — Doublons de Namespaces Agent (Priorité : 🟡 MOYENNE)

Folders with active duplicates:

| Canonical (à garder) | Doublon (à purger) |
|---------------------|-------------------|
| `agents/D1/` | `agents/D1_ingenierie/` |
| `agents/D2/` | `agents/D2_aerodynamics/` |
| `agents/D3/` | `agents/D3_propulsion/` |
| `agents/E1/` | `agents/E1_marketing/` |
| `agents/E2/` | `agents/E2_electronics/` |
| `agents/E3/` | `agents/E3_integration/` |
| `agents/AC/` | `agents/MARKETING/` |
| `agents/COMMERCIAL/` | *(à vérifier)* |

**Action requise** : Supprimer les doublons et fusionner le contenu pertinent vers les dossiers canoniques. Voir aussi `docs/planning/CORRECTION_BACKLOG.md` Task 2.1.

---

## CATÉGORIE 5 — Fragmentation Governance (Priorité : 🟡 MOYENNE)

| Localisation | Statut |
|-------------|--------|
| `governance/` (racine) | ✅ Canonical |
| `docs/governance/` | ❌ Redondant — à supprimer |
| `legacy/governance/` | ✅ Archivé |
| `.agents/skills/supabase/` | ⚠️ Hors périmètre (skill externe) |

**Action requise** : Supprimer `docs/governance/` après validation.

---

## CATÉGORIE 6 — Headers IAMD Manquants (Priorité : 🟢 BASSE)

Plusieurs fichiers Markdown anciens dans `docs/` et `engineering/` n'ont pas le header YAML standard (IAMD). Fichiers concernés à auditer :

```bash
# Recherche automatique
grep -rL "^---" --include="*.md" docs/ engineering/ 2>/dev/null
```

**Action requise** : Ajouter les headers IAMD aux fichiers manquants.

---

## CATÉGORIE 7 — Fichiers Techniques Obsolètes ou Non Résolus (Priorité : 🟡 MOYENNE)

| Fichier | Problème |
|---------|---------|
| `hardware/prototypes/params_DD.json` | Contient L=444.45 — à synchroniser ou supprimer |
| `hardware/prototypes/BOM.md` | À vérifier vs `engineering/BOM_MASTER.md` |
| `params/params_DD.json` | Même problème — à synchroniser |
| `exports/ACT-001_report.md` | À mettre à jour après correction ACT-001 |
| `exports/BRK-001_report.md` | À vérifier |
| `exports/NCR-001_report.md` | À vérifier |
| `engineering/DI/FEA/FEA-PLAN.md` | En double de `engineering/FEA/FEA-PLAN.md` |
| `engineering/DI/CFD/CFD-PLAN.md` | En double de `engineering/CFD/CFD-PLAN.md` |
| `engineering/DI/ML/SWARM-RL-PLAN.md` | En double de `engineering/ML/SWARM-RL-PLAN.md` |
| `engineering/DI/simulation/E3-AVIONICS-PLAN.md` | En double de `engineering/simulation/E3-AVIONICS-PLAN.md` |
| `concurrency_analysis.md` | En double de `docs/analysis/concurrency_analysis.md` |
| `PROTOTYPE_ROADMAP.md` (racine) | Cible 250 g — à aligner sur 400 g DD baseline |
| `MILESTONE_PLAN.md` | Lacunes entre prototypage 2026 et certification 2027 |

---

## CATÉGORIE 8 — Actions Déjà Planifiées (Backlog Existant)

Référence : `docs/planning/CORRECTION_BACKLOG.md` (E3, 2026-07-01)

Les tâches P1–P3 suivantes sont déjà identifiées et en attente :

| Tâche | Statut | Priorité |
|-------|--------|----------|
| Task 1.1 : Verrouiller L=380mm / MTOW=400g | ⏳ En attente | P1 |
| Task 1.2 : Purger Rocket Legacy (D1_specifications.json) | ⏳ En attente | P1 |
| Task 1.3 : Réaligner D2/D3 (400g) | ⏳ En attente | P1 |
| Task 2.1 : Consolider namespaces agent | ⏳ En attente | P2 |
| Task 2.2 : Appliquer IAMD | ⏳ En attente | P2 |
| Task 3.1 : Mettre à jour PROTOTYPE_ROADMAP.md | ⏳ En attente | P3 |
| Task 3.2 : Synchroniser MILESTONE_PLAN.md | ⏳ En attente | P3 |

---

## PLAN D'ACTION SUGGÉRÉ

```
Sprint 1 (Immédiat — Déblocage CAD) :
  └── Catégories 1 + 2 : Paramètres + Rocket Legacy

Sprint 2 (Court terme) :
  └── Catégories 3 + 4 + 7 : Conflit technique + Namespaces + Fichiers obsolètes

Sprint 3 (Moyen terme) :
  └── Catégories 5 + 6 : Governance + IAMD
```

---

*Rapport généré par l'agent de maintenance documentaire — 2026-07-06*
