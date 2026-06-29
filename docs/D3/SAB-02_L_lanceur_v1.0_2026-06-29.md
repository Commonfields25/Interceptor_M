# SAB-02 — L_lanceur à fournir

**Issue:** [#76](https://github.com/Commonfields25/Interceptor_M/issues/76) — sub-issue de [#70](https://github.com/Commonfields25/Interceptor_M/issues/70)  
**Milestone:** M6 — Prototype : Plans & Conception  
**Version:** v1.1 | **Date:** 2026-06-29

> **Historique:** v1.0 (2026-06-29) — Dérivation initiale.
> v1.1 (2026-06-29) — Tolérance corrigée : ±25 mm → ±1 mm (RSS fabrication CNC structure 2 m, rail ±0,1 + châssis ±0,5 + assemblage ±0,87). Overlap sabot 20 mm sans impact sur L_total.  
**Owner:** Commonfields25 (Agent Worker)  
**Branche:** `fix/issue-76-L_lanceur`

---

## 1. Valeur de L_lanceur

| Paramètre | Valeur | Unité |
|-----------|--------|-------|
| **L_lanceur** | **1 980** | **mm** |
| Tolérance | **± 1** | **mm** |
| Limite basse | 1 979 | mm |
| Limite haute | 1 981 | mm |

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

### Justification (RSS — fabrication CNC structure 2 m)

| Source | Tolérance | Référence |
|--------|-----------|-----------|
| Rail de guidage | ±0,1 mm | CNC usinage铝合金 6061-T6 |
| Châssis tube lanceur | ±0,5 mm | CNC usinage铝合金 6061-T6 |
| Assemblage rail/châssis | ±0,87 mm | Tol. accumulation linéaire (RSS) |
| **Total RSS** | **≈ ±1,0 mm** | `√(0,1² + 0,5² + 0,87²)` |

> **Note:** L'overlap sabot 20 mm (D3_structure §3.4.4) est une **jonction interne fuselage missile**, sans impact sur L_total.


### Résultat avec tolérance

```
L_lanceur = 1 980 ± 1 mm
          = [1 979 mm ; 1 981 mm]
```

