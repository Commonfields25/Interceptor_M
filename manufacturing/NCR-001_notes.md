# Manufacturing Notes — NCR-001 (Carénage Aero)

## Matériau & Stock
- **Production** : Nomex honeycomb HRH 327 + peaux CF (layup manual)
- **Prototype** : ASA/ABS FDM printing (non-structural)
- **Stacking sequence** : [+45/-45/0/90/0/-45/+45]s

## Opérations (layup production)
| Op | Description | Standard |
|----|-------------|----------|
| OP10 | Découpe noyaux Nomex CNC | IT10 |
| OP20 | Pré-imprégnation peaux CF | aerospace spec |
| OP30 | Mise sous vide (autoclave 7 bar / 135°C) | NADCAP |
| OP40 | Post-cuisson & débulage | NADCAP |

## Tolérances critiques
- Épaisseur paroi sandwich : ±0.3 mm
- Planéité carène externe : 1 mm/m
- Rugosité surface externe (CF) : Ra 3.2 µm

## Finitions
- Ponçage léger + mastic époxy
- Peinture radar-absorbing (RAM) si requis
- Installation inserts métalliques M3 (bonded)

## QC
- Contrôle nondestructif (ultrasons c-scan)
- Contrôle dimensionnel : 3D scanning
- Test de pression interne (burst test)
