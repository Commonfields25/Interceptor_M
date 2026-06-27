# Manufacturing Notes — BRK-001 (Structure Primaire)

## Matériau & Stock
- **Matériau** : AlSi10Mg poudre (SLM/DMLS)
- **Post-traitement** : T6 (solubilisation + vieillissement)
- **Stock initial** : 15–20% surépaisseur sur dimensions finies

## Opérations d'usinage CNC (post-DMLS)
| Op | Description | Tool | Tolérance |
|----|-------------|------|-----------|
| OP10 | Surfacer face de référence | Fraise 50mm | IT10 |
| OP20 | Percer trous de fixation M3 (4×) | Foret 2.5mm | IT10 |
| OP30 | Aléser logement vérin | Alesoir 8mm | IT7 |
| OP40 | Fraiser rainures cable management | Fraise 3mm | IT10 |

## Tolérances critiques
- Planéité surface externe : 0.05 mm
- Concentricité alésage/visserie : Ø 0.03 mm
- Rugosité face interne : Ra 1.6 µm

## Finitions
- microbillage (shot peening) zones de fixation
- anodisation noire type III (MIL-A-8625 Type II)
- inspection finale : control optical 3D

## QC
-CMM sur 5 points de référence
- contrôle masse : 111.78g ± 5%
- certificat matériau (powder batch traceability)
