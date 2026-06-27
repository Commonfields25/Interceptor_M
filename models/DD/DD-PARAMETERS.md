---
agent: D3
action: Create
timestamp: 2026-06-27T15:21:00Z
related_gate: G2
status: Draft
---

# 📋 DD — CAD Parameters & Specifications (Skeleton)
**Version:** 0.1-draft | **Owner:** D3 (Defense / CAD)
**Projet:** Interceptor_M — Defense Line (DD)
**Status:** STANDBY-RELEASE — en attente de go-ahead DG (C4)

---

## 1. Géométrie de Référence

| Paramètre | Valeur | Source |
|---|---|---|
| Diamètre fuselage | 35 mm | PARAMETERS.json |
| Longueur totale | ≤ 900 mm | D1 spec |
| Tube lanceur (Øint) | 40 mm | PARAMETERS.json |
| Épaisseur paroi | TBD (FEA → E1) | À calculer |
| Ailes (4× delta) | envergure 110 mm, corde 60 mm | D2 aerodynamics |
| Empennage cruciforme (4×) | envergure 75 mm, corde 40 mm | D2 aerodynamics |
| Ogive | Tangente, L/D = 3.5 | D2 |

## 2. Contraintes de Design

- [ ] Poids cible : MTOW = 250 g (dont Ø35 mm × L ≤ 900 mm)
- [ ] Interface sabot/lanceur (Ø 40 mm)
- [ ] Montage moteur : brushless, support 9/12 mm
- [ ] Visserie : M2 (ailes), M3 (moteur)
- [ ] Compartiment electronics (E2) : TBD volume

## 3. Assemblage Prévu

```
ROOT_ASSEMBLY
├── AIRFRAME (fuselage + ogive)
├── ELECTRONICS_TRAY (E2)
├── PROPULSION_UNIT (E1)
└── LAUNCHER_INTERFACE (sabot + rings)
```

## 4. Outil CAO

- Inventor (principal) / SolidWorks (secondary)

## 5. Livrables Attendus (G2)

- [ ] ROOT_ASSEMBLY_v0.1.iam
- [ ] AIRFRAME_PART.F3D (ou .SLDPRT)
- [ ] BOM (Bill of Materials)
- [ ] DD-PARAMETERS-v0.1.md (ce document, mis à jour)

---
*Skeleton — À développer dès libération standby (C4)*
