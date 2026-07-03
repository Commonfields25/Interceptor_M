---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# Manufacturing Notes — ACT-001 (Vérin Tubulaire 3 Axes)

## Spécification dominante
**Spec E3** (tightest surface finish Ra 0.8 µm / IT7) — MTOW-insensitive
Geometry driven by functional envelope, NOT by scale.

## Matériau & Stock
- **Matériau** : AlSi10Mg poudre (SLM/DMLS)
- **Post-traitement** : T6 stress-relief + hip (Hot Isostatic Pressing)

## Opérations d'usinage CNC (post-DMLS)
| Op | Description | Tool | Tolérance |
|----|-------------|------|-----------|
| OP10 | Dresser faces d'appui vérin | Fraise 40mm | IT7 |
| OP20 | Aléser alésages tubes internes | Alesoir 6mm | IT7 |
| OP30 | Usiner rainures de guidage | Fraise 2mm | IT7 |
| OP40 | Tarauder M2x0.4 (6× fixations) | Taraud M2 | IT7 |

## Tolérances critiques
- Concentricité alésages : Ø 0.01 mm (IT7)
- Rugosité pistes de guidage : Ra 0.8 µm
- Paralélisme axes : 0.02 mm/100mm

## Finitions
- Polissage electrolyte (buffing)
- Revêtement DLC (Diamond-Like Carbon) optional
- Nettoyage ultrasons avant assembly

## QC
- CMM 100% suraxe principal
- contrôle force déploiement (bench test)
- contrôle jeu fonctionnel < 0.03mm
