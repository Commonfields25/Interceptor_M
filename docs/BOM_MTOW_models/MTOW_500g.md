---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# MTOW 500g — Spécification Provisoire
**STATUS:** `PROVISIONAL — awaiting DG lock`
**Version:** 1.0-draft
**Dernière mise à jour:** 2026-06-30

---

## Vue d'ensemble

| Paramètre | Valeur | Notes |
|-----------|--------|-------|
| Masse totale (MTOW) | **500 g** | +67% vs 300g |
| Masse à vide (dry) | ~330 g | structure robuste + avionique complète |
| Charge utile disponible | ~170 g | batterie grande capacité + mission payload |
| Autonomie cible | ~15 min | batterie 3S 850mAh |
| Motorisation | 2× DD (ø16mm, ~70W) | TWR ~2.8:1 |

---

## Répartition par sous-système

| Sous-système | Masse | % MTOW | Composants clés |
|---|---|---|---|
| **Airframe** | 160 g | 32.0 % | Carbone 3mm, longerons 5mm, visserie titane |
| **Propulsion** | 120 g | 24.0 % | 2× DD ø16mm, 2× hélices 5" CF |
| **Avionique** | 45 g | 9.0 % | FCU + IMU + RX diversity + GPS + baro |
| **Batterie** | 135 g | 27.0 % | LiPo 3S 850mAh (~120g cells + wiring) |
| **Charge utile** | 40 g | 8.0 % | Capteurs mission, LEDs, câblage |

---

## BOM simplifiée — Composants principaux

| Réf | Composant | Qté | Masse unitaire | Masse totale |
|-----|-----------|-----|----------------|--------------|
| AF-001 | Plaque carbone 3mm 140×100mm | 2 | 28 g | 56 g |
| AF-002 | Longerons carbone 5×140mm | 4 | 14 g | 56 g |
| AF-003 | Visserie titane M2.5×10 | ~40 | 0.7 g | ~28 g |
| AF-004 | Entretoises nylon M3 | 14 | 1.0 g | 14 g |
| AF-005 | Bras carbone 8mm dia 140mm | 4 | 6 g | 24 g |
| AF-006 | Renforts carbone 2mm | 4 | 3 g | 12 g |
| PR-001 | Moteur DD ø16mm 2400KV | 2 | 32 g | 64 g |
| PR-002 | Hélices 5" carbone 3-blades | 2 | 18 g | 36 g |
| PR-003 | ESC 4-en-1 20A | 1 | 16 g | 16 g |
| AV-001 | FCU ESP32-S3 + IMU + baro | 1 | 12 g | 12 g |
| AV-002 | Rx ELRS 2.4GHz diversity | 1 | 6 g | 6 g |
| AV-003 | GPS NEO-M10Q + baro DPS310 | 1 | 9 g | 9 g |
| AV-004 | OSD / Telemetry module | 1 | 8 g | 8 g |
| AV-005 | Câblage & connecteurs | 1 | 10 g | 10 g |
| BT-001 | Batterie LiPo 3S 850mAh | 1 | 120 g | 120 g |
| PU-001 | Capteur mission (lidar mini + cam) | 1 | 22 g | 22 g |
| PU-002 | LEDs + support | 1 | 8 g | 8 g |
| PU-003 | Réserve charge utile | 1 | 10 g | 10 g |
| **TOTAL** | | | | **~511 g** |

> ⚠️ UPSIZING vs 400g : propulsion +41%, batterie +14%, airframe +33%.
> ⚠️ TWR légèrement réduit (2.8:1) — maniabilité toujours excellente.
> ⚠️ Capacité de charge utile la plus élevée — usage ISR / surveillance.

---

## Notes DG

- Cette configuration est le **modèle lourd DC** pour missions de longue durée.
- 170g de charge utile permet intégration lidar + caméra + module RF complet.
- La batterie 3S 850mAh donne ~15 min de vol — suffisant pour la majorité des missions ISR.

---
*Généré automatiquement — NE PAS signer sans validation DG*
