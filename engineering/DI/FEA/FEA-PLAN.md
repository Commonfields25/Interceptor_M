---
action: Create
agent: E1
related_gate: G2
status: Draft
timestamp: 2026-06-27 15:21:00+00:00
---

# 🔧 FEA Plan — Launch Stress Analysis
**Version:** 0.1-draft | **Owner:** E1 (Systems / NDC / FEA)
**Projet:** Interceptor_M — Defense Line (DD)
**Dependencies:** D3 CAD → airframe mesh; E2 propulsion → thrust loads

---

## 1. Objectif

Vérifier la résistance mécanique du micro-intercepteur sous charges de lancement :
- Accélération 50 g (pression lancement 8 bar, tube 40 mm, sabot)
- Contraintes Von Mises maximales acceptables : σ < σ_max (matériau TBD)

## 2. Configurations à Vérifier

| Config | Description | Loads | Critère |
|---|---|---|---|
| F1 | Fuselage — lancement axial | 50 g, pression 8 bar | σVonMises < σyield |
| F2 | Montage moteur M3 | Couple moteur max | Déplacement < 0.1 mm |
| F3 | Fixations ailes M2 | Charge 25 g en vol | Pas de défaillance |

## 3. Matériaux à Evaluer

| Matériau | σ_yield (MPa) | Usage |
|---|---|---|
| Carbone EPS / CFRP | TBD | Fuselage principal |
| Aluminium 7075-T6 | 503 MPa | Connecteurs |
| PLA / ABS (prototype) | ~50 MPa | Impression 3D |

## 4. Jalons

| Jalon | Date cible |
|---|---|
| Maillage airframe reçu (D3) | 2026-07-03 |
| FEA run F1–F3 | 2026-07-06 |
| Résultats → NDC final | 2026-07-09 |

## 5. Outil

- Ansys Mechanical (si disponible) / FreeCAD + Calculix (backup)

---
*Skeleton — À exécuter dès réception CAD D3*
