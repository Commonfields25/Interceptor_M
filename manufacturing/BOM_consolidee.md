---
agent: Lead Designer (Jules)
action: Update
timestamp: 2026-06-30T16:00:00Z
related_gate: G2
status: Validated
---

# BOM Consolidée — Interceptor M (v1.5 Baseline)

| Réf. | Désignation | Matériau | Tech. Primaire | Masse (DD - Defense) | Statut |
|------|-------------|----------|---------------|----------------------|--------|
| **BRK-001** | Coque fuselage + 支翼 | AlSi10Mg | DMLS (SLM) | 130.74g | Refactored v2.3 |
| **ACT-001** | Vérin tubulaire 3 axes | AlSi10Mg | DMLS (SLM) | 55.49g | Refactored v2.3 |
| **NCR-001** | Carénage aero complexe | Nomex CF | Layup manual | 104.48g | Spec Lock |
| **SABOT-001** | Interface Lanceur/Drone | FDM ASA | FDM 3D Print | 15.00g | **NEW** |
| **FC-001** | Flight Controller (H7) | PCB | SMT Assembly | 12.50g | **NEW** |
| **PDB-001** | Power Distribution Board | PCB | SMT Assembly | 18.00g | **NEW** |

**Total Structure (Masse Sèche)** | | | | **336.21g** |
**Budget Cible (DD)** | | | | **290.71g** | ⚠️ +15% Over budget

## ⚠️ Analyse de l'Écart de Masse
L'ajout du **SABOT-001** et de l'électronique haute-fidélité (**FC/PDB**) pousse la masse DD à 336g. Une optimisation de 15% est requise sur le `BRK-001` (pochettage) pour revenir sous les 290g.

---
*Généré pour Revue G2 — Alignement avec engineering/BOM_BASELINE.md*
