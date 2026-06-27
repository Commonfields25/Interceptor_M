---
agent: E2
action: Create
timestamp: 2026-06-27T15:21:00Z
related_gate: G2
status: Draft
---

# 🌀 CFD Plan — Propulsion / Aerodynamics
**Version:** 0.1-draft | **Owner:** E2 (Propulsion / CFD)
**Projet:** Interceptor_M — Defense Line (DD)
**Dependencies:** D3 CAD → geometry inputs; E1 NDC → boundary conditions

---

## 1. Objectif

Validation aérodynamique du micro-intercepteur en configuration :
- Déployé (vol libre)
- Lancement (tube 40 mm, pression TBD)

## 2. Configurations à Simuler

| Config | Description | Outil cible | Priorité |
|---|---|---|---|
| C1 | Aile delta 4× déployée — M 0,3–2,2 | OpenFOAM /手段 | HAUTE |
| C2 | Configuration launcher — sabotinside tube | OpenFOAM | Moyenne |
| C3 | Empennage cruciforme — stabilité | OpenFOAM | Moyenne |

## 3. Paramètres d'Entrée (depuis NDC E1)

| Paramètre | Valeur | Source |
|---|---|---|
| Géométrie | CAD D3 → STL | D3 workspace |
| Conditions limites | Pression/velocity inlet | E1 NDC |
| MTOW | 250 g → massevolumique | PARAMETERS.json |
| Profil ailes | NACA 0004 | D1 |

## 4. Jalons

| Jalon | Date cible | Critère de Succès |
|---|---|---|
| Géométrie STL reçue | 2026-07-03 | D3 → AM → E2 |
| CFD C1 résultats | 2026-07-07 | Cl/Cd à M 2,2 convergence |
| Rapport CFD complet | 2026-07-09 | Prêt pour G2 |

## 5. Ressentissements

- Blocage : En attente de D3 CAD geometry (standby-release actif — C4 OPEN)
- Outil CFD : validation choix OpenFOAM vs Ansys en cours (E1)

---
*Skeleton — Mise à jour dès réception geometry D3*
