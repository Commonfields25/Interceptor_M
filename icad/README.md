# Interceptor CAD (ICAD) Engine

ICAD est une application CLI de génération de pièces mécaniques de grade **L3 (Manufacturing)**. Elle remplace les anciens scripts FreeCAD par un moteur basé sur **Build123d** pour garantir une fidélité géométrique absolue (congés, chanfreins, tolérances).

## Fonctionnalités
- **Grade L3** : Géométries précises prêtes pour CNC et Impression 3D.
- **Multi-Export** : Génère des fichiers STEP (Ingénierie) et STL (Impression).
- **Dessins Techniques** : Génère automatiquement des vues 2D (SVG) pour les rapports.
- **Rapports Automatisés** : Fiches techniques Markdown avec masse calculée et métadonnées.

## Utilisation
```bash
PYTHONPATH=. python3 -m icad.cli interceptor_parts.yaml --output exports
```

## Pièces Supportées
- `BRK-001` : Structural Mounting Bracket.
- `ACT-001` : Actuator Mount & Thermal Plate.
- `NCR-001` : Nose-Cone Interface Ring.
