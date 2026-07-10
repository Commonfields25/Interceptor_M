# Interceptor V3 — Dossier Complet

**Version:** V3 (redesign paramétrique)
**Repo:** `Commonfields25/Interceptor`
**Date:** 2026-07-10
**Status:** Dossier de synthèse initial — tickets INT-101→INT-504 en cours

---

## 1. État actuel du repo

### Ce qui existe (fichiers locaux)

| Fichier | Contenu | Status V3 |
|---|---|---|
| `README.md` | Specs V2, X-tail mixing, subassemblies, masse estimée ~7300g | À mettre à jour |
| `BOM.csv` | 85 lignes de pièces V2, masses estimées | ⚠️ 8587g (MTOW 6000g dépassé de 43%) |
| `assignment_matrix.csv` | 85 assignations sous-systèmes | À intégrer dans V3 |
| `interface_matrix.csv` | ~75 interfaces mécaniques/électriques | À enrichir avec V3 |
| `clipboard.txt` | Ticket backlog V3 complet (21 tickets, 5 épics) | Référence maître |

### Ce qui manque (trous critiques V2)

| Trou | Impact | Ticket V3 associé |
|---|---|---|
| **Pièces nacelle avant lift manquantes** (PROP-022→025) | Propulsion avant impossible à assembler | INT-301 |
| **Tilt pivot mechanism absent** (PROP-026) | Nacelles arrière non montables | INT-302 |
| **Profil NACA non pinning** (12–15%t/c vague) | Aero non validable | INT-101 |
| **Longueur boom non définie** (TAIL-001/002) | CG et stabilité non calculables | INT-201 |
| **Confusion ailerons 2 vs 4** | BOM dit 2, README dit 4 | INT-104 |
| **Masse BOM = 8587g vs MTOW 6000g** | Écrasant 43% de dépassement | INT-202 |

---

## 2. Spécifications techniques figées V3

### Aéronef

| Paramètre | Valeur | Notes |
|---|---|---|
| Envergure | **1600 mm** | Aile haute fixe |
| MTOW | **6000 g** | Cible — masse BOM actuelle 8587g (à résoudre) |
| Charge utile | ~1000 g | Après structure + propulsion + avionique |
| Vitesse cible | **97 m/s (~350 km/h)** | Option B — renforcement structurel |
| Autonomie | Batterie 12S 5000 mAh | Cellules à définir (C-rate affecte endurance) |

### Profil aérodynamique

| Paramètre | Valeur | Statut |
|---|---|---|
| Profil aile | **NACA 4412** (12% t/c) | ✅ Choisi — à valider et documenter (INT-101) |
| Profil X-tail | **NACA 4412** (~10% t/c) | Même profil, plus fin |
| Material | Sandwich carbone | Fibres Toray T300 |

### Configuration X-Tail asymétrique

| Surface | Angle | Rôle |
|---|---|---|
| UR (supérieur droit) | **+60°** | Couplé pas (pitch dominant) |
| UL (supérieur gauche) | **+60°** | Couplé pas (pitch dominant) |
| LR (inférieur droit) | **+30°** | Couplé lacet (yaw dominant) |
| LL (inférieur gauche) | **+30°** | Couplé lacet (yaw dominant) |

> **Pourquoi 60°/30° au lieu de ±45° symétrique ?**
> Un X symétrique ±45° annule le moment de lacet car les surfaces haute/basse sont des miroirs géométriques. Le split 60°/30° casse la symétrie : les surfaces à 60° génèrent plus de portance induite → plus de traînée → moment de lacet net à partir de la même déflexion. Le ratio 2:1 permet un tuning indépendant en firmware.

### Propulsion — 6 moteurs / 6 hélices

#### Moteurs lift (VTOL vertical)

| Réf | Position | Type | Spécification | Puissance |
|---|---|---|---|---|
| PROP-001 | Avant gauche | Outrunner BLDC Ø63mm | 800W peak, 12S | ~180g |
| PROP-002 | Avant droit | Outrunner BLDC Ø63mm | 800W peak, 12S | ~180g |
| PROP-003 | Arrière gauche | Outrunner BLDC Ø63mm | 800W peak, 12S | ~180g |
| PROP-004 | Arrière droit | Outrunner BLDC Ø63mm | 800W peak, 12S | ~180g |
| **Hélice lift (×4)** | — | 18×8" carbone ou nylon | Paires CW/CCW | ~95g/u |

#### Moteurs tilt (croisière + poussée)

| Réf | Position | Type | Spécification | Puissance |
|---|---|---|---|---|
| PROP-009 | Gauche | Outrunner BLDC Ø52mm | 600W peak, 12S, tilt 0–90° | ~145g |
| PROP-010 | Droit | Outrunner BLDC Ø52mm | 600W peak, 12S, tilt 0–90° | ~145g |
| **Hélice tilt L** | — | 16×10" carbone | Config push en croisière, CW | ~75g |
| **Hélice tilt R** | — | 16×10" carbone | Config push en croisière, CCW | ~75g |

#### ESCs et distribution

| Réf | Catégorie | Spécification |
|---|---|---|
| PROP-007 | ESC lift avant (×2) | 60A, 12S, alimente PROP-001+002 |
| PROP-008 | ESC lift arrière (×2) | 60A, 12S, alimente PROP-003+004 |
| PROP-018 | ESC tilt gauche | 80A, 12S |
| PROP-019 | ESC tilt droit | 80A, 12S |
| PROP-020 | PDB | 12S, rails 5V/12V, Anderson PP45 |

#### Pièces manquantes (à ajouter en V3)

| Réf | Nom | Justification |
|---|---|---|
| PROP-022 | Support moteur nacelle lift avant | Motor mount bracket Al 7075, bolt pattern Ø44mm |
| PROP-023 | Coquille nacelle lift avant | Fairing ABS/PA12, protège rotor |
| PROP-024 | Bras de pylône lift avant | Link FUS-007 → nacelle |
| PROP-025 | Support ESC lift avant | ESC mount sur pylône |
| PROP-026 | Pivot tilt (×2) | Pivot bearing bracket + hinge pin Al 7075/acier |

### Contrôle surfaces

| Surface | Qté | Type | Actionneur | Course max |
|---|---|---|---|---|
| Ailerons | 2 | Panneau carbone 10%t | WNG-006/007 servo 12g | ±20° |
| X-tail UR | 1 | Ruddervator carbone 10%t | XTAL-005 servo 25g | ±25° |
| X-tail UL | 1 | Ruddervator carbone 10%t | XTAL-006 servo 25g | ±25° |
| X-tail LR | 1 | Ruddervator carbone 10%t | XTAL-007 servo 25g | ±25° |
| X-tail LL | 1 | Ruddervator carbone 10%t | XTAL-008 servo 25g | ±25° |
| Tilt nacelles | 2 | Pivot servo | PROP-015/016 servo 35g | 0–90° |

---

## 3. Matrice pièce → sous-système → emplacement

| Part_ID | Nom | Sous-système | Emplacement physique |
|---|---|---|---|
| FUS-001 | Fuselage hull | Fuselage | Corps principal — épine dorsale |
| FUS-002 | Nose cone / radome | Fuselage | Pointe avant —罩 |
| FUS-003 | Wing root spar adapter | Fuselage | Junction fuselage/ailes |
| FUS-004 | Avionics tray | Fuselage | Baie avionique interne |
| FUS-005 | Payload bay inserts | Fuselage | Parois baie de charge utile |
| FUS-006 | Battery tray / cage | Fuselage | Baie batterie — glissement axial |
| FUS-007 | VTOL pylon mount front | Fuselage | Points de montage moteurs avant (×2) |
| FUS-008 | VTOL pylon mount rear | Fuselage | Points de montage nacelles tilt (×2) |
| FUS-009 | Landing gear strut front | Fuselage | Train avant (×2) |
| FUS-010 | Landing gear strut rear | Fuselage | Train arrière (×2) |
| FUS-011 | Wheel / tyre assembly | Fuselage | 4 roues — 2 directrices arrière |
| FUS-012 | Pushrod connectors | Fuselage | Ligne de chape sur toutes les surfaces |
| TAIL-001 | Tail boom tube L | Tail Boom | Tube CF Ø20×1.5mm — longeron gauche |
| TAIL-002 | Tail boom tube R | Tail Boom | Tube CF Ø20×1.5mm — longeron droit |
| TAIL-003 | Boom cross-brace | Tail Boom | Entretoise entre les deux longerons |
| TAIL-004 | X-tail hinge bracket (×4) | Tail Boom | Extrémité boom — pivot pour X-tail |
| TAIL-005 | X-tail surface root rib (×4) | Tail Boom | Embase de chaque surface X-tail |
| WNG-001 | Wing panel L | Wing | Panneau aile gauche — surface portante |
| WNG-002 | Wing panel R | Wing | Panneau aile droit — surface portante |
| WNG-003 | Main spar tube | Wing | Tube longeron principal traversant les 2 panneaux |
| WNG-004 | Aileron panel L | Wing | Trailing edge aile gauche |
| WNG-005 | Aileron panel R | Wing | Trailing edge aile droite |
| WNG-006 | Aileron servo L | Wing | Racine aile gauche — actionne WNG-004 |
| WNG-007 | Aileron servo R | Wing | Racine aile droite — actionne WNG-005 |
| WNG-008 | Wing-tip endcap L | Wing | Bouchon d'extrémité aile gauche |
| WNG-009 | Wing-tip endcap R | Wing | Bouchon d'extrémité aile droite |
| WNG-010 | Wing root fairing | Wing | Junction fuselage/aile — 2 pièces |
| XTAL-001 | X-tail surface UR | X-Tail | Surface sup. droite — +60° |
| XTAL-002 | X-tail surface UL | X-Tail | Surface sup. gauche — +60° |
| XTAL-003 | X-tail surface LR | X-Tail | Surface inf. droite — +30° |
| XTAL-004 | X-tail surface LL | X-Tail | Surface inf. gauche — +30° |
| XTAL-005 | X-tail servo UR | X-Tail | Monté sur TAIL-005 — actionne XTAL-001 |
| XTAL-006 | X-tail servo UL | X-Tail | Monté sur TAIL-005 — actionne XTAL-002 |
| XTAL-007 | X-tail servo LR | X-Tail | Monté sur TAIL-005 — actionne XTAL-003 |
| XTAL-008 | X-tail servo LL | X-Tail | Monté sur TAIL-005 — actionne XTAL-004 |
| XTAL-009 | X-tail mount brace | X-Tail | Entretoise boom → racine X-tail (×4) |
| XTAL-010 | X-tail pushrod | X-Tail | 8 pushrods — liaison servo → surface |
| PROP-001 | Lift rotor motor front L | Propulsion | Nacelle avant gauche — thrust vertical |
| PROP-002 | Lift rotor motor front R | Propulsion | Nacelle avant droit — thrust vertical |
| PROP-003 | Lift rotor motor rear L | Propulsion | Nacelle arrière gauche — thrust vertical |
| PROP-004 | Lift rotor motor rear R | Propulsion | Nacelle arrière droit — thrust vertical |
| PROP-005 | Lift rotor prop (×4) | Propulsion | Sur chaque moteur lift |
| PROP-006 | Lift nacelle shell (×4) | Propulsion | Coquille protection moteurs lift |
| PROP-007 | ESC lift front (×2) | Propulsion | Monté sur FUS-007 pylône avant |
| PROP-008 | ESC lift rear (×2) | Propulsion | Monté sur FUS-008 pylône arrière |
| PROP-009 | Tilt motor L | Propulsion | Nacelle tilt gauche — horizontal cruise |
| PROP-010 | Tilt motor R | Propulsion | Nacelle tilt droit — horizontal cruise |
| PROP-011 | Tilt nacelle assembly L | Propulsion | Nacelle tilt gauche complète avec mécanisme |
| PROP-012 | Tilt nacelle assembly R | Propulsion | Nacelle tilt droite complète avec mécanisme |
| PROP-013 | Tilt prop L | Propulsion | Hélice push cruise — gauche (CW) |
| PROP-014 | Tilt prop R | Propulsion | Hélice push cruise — droite (CCW) |
| PROP-015 | Tilt servo L | Propulsion | Sur articulateur tilt gauche |
| PROP-016 | Tilt servo R | Propulsion | Sur articulateur tilt droit |
| PROP-017 | Tilt pushrod/linkage | Propulsion | 2 pushrods liaison servo → pivot |
| PROP-018 | ESC tilt L | Propulsion | Dans nacelle tilt gauche |
| PROP-019 | ESC tilt R | Propulsion | Dans nacelle tilt droit |
| PROP-020 | PDB | Propulsion | Baie avionique FUS-004 — bus électrique central |
| PROP-021 | Battery 12S LiPo | Propulsion | Glisse dans FUS-006 — batterie principale |
| PROP-022 | Front lift nacelle motor mount | Propulsion | Support moteur avant — 2 pcs (NOUVEAU V3) |
| PROP-023 | Front lift nacelle shell | Propulsion | Coquille nacelle avant — 2 pcs (NOUVEAU V3) |
| PROP-024 | Front lift pylon link | Propulsion | Bras pylône avant — 2 pcs (NOUVEAU V3) |
| PROP-025 | Front lift ESC mount bracket | Propulsion | Support ESC avant — 2 pcs (NOUVEAU V3) |
| PROP-026 | Tilt pivot bracket | Propulsion | Pivot mécanisme tilt — 2 pcs (NOUVEAU V3) |
| AVN-001 | Flight controller | Avionics | Monté sur FUS-004 — cerveau du système |
| AVN-002 | GPS + magnetometer | Avionics | Surface supérieure aile — minimiser EMI |
| AVN-003 | IMU primary | Avionics | Sur FUS-004 tray |
| AVN-004 | IMU redundant | Avionics | Bus I2C séparé — redondance |
| AVN-005 | Baro / pitot module | Avionics | Prise de pression statique + dynamique |
| AVN-006 | Telemetry radio | Avionics | Liaison sol — UART vers AVN-001 |
| AVN-007 | Power module / current sensor | Avionics | Entre batterie et PDB |
| AVN-008 | Battery checker / buzzer | Avionics | Avertissement batterie basse |
| AVN-009 | Payload connector | Avionics | Baie de charge utile — power + data |
| AVN-010 | Antenna telemetry | Avionics | SMA bulkhead sur FUS-002 — pointe nose |
| STR-001 à STR-010 | Visserie et fixations | Structure | Distribution tout le drone |

---

## 4. Matrice des changements V2 → V3

| Domaine | V2 (existant) | V3 (cible) | Raison du changement | Ticket |
|---|---|---|---|---|
| **Profil aile** | 12–15% t/c (vague) | NACA 4412 (12%) | Permet calcul aero, coordonnées, polaire | INT-101 |
| **Longueur boom** | Non définie | À calculer (INT-201) | CG, bras de levier, stabilité | INT-201 |
| **X-tail sizing** | Non défini (chord/span/area) | À calculer (INT-102) | Autorité pitch/yaw, dimensionnement structurel | INT-102 |
| **Nacelle avant lift** | **ABSENTE du BOM** | PROP-022→025 ajoutés | Propulsion avant impossible sans ces pièces | INT-301 |
| **Mécanisme tilt** | Pivot non listé comme pièce | PROP-026 ajouté | Nacelle tilt non assemblable sans pivot bearing | INT-302 |
| **Masse BOM** | 8587g (43% over MTOW) | ≤6000g (cible) | Violation critique — 3 options de résolution | INT-202 |
| **Aileron count** | Ambigu (README 4, BOM 2) | Résolu: 2 ailerons (BOM correct) | Option B — README à corriger | INT-104 |
| **Mixing firmware** | Table générique | Mixing matrix complet documenté | X-tail 60°/30° asymétrique besoin logique custom | INT-404 |
| **CG envelope** | Non calculé | À calculer (INT-203) | Sensibilité VTOL au CG — contrôle en vol | INT-203 |
| **BOM airfoil column** | Absente | Ajoutée | Traçabilité profil par pièce | INT-401 |
| **BOM length column** | Absente pour TAIL | Ajoutée | Dimension boom pour CAD et structure | INT-401 |
| **Folder hierarchy** | Plate (flat) | Structuré (docs/cad/data) | Organisation engineering standard | INT-501 |

### Pièces G2 (nouvelle génération) introduites en V3

| Réf G2 | Remplace | Changement |
|---|---|---|
| PROP-022 | (nouveau) | Support moteur nacelle avant — pièce G2 |
| PROP-023 | (nouveau) | Coquille nacelle avant — pièce G2 |
| PROP-024 | (nouveau) | Bras pylône avant — pièce G2 |
| PROP-025 | (nouveau) | Support ESC avant — pièce G2 |
| PROP-026 | (nouveau) | Pivot tilt mechanism — pièce G2 |

---

## 5. Maquette de vol et phases de vol

### Séquence de vol

```
[HOVER VTOL]          [TRANSITION]           [CROISIÈRE]
 0° tilt                  0→90°                  90° tilt
 4 lift à fond       4 lift + 2 tilt          2 tilt only
 X-tail actif        X-tail + ailerons        X-tail + ailerons
 ~5s de transition                            ~97 m/s
```

### États du contrôleur de vol

| État | Tilt angle | Moteurs lift | Moteurs tilt | X-tail |
|---|---|---|---|---|
| HOVER | 0° | 100% throttle (égaux) | 0% | Actif |
| TRANSITION_UP | 0→90° | Réduction proportionnelle | Increase proportionnel | Actif |
| CRUISE | 90° | OFF ou ralenti | Poussée | Actif |
| TRANSITION_DOWN | 90→0° | Increase proportionnel | Réduction proportionnel | Actif |
| FAILSAFE_TILT | last pos ou 0° | 100% | 0% | Actif |

---

## 6. Masse actuelle — audit V2

| Sous-système | Masse (g) | Notes |
|---|---|---|
| Fuselage (FUS-001→012) | 2331 | |
| Tail Boom (TAIL-001→005) | 380 | |
| Wing (WNG-001→010) | 995 | |
| X-Tail (XTAL-001→010) | 395 | |
| Propulsion (PROP-001→021) | 3795 | ⚠️ Propulsion la plus lourde |
| Avionics (AVN-001→010) | 180 | |
| Structure (STR-001→010) | 431 | |
| **TOTAL BOM** | **8587 g** | ⚠️ +2587g vs MTOW 6000g |
| **Cible MTOW** | **6000 g** | Écart: +43.1% |

> La propulsion représente 44% de la masse totale BOM. L'audit de masse (INT-202) identifie les options A/B/C pour revenir sous 6000g.

---

## 7. Arbre de dépendances critiques (chemin long)

```
INT-202 (masse)  ──→  INT-401 (BOM V3)  ──→  INT-501 (Git push)
     ↑                            ↑
INT-301 (nacelles avant)     INT-402, INT-403
INT-302 (mécanisme tilt)            ↑
INT-201 (longueur boom)  ──→  INT-102 (X-tail sizing)
INT-101 (NACA profil)  ──→  INT-204, INT-205, INT-207  ──→  INT-503 (assemblage CAD)
```

> **INT-202 est le ticket le plus critique** — il bloque la BOM V3, tous les CAD en aval, et le push Git.

---

## 8. Structure repo cible V3

```
Interceptor/
├── README_V3.md              (mis à jour avec specs V3)
├── CHANGELOG_V3.md
├── docs/
│   ├── airfoils/
│   │   ├── NACA_4412_datasheet.md        (INT-101)
│   │   ├── X-tail_sizing_calculation.md  (INT-102)
│   │   └── aero_performance_summary.md   (INT-103)
│   ├── engineering/
│   │   ├── mass_audit_and_resolution.md  (INT-202)
│   │   └── cg_envelope.md               (INT-203)
│   └── firmware/
│       └── X-tail_mixing_table.md       (INT-404)
├── cad/
│   ├── fuselage/         (INT-204)
│   ├── wing/             (INT-205)
│   ├── boom/             (INT-206)
│   ├── xtail/            (INT-207)
│   ├── propulsion/       (INT-303, INT-304)
│   └── assemblies/       (INT-503, INT-305)
├── data/
│   ├── BOM_V3.csv        (INT-401)
│   ├── BOM_V2_backup.csv
│   ├── assignment_matrix_V3.csv (INT-402)
│   └── interface_matrix_V3.csv  (INT-403)
└── engineering/           (calcs, spreadsheets)
```

---

*Dossier généré depuis les fichiers sources du projet (README.md, BOM.csv, assignment_matrix.csv, interface_matrix.csv, clipboard.txt).*
*Toutes les spécifications sont des estimés d'ingénierie tant que les tickets V3 ne sont pas résolus.*
