# Simulation E3 — Chaîne de guidage et calcul de P(intercept)

## Vue d'ensemble

Cette chaîne simule un engagement interceptor / cible avec :

- **Guidage Proportional Navigation (PN)** — loi de commande bang-bang
  (`flight_control_poc.py`)
- **Modèle de vol 6-DOF simplifié (point-masse 3D)** — intègre la dynamique, la traînée, la portance et la gravité (`sim_6dof.py`)
- **Monte Carlo** — échantillonne l'enveloppe E1 et calcule la probabilité d'interception `P(intercept)` avec intervalle de confiance à 95 % (`montecarlo_pintercept.py`)
- **Constantes partagées** (`constants.py`) — tous les paramètres physiques, aérodynamiques et numériques

## Organisation

```
simulation/
├── constants.py             — constantes SI partagées (enveloppes, coeffs, PN)
├── sim_6dof.py             — modèle de vol 6-DOF / point-masse 3D
├── flight_control_poc.py    — loi de guidage PN + interface
├── montecarlo_pintercept.py — Monte Carlo P(intercept)
└── README.md               — ce fichier
```

## Comment lancer

### 1. Test d'un module individuel

```bash
cd simulation
python -c "from sim_6dof import simulate_engagement; print('sim_6dof OK')"
python -c "from flight_control_poc import loi_guidage; print('PN OK')"
```

### 2. Simulation de guidage seule (sans Monte Carlo)

```bash
cd simulation
python flight_control_poc.py
```

### 3. Monte Carlo P(intercept)

```bash
cd simulation
python montecarlo_pintercept.py
```

Cela exécute `NB_TIRAGES = 10000` tirages dans l'enveloppe E1
(portée 1–12 km, altitude 0–5000 m, cible jusqu'à Mach 2.5).

Pour un test rapide, modifier temporairement `NB_TIRAGES` dans `constants.py`.

### 4.Importer depuis un autre script

```python
from simulation import constants as C
from simulation.sim_6dof import simulate_engagement
from simulation.flight_control_poc import loi_guidage

resultat = simulate_engagement(
    pos_init_m    = [0.0, 0.0, 1000.0],
    vel_init_m_s  = 400.0,
    cap_init_rad  = 0.0,
    pos_cible_m   = [5000.0, 0.0, 1000.0],
    vel_cible_m_s = 300.0,
    cap_cible_rad = 3.14159,
    guidage_fn    = loi_guidage,
)
print(f"Intercept: {resultat['intercept']}")
```

## Constantes clés

| Constante | Valeur | Description |
|---|---|---|
| `PORTEE_MIN/MAX_KM` | 1–12 km | Enveloppe d'engagement (E1) |
| `ALTITUDE_MIN/MAX_M` | 0–5000 m | Altitude opérationnelle |
| `MASSE_INTERCEPTOR_KG` | 2.34 kg | Masse de l'interceptor |
| `ACCELERATION_LATERALE_MAX_G` | 25 g | Commande max admissible |
| `GAIN_PN` | 4 | Gain de navigation PN |
| `COEFF_TRAITEE_Cx` | 0.35 | Coefficient de traînée |
| `PAS_DE_TEMPS_S` | 0.01 s | Pas d'intégration Euler |
| `NB_TIRAGES` | 10 000 | Échantillons Monte Carlo |

## Hypothèses et limites

- **Atmosphère isotherme** (modèle exponentiel, niveau mer ISA) — pas de profil de vent
- **Cible en trajectoire rectiligne uniforme** — pas de manœuvre cible
- **Pas de poussée** — interceptor purement réactif (masse constante)
- **Accélération latérale saturée à 25 g** par le modèle de vol
- **Seuil d'interception : 5 m** — distance minimale pour valider l'interception

Pour améliorer : modèle d'atmosphère std, poussée moteur, manœuvres cibles, filtre de Kalman sur la LOS.
