---
agent: Amélioration Continue
action: Create / Refactor
timestamp: 2026-06-22T22:45:00Z
related_gate: G4 (Semaine 1-2)
status: Draft
---

# NOTE DE CADRAGE CAO — INTERCEPTOR_M
## Micro-drone Intercepteur — Avant-projet CAO

**Version :** v0.1-draft  
**Date :** 22.06.2026  
**Classification :** CONFIDENTIEL — Segment Défense  
**Source :** https://github.com/Commonfields25/Interceptor_M  
**Responsable rédaction :** Amélioration Continue  
**Destinataires :** D3 (Designer Défense), E1 / E2 / E3 (Ingénieurs)

---

## 1. OBJET ET PORTÉE

Cette note définit le périmètre de modélisation CAO (Inventor) du micro-drone intercepteur **Interceptor_M** pour la **Semaine 1–2** du PROTOTYPE_ROADMAP.

Elle ne constitue pas un plan de fabrication final. C'est un **point de départ** (avant-projet) basé sur les informations disponibles dans le repo à ce jour.

> ⚠️ **Point critique** : De nombreuses valeurs dimensionnelles sont des **propositions** (non encore validées par les ingénieurs). Aucune geometry ne doit être figée avant Gate G4.

---

## 2. CONTEXTE REPO — CE QUI EST CONNU vs INCONNU

### 2.1 Valeurs confirmées par le repo (fichiers analysés)

| Paramètre | Valeur | Source |
|---|---|---|
| MTOW | 250g | PROTOTYPE_ROADMAP.md |
| Visserie | M2 / M3 | PROTOTYPE_ROADMAP.md |
| Monture moteur standard | 9mm / 12mm | PROTOTYPE_ROADMAP.md |
| Architecture ROOT_ASSEMBLY | AIRFRAME + ELECTRONICS_TRAY + LAUNCHER_INTERFACE | PROTOTYPE_ROADMAP.md |
| Outil CAO principal | Autodesk Inventor | guidelines.md (D3) |
| Outil CAO secondaire | SolidWorks | guidelines.md (D3) |
| Tâches D3 Semaine 1 | TASK_DD_001 (modélisation airframe) | PROTOTYPE_ROADMAP.md |
| Tâches D3 Semaine 2 | TASK_DD_004 (design sabot) | PROTOTYPE_ROADMAP.md |
| Tâche E3 Semaine 1 | TASK_DD_002 (zones interdites battery/ESC/motor) | PROTOTYPE_ROADMAP.md |
| Tâche E1 Semaine 2 | TASK_DD_006 (vitesse sortie vs pression air) | PROTOTYPE_ROADMAP.md |

### 2.2 Valeurs NON définies dans le repo (à confirmer par les ingénieurs)

| Paramètre | Statut | Action requise | Responsable |
|---|---|---|---|
| Diamètre intérieur du tube lanceur | `[PROPOSÉ]` 40mm | Validation par E1 (contrainte pression) | D3 → E1 |
| Diamètre extérieur fuselage | `[PROPOSÉ]` 35mm | Validation par E1 (résistance G) | D3 → E1 |
| Longueur bras | `[PROPOSÉ]` 75mm | Analyse mass budget + compacité | D3 |
| Corde aile | `[PROPOSÉ]` 60mm | CFD requis — voir E2 | D3 → E2 |
| Envergure | `[PROPOSÉ]` 150mm | CFD requis | D3 → E2 |
| Pression de service lanceur | `[À DÉFINIR]` — | TASK_DD_006 (E1) | E1 |
| Vitesse de sortie drone | `[À DÉFINIR]` — | TASK_DD_006 (E1) | E1 |
| Volume batterie | `[PROPOSÉ]` — | TASK_DD_002 (E3) | E3 |
| Volume ESC | `[PROPOSÉ]` — | TASK_DD_002 (E3) | E3 |
| Volume FC | `[PROPOSÉ]` — | TASK_DD_002 (E3) | E3 |

---

## 3. PÉRIMÈTRE DE MODÉLISATION — CE QUE D3 DOIT PRODUIRE

### 3.1 Semaine 1 — Airframe primaire (TASK_DD_001)

**Objectif :** Modéliser la structure primaire du micro-drone, en se concentrant sur l'aérodynamique et le stockage compact.

Livrables attendus par D3 :
- [ ] `FUSELAGE.ipt` — tube principal, 35mmOD × paroi 2.5mm × ~100mm long [PROPOSÉ]
- [ ] `ARM_x4.ipt` — 4 bras, 75mm long, Ø5mm tube carbone [PROPOSÉ]
- [ ] `MOTOR_MOUNT_x4.ipt` — supports moteur standard 9/12mm [REPO-CONFIRMÉ]
- [ ] `WING_PANEL_x2.ipt` — panneaux aile, corde 60mm, envergure 150mm [PROPOSÉ]
- [ ] `FASTENER_M2_M3.ipt` — visserie M2/M3 pour assemblage [REPO-CONFIRMÉ]
- [ ] `ROOT_ASSEMBLY.iam` — assemblage des sous-ensembles ci-dessus

**Contraintes à intégrer :**
- Les dimensions sont des hypothèses de départ — **flaguer chaque feature comme `[PROPOSÉ]` dans iProperty**
- Garder le design **modulaire** : chaque sous-assemblage éditable indépendamment
- Prévoir des zones de flexibilité (slots d'ajustement) là où les contraintesengineering ne sont pas encore figées
- Créer un fichier `PARAMETERS.json` (fourni en annexe de cette note) pour piloter les variables globales

### 3.2 Semaine 2 — Interface Sabot / Lanceur (TASK_DD_004)

**Objectif :** Concevoir l'interface entre le drone et le tube du lanceur air comprimé.

Livrables attendus par D3 :
- [ ] `SABOT.ipt` — pièce d'interface sabot-drone [À DÉFINIR]
- [ ] `LAUNCHER_INTERFACE.iam` — sous-assemblage sabot + bride de fixation
- [ ] `TUBE_CLAMP.ipt` — bride de serrage sur tube Ø40mm [PROPOSÉ]
- [ ] `O_RING_SEAL.ipt` — joint torique d'étanchéité [À DÉFINIR par E3]

**Contraintes mécaniques critiques :**
1. **Étanchéité pneumatqiue** : le sabot doit assurer l'étanchéité pendant le remplissage en air comprimé (joint O-ring)
2. **Libération contrôlée** : le drone doit se séparer proprement du sabot à la sortie du tube (aucun contact parasite)
3. **Résistance G** : la structure doit résister aux accélérations de lancement estimées (à confirmer par E1 — TASK_DD_006)
4. **Géométrie compacte** : le drone doit se replier pour rentrer dans le tube Ø40mm [PROPOSÉ]

### 3.3 Fichiers complémentaires à produire

- [ ] `ELECTRONICS_TRAY.ipt` — plateau électronique avec découpes keep-out (volume fourni par E3 — TASK_DD_002)
- [ ] `PARAMETERS.json` — mis à jour avec les dimensions validées

---

## 4. CONTRAINTES PNEMATIQUES — VALIDATION E1 / E2 REQUISE

> ⚠️ **Ces contraintes ne sont PAS encore résolues.** Elles doivent être traitées par E1 (TASK_DD_006) et E3 (TASK_DD_005) avant toute validation CAO finale.

### 4.1 Vitesse de sortie vs pression (E1 — TASK_DD_006)

| Question | Réponse actuelle | Action |
|---|---|---|
| Pression de service ? | `[À DÉFINIR]` | E1 calcule (NDC) |
| Vitesse de sortie drone ? | `[À DÉFINIR]` | E1 calcule (NDC) |
| Force de résistance structurale requise ? | `[À DÉFINIR]` | E1 FEA sur TASK_DD_008 |
| Quel matériau pour le tube/interface ? | `[PROPOSÉ]` Carbone / PA12 impres. 3D | E1 valide |

**Formules de référence pour E1 :**
```
Énergie cinétique à la sortie :  E = ½ × m × v²
Travail du piston (gaz comprimé) : W = P × ΔV (approx. isotherme/adiabatique)
Accélération de lancement : a = F/m = P × A / m
```

### 4.2 Volume keep-out electronics (E3 — TASK_DD_002)

E3 doit fournir à D3 un modèle de zones interdites (fichier `.stp` ou `keepout_zones.pdf`) pour :
- **Batterie LiPo** : volume approximatif 40×20×15mm — à confirmer
- **ESC** : volume approximatif 30×15×8mm — à confirmer
- **FC (contrôleur de vol)** : volume approximatif 30×30×8mm — à confirmer
- **Moteurs brushless** : Ø12mm extérieur

Ces volumes doivent être intégrés comme **booléen négatif** dans le modèle CAO de l'electronics tray.

---

## 5. ZONES KEEP-OUT — RÈGLES À RESPECTER EN CAO

### 5.1 Zone propulsion (E2 à valider)

```
┌─────────────────────────────────────────────────────┐
│  ZONE PROPULSION — RAYON DE ROTATION HÉLICES        │
│  • Diamètre de fonctionnement : ~60mm [PROPOSÉ]     │
│  • Tolérance : +5mm par rapport à l'enveloppe       │
│  • Matériau bras : tube carbone 5mm OD minimum     │
│  • Fixation moteur : vis M2 sur support 9/12mm     │
└─────────────────────────────────────────────────────┘
```

### 5.2 Zone électrique (E3 à valider)

```
┌─────────────────────────────────────────────────────┐
│  KEEP-OUT ZONE — ÉLECTRONIQUE                       │
│  • Batterie et ESC : 0mm de contact (espace libre) │
│  • FC : protégé mécaniquement (caisson ou cadre)   │
│  • Routing câbles : chemins dédiés dans CAO        │
│  • Isolation vibratoire : silent blocks optionnels  │
└─────────────────────────────────────────────────────┘
```

---

## 6. FEUILLE DE ROUTE — LIVRAISONS D3 (SEMAINE 1–2)

| Semaine | Tâche | Fichier | Dépendance |
|---|---|---|---|
| S1-J1 | Créer structure dossiers | `models/DD/airframe/` | Aucune |
| S1-J2 | Modéliser fuselage | `FUSELAGE.ipt` | PARAMETERS.json |
| S1-J3 | Modéliser bras ×4 | `ARM_x4.ipt` | PARAMETERS.json |
| S1-J4 | Modéliser supports moteur | `MOTOR_MOUNT_x4.ipt` | Monture 9/12mm |
| S1-J5 | Modéliser panneaux aile | `WING_PANEL_x2.ipt` | Corde 60mm [PROPOSÉ] |
| S1 |Assembler ROOT | `ROOT_ASSEMBLY.iam` | Tous les sous-ensembles |
| S2-J1 | Définir géométrie sabot | `SABOT.ipt` | TASK_DD_006 (E1) |
| S2-J2 | Modéliser bride lanceur | `TUBE_CLAMP.ipt` | Ø40mm [PROPOSÉ] |
| S2-J3 | Intégrer zones keep-out | `ELECTRONICS_TRAY.ipt` | TASK_DD_002 (E3) |
| S2 | Assembler launcher | `LAUNCHER_INTERFACE.iam` | Sabot + bride |

---

## 7. CONTRÔLE QUALITÉ CAO — CHECKLIST AVANT GATE G4

Avant de soumettre le package Gate G4, D3 doit s'assurer que :

- [ ] Chaque fichier `.ipt` / `.iam` contient des **iProperties** remplis :
  - `Designer` = D3
  - `Status` = Draft / Review / Validated
  - `Source` = `PARAMETERS.json` (référence de la variable)
  - `Date` = date de modification
- [ ] Les fichiers de visserie M2/M3 sont modélisés (pas juste esquissés)
- [ ] L'assemblage ROOT ne contient que des **liens** vers les 3 sous-assemblies (AIRFRAME, ELECTRONICS_TRAY, LAUNCHER_INTERFACE)
- [ ] Chaque feature dont la dimension est `[PROPOSÉ]` est **pilotée par équation paramétrique** (pas de valeur en dur)
- [ ] Le PARAMETERS.json est à jour et reflète toutes les dimensions utilisées
- [ ] Peer review réalisé par D1 ou D2 avant soumission Gate G4

---

## 8. GOUVERNANCE ET RAPPORTS

| Événement | Action | Qui → Qui |
|---|---|---|
| Fin de Semaine 1 | Rapport d'avancement à Agent Manager | D3 → AM |
| Blocage sur dimension | Flag immediate dans DECISION_LOG | D3 → AM |
| Résultat NDC disponible | Mise à jour PARAMETERS.json | E1 → D3 |
| Zones keep-out disponibles | Envoi fichier à D3 | E3 → D3 |
| Gate G4 prêt | Package pour DG | AM → DG |

---

## ANNEXE — PARAMETERS.json (extrait, à jour)

Le fichier `PARAMETERS.json` complet est disponible dans le livrable séparé `PARAMETERS.json`.

**Variables clés pour D3 :**

| Variable | Valeur actuelle | Statut |
|---|---|---|
| `tube_diameter_mm` | 40 | [PROPOSÉ] |
| `fuselage_outer_diameter_mm` | 35 | [PROPOSÉ] |
| `arm_length_mm` | 75 | [PROPOSÉ] |
| `wing_chord_mm` | 60 | [PROPOSÉ] |
| `fasteners` | M2 / M3 | REPO-CONFIRMÉ |
| `motor_mount_mm` | 9 / 12 | REPO-CONFIRMÉ |

---

*Document généré le 22.06.2026 par Amélioration Continue — UAV Venture*
*Ce document est vivant : toute modification doit être tracée en tête du fichier.*
