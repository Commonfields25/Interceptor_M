# 📖 Guide d'Intégration Linear + Supabase pour Interceptor_M

Ce guide explique comment configurer **Linear** et **Supabase** pour automatiser la gestion des tâches, des rapports et des alertes pour le projet **Interceptor_M**.

---

## 📌 Prérequis

Avant de commencer, assurez-vous d'avoir :

1. **Un compte Linear** : [https://linear.app](https://linear.app)
   - Créer un **workspace** pour le projet.
   - Récupérer votre **clé API** (dans **Settings > API**).
   - Noter l'**ID de votre équipe** (dans l'URL de votre équipe : `https://linear.app/TEAM_ID`).

2. **Un projet Supabase** : [https://app.supabase.com](https://app.supabase.com)
   - Créer un nouveau projet.
   - Récupérer l'**URL du projet** et la **clé de service** (dans **Settings > API**).

3. **Un dépôt GitHub** : [https://github.com/Commonfields25/Interceptor_M](https://github.com/Commonfields25/Interceptor_M)
   - Assurez-vous d'avoir un **token GitHub** avec les permissions `repo` (pour accéder aux issues).

4. **Python 3.8+** et les dépendances :
   ```bash
   pip install requests python-dotenv supabase
   ```

5. **(Optionnel) Un webhook Slack** :
   - Pour recevoir les alertes dans Slack, créez un **Incoming Webhook** dans votre espace Slack.

---

## 🛠️ Configuration

### 1️⃣ Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet avec les informations suivantes :

```env
# GitHub
GITHUB_TOKEN=ghp_votre_token_github
REPO_OWNER=Commonfields25
REPO_NAME=Interceptor_M

# Linear
LINEAR_API_KEY=votre_clé_api_linear
LINEAR_TEAM_ID=votre_id_d_équipe_linear

# Supabase
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_SERVICE_KEY=votre_clé_de_service_supabase

# Slack (optionnel)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/votre/webhook
```

> ⚠️ **Ne partagez jamais ce fichier `.env` publiquement !** Ajoutez-le à votre `.gitignore`.

---

### 2️⃣ Configurer Supabase

#### a. Créer le schéma de la base de données

1. Allez dans votre projet Supabase : [https://app.supabase.com](https://app.supabase.com).
2. Ouvrez l'onglet **SQL Editor**.
3. Copiez-collez le contenu du fichier **`supabase_schema.sql`** et exécutez-le.
   - Cela créera les tables : `agents`, `milestones`, `agent_reports`, `simulation_results`, `blockages`, `alerts`, `execution_logs`.

#### b. Peupler la base de données avec les données initiales

1. Dans l'onglet **Table Editor**, sélectionnez la table `agents`.
2. Cliquez sur **Import** et chargez le fichier **`supabase_seed_data.json`** pour importer les agents et milestones.

> ✅ **Vérification** : Exécutez une requête SQL pour vérifier que les données sont bien importées :
> ```sql
> SELECT * FROM agents;
> SELECT * FROM milestones;
> ```

---

### 3️⃣ Configurer Linear

#### a. Créer les projets pour chaque agent

1. Allez dans votre espace Linear : [https://linear.app](https://linear.app).
2. Pour chaque agent (E1, E2, E3, D1, D2, D3, AM, AC), créez un projet :
   - Cliquez sur **+ New Project**.
   - Donnez-lui un nom (ex: `E3 - Simulation Avancée`).
   - Assignez-le à votre équipe.
   - Ajoutez une description (ex: `Projet dédié aux tâches de simulation avancée pour l'agent E3`).

> 💡 **Astuce** : Vous pouvez utiliser le fichier **`linear_projects_setup.json`** comme référence pour les noms et descriptions des projets.

#### b. Synchroniser GitHub avec Linear

1. Exécutez le script **`linear_github_sync_script.py`** pour synchroniser les issues GitHub avec Linear :
   ```bash
   python linear_github_sync_script.py
   ```
   - Cela créera automatiquement des tâches dans Linear pour chaque issue GitHub.
   - Les issues avec un label `agent:E3` seront assignées au projet de l'agent E3.

> ✅ **Vérification** : Allez dans Linear et vérifiez que les tâches sont bien créées.

---

### 4️⃣ Automatiser les rapports des agents

Les agents doivent envoyer leurs rapports quotidiens au format :
```
[AGENT]|[DATE]|[ACTIONS]|[BLOCAGES]|[BESOINS]
```

#### a. Envoyer un rapport manuellement

Exécutez le script **`agent_report_to_supabase.py`** pour envoyer un rapport :
```bash
python agent_report_to_supabase.py \
    --agent E3 \
    --actions "Simulation CFD terminée, optimisation des paramètres RL" \
    --blockages "Aucun" \
    --needs "Validation des résultats par AM"
```

> ✅ **Vérification** : Dans Supabase, exécutez :
> ```sql
> SELECT * FROM agent_reports WHERE agent_id = 'E3';
> ```

#### b. Automatiser les rapports

1. Modifiez le code de chaque agent pour qu'il appelle **`agent_report_to_supabase.py`** à la fin de chaque journée.
2. Exemple pour l'agent E3 :
   ```python
   import subprocess

   def send_daily_report():
       actions = "Synthèse des actions effectuées"
       blockages = "Blocages en cours"
       needs = "Besoins pour avancer"

       subprocess.run([
           "python", "agent_report_to_supabase.py",
           "--agent", "E3",
           "--actions", actions,
           "--blockages", blockages,
           "--needs", needs
       ])
   ```

---

### 5️⃣ Configurer les alertes

Le script **`supabase_alerts.py`** surveille :
- Les **blocages ouverts depuis plus de 2 heures**.
- Les **agents qui n'ont pas envoyé de rapport dans les 24 dernières heures**.

#### a. Démarrer le script de surveillance

Exécutez le script en arrière-plan :
```bash
nohup python supabase_alerts.py > alerts.log 2>&1 &
```

> ✅ **Vérification** :
> - Dans Supabase, exécutez :
>   ```sql
>   SELECT * FROM alerts;
>   ```
> - Si vous avez configuré Slack, vérifiez que les alertes apparaissent dans votre canal.

#### b. (Optionnel) Configurer un cron job

Pour exécuter le script toutes les heures, ajoutez une entrée dans votre crontab :
```bash
0 * * * * /chemin/vers/venv/bin/python /chemin/vers/supabase_alerts.py >> /chemin/vers/alerts.log 2>&1
```

---

### 6️⃣ Configurer GitHub Actions

Le workflow **`.github/workflows/linear-supabase-sync.yml`** automatise :
- La synchronisation **GitHub → Linear** toutes les 4 heures.
- L'envoi des rapports des agents à Supabase.

#### a. Configurer les secrets GitHub

1. Allez dans **Settings > Secrets > Actions** de votre dépôt GitHub.
2. Ajoutez les secrets suivants :
   - `LINEAR_API_KEY` : Votre clé API Linear.
   - `LINEAR_TEAM_ID` : L'ID de votre équipe Linear.
   - `GITHUB_TOKEN` : Un token GitHub avec les permissions `repo`.
   - `SUPABASE_URL` : L'URL de votre projet Supabase.
   - `SUPABASE_SERVICE_KEY` : La clé de service de votre projet Supabase.

#### b. Activer le workflow

1. Le workflow est déjà dans le dépôt (`.github/workflows/linear-supabase-sync.yml`).
2. Il s'exécutera automatiquement toutes les 4 heures.

> ✅ **Vérification** : Allez dans l'onglet **Actions** de votre dépôt GitHub pour voir les exécutions du workflow.

---

## 🧪 Tests

### 1️⃣ Tester la synchronisation GitHub → Linear

1. Créez une nouvelle issue dans GitHub avec un label `agent:E3`.
2. Exécutez le script :
   ```bash
   python linear_github_sync_script.py
   ```
3. Vérifiez dans Linear que la tâche a bien été créée.

### 2️⃣ Tester l'envoi d'un rapport

Exécutez :
```bash
python agent_report_to_supabase.py \
    --agent E3 \
    --actions "Test de rapport quotidien" \
    --blockages "Aucun" \
    --needs "Aucun"
```

Vérifiez dans Supabase :
```sql
SELECT * FROM agent_reports WHERE agent_id = 'E3';
```

### 3️⃣ Tester les alertes

1. Créez un blocage manuellement dans Supabase :
   ```sql
   INSERT INTO blockages (agent_id, issue_title, start_time, status)
   VALUES ('E3', 'Test de blocage', NOW() - INTERVAL '3 hours', 'OPEN');
   ```
2. Exécutez le script d'alertes :
   ```bash
   python supabase_alerts.py
   ```
3. Vérifiez dans Supabase :
   ```sql
   SELECT * FROM alerts;
   ```

---

## 📊 Tableau de bord (Optionnel)

Pour visualiser les données, vous pouvez utiliser :

1. **Supabase Dashboard** :
   - Allez dans **Table Editor** pour voir les données brutes.
   - Utilisez **SQL Editor** pour exécuter des requêtes personnalisées.

2. **Metabase** :
   - Connectez Metabase à votre projet Supabase.
   - Créez des tableaux de bord pour :
     - Suivre l'avancement des milestones.
     - Visualiser les blocages et alertes.
     - Analyser les rapports des agents.

3. **Linear** :
   - Utilisez les **vues Kanban** pour suivre les tâches par agent.
   - Créez des **roadmaps** pour visualiser les milestones.

---

## 🚨 Résolution des problèmes

### Problème : Les issues GitHub ne sont pas synchronisées avec Linear
- **Cause** : Token GitHub ou clé API Linear invalide.
- **Solution** : Vérifiez vos variables d'environnement dans `.env`.

### Problème : Les rapports ne sont pas envoyés à Supabase
- **Cause** : URL ou clé de service Supabase incorrecte.
- **Solution** : Vérifiez `SUPABASE_URL` et `SUPABASE_SERVICE_KEY` dans `.env`.

### Problème : Les alertes ne sont pas envoyées à Slack
- **Cause** : Webhook Slack non configuré ou invalide.
- **Solution** : Vérifiez `SLACK_WEBHOOK_URL` dans `.env`.

### Problème : Erreur de dépendance Python
- **Cause** : Les dépendances ne sont pas installées.
- **Solution** : Exécutez :
  ```bash
  pip install -r requirements.txt
  ```

---

## 📚 Références

- [Documentation Linear API](https://developers.linear.app/docs)
- [Documentation Supabase](https://supabase.com/docs)
- [Documentation GitHub API](https://docs.github.com/en/rest)
- [Dépôt Interceptor_M](https://github.com/Commonfields25/Interceptor_M)

---

## 🎯 Prochaines étapes

1. **Tester l'intégration** avec quelques agents (ex: E3).
2. **Automatiser les rapports** pour tous les agents.
3. **Configurer Metabase** pour visualiser les données.
4. **Améliorer les scripts** en fonction des retours des agents.
