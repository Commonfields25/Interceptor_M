---
action: Create
agent: E1
related_gate: G2
status: Draft
timestamp: 2026-06-27 15:21:00+00:00
---

# 📐 NDC — Notes de Calcul (Skeleton)
**Version:** 0.1-draft | **Owner:** E1 (Systems / NDC / FEA)
**Projet:** Interceptor_M — Defense Line (DD)

---

## 1. Portée

Ce document est le squelette des Notes de Calcul pour le micro-intercepteur.
Sections à compléter avant G2 : structure, propulsion, aérodynamique.

## 2. Hypothèses de Base

| Paramètre | Valeur | Source |
|---|---|---|
| MTOW | 250 g | PARAMETERS.json |
| Diamètre fuselage | 35 mm | PARAMETERS.json |
| Longueur totale | ≤ 900 mm | D1 spec |
| Tube lanceur Ø | 40 mm | PARAMETERS.json |
| Pression lancement | TBD (E2) | E2 valve specs |
| Vitesse sortie | TBD | Calcul G2 |

## 3. Structure — Vérifications prevues

- [ ] Contrainte max en paroi fuselage (lancement, 50g)
- [ ] Vérification montage moteur M3
- [ ] Résistance attaches ailes (M2)
- [ ] FEA preliminary launch stress

## 4. Propulsion — Calculs prevus

- [ ] Poussée nécessaire pour M 2,2 mission profile
- [ ] Sélection moteur (EDF/brushless)
- [ ] Autonomie estimé (batterie 2S/3S)

## 5. Interfaces

- `models/DD/` — Géométrie CAO (D3)
- `engineering/FEA/` — Résultats FEA
- `engineering/CFD/` — Résultats CFD

## 6. Prochaines Étapes

- [ ] Collecter dimensions exactes depuis D3 CAD
- [ ] Lancer FEA preliminary sur airframe (E1 self)
- [ ] Intégrer résultats CFD E2

---
*Skeleton — À compléter pour Gate G3*
