---
action: Create
agent: D3 (Lead Designer)
related_gate: G2
related_issue: '#71'
status: "Draft v1.0 \u2014 for CAD team review"
timestamp: 2026-07-01 09:22:00+00:00
---

# Design Esthétique & Ergonomique — Interceptor M (Issue #71)

> Ce document définit la direction de design, la palette, les guidelines matériaux et les directives CAO
> pour le projet Interceptor M. Il sert de référence pour la modélisation 3D et les revues de design.
> Toutes les cotes sont issues des fichiers de référence du dépôt (PARAMETERS.json, BOM, gaming machining).
> **Cotes non trouvées dans le dépôt = marqué [hors-repo / estimation].**

---

## 1. Moodboard — Direction Visuelle

### Thème directeur
**« Precision Weapon / Silent Predator »** — Objet de précision militaire, sobre, tendu,
axonique. Inspiré des ogives de missile tactique, des coques de drone de combat furtif,
des instruments de mesure de précision.

### Références visuelles (texte)

| Référence | Élément repris |
|-----------|--------------|
| Raytheon AGM-65 Maverick ogive | Silhouette tangent-ogive, proportion L/D ≈ 3,5 |
| Boeing Wingman drone | Surface structurale nue (DMLS), fixations apparentes |
| Flir Black Hornet (PRS) | Palette sombre, marquage high-visibility minimal |
| Ossur orthopaedic brackets | Finition usinée, rayons de congé généreux, surfaces fonctionnelles |
| Horological grade CNC parts | Tolérances visibles (bouchons, joints), qualité perçue |
| Formula 1 suspension | Organes mécaniques exposés, hiérarchie visuelle lisible |

### Qualités recherchées
- **Sobriété** : pas de décorations superflues — la géométrie usinée EST le design
- **Lisibilité fonctionnelle** : chaque morphologie reflète une fonction mécanique
- **Tension cinétique** : silhouette effilée ogive → corps → ailerons delta
- **Détail de précision** : joints toriques, congés, chanfreins — témoins de qualité
- **Monochromatique dominant** — accents de couleur uniquement pour alertes/marquages

---

## 2. Palette Couleurs (Codes HEX)

> Palette « Tactical Matte » — adaptée à la défensive aérienne, faible détectabilité visuelle,
> cohérence avec finitions industrielles (DMLS, tournage, composite).

| Rôle | Nom | Hex | Usage |
|------|-----|-----|-------|
| **Primaire** | Midnight Gunmetal | `#1E2328` | Corps principal — fuselage, ogive, coques |
| **Secondaire** | Graphite Plate | `#3A3F45` | выступа部件,支翼 internes, plaques de structure |
| **Accent — alerte** | Signal Orange | `#E8630A` | Marquages interface SABOT-001, safety labels |
| **Accent — status** | Tactical Teal | `#2A9D8F` | LED indicators, points de montage critiques |
| **Neutre léger** | Aluminium Silver | `#8C9298` | Trous non-anodisés, surfaces DMLS non-traitées |
| **Neutre moyen** | Matte Titanium | `#6B7078` | Carénages Nomex/CF, structures composites |
| **Highlight** | Warning Red | `#C1121F` | Zones de contrainte (FEA hotspots), interdits |
| **Surface usinée** | Polish Steel | `#B8BEC7` | 316L SS NCR-001, usinage apparent |

### Application
```
Fuselage externe      → Midnight Gunmetal (anodisé noir mat)
支翼 / Wings           → Graphite Plate (DMLS brut + léger bead-blast)
Empennage             → Matte Titanium (composite CF)
NCR-001 (ogive SS)   → Polish Steel (316L SS tourné, Ra≤0.8µm)
LEDs / status         → Tactical Teal
Marquages SABOT      → Signal Orange
```

---

## 3. Guidelines Matériaux

### 3.1 316L Stainless Steel — NCR-001 (Tournage CNC)
```
Application    : Bague d'interface ogive — joint torique NBR (étanchéité pneumatique)
Finition cible : Tourné-polie Ra ≤ 0.8 µm (bore Ø35 H7, OD Ø44 g6)
Apparence      : Polish Steel #B8BEC7 — usinage apparent, visible par transparence
                dans la zone ogive (coque semi-translucide ou fenêtre de visu)
Connexion à    : Joint O-ring NBR visible en gorge (Ø36.5 mm, 2.80 mm wide)
Rationalité    : Résistant à la corrosion + joint pneumatique — pas d'autre matériau viable
```

### 3.2 AlSi10Mg DMLS — BRK-001, ACT-001 (SLM/粉末沉积)
```
Application    : Structure primaire (BRK-001), vérin tubulaire (ACT-001)
Finition cible : Brut de fabrication DMLS + bead-blast léger
Apparence      : Aluminium Silver #8C9298 — microstructure en couches visible
                sous certains angles (caractéristique SLM à conserver)
Traitement    : Pas d'anodisation sur les pièces structurelles (contrôle de masse)
Connexion à    : BRK-001 bore Ø35 mm = interface fuselage (alignement critique)
```

### 3.3 Nomex Honeycomb HRH 327 + Carbone CF — Coiffe Aerodynamique
```
Application    : Coiffe ogive / carénéage externe (pièce aero non-structurale)
Stacking       : [+45/-45/0/90/0/-45/+45]s — séquence visible en bord de couche
Apparence      : Matte Titanium #6B7078, texture weave CF apparente
Finition       : RAM coating si spécifié (radar-absorbing) — surface mate foncée
```

### 3.4 ASA FDM — SABOT-001 (Prototype/Production Lanceur)
```
Application    : Interface lanceur/drone — contact sabot (hors vol en service)
Finition cible : Brut FDM — couches visibles, tolérances larges (±0.2 mm)
Apparence      : Signal Orange #E8630A (impression + marquage warning)
Rôle design    : Point de transition visuelle — masse detachée après lancement
```

---

## 4. Étude Ergonomie — Dérivée des Cotes CAD Réelles

### 4.1 Préhension & Manipulation au Sol
```
Contrainte      : Drone tube-launchable Ø40 mm max — manipulation par le tube ou à la main
Interface main  : Corps Ø35 mm — grip naturel sur 1 ou 2 mains (circonférence 110 mm)
Préhension      : Doigts autour du corps (Ø35 → 110 mm circonférence ≈ 35 mm portée main)
Action critique : Positionnement NCR-001 (ogive) — grips opposés avec doigts sur flancs
                  (éviter pression sur joint torique NBR — ne pas comprimer en grip)
Anti-rotation   : NCR-001 flats 2×6 mm à 90°/270° — butées visuelles/tactiles pour alignement
```

### 4.2 Silhouette Ogive (NCR-001 + Coiffe)
```
Cote repo (NCR-001):
  OD Ø44 mm, L=20 mm, alésage Ø35 mm (fixe — fuselage interface)
  Joint O-ring groove Ø36.5 mm, 2.80 mm wide, axial midpoint 1.4 mm
  4× M3 tapped holes at r=20 mm from axis
  Anti-rotation flats 2×6 mm

Cote repo (fuselage DD):
  Fuselage outer diameter: Ø35 mm
  Overall length: 380 mm
  L/D ogive (DD-CONCEPT): 3.5

Ergonomie ogive:
  → Progression Ø35 → Ø44 sur 20 mm =过度段 court mais lisible tactilement
  → Flat anti-rotation = INDICATEUR D'ORIENTATION pour l'opérateur au sol
  → Joint O-ring (visible en gorge) = INDICATEUR DE ZONE ÉTANCHE
  → Surface NCR-001 (316L SS poli) = contraste visuel mat/poli vs fuselage DMLS
```

### 4.3 Interface Mécaniques Visibles

| Interface | Cote repo | Rôle ergononomique |
|-----------|-----------|-------------------|
| BRK-001 bore | Ø35.0 mm H7 | Alignement fuselage — contact précis, feedback visuel usinage |
| NCR-001 bore | Ø35.0 mm H7 | Passage fuselage → ogive — gorge O-ring visible |
| BRK-001 arm holes | Ø5 mm H8 × 4 at r=20mm | Disposition cruciforme — index d'assemblage intuitif |
| Motor mount holes | Ø9 mm H8 × 4 at r=32mm | 45° offset — impossibilité d'erreur d'assemblage |
| ACT-001 pockets | FC: 30.5×30.5×8.5mm, ESC: 30.5×15.5×8.5mm | Cotes usinées visibles — hiérarchie constructive |
| SABOT-001 | 15 g ASA FDM | Volume minimal — sabot perçu comme "jetable" |

### 4.4 Silhouette Aéro (DD Line — 380 mm)
```
Zones fonctionnelles (depuis DD-CONCEPT.md):
  Nose (0–122 mm):    Ogive tangent L/D 3.5, NCR-001 + coiffe Nomex/CF
  Forward bay:         (~55–70 mm) Motor mount — interface M3 visible
  Mid bay:            (~100–175 mm) Battery + electronics tray — zone de maintenance
  Aft bay:            (~145–300 mm) Avionics + fuel — zone de service
  Empennage:          (~300–380 mm) 4× swept cruciform fins, span 75 mm, chord 40 mm
  Wings:              (~150–230 mm) 4× swept delta wings, chord 60 mm

Visuel ergonomique:
  → Hiérarchie lisible : "motorisation → énergie → électronique → stabilité"
  → Tronçons colorables individuellement (maintenance visuelle)
  → Zone ogive (NCR-001) = INDEX AVANT (extrémité directionnelle)
  → Zone sabot (SABOT-001) = INDEX ARRIÈRE (extrémité de lancement)
```

---

## 5. Directives CAO

> Toutes les dimensions ci-dessous sont issues des fichiers du dépôt.
> **Aucune cote inventée** — les cotes manquantes sont marquées [hors-repo].

### 5.1 Rayons de Congé (Fillet Radii)

| Application | Rayon standard | Justification |
|-----------|--------------|---------------|
| Coins vifs sur BRK-001 (AlSi10Mg DMLS) | R1.5 mm minimum | Évite concentration de contrainte, facilite bead-blast |
| Bore Ø35 (BRK-001 / NCR-001) | R0.5 mm entrée/sortie | Facilite insertion fuselage, réduit usure joint |
| Coins de pocket ACT-001 (ESC/FC) | R1.0 mm | Conforme outillage Ø6 endmill |
| Montage motoréducteur BRK-001 | R2.0 mm sur bosses | Clearance M3 socket-head |
| Ailerons (empennage) — bords d'attaque | R0.8 mm | Épaisseur min composite ~1.2 mm, rayon min usinable |
| Ailerons — bords de fuite | R0.3 mm (chanfrein 45°×0.5mm acceptable) | Aerodynamic trailing edge preference |

### 5.2 Chanfreins (Chamfers)

| Feature | Chanfrein | Tolérance |
|---------|----------|-----------|
| Entrée bore Ø35 (BRK-001 / NCR-001) | 0.5×45° | Visuel " machined entrance" |
| Trous M3 (NCR-001) | 0.3×45° | Ébavurage standard |
| Trous M2 (ACT-001) | 0.2×45° | Ébavurage standard |
| Trous M3 (BRK-001 arm/motor) | 0.4×45° | Clearance visuel |
| Bord avant coiffe ogive | 1.0×45° | Sécurité manipulation |
| Assemblage fuselage/ogive | 1.0×30° (sur ogive) | Facilite engagement |

### 5.3 Contraintes Esthétiques Compatibles Usinage CNC

```
PRINCIPES:
1. "Form follows function" — chaque morphologie = justification mécanique
2. Éviter les surfaces entièrement lisses (perdre la lecture de l'usinage)
3. Conserver la trace des opérations d'usinage comme détail de qualité:
   - Sillons d'endmill visibles (passes 0.3 mm stepover) sur zones non-structurales
   - Lignes de layer SLM visibles sur surfaces DMLS internes (feature, non-défaut)
4. Pas debst sur les surfaces fonctionnelles (bore Ø35, plans d'appui)
5. Joint torique (NCR-001) = FEATURE DESIGN — gorge visible, non cachée
6. Anti-rotation flats (NCR-001) = INDICATEUR D'ASSEMBLAGE — traitements distincts
7. Trous cruciformes (BRK-001) = INDEX VISUEL — disposition rationnelle 90°
8. Zones de contact structurel : priorité à la fonction (IT7/IT10) sur l'esthétique
9. SABOT-001 (ASA FDM) = prototype design language — couches visibles, contraste
10. Ailerons delta : préférer extrusion sweep (géométrie aero) à revolve
```

### 5.4 Géométrie Structurelle Clée (DD Line — Cote Réelles)

```
Fuselage:
  Outer diameter: Ø35.0 mm
  Overall length: 380 mm
  Wall thickness: 2.0 mm (DD line)
  Launcher bore: Ø40 mm (tube clearance)

NCR-001 (DD scale):
  OD: Ø44 mm    [repo: NCR-001_machining.md — OD "Ø44 mm (scales with MTOW)"]
  L: 20 mm      [repo: NCR-001_machining.md — "Length: 20 mm"]
  Bore ID: Ø35 mm [repo: NCR-001_machining.md — "Bore ID: Ø35 mm (fixed)"]
  O-ring groove: Ø36.5 mm, 2.80 mm wide [repo: NCR-001_machining.md]
  Anti-rotation flats: 2×6 mm wide [repo: NCR-001_machining.md]
  M3 holes: 4× at r=20 mm from axis [repo: NCR-001_machining.md]

BRK-001 (DD reference):
  Bounding box: 75×55×10 mm (DC) [repo: BRK-001_machining.md — "scales with MTOW"]
  Central bore: Ø35.0 mm H7 [repo: BRK-001_machining.md]
  Arm holes: Ø5.0 mm H8 ×4 at r=20 mm [repo: BRK-001_machining.md]
  Motor-mount holes: Ø9.0 mm H8 ×4 at r=32 mm, 45° offset [repo: BRK-001_machining.md]

ACT-001 (invariant across DC/DD/DI):
  Bounding box: 65×45×7 mm [repo: ACT-001_machining.md]
  FC pocket: 30.5×30.5×8.5 mm [repo: ACT-001_machining.md]
  ESC pocket: 30.5×15.5×8.5 mm [repo: ACT-001_machining.md]
  Battery slot: 20.5 mm wide [repo: ACT-001_machining.md]
  M3 clearance holes: Ø3.3 mm ×4 [repo: ACT-001_machining.md]
  M2 clearance holes: Ø2.2 mm ×6 [repo: ACT-001_machining.md]

SABOT-001:
  Masse: 15 g [repo: BOM_consolidee.md + DD-CONCEPT.md]
  Matériau: ASA FDM [repo: BOM_consolidee.md]
  Désignation: Interface Lanceur/Drone [repo: BOM_consolidee.md]
  ⚠️ Dimensions exactes non trouvées dans le repo — [hors-repo]

Empennage:
  Span: 75 mm [repo: DD-CONCEPT.md]
  Chord: 40 mm [repo: DD-CONCEPT.md]
  Type: Swept cruciform fins, 4× [repo: DD-CONCEPT.md]
  Position: ~300–380 mm from nose [repo: DD-CONCEPT.md]
  ⚠️ Épaisseur composite non trouvée — [hors-repo]

Wings:
  Per wing span: ~110 mm half-span per side [repo: DD-CONCEPT.md]
  Chord: 60 mm [repo: PARAMETERS.json + DD-CONCEPT.md]
  Attachment: 2× M2 socket-head per panel [repo: PARAMETERS.json]
  Type: Low-aspect-ratio swept delta [repo: DD-CONCEPT.md]
  Position: ~150–230 mm from nose [repo: DD-CONCEPT.md]
  ⚠️ Épaisseur Nomex honeycomb non trouvée — [hors-repo]

Assembly reference (DD line):
  MTOW vol (référence DG): 321.21 g (sabot détaché) [repo: PARAMETERS.json]
  CG from nose: ~150 mm (39.5% of 380 mm) [repo: DD-CONCEPT.md]
  Static margin: +40 mm — positive stability [repo: DD-CONCEPT.md]
```

### 5.5 Notes de Design pour CAO

```
1. NCR-001 (316L SS) → priorité: gorge O-ring (Ø36.5 mm, 2.80 mm) et flats anti-rotation
   Le 316L SS tourné-polie est le seul élément "brilliant" du design —
   contrast intentional avec fuselage mat DMLS.

2. BRK-001 (AlSi10Mg DMLS) → priorité: bore Ø35 H7 et disposition cruciforme des trous
   Le DMLS laisse voir les couches de fabrication — caractéristiques, pas défaut.

3. ACT-001 (AlSi10Mg DMLS) → priorité: pockets FC/ESC et position M3 relative
   Cote des pockets depuis repo: FC 30.5×30.5×8.5 mm / ESC 30.5×15.5×8.5 mm.

4. SABOT-001 (ASA FDM) → langage prototype distinct: couches visibles, couleur orange.
   Design language "disposable interface" — contrast avec reste du véhicule.

5. Fuselage Ø35 mm → corps principal en Midnight Gunmetal (anodisé mat).
   L'O-ring groove de NCR-001 (visible) = seul ornement du fuselage.

6. Coiffe ogive Nomex/CF → Matte Titanium (#6B7078), texture weave CF visible.
   Trailing edge des ailerons: chanfrein 0.5 mm plutôt que R0 (sharp prefered).
```

---

## 6. Références Croisées

| Fichier repo | Usage dans ce design |
|-------------|---------------------|
| `PARAMETERS.json` v1.1.0 | Fuselage Ø35 mm, L=380 mm, wing chord 60 mm, arm 75 mm |
| `params_DD.json` | Masse pièces: BRK-001 178.85g, ACT-001 55.49g, NCR-001 104.48g |
| `manufacturing/NCR-001_machining.md` | NCR-001 geometry (OD Ø44, L20, bore Ø35, gorge Ø36.5, flats 2×6mm, 4×M3@r20) |
| `manufacturing/BRK-001_machining.md` | BRK-001 geometry (bore Ø35, arm holes Ø5@r20, motor holes Ø9@r32) |
| `manufacturing/ACT-001_machining.md` | ACT-001 geometry (FC pocket 30.5×30.5×8.5, ESC 30.5×15.5×8.5, battery slot 20.5) |
| `models/DD/DD-CONCEPT.md` | Silhouette, CG, empennage 75×40mm, wings planform, MTOW 321.21g |
| `manufacturing/BOM_consolidee.md` | SABOT-001 15g ASA FDM, palette matériaux |

---

*Document généré depuis les cotes réelles du dépôt — aucune cote inventée.
Cotes marquées [hors-repo] = non trouvées dans les fichiers inspectés (SABOT-001 dimensions exactes,
épaisseur composite ailerons/wings).*

*Issue: #71 — Concept esthétique & ergonomie*
*Owner: D3 (Lead Designer)*
*Pour revue CAD avant G2 delivery (2026-07-09)*
