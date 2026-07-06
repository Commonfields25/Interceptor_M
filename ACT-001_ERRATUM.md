# ACT-001 — Erratum : Clarification de la nature de la pièce

**Date :** 6 juillet 2026  
**Fichier concerné :** `ACT-001`  
**Dépôt :** [Commonfields25/Interceptor_M](https://github.com/Commonfields25/Interceptor_M)

---

## Contexte

Une contradiction importante a été identifiée dans la documentation du dépôt concernant la pièce **ACT-001** :

- Les **anciens fichiers texte et notes de fabrication** (fichiers `.md` dans `/docs/` ou `/notes/`) décrivent ACT-001 comme une **petite platine de fixation pour l'électronique**, de dimensions approximatives 65 mm.
- Les **modèles 3D actuels** (fichiers STEP `.stp` et schémas SVG `.svg`) décrivent une pièce bien plus grande, d'environ **33 cm de long**, de forme tubulaire avec **3 axes de bifurcation**.

---

## Résolution

Après analyse des fichiers actuels du dépôt, la description basée sur les **modèles 3D (STEP/SVG)** est considérée comme la version de référence.

### Description correcte d'ACT-001

> ACT-001 est un **mécanisme de déploiement des ailes** du drone Interceptor-M.  
> Il s'agit d'un corps tubulaire de **~330 mm de long**, usiné ou imprimé en métal (AlSi10Mg), intégrant **3 axes de bifurcation** permettant le déploiement mécanique des ailes repliées dans le fuselage.

- **Fabrication :** DMLS (impression métal) — AlSi10Mg
- **Masse :** ~133 g
- **Dimensions réelles :** ~330 × 85 × variable mm
- **Fonction :** Mécanisme de déploiement des ailes (pas un support électronique)

### Pourquoi "3 axes" et "tubulaire" ?

- **"3 axes"** fait référence aux **3 points de bifurcation/articulation** du mécanisme, permettant le pliage/dépliage de chaque aile.
- **"Tubulaire"** décrit la forme du corps principal du mécanisme, qui s'insère dans le fuselage tubulaire du drone.

---

## Action requise

Les fichiers de documentation текстовые (`.md`) décrivant ACT-001 comme une platine de montage électronique sont **obsolètes** et doivent être mis à jour pour refléter la réalité du modèle 3D actuel.

---

*Rapport généré depuis l'analyse du dépôt `Interceptor_M`, branche `main`.*