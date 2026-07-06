---
agent: Jules
action: Fix
timestamp: 2026-07-02T13:27:36Z
status: Validated
---

# 🛠️ Script de Génération de Pièces FreeCAD

Ce script permet de **générer automatiquement des pièces 3D dans FreeCAD** à partir d'un fichier JSON contenant leurs paramètres géométriques. Il exporte ensuite la pièce en **STEP** et **FCStd** (format natif FreeCAD).

---

## 📌 Prérequis

1. **FreeCAD** : Version 0.19 ou ultérieure.
   - Téléchargement : [https://www.freecad.org/](https://www.freecad.org/)
   - Assure-toi que FreeCAD est installé et fonctionnel.

2. **Python 3.x** : Inclus avec FreeCAD (pas d'installation supplémentaire nécessaire).

3. **Dépôt Git** : Ce script est conçu pour être utilisé dans le dépôt **Interceptor_M**.

---

## 📁 Structure du Projet

```
Interceptor_M/
├── parts/
│   ├── BRK001/
│   │   ├── params_BRK001.json  # Fichier de paramètres
│   │   ├── BRK001.step          # Pièce exportée (générée)
│   │   └── BRK001.FCStd         # Pièce FreeCAD (générée)
│   └── ...
└── scripts/
    ├── generate_part.py         # Script de génération
    └── README_GENERATE_PART.md  # Ce guide
```

---

## 📄 Format du Fichier JSON

Le script attend un fichier JSON avec la structure suivante :

```json
{
  "name": "BRK001",
  "description": "Description de la pièce",
  "dimensions": {
    "length": 100.0,        # Longueur (mm)
    "width": 50.0,          # Largeur (mm)
    "height": 20.0,         # Hauteur (mm)
    "hole_diameter": 10.0,  # Diamètre du trou (mm) - optionnel
    "hole_position": [25.0, 25.0]  # Position du trou [x, y] (mm) - optionnel
  },
  "material": "Aluminium",
  "units": "mm"
}
```

### Champs obligatoires :
- `name` : Nom de la pièce (utilisé pour les fichiers de sortie).
- `dimensions.length` : Longueur de la pièce.
- `dimensions.width` : Largeur de la pièce.
- `dimensions.height` : Hauteur de la pièce.

### Champs optionnels :
- `hole_diameter` et `hole_position` : Si présents, un trou sera ajouté à la pièce.

---

## 🚀 Utilisation du Script

### Étape 1 : Préparer le fichier JSON
Crée un fichier JSON pour ta pièce dans le dossier `parts/<nom_de_la_pièce>/`.
Exemple pour **BRK001** :
```bash
mkdir -p parts/BRK001
touch parts/BRK001/params_BRK001.json
```

Remplis le fichier avec les paramètres de ta pièce (voir [Format du Fichier JSON](#-format-du-fichier-json)).

### Étape 2 : Ouvrir FreeCAD et la Console Python
1. Lance **FreeCAD**.
2. Va dans **Macro → Python Console** (ou appuie sur `Ctrl+Shift+P`).

### Étape 3 : Exécuter le Script
Dans la console Python, exécute :
```python
# Charge le script
exec(open("scripts/generate_part.py").read())

# Génère la pièce
generate_part_from_json("parts/BRK001/params_BRK001.json")
```

### Étape 4 : Vérifier les Fichiers Générés
- Un fichier **STEP** (`BRK001.step`) et un fichier **FCStd** (`BRK001.FCStd`) seront créés dans le dossier `parts/BRK001/`.
- Tu peux les ouvrir dans FreeCAD pour vérifier la pièce.

---

## 📂 Exemple Complet : Pièce BRK001

### 1. Fichier JSON (`parts/BRK001/params_BRK001.json`)
```json
{
  "name": "BRK001",
  "description": "Pièce de base avec un trou central",
  "dimensions": {
    "length": 100.0,
    "width": 50.0,
    "height": 20.0,
    "hole_diameter": 10.0,
    "hole_position": [50.0, 25.0]
  },
  "material": "Aluminium",
  "units": "mm"
}
```

### 2. Exécution dans FreeCAD
```python
# Dans la console Python de FreeCAD
exec(open("scripts/generate_part.py").read())
generate_part_from_json("parts/BRK001/params_BRK001.json")
```

### 3. Résultat
- **Fichiers générés** :
  - `parts/BRK001/BRK001.step`
  - `parts/BRK001/BRK001.FCStd`

---

## ⚠️ Dépannage

### Erreur : `ModuleNotFoundError: No module named 'FreeCAD'`
**Cause** : Le script est exécuté en dehors de FreeCAD.
**Solution** : Exécute le script **uniquement dans la console Python de FreeCAD**.

---

### Erreur : `FileNotFoundError: [Errno 2] No such file or directory: 'parts/BRK001/params_BRK001.json'`
**Cause** : Le chemin vers le fichier JSON est incorrect.
**Solution** :
1. Vérifie que le fichier existe.
2. Utilise un **chemin relatif** depuis le dossier racine du dépôt.
   Exemple : Si ton dépôt est dans `C:/Interceptor_M`, utilise :
   ```python
   generate_part_from_json("parts/BRK001/params_BRK001.json")
   ```

---

### Erreur : `AttributeError: 'module' object has no attribute 'export'`
**Cause** : Problème avec l'import du module `Part`.
**Solution** : Assure-toi que FreeCAD est bien lancé et que la console Python est ouverte **dans FreeCAD**.

---

### La pièce n'a pas de trou
**Cause** : Les champs `hole_diameter` ou `hole_position` sont manquants dans le JSON.
**Solution** : Ajoute ces champs dans ton fichier JSON (voir [Format du Fichier JSON](#-format-du-fichier-json)).

---

### La pièce est générée mais les dimensions sont incorrectes
**Cause** : Erreur dans les valeurs du JSON.
**Solution** : Vérifie que toutes les valeurs sont en **millimètres (mm)** et qu'elles sont numériques (ex: `100.0` et non `"100"`).

---

## 💡 Conseils

1. **Teste avec une pièce simple** avant de complexifier.
2. **Utilise des noms uniques** pour chaque pièce (évite les espaces et caractères spéciaux).
3. **Versionne tes fichiers JSON** : Ils contiennent les paramètres de tes pièces et doivent être commités dans Git.
4. **Ignore les fichiers générés** : Ajoute `*.step` et `*.FCStd` à ton `.gitignore` si tu ne veux pas les versionner (mais cela est déconseillé pour la collaboration).

---

## 📜 Licence
Ce script est fourni **sans garantie** et peut être modifié selon tes besoins.
