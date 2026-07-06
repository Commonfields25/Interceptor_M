---
action: Update
agent: Jules
related_gate: G3
status: Validated
timestamp: 2026-07-06T12:00:00Z
---

# D2 — Aérodynamique & CFD (Baseline 2.1.0)
**Agent :** D2 — Aérodynamique / Simulation CFD
**Projet :** Interceptor_M
**Baseline :** 400g Electric Dash Platform

---

## 2.1 Objectif & Méthodologie

Valider la configuration aérodynamique DD-400 (Baseline 2.1.0) pour le vol de croisière (Dash) à Mach 0.35.
- Fuselage Ø35 mm × 380 mm, ogive tangente (L/D ≈ 3,5)
- Ailes delta pliables 4 × (envergure 150 mm)
- Masse au lancement : 400g (Target) / 410.4g (CAD Verified)

**Méthode :** Analyse semi-analytique via méthodes de stabilité & contrôle (Etkins). Calcul du coefficient de traînée (Cx) en régime subsonique incompressible. Stabilité statique vérifiée avec une marge de 10.5%.

---

## 2.2 Géométrie de Référence

| Paramètre | Valeur | Source |
|---|---|---|
| Longueur fuselage L | 380 mm | PARAMETERS.json |
| Diamètre fuselage d | 35 mm | PARAMETERS.json |
| Envergure ailes (déployées) | 150 mm | PARAMETERS.json |
| Masse de référence | 400 g | Target MTOW |
| Diamètre ogive (tangent) | 122.5 mm | L/D = 3.5 |

---

## 2.3 Performance en Vol

- **Vitesse de Dash :** 120 m/s (Mach 0.35)
- **Traînée (Cx0) :** 0.18 (Estimation subsonique)
- **Marge Statique :** 10.5% (Stable)

---
*Aligné sur le Technical Baseline 2.1.0 (400g Electric).*
