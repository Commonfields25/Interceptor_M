---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# Synthèse Fabrication Additive — Interceptor M

## Vue d'ensemble

La fabrication additive (AM) est le procédé primaire pour BRK-001 et ACT-001.
Deux approches complémentaires selon criticité et volume :

---

## 1. DMLS / SLM — AlSi10Mg (Primary Structural)

### BRK-001 — Coque fuselage
- **Procédé** : DMLS (Direct Metal Laser Sintering)
- **Matériau** : AlSi10Mg poudre atomisée (30µm)
- **Densité** : > 99.5% théorique
- **Post-traitement** :
  1. Dépulvérisation (bead blasting)
  2. Heat treatment T6 (solution + aging)
  3. Hot Isostatic Pressing (HIP) — optionnel haute criticité
  4. Microbillage zones de fixation
  5. Anodisation noire Type III
- **Paramètres de build** :
  - Layer thickness : 30 µm
  - Laser power : 200–350 W
  - Scan speed : 700–1300 mm/s
  - Support structures : lattice-tree sur zones creuses
  - Orienté build optimal : face plane vers plateau

### ACT-001 — Vérin tubulaire avec lattice gyroid
- **Procédé** : DMLS/SLM
- **Matériau** : AlSi10Mg T6 + stress-relief
- **Gcométrie interne** : lattice gyroid TPMS (Triply-Periodic Minimal Surface)
  - Objectif : allègement interne sans thérapeut structural
  - Volume fraction : 15–25% (à optimiser par FEA)
- **Post-traitement** :
  1. HIP obligatoire (porosité interne < 0.2%)
  2. Electro-polishing (Ra < 0.8 µm)
  3. DLC coating optional sur pistes de guidage

---

## 2. FDM / FFF — ASA/ABS (Prototype only)

### NCR-001 — Prototype carénage
- **Usage** : prototype non-structural uniquement
- **Matériau** : ASA ou ABS-HR (UV-resistant pour outdoor)
- **Orientation** : flat-on-build-plate (minimise supports)
- **Supports** : tree/line auto-generated
- **Note** : ne pas utiliser en production — non NADCAP

---

## 3. Décision matrix — Procédé vs. pièce

| Critère | DMLS AlSi10Mg | FDM ASA | Layup Nomex-CF |
|---------|---------------|---------|----------------|
| Pièce | BRK-001, ACT-001 | NCR-001 proto | NCR-001 prod |
| Résolution | ±0.05mm | ±0.2mm | dépendant |
| Finish surface | 1.6 µm Ra | 12 µm Ra | 3.2 µm Ra |
| Masse finale | optimisée | indicative | optimisée |
| Coût unitaire | $$$ | $ | $$$ |
| Volume production | petites séries | prototype | petites/moyennes |
| Certification | aerospace-ready | non-certifiable | NADCAP possible |

---

## 4. Recommandations DFM (Design for Manufacturability)

1. **Wall thickness minimum** : 0.8 mm (dMLS AlSi10Mg) — respecté sur toutes lignes
2. **Overhang angle** : > 45° → supports requis ; < 45° → auto-supported
3. ** hatch spacing** : 0.12–0.18 mm (surface quality vs. speed)
4. **Escape holes** : usiner avant DMLS ou chanfreiner après pour evacuation poudre
5. **Surface finish** : post-process required (machining/milling pour zones fonctionnelles)

---

## 5. Ingénieur Conception & Design Industriel — Profil

### Poste : Ingénieur Conception & Design Industriel (H/F)
**Département** : R&D / Bureau d'Études

### Objectif du poste
Concevoir et industrialiser les pièces mécaniques du drone Interceptor M en optimisant
coûts, manufacturabilité et performances structurales. Interface privilégiée entre
conception CAO et procédés de fabrication additive / CNC / composites.

### Missions principales
1. **Conception CAO** : modélisation SolidWorks/CATIA/NX, mise en plan GD&T,
   définition interfaces mécaniques BRK/ACT/NCR
2. **DFM / DFA** : optimisation conception pour DMLS, CNC et layup composite ;
   réduction masse sans thérapeut性能 (topology optimization)
3. **Spécification matériaux** : AlSi10Mg (DMLS), Nomex-CF, titane TA6V ;
   sélection traitements thermiques et finitions
4. **Prototypage** : gestion全过程 prototype → production ; coordination fournisseurs AM
5. **Amélioration continue** : analyse modes de défaillance, retour d'expérience production

### Profil requis
- **Formation** : Ingénieur ENISE/INSA/Arts et Métiers/mécanique ou équivalent
- **Expérience** : 3–5 ans en conception mécanique et fabrication additive industrielle
- **Compétences techniques** :
  - Maîtrise CAO : SolidWorks mandatory, CATIA ou NX appreciated
  - GD&T selon ASME Y14.5 / ISO 1101
  - Connaissance procédés AM : DMLS/SLM, FDM, FDM-FFF
  - Connaissance matériaux métalliques et composites
  - Notions de calculs éléments finis (Abaqus/Nastran appreciated)
- **Soft skills** : autonomie, rigueur, capacité à arbitrer design vs. coût

### Conditions
- CDI — poste basé [lieu à préciser]
- Rémunération : selon expérience
- Avantages : mutuelle, tickets restaurant, participation
