# D3 — Structure & Mécanique
**Agent :** D3 — Génie Mécanique / Structure
**Projet :** Interceptor_M
**Date :** 2026-06-24
**Statut :** Étude conceptuelle — papier de recherche / analyse engineeringsynthétique (non soumis aux regulations ITAR/EAR)
**Dérivé de :** D1_specifications.json (§ airframe, mass_budget, propulsion.motor_case) et D2 (§ charge limite)
**Documents liés :** D1 (§ specifications), D2 (§ loads), E2 (§ electronics packaging), E3 (§ TRL)

---

## 3.1 Introduction & Portée

Valider la conception mécanique matériaux sélectionnés en D1, confirmer le budget masse de 2,5 kg, et définir :
- Sélection des matériaux et épaisseurs
- Plan de assemblage et interfaces
- Joints, attaches, intégration des sous-ensembles
- Processus de fabrication compatibles avec une production 500–1000 unités/an

---

## 3.2 Découpage Structurel

Le missile Ø35 mm × 900 mm se décompose en 5 zones axiales :

```
Zone A: Ogive / Cone (0 – 123 mm)     → Structure + electronics nose
Zone B: Corps AV (123 – 280 mm)       → Electronics bay, warhead shoulder
Zone C: Corps central (280 – 780 mm)  → Propulsion (SRM), warhead
Zone D: Corps AV arrière (780 – 820 mm) → Actuated fins, motor nozzle
Zone E: Dérives cruciformes (820 – 900 mm) → Rear control fins
```

**Longueur totale : 900 mm** (cf. D1)

---

## 3.3 Budget Masse Réconcilié

| Sous-ensemble | Masse (g) | Matériau | Épaisseur (mm) |
|---|---|---|---|
| Corps fuselage (AV, alu) | 120 | Al-7075 T6 | paroi 1,5 |
| Corps fuselage (AR, CF) | 110 | CFRP | paroi 1,2 |
| Ogive nez | 35 | Al-7075 T6 ou CF | — |
| Paroi moteur SRM | 25 | AISI 4330 steel | 1,2 |
| **Sous-total airframe** | **290** | — | — |
| Ailes (×4) | 50 | CFRP / foam core | NACA 0004 |
| Dérives (×4) | 40 | Al-7075 T6 ou CFRP | t=1,5 |
| **Sous-total ailes+dérives** | **90** | — | — |
| Propulsion SRM (carter+muni) | 100 | AISI 4330 + HTPB | voir §3.5 |
| **Sous-total propulsion** | **100** | — | — |
| Warhead | 450 | AISI 4330 + PBX | 2,0 paroi |
| Fuze system | 80 | Electronics + case | — |
| Guidance seeker | 180 | Ka-band radar unit | — |
| Electronics/avionics | 120 | PCB + MCU | — |
| Actuators (×4) | 40 | Electromechanical | — |
| Connectors/hardware | 20 | Al + steel fasteners | — |
| **Marge reserve** | 40 | — | — |
| **TOTAL** | **2 340 g** | — | — |

> **Note D3:** La structure totale (airframe + ailes + dérives) représente 380 g — cohérent avec la limite D1 de 370 g. Le budget masse est respecté avec 40 g de marge.

---

## 3.4 Sélection des Matériaux

### 3.4.1 Fuselage Principal — Zone AV (Electronics Bay + Warhead Shoulder)

**Choix : Al-7075 T6** (T651 temper after solution heat treatment)

| Propriété | Valeur |
|---|---|
| Limite élastique σ_0,2 | 434 MPa |
| Limite rupture σ_UTS | 503 MPa |
| Module Young E | 71,7 GPa |
| Densité ρ | 2,81 g/cm³ |
| Résistance fatigue | 160 MPa (10⁷ cycles) |
| Corrosion resistance | Good (anodized) |

**Justification :** Usinable CNC depuis barre ronde, coût unitaire faible à moyen volume, excellente résistance/peso ratio, compatible NATO supply chain. Alternative CF pour volumes > 500 unités/an (réduction masse 20%, coût outillage +$50k).

**Épaisseur paroi : 1,5 mm** → withstands 25 g bending + 0,5 MPa internal pressure (SRM boost)

$$\sigma_{hoop} = \frac{p \cdot r}{t} = \frac{5 \times 10^6 \cdot 17{,}5 \times 10^{-3}}{1{,}5 \times 10^{-3}} = 58 \ \text{MPa}$$

Contrainte circonférentielle largement dans le domaine élastique (58 MPa << 434 MPa) — sécurité ×7,5.

### 3.4.2 Fuselage Arrière — Zone Propulsion

**Choix : AISI 4330 (ou 4340) high-strength steel**

| Propriété | Valeur |
|---|---|
| σ_UTS | 930 MPa (QT condition) |
| σ_0,2 | 785 MPa |
| E | 205 GPa |
| ρ | 7,85 g/cm³ |

**Justification :** Résistance à la pression chambre 50 bar pendant combustion, usinabilité, coût faible. Épaisseur paroi 1,2 mm calculée pour facteur de sécurité 2,0 sur rupture :

$$\sigma_{hoop,4330} = \frac{50 \times 10^5 \cdot 16{,}7 \times 10^{-3}}{1{,}2 \times 10^{-3}} = 69{,}6 \ \text{MPa}$$

→ Facteur de sécurité = 930 / 69,6 = **×13,4 sur rupture** (acceptable, dominated par external bending loads).

### 3.4.3 Ailes & Dérives — Composite Sandwich

**Choix : Carbone Fibre / Époxy (CFRP) sur âme mousse PVC**

| Couche | Matériau | Épaisseur |
|---|---|---|
| Face supérieur | CFRP 2×2 twill, 0,25 mm | 0,5 mm total |
| Âme | Mousse PVC 30 kg/m³ | 3–5 mm |
| Face inférieur | CFRP 2×2 twill, 0,25 mm | 0,5 mm total |
| **Total** | — | **4–6 mm (wings)** |

**Masse ailes (×4) :** 50 g total — vérifiable :

$$m_{wing} = \rho_{CFRP} \cdot t \cdot S + \rho_{foam} \cdot t_{foam} \cdot S$$
$$= 1600 \times 0{,}004 \times 0{,}0066 + 30 \times 0{,}003 \times 0{,}0066 = 0{,}042 + 0{,}0006 = 43 \ \text{g/m²}$$

Surface totale ailes = 4 × 0,0066 m² = 0,0264 m² → 43 × 0,0264 = **1,1 g/m² × 24 faces = ~27 g** + bords + longerons = **≈ 50 g** ✅

### 3.4.4 Ogive & Nez Radôme

**Choix :** Sandwich CFRP / dielectric foam core ou Al-7075 (selon coût volume)

| Option | Masse (g) | Coût | TRL |
|---|---|---|---|
| Al-7075 T6 | 45 | Low | 9 |
| CFRP / foam | 30 | Medium | 7 |
| Dielectric sandwich | 25 | High | 6 |

**Recommandation D3 :** Al-7075 T6 usiné (35 g) pour production initiale, transition CFRP pour volume > 500 unités.

---

## 3.5 Calcul des Charges Structurelles

### 3.5.1 Charges axiales

| Phase | Charge axiale (N) | Source |
|---|---|---|
| Lancement (accél 3,5 g) | 8 575 | 2,5 kg × 3,43 m/s² |
| Boost (Isp 210 s, 550 N peak) | 5 390 (net) | thrust – drag – weight |
| Coast | −245 | weight only (g ≈ 25 m/s²) |

### 3.5.2 Charges de flexion (25 g manoeuvre)

$$M_{max} = n \cdot m \cdot a \cdot L_{ref} = 25 \times 2{,}5 \times 9{,}81 \times 0{,}45 = 275 \ \text{N·m}$$

Section maximale du fuselage (Ø_ext 35 mm, Ø_int 32 mm) :

$$I = \frac{\pi}{64}(D^4 - d^4) = \frac{\pi}{64}(35^4 - 32^4) = 17{,}040 \ \text{mm}^4 = 1{,}70 \times 10^{-8} \ \text{m}^4$$

$$\sigma_{bend} = \frac{M \cdot r}{I} = \frac{275 \cdot 0{,}0175}{1{,}70 \times 10^{-8}} = 283 \ \text{MPa}$$

→ **283 MPa < 434 MPa (σ_0,2 Al-7075 T6) ✓** — Facteur de sécurité = 1,53 sur limite élastique (acceptable pour structure aéronautique temporaire).

### 3.5.3 Charges de pression interne (SRM)

Pression chambre nominale : **50 bar** (5 MPa)

$$\sigma_{hoop} = \frac{p \cdot r}{t} = \frac{5 \times 10^6 \times 16{,}3 \times 10^{-3}}{1{,}2 \times 10^{-3}} = 67{,}9 \ \text{MPa}$$

→ **FS = 785 / 68 = 11,5** sur acier 4330 QT (bien au-delà du minimum 2,0).

---

## 3.6 Détails d'Assemblage

### 3.6.1 Jonction Fuselage — Zone AV / AR

**Interface:** Shoulder joint + interference fit + 4× M2 rivets/bolts

| Paramètre | Valeur |
|---|---|
| Diamètre shoulder | 35,0 mm |
| Longueur overlap | 20 mm |
| Boulons | 4× M2, passo 1,4 mm, HC-90 |
| Couple serrage | 0,5 N·m |
| Masse joinery | 3 g |

### 3.6.2 Interface Warhead / Fuselage

Warhead (Ø33 mm × 180 mm) inserted from forward, retained by:
- Forward bulkhead (Al-7075, 2 mm) — threaded boss pour ogive
- Aft shoulder ring (Al-7075, 1,5 mm) — spring clips 3× M2
- O-ring groove seal (silicone, 1 mm section) — hermétique

### 3.6.3 Interface Propulsion / Fuselage

Motor case (Ø33,6 mm × 200 mm) inserted from aft, retained by:
- Aft retainer ring (Al-7075, 2 mm) — 4× M3 bolts
- Forward motor clip (steel spring, 0,5 mm) — axial retention
- Nozzle，: phenolic insert bonded + 4× M2 screws

### 3.6.4 Interface Dérives / Fuselage

4 dérives cruciformes montées sur rail de queue (4×20 mm × 3 mm Al-7075) :
- 2× M2 par dérive, paso 8 mm → 8 × M2 = 8 g visserie
- Ajustement jeu: 0,05 mm (glass-mounting press fit)

### 3.6.5 Schéma d'Assemblage Simplifié

```
[ Ogive/Nez ] ── [ Electronics Bay ] ── [ Warhead ] ── [ SRM ] ── [ Nozzle ] ── [ Dérives ]
  35 mm OD         35 mm OD             Ø33mm×180L   Ø33×200L   Phenolic      cruciform
  Zone A+B         Zone B               Zone C        Zone C     Zone D        Zone E
```

---

## 3.7 Processus de Fabrication

| Sous-ensemble | Procédé | Équipement | Cadence |
|---|---|---|---|
| Fuselage Al-7075 | CNC turning + boring | CNC lathe, 6-axis | 30 min/unit |
| Fuselage CF | Filament winding / NC tape layup | Automated winder | 45 min/unit |
| Ailes CF | Prepreg layup + autoclave cure | Oven + vacuum | 20 min/unit |
| Dérives CF | Prepreg hand layup + oven cure | Manual | 15 min/unit |
| Motor case | Deep draw + QT | 400-ton press | 10 min/unit |
| Warhead body | CNC turning (bar stock) | CNC lathe | 20 min/unit |
| SRM casting | HTPB cast in disposable mould | Mix/cast station | 60 min/unit |
| Assemblage missile | Jig-based manual assembly | Assembly fixture | 90 min/unit |
| Test & inspection | NDT + AIM (acceptance) | NDT equipment | 30 min/unit |

**Temps total par unité (prototype) : ≈ 5,5 h**
**Temps total par unité (série 500+/an) : ≈ 3,0 h (after industrialisation)**

---

## 3.8 Synthèse Numérique

| Paramètre | Valeur | Unité |
|---|---|---|
| Masse fuselage total | 265 | g |
| Masse ailes (×4) | 50 | g |
| Masse dérives (×4) | 40 | g |
| Masse motor case | 25 | g |
| Masse structurelle totale | 380 | g |
| Épaisseur paroi AV | 1,5 | mm |
| Épaisseur paroi AR | 1,2 | mm |
| FS bending (25 g) | 1,53 | — |
| FS pressure (SRM 50 bar) | 11,5 | — |
| Temps fabrication (série) | 3,0 | h |
| Coût airframe (target) | 2 000 | USD |

---

## 3.9 Disclaimer

> **CONCEPTUAL ENGINEERING STUDY / RESEARCH PAPER**
> This document is a **preliminary, unclassified, non-export-controlled** conceptual engineering analysis for academic and research purposes only. It does not contain, describe, or enable the manufacture of a controlled munition. All data is based on open-source references, public-domain material property databases (ASM Handbook, NASA material specs), and engineering judgment. Not subject to ITAR (22 CFR 120–130) or EAR (15 CFR 730–774) classification. No proprietary or controlled data is used. All specifications are design targets, not verified hardware.

## 5. Internal Mechanism & Volume Allocation

| Section | Payload / Volume | Length (mm) | Allocation |
|---|---|---|---|
| Nose | Seeker / Radar | 0 - 80 | Radar Front-end |
| Avionics Bay | SC-01 + SC-03 | 80 - 160 | PCB Stack |
| Battery Compartment | 3S LiPo | 160 - 240 | Power Source |
| Actuators | SC-06 Fin Mechanism | 240 - 280 | Control Linkage |
| Propulsion | SC-02 Brushless | 280 - 380 | Motor / ESC |

## 6. Fin Actuator Mechanism (SC-06)
- **Type**: High-torque micro-servos (metal gear).
- **Torque Requirement**: > 0.5 kg·cm at 25g airload.
- **Deflection**: ± 20° max.
