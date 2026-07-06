# BOM Consolidée — Interceptor_M (Baseline 2.1.0)

**Version:** 2.1.0
**Baseline:** engineering/BOM_MASTER.md
**Date:** 2026-07-06

## 1. Récapitulatif Masse (DD-400 Reference)

| Composant | Masse (g) | Matériau | Note |
|-----------|-----------|----------|------|
| **BRK-001** | 25.1 | AlSi10Mg | Coque fuselage (CAD calc) |
| **ACT-001** | 158.5 | AlSi10Mg | Mécanisme de déploiement (CAD calc) |
| **WING-001**| 21.5  | CFRP     | 4x Ailes pliables (5.38g each) |
| **NCR-001** | 35.3  | Al-7075  | Bague interface |
| **Avionique**| 40.0  | -        | AVS-001 included |
| **Batterie** | 105.0 | LiPo      | BAT-3S-001 included |
| **Moteur**   | 25.0  | -        | MMT-001 included |
| **TOTAL**    | **410.4** | -      | **⚠️ SLIGHT OVERAGE** |

## 2. Variante F1-Chaser (450g)

| Composant | Masse (g) | Matériau | Note |
|-----------|-----------|----------|------|
| **F1-BODY-01** | 350.2 | AlSi10Mg | Monocoque fusée |
| **F1-MOTOR-X4**| 181.3 | -        | 4x Motors (45.32g each) |
| **F1-PROP-X4** | 6.4   | Carbon   | 4x Props (1.60g each) |
| **Avionique**  | 50.0  | -        | Stack FC/ESC |
| **Batterie**   | 240.0 | LiPo      | High-discharge |
| **TOTAL**      | **827.9** | -      | **⚠️ REDESIGN REQUIRED** |

---
*Note: This BOM is synchronized with parametric CAD models. F1-Chaser masses are significantly higher than conceptual targets due to L3-grade component density. A mass reduction campaign is scheduled.*
