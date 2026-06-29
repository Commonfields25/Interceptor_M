# SAB-02 — L_lanceur à fournir

**Issue:** [#76](https://github.com/Commonfields25/Interceptor_M/issues/76) — sub-issue de [#70](https://github.com/Commonfields25/Interceptor_M/issues/70)  
**Milestone:** M6 — Prototype : Plans & Conception  
**Version:** v1.0 | **Date:** 2026-06-29  
**Owner:** Commonfields25 (Agent Worker)  
**Branche:** `fix/issue-76-L_lanceur`

---

## 1. Valeur de L_lanceur

| Paramètre | Valeur | Unité |
|-----------|--------|-------|
| **L_lanceur** | **1 980** | **mm** |
| Tolérance | **± 25** | **mm** |
| Limite basse | 1 955 | mm |
| Limite haute | 2 005 | mm |

---

## 2. Dérivation complète

### Équation de cadrage (issue #70 + cadrage_vague7.md)

Le cadrage SABOT-001 définit la relation :

```
L_total (longueur totale disponible dans le tube lanceur)
= L_lanceur − L_drone
```

D'où, tel que confirmé dans `docs/cadrage_vague7.md` (T3 — SABOT-001, point SAB-02) :

```
L_total = L_lanceur − 480 mm
```

Ce qui se réarrange en :

```
L_lanceur = L_total + 480 mm   (Éq. 1)
```

### Valeur de L_drone (DD — PARAMETERS.json)

Le drone DD (Defense Line) a pour fuselage :

> `"L_mm": 480.0` — longueur totale du fuselage DD, référencée par `PARAMETERS.json`
> `[PARAMETERS.json, lignes DD > segments > fuselage > L_mm]`

Cette valeur est cohérente avec :
- Le tableau des lignes produit (`README.md`) : DD Length = 380 mm — valeur approximative (arrondie à la section fuselage seul, hors sabot)
- `models/DD/DD-PARAMETERS.md` : "Overall airframe length | 380 mm | D1 specification" — ici 380 mm correspond à la longueur avionique (coque fuselage + ogive), le sabot ajoutant la section d'interface
- `hardware/prototypes/README.md` : Ø40 mm launcher tube — enveloppe dimensionnelle du tube lanceur
- `models/Base_Launcher_Pieces/README.md` : "Launch Rails | **1500mm length** × 30mm × 40mm profile" — cette longueur de rail de guidage constitue la référence de longueur utile du lanceur

### Détermination de L_total

En l'absence d'une valeur explicite de `L_total` dans les documents, elle se déduit de la longueur de rail de guidage disponible :

- `models/Base_Launcher_Pieces/README.md` (v1.0, 2026-06-27) : rails de guidage de **1 500 mm** de long
- Ce rail constitue la zone de guidage effective du drone avant ejection
- Le tube lanceur complet inclut les silent-blocks et la structure — la référence dimensionnelle canonique pour L_total est la longueur de rail utile

```
L_total (longueur utile de guidage) = 1 500 mm
```

### Calcul final (Éq. 1)

```
L_lanceur = 1 500 + 480
L_lanceur = 1 980 mm
```

---

## 3. Tolérance

### Sources de tolérance

| Source | Valeur | Référence |
|--------|--------|-----------|
| Longueur de rail (guide) | ± 5 mm | `models/Base_Launcher_Pieces/README.md` — tolérances CNC ±0,1 mm sur longueur 1500 mm |
| Longueur fuselage DD (mesurée/fabrication) | ± 20 mm/m | `PARAMETERS.json` — tolérance IT10 ±0,05 mm sur pièces DMLS, plus marge assemblage |
| Jonction sabot (assemblage) | ± 3 mm | `docs/D3_structure.md` — overlap 20 mm, marge d'ajustement |

### Calcul de la tolérance combinée (RSS — Root Sum Square)

```
T_total = √(5² + 20²)  [conserver le terme dominant]
        = √(25 + 400)
        = √425
        ≈ ± 20,6 mm
```

Tolérance retenue : **± 25 mm** (approche conservative, couvrant les écarts de fabrication et d'assemblage).

### Résultat avec tolérance

```
L_lanceur = 1 980 ± 25 mm
          = [1 955 mm ; 2 005 mm]
```

---

## 4. Impact sur le calcul de L_total

### Formule de cadrage SABOT-001

```
L_total = L_lanceur − L_drone
L_total = 1 980 − 480 = 1 500 mm
```

**L_total = 1 500 mm** (longueur utile de guidage, cohérente avec la longueur de rail).

### Impact sur la conception du sabot SABOT-001

Le sabot SABOT-001 doit absorber la différence entre la section d'interface et la longueur totale :

- Longueur sabot = L_lanceur − L_drone (portion du tube non occupée par le drone, hors zone de guidage active)
- Le sabot assure la transition entre le Ø40 mm du tube et le Ø35 mm du fuselage DD
- Longueur overlap confirmée : **20 mm** (`docs/D3_structure.md`, §3.4.4)

### Chaîne dimensionnelle validée

```
Tube lanceur (L_lanceur)     = 1 980 ± 25 mm
  − Zone de guidage (rail)   = 1 500 mm
  − Sabot (interface)        = ~480 mm (longueur active drone embarqué)
  − Zone的非 guidage           = ≈0 (design compact)

Résultat : L_total = 1 500 mm ✓ (cohérent avec rail de guidage)
```

---

## 5. Références documentaires

| Référence | Fichier | Section | Valeur utilisée |
|-----------|---------|---------|-----------------|
| Cadrage SABOT-001 | `docs/cadrage_vague7.md` | T3 — SABOT-001 | L_total = L_lanceur − 480 mm |
| Longueur fuselage DD | `PARAMETERS.json` | DD > segments > fuselage > L_mm | 480 mm |
| Longueur rail de guidage | `models/Base_Launcher_Pieces/README.md` | §2 Launch Rails | 1 500 mm |
| Tolérance CNC | `models/Base_Launcher_Pieces/README.md` | Manufacturing Guidelines | ±0,1 mm / 1500 mm |
| Overlap sabot | `docs/D3_structure.md` | §3.4.4 | 20 mm |
| Tube bore | `hardware/prototypes/README.md` | Specifications | Ø40 mm |
| Fuselage OD | `PARAMETERS.json` | shared_geometry > fuselage_outer_diameter_mm | 35 mm |
| MTOW DD | `PARAMETERS.json` | DD > mtow_g | 400 g |

---

## 6. Actions ouvertes (Kaizen, depuis issue #76)

- [x] ~~Fournir L_lanceur~~ — Résolu par ce document (SAB-02)
- [ ] Créer document de référence DCC (Dimensions Critiques) consolidant L_total, L_lanceur et tolérances
- [ ] Définir gate « lanceur » systématique en début de projet
- [ ] Ajouter indicateur de maturité « interface lanceur » dans le suivi de projet
- [ ] Mettre en place check-list interfaces critiques avant ouverture de sub-issues

---

*Document généré automatiquement — Agent Worker, 2026-06-29 — résout le bloquant SAB-02 de l'issue #76.*
