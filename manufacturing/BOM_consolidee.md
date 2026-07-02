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
| **NCR-001** | Bague interface ogive — joint torique NBR (étanchéité pneumatique) | **316L SS** | Tournage CNC | 104.48g | Spec Lock |
| **SABOT-001** | Interface Lanceur/Drone | FDM ASA | FDM 3D Print | 15.00g | **NEW** |
| **FC-001** | Flight Controller (H7) | PCB | SMT Assembly | 12.50g | **NEW** |
| **PDB-001** | Power Distribution Board | PCB | SMT Assembly | 18.00g | **NEW** |

**Total Structure (Masse Sèche)** | | | | **336.21g** |
**Budget Cible (DD)** | | | | **290.71g** | ⚠️ +15% Over budget

## ⚠️ Analyse de l'Écart de Masse

> **Réference MTOW DD = 321.21 g** (en vol — sabot détaché, DG decision). Spec E1 400 g conservée comme plafond de design.

En vol (référence MTOW), la structure seule (hors sabot) est à ~321 g — **79 g sous le plafond 400 g** (DG decision). Le pocketing BRK-001 conserve ~20 g de marge.

---
*Généré pour Revue G2 — Alignement avec engineering/BOM_BASELINE.md*
