---
action: Update
agent: Jules
related_gate: G3
status: Validated
timestamp: 2026-07-06T12:00:00Z
---

# D3 — Structure & Mécanique (Baseline 2.1.0)
**Agent :** D3 — Génie Mécanique / Structure
**Projet :** Interceptor_M
**Baseline :** 400g Electric Dash Platform

---

## 3.1 Introduction & Portée

Valider la conception mécanique L3 (Manufacturing) pour la plateforme DD-400 (400g MTOW).
- Sélection des matériaux : AlSi10Mg (Fuselage/Mécanisme), CFRP (Ailes), Al-7075 (Interface).
- Processus : Impression 3D Métal (DMLS) et composites.
- Cible de masse : 400g.

---

## 3.2 Découpage Structurel (380 mm)

```
Zone A: Ogive / Seeker (0 – 122.5 mm)
Zone B: Avionique & Batterie (122.5 – 280 mm)
Zone C: Mécanisme Ailes (ACT-001) (280 – 340 mm)
Zone D: Moteur & Support (340 – 380 mm)
```

---

## 3.3 Budget Masse (CAD Verified)

| Sous-ensemble | Masse (g) | Matériau | Note |
|---|---|---|---|
| Fuselage (BRK-001) | 25.1 | AlSi10Mg | CAD Calc |
| Mécanisme (ACT-001) | 158.5 | AlSi10Mg | CAD Calc |
| Ailes (WING-001 x4) | 21.5 | CFRP | CAD Calc |
| Interface (NCR-001) | 35.3 | Al-7075 | CAD Calc |
| Électronique & Batt | 145.0 | Mixed | Estimated |
| Moteur (SC-02) | 25.0 | - | Spec |
| **TOTAL** | **410.4** | - | **✅ Baseline 2.1.0** |

---
*Aligné sur le Technical Baseline 2.1.0.*
