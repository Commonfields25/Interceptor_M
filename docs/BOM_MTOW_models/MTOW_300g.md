---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# MTOW 300g — Spécification Provisoire
**STATUS:** `PROVISIONAL — awaiting DG lock`
**Version:** 1.0-draft
**Dernière mise à jour:** 2026-06-30

---

## Vue d'ensemble

| Paramètre | Valeur | Notes |
|-----------|--------|-------|
| Masse totale (MTOW) | **300 g** | masse max au décollage |
| Masse à vide (dry) | ~210 g | structure + avionique |
| Charge utile disponible | ~90 g | capteurs, batteries... |
| Autonomie cible | ~8 min | avec batterie 2S 350mAh |
| Motorisation | 2× DC (ø10mm, ~30W) | couple élevé pour 300g |

---

## Répartition par sous-système

| Sous-système | Masse | % MTOW | Composants clés |
|---|---|---|---|
| **Airframe** | 95 g | 31.7 % | Carbone 2mm, longerons 3mm, visserie titane |
| **Propulsion** | 60 g | 20.0 % | 2× DC ø10mm, 2× hélices 3" CF |
| **Avionique** | 30 g | 10.0 % | FCU (ESP32-S3), RX (ELRS 2.4GHz), GPS |
| **Batterie** | 80 g | 26.7 % | LiPo 2S 350mAh (~75g cells + wiring) |
| **Charge utile** | 35 g | 11.7 % | Module RF, LEDs, câblage |

---

## BOM simplifiée — Composants principaux

| Réf | Composant | Qté | Masse unitaire | Masse totale |
|-----|-----------|-----|----------------|--------------|
| AF-001 | Plaque carbone 2mm 100×60mm | 2 | 12 g | 24 g |
| AF-002 | Longerons carbone 3×100mm | 4 | 6 g | 24 g |
| AF-003 | Visserie titane M1.6×6 | ~30 | 0.3 g | ~9 g |
| AF-004 | Entretoises nylon M2 | 10 | 0.5 g | 5 g |
| PR-001 | Moteur DC ø10mm 3000KV | 2 | 14 g | 28 g |
| PR-002 | Hélices 3" carbone 3-blades | 2 | 8 g | 16 g |
| PR-003 | ESC 4-en-1 6A | 1 | 8 g | 8 g |
| AV-001 | FCU ESP32-S3 custom | 1 | 8 g | 8 g |
| AV-002 | Rx ELRS 2.4GHz | 1 | 4 g | 4 g |
| AV-003 | GPS NEO-M10Q | 1 | 6 g | 6 g |
| AV-004 | Câblage & connecteurs | 1 | 12 g | 12 g |
| BT-001 | Batterie LiPo 2S 350mAh | 1 | 75 g | 75 g |
| PU-001 | Module RF additionnel | 1 | 8 g | 8 g |
| PU-002 | LEDs + support | 1 | 5 g | 5 g |
| PU-003 | Réserve charge utile | 1 | 22 g | 22 g |
| **TOTAL** | | | | **~295 g** |

> ⚠️ Marges de tolérance de fabrication : ±10 g sur airframe et propulsion.
> ⚠️ La masse batterie dépend du lot fournisseur — vérifier avant assembly final.

---

## Notes DG

- Cette configuration est la **baseline de référence** pour les itérations DD et DC.
- La charge utile (35g) laisse de la marge pour capteurs additionnels (lidar miniature, caméra FPV).
- En l'absence de confirmation de masse réelle après fabrication du prototype M6, cette spec reste **provisoire**.

---
*Généré automatiquement — NE PAS signer sans validation DG*
