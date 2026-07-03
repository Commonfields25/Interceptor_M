---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# MTOW 400g — Spécification Provisoire
**STATUS:** `PROVISIONAL — awaiting DG lock`
**Version:** 1.0-draft
**Dernière mise à jour:** 2026-06-30

---

## Vue d'ensemble

| Paramètre | Valeur | Notes |
|-----------|--------|-------|
| Masse totale (MTOW) | **400 g** | +33% vs 300g |
| Masse à vide (dry) | ~275 g | structure + avionique upsized |
| Charge utile disponible | ~125 g | batterie plus grosse + capteurs |
| Autonomie cible | ~12 min | batterie 3S 650mAh |
| Motorisation | 2× DD (ø14mm, ~50W) | TWR ~3:1 |

---

## Répartition par sous-système

| Sous-système | Masse | % MTOW | Composants clés |
|---|---|---|---|
| **Airframe** | 120 g | 30.0 % | Carbone 2.5mm, longerons 4mm, visserie titane |
| **Propulsion** | 85 g | 21.3 % | 2× DD ø14mm, 2× hélices 4" CF |
| **Avionique** | 38 g | 9.5 % | FCU (ESP32-S3), RX (ELRS 2.4GHz), GPS, baro |
| **Batterie** | 115 g | 28.8 % | LiPo 3S 650mAh (~105g cells + wiring) |
| **Charge utile** | 42 g | 10.5 % | Capteur additionnel, LEDs, câblage |

---

## BOM simplifiée — Composants principaux

| Réf | Composant | Qté | Masse unitaire | Masse totale |
|-----|-----------|-----|----------------|--------------|
| AF-001 | Plaque carbone 2.5mm 120×80mm | 2 | 18 g | 36 g |
| AF-002 | Longerons carbone 4×120mm | 4 | 10 g | 40 g |
| AF-003 | Visserie titane M2×8 | ~35 | 0.5 g | ~18 g |
| AF-004 | Entretoises nylon M2.5 | 12 | 0.7 g | 8 g |
| AF-005 | Bras carbone 6mm dia 120mm | 4 | 4 g | 16 g |
| PR-001 | Moteur DD ø14mm 2800KV | 2 | 22 g | 44 g |
| PR-002 | Hélices 4" carbone 3-blades | 2 | 12 g | 24 g |
| PR-003 | ESC 4-en-1 12A | 1 | 12 g | 12 g |
| AV-001 | FCU ESP32-S3 + IMU | 1 | 10 g | 10 g |
| AV-002 | Rx ELRS 2.4GHz + diversity | 1 | 5 g | 5 g |
| AV-003 | GPS NEO-M10Q + baro DPS310 | 1 | 9 g | 9 g |
| AV-004 | Câblage & connecteurs | 1 | 14 g | 14 g |
| BT-001 | Batterie LiPo 3S 650mAh | 1 | 105 g | 105 g |
| PU-001 | Capteur additionnel (lidar/cam) | 1 | 15 g | 15 g |
| PU-002 | LEDs + support | 1 | 7 g | 7 g |
| PU-003 | Réserve charge utile | 1 | 20 g | 20 g |
| **TOTAL** | | | | **~383 g** |

> ⚠️ UPSIZING vs 300g : propulsion +42%, batterie +40%, airframe +26%.
> ⚠️ Le TWR reste à 3:1 — performances de vol similaires mais autonomie accrue.

---

## Notes DG

- Cette configuration est le **point milieu** entre DD300 et le modèle lourd DC500.
- La batterie 3S 650mAh double l'énergie embarquée vs 300g.
- Charge utile (42g) permet intégration lidar miniature ou caméra FPV premium.

---
*Généré automatiquement — NE PAS signer sans validation DG*
