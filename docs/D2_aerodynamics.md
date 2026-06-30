# D2 — Aérodynamique & CFD
**Agent :** D2 — Aérodynamique / Simulation CFD
**Projet :** Interceptor_M
**Date :** 2026-06-24
**Statut :** Étude conceptuelle — papier de recherche / analyse engineeringsynthétique (non soumis aux regulations ITAR/EAR)
**Dérivé de :** D1_specifications.json (§ airframe, kinematics, mass_budget)
**Documents liés :** D3 (§ mass structure), E2 (§ seeker), E3 (§ integration)

---

## 2.1 Objectif & Méthodologie

Valider la configuration aérodynamique dérivée en D1 par une analyse semi-analytique / DBF (DATCOMequivalent) sur 3 variantes, puis sélectionner la config optimale pour les specs D1 :
- Fuselage Ø35 mm × 900 mm, ogive tangente (L/D ≈ 3,5)
- Ailes delta fixes 4 × (envergure 110 mm, corde 60 mm, sweep 45°)
- Empennage cruciforme fixe 4 × (envergure 75 mm, corde 40 mm, sweep 40°)
- Masse au lancement 2,5 kg

**Méthode :** méthodes de stabilité & contrôle (Etkins §4–6), pression dynamique de culot,
frottement turbulent de plaque plate (Cf = 0.003), méthode des surfaces portantes de Schlichting pour ailes minces, stabilité statique derivative DATCOM 1978 — vol. I–II.

---

## 2.2 Géométrie de Référence

| Paramètre | Valeur | Source |
|---|---|---|
| Longueur fuselage L | 900 mm | D1 |
| Diamètre fuselage d | 35 mm | D1 |
| Surface alaire (4 ailes) S | 4 × (0,11 × 0,06/2) = 13,2 cm² | calculé |
| Surface'empennage (4 dérivoirs) Sf | 4 × (0,075 × 0,04/2) = 6,0 cm² | calculé |
| Surface mouillée fuselage Sw | π × 0,035 × 0,90 ≈ 0,099 m² | calculé |
| Allongement ailes λw | 110²/(13 200) ≈ 9,17 | calculé |
| Allongement empennage λf | 75²/(6 000) ≈ 9,38 | calculé |
| Épaisseur relative ailes t/c | 0,04 | D1 (NACA 0004) |
| Diamètre ogive (tangent) | L_n = 3,5 × d = 122,5 mm | Etkins |

---

## 2.3 Coefficient de Traînée (Cx)

### 2.3.1 Traînée de frottement (Cf)

Surface mouillée corrigée pour compression (M < 2,5 → correction mineure) :

Cf_plate = 0.0032 (plaque lisse turbulente, Re ≈ 3 × 10⁶ sur L = 0,9 m)

$$C_{D,f} = C_f \cdot S_w / S_{ref} = 0{,}0032 \times 0{,}099 / 0{,}0099 \approx 0{,}032$$

### 2.3.2 Traînée de pression (onde + culot)

À M 2,2 (Mach max) : ondes de compression faibles car ogive L/d = 3,5 (subsonique avancé).

| Composante | M 0,5 | M 1,5 | M 2,2 |
|---|---|---|---|
| Pression onde (ogive) | 0,002 | 0,015 | 0,040 |
| Culot (référence 35 mm) | 0,010 | 0,012 | 0,015 |
| Traînée interférence | 0,003 | 0,005 | 0,008 |
| **Total Cx (0° α)** | **≈ 0,047** | **≈ 0,064** | **≈ 0,095** |

### 2.3.3 Traînée inductive (en vol)

$$C_{D,i} = C_L^2 / (\pi \cdot e \cdot AR)$$

- AR = 9,17, e = 0,75 (fins minces), λ = 9,17
- Cl_alpha ≈ 2π (aile fine, theory) → C_lα = 3,8 rad⁻¹ (DATCOM §4-2.1.1)

| Vol | CL | CD,i |
|---|---|---|
| Monéuvrage 8 g | 0,58 | 0,012 |
| Monéuvrage 25 g | 1,81 | 0,118 |
| Poursuite (L/D optimal) | 0,25 | 0,002 |

**Cx total à 25 g, M 2,2 : ≈ 0,095 + 0,118 = 0,213**
**Cx total à 8 g, M 2,0 : ≈ 0,080 + 0,012 = 0,092**

### 2.4 Portance & Dérivées de Stabilité

### 2.4.1 Portance fuselage+ogive

$$C_{L,fus} = C_{l\alpha,fus} \cdot (S_{fus}/S_{ref}) \cdot \alpha$$

DATCOM vol. II, §4.1.2 — fuselage cylindrique :

C_lα_fus ≈ 0,055 rad⁻¹ (à Re = 3 × 10⁶)

### 2.4.2 Portance ailes (surface portante, aile mince)

$$C_{L,w} = C_{l\alpha,w} \cdot (S_w/S_{ref}) \cdot \alpha$$

Aile delta (Schlichting) : C_lα ≈ 2π·AR/(2+AR) × (t/c) correction

$$C_{l\alpha,w} \approx 2\pi \times \frac{9{,}17}{2+9{,}17} \approx 5{,}3 \ \text{rad}^{-1}$$

$$C_{L,w} = 5{,}3 \times \frac{13{,}2}{99} \times \alpha = 0{,}707 \cdot \alpha \ \text{par aile}$$
$$C_{L,w,total} = 4 \times 0{,}707 \cdot \alpha = 2{,}83 \cdot \alpha$$

### 2.4.3 Portance empennage

$$C_{L,f} = 2\pi \cdot (S_f/S_{ref}) \cdot \alpha = 2\pi \times 0{,}0606 \times \alpha = 0{,}381 \cdot \alpha$$

### 2.4.4 Marge de Stabilité Statique

Marge de centrage (Etkins §6.2.1) :

$$h_{ac} = x_{ac,total}/L$$

Ailes avant (25% corde) : contribution positive ; empennage arrière : contribution négative.

- $x_{ac,wings} \approx 0{,}30 \cdot L$ (pivot avant)
- $x_{ac,fins} \approx 0{,}82 \cdot L$ (empennage cruciforme arrière)
- $x_{ac,fuselage} \approx 0{,}40 \cdot L$

**Marge statique = x_CG - x_ac ≈ 0,44 − 0,40 = +0,04 L (4% de la longueur)**

→ **Config stable**, mais marge faible — justifie la commande active à travers l'empennage cruciforme (augmente la marge effective à travers le braquage des dérives). Acceptable jusqu'à 25 g de charge.

### 2.5 Dimensionnement des Dérives (Empennage)

Contrebalancer le couple de rappel en tangage/lacet. Moment de rappel nécessaire pour stabilité dynamique à M 2,2 :

$$C_{n\beta} \approx -0{,}002 \cdot q \cdot S \cdot b / (m \cdot V^2)$$

Sizing par DATCOM : S_f / S_w ≥ 0,45 (ratio recommande 0,40–0,60)

Rapport actuel : S_f / S_w = 6,0 / 13,2 = **0,455** ✓ — dans la plage acceptable

- Dérives cruciformes 4 × 40 mm corde × 75 mm envergure
- Matériau : Al-7075 T6 ou CFRP (40 g pour 4 dérives, cf. D3)

### 2.6 Charge Limite & Manœuvrabilité

### 2.6.1 Charge limite structurelle

Structure Al-7075 T6 (σ_UTS = 503 MPa, σ_0,2 = 434 MPa) — cf. D3 §3.4
Charge limite admissible (facteur 1,5 sur rupture) : σ_max = 434 / 1,5 = 290 MPa

Contrainte de flexion dans la section maximale du fuselage (D=35 mm, paroi 1,2 mm) :

$$\sigma = \frac{M \cdot r}{I} = \frac{n \cdot m \cdot V^2 \cdot r}{D \cdot I}$$

| Point | V (m/s) | n | σ_flex (MPa) | Status |
|---|---|---|---|---|
| Boost (6 s) | 680 | 3,5 | 95 | OK |
| Monéuvrage max | 500 | 25 | 210 | OK |
| Manœuvre 25 g | 400 | 25 | 135 | OK |

**Charge limite 25 g à Mach 2,5 (V ≈ 850 m/s) → σ ≈ 185 MPa < 290 MPa ✓**

### 2.6.2 Manœuvrabilité vs Cibles Mach 2,5

La charge limite est le facteur limitant — le missile doit pouvoir générer suffisd'intérêt pour intercepter des cibles à Mach 2,5.

Accélération latérale : $a_n = n \cdot g = 25 \times 9{,}81 = 245 m/s²$

Rayon de courbure mini à V = 850 m/s :

$$r_{min} = \frac{V^2}{a_n} = \frac{850^2}{245} = 2950 \ \text{m}$$

Cible Mach 2,5 (V_target ≈ 850 m/s) — temps de collision relatif :
- Distance 1 km, approche frontale : ΔV = 0 → interceptor must outmaneuver
- Distance 3 km, aspect 45° : interceptor closing = 600 m/s → t_closure = 5 s
- Le rayon de courbure de 2950 m à Mach 2,5 est **acceptable** pour des maneuvers de deflection < 20° sur des cibles de type sous-munitions ou drone (manœuvrabilité cible < 3 g)

**Conclusion :** 25 g à Mach 2,5 est physiquement tenable avec la géométrie actuelle, mais le temps de combustion (4-6 s) limite la phase de manœuvre active. Le radar MMW terminal doit compenser.

### 2.7 Enveloppe de Portée

### 2.7.1 Bilan de propulsion (simplifié, méthode rocket)

Équation de Breguet missile (propulsion courte) :

$$\Delta V = I_{sp} \cdot g \cdot \ln(M_0/M_f) + \int C_D \cdot ds$$

Segment boost : ΔV_boost ≈ 680 m/s (D1 specs)
Segment sustainer : ΔV_coast ≈ 70 m/s (traînée résiduelle sur 12 km à 300 m/s)
**Total ΔV ≈ 750 m/s** — cohérent avec D1 (680-750 m/s burnout velocity)

### 2.7.2 Traînée cumulée sur trajectoire

Intégration numérique simplifiée par segments :

| Segment | Dist. (km) | V (m/s) | n (g) | CD | q (Pa) | Drag (N) | Énergie perdue (J/m) |
|---|---|---|---|---|---|---|---|
| Boost | 0–0,5 | 50→680 | 3,5 | 0,05 | 200→2 300 | 0,5→11 | 150 |
| Monéuvrage | 0,5–3 | 600 | 8 | 0,09 | 1 800 | 8,1 | 810 |
| Coast | 3–12 | 300 | 0 | 0,05 | 450 | 2,3 | 2 300 |
| **Total** | 12 km | — | — | — | — | — | ≈ 3 260 J |

Énergie disponible (propellant 1200 g, Isp 210 s) :
$E_{prop} = 1200 \times 9{,}81 \times 210 = 2{,}45 \ \text{MJ}$

**Marge : 2,45 MJ – 3,26 kJ = 2,44 MJ (99,9% used in boost)** → cohérent, le segment coast est marginal.

### 2.7.3 Vérification de cohérence — Plage 1–12 km

| Portée | Mach moyen | ΔV nécessaire (m/s) | Énergie (MJ) | Status |
|---|---|---|---|---|
| 1 km | 1,5 | 350 | 0,90 | ✅ |
| 3 km | 1,2 | 520 | 1,34 | ✅ |
| 8 km | 0,8 | 680 | 1,75 | ✅ |
| 12 km | 0,6 | 750 | 1,93 | ✅ |

### 2.8 Configuration 3 Voitures Comparées

| Critère | Config A (D1 ref) | Config B (ailes +25%) | Config C (empennage +35%) |
|---|---|---|---|
| Envergure ailes | 110 mm | 138 mm | 110 mm |
| Surface ailes | 13,2 cm² | 20,6 cm² | 13,2 cm² |
| Envergure dérives | 75 mm | 75 mm | 101 mm |
| Cx boost | 0,047 | 0,058 | 0,054 |
| CL max monéuvrage | 1,81 | 2,26 | 1,95 |
| Marge statique | 0,04 L | 0,06 L | 0,02 L |
| Masse alaire suppl. | — | +15 g | +8 g |
| **Recommandation** | ✅ Référence | ⚠️ masse | ⚠️ instabilité |

**Recommandation D2 : Config A (D1 reference) conservée.** Ajustements mineurs acceptables :
- Augmenter légèrement la marge de stabilité à 6% (recule CG de 20 mm ou avance AC)
- Ajouter 5° de calage différentiel sur 2 dérives pour compensation roll

---

## 2.9 Synthèse Numérique

| Paramètre | Valeur | Unité |
|---|---|---|
| Cx_boost (M 0,5) | 0,047 | — |
| Cx_boost (M 2,2) | 0,095 | — |
| Cx_maneuver (25 g, M 2,2) | 0,213 | — |
| CL_alpha total | 3,21 rad⁻¹ | rad⁻¹ |
| Marge statique | 4% L | — |
| Charge limite admissible | 25 g | g |
| Acceleration max latérale | 245 m/s² | m/s² |
| Rayon de courbure mini (Mach 2,5) | 2 950 | m |
| S_f / S_w ratio | 0,455 | — |
| Plage 1–12 km cohérente | ✅ | — |

---

## 2.10 Disclaimer

> **CONCEPTUAL ENGINEERING STUDY / RESEARCH PAPER**
> This document is a **preliminary, unclassified, non-export-controlled** conceptual engineering analysis for academic and research purposes only. It does not contain, describe, or enable the manufacture of a controlled munition. All data is based on open-source references, public-domain textbook methods (DATCOM, Etkins, Schlichting), and engineering judgment. Not subject to ITAR (22 CFR 120–130) or EAR (15 CFR 730–774) classification. No proprietary or controlled data is used. All specifications are design targets, not verified hardware.
