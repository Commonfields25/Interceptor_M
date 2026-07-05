# Manufacturing Drawings — D1 Industrial Design

Ce dossier contient les spécifications et dessins de fabrication pour les composants critiques du projet **Interceptor_M**.

## Composants

| Composant | Description | Matériau | Processus | Masse Cible | Statut |
|-----------|-------------|----------|-----------|-------------|--------|
| BRK-001 | Structural Junction Bracket | AlSi10Mg | DMLS + Pocketing | <90g | 🟡 En cours |
| ACT-001 | Actuator/FC/ESC Mount | AlSi10Mg | DMLS | 65g | 🟡 En cours |
| NCR-001 | Nose-Cone Interface Ring | 316L SS | CNC Turning | 110g | 🟡 En cours |

## Structure

```
manufacturing/
└── drawings/
    ├── README.md
    ├── BRK-001/
    │   └── BRK-001_SPEC.md
    ├── ACT-001/
    │   └── ACT-001_SPEC.md
    └── NCR-001/
        └── NCR-001_SPEC.md
```

## Processus de validation

1. **Spécifications** → Validation par D1 et Engineering Lead
2. **Dessins 2D** → Production dans LibreCAD
3. **Review** → Validation croisée avec les contraintes du BOM
4. **Approbation** → Signature par Jules (Engineering Lead)

## Traçabilité

- Fichiers source: `docs/PARAMETERS.json`
- Modèles 3D: `CAD/` (BRK-001, ACT-001, NCR-001)
- Budget masse: BOM v1.2.0

---
*Dernière mise à jour: 2026-07-05 | D1 Industrial Design*
