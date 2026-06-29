# 🚀 Guide d'Intégration Linear + Supabase pour Interceptor_M

## 📋 Table des Matières
1. [Vue d'Ensemble](#vue-densemble)
2. [Prérequis](#prérequis)
3. [Installation de Supabase](#installation-de-supabase)
4. [Installation de Linear](#installation-de-linear)
5. [Configuration des Variables d'Environnement](#configuration-des-variables-denvironnement)
6. [Scripts d'Automatisation](#scripts-dautomatisation)
7. [Workflows GitHub Actions](#workflows-github-actions)
8. [Dashboard et Monitoring](#dashboard-et-monitoring)

---

## 🔭 Vue d'Ensemble

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Interceptor_M Project                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │  GitHub      │◄────────│   Linear    │  ← Project Management │
│  │  Repository  │────────►│   API       │                      │
│  └──────────────┘         └──────────────┘                      │
│         │                         │                             │
│         │                         │                             │
│         ▼                         ▼                             │
│  ┌──────────────────────────────────────────────┐              │
│  │            Supabase Database                  │              │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐     │              │
│  │  │  Agents  │ │  Reports │ │  Tasks   │     │              │
│  │  └──────────┘ └──────────┘ └──────────┘     │              │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐     │              │
│  │  │   Sim    │ │  Logs    │ │  Alerts  │     │              │
│  │  └──────────┘ └──────────┘ └──────────┘     │              │
│  └──────────────────────────────────────────────┘              │
│                        │                                        │
│                        ▼                                        │
│  ┌──────────────────────────────────────────────┐              │
│  │         Alert Monitoring (blocages, etc.)     │              │
│  │         Slack / Console / Email              │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Flux de Données

1. **Agents → Supabase**: Les agents soumettent leurs rapports quotidiens
2. **GitHub → Linear**: Les issues sont synchronisées vers Linear
3. **Linear → Supabase**: Les tâches sont stockées pour analytics
4. **Supabase → Alerts**: Les blocages > 2h déclenchent des alertes

---

## ✅ Prérequis

### Outils Requis

```bash
# Python 3.9+
python --version

# pip
pip install -r requirements.txt

# Git
git --version
```

### Packages Python

```bash
# Créez un fichier requirements.txt
cat > requirements.txt << 'EOF'
requests>=2.28.0
python-dotenv>=1.0.0
rich>=13.0.0
psycopg2-binary>=2.9.0
schedule>=1.2.0
EOF

pip install -r requirements.txt
```

---

## 🗄️ Installation de Supabase

### Option 1: Supabase Cloud (Recommandé)

1. **Créer un compte**
   ```
   https://app.supabase.com
   ```

2. **Créer un nouveau projet**
   ```
   Name: interceptor-m-production
   Region: Choisir la plus proche
   Database Password: [générer un mot de passe fort]
   ```

3. **Récupérer les identifiants**
   - Allez dans Settings > API
   - Notez `Project URL` et `anon/public key`

4. **Exécuter le Schema**
   ```bash
   # Installez psql si nécessaire
   brew install postgresql  # macOS
   # ou
   apt install postgresql-client  # Ubuntu
   
   # Connectez-vous
   psql "postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
   
   # Exécutez le schema
   \i supabase_schema.sql
   ```

### Option 2: Supabase Local (Docker)

```bash
# Installez Supabase CLI
npm install -g supabase

# Initialisez le projet
supabase init

# Démarrez Supabase
supabase start

# Le schema sera dans supabase/migrations/
```

### Initialisation des Données

```bash
# seed_data.json contient les données initiales
# Importez-les via l'interface Supabase ou via script

# Exemple d'import via curl
curl -X POST "https://[PROJECT-REF].supabase.co/rest/v1/agents" \
  -H "apikey: [ANON-KEY]" \
  -H "Authorization: Bearer [ANON-KEY]" \
  -H "Content-Type: application/json" \
  -d @supabase_seed_data.json
```

---

## 📊 Installation de Linear

### 1. Créer un Workspace

1. Allez sur https://linear.app
2. Créez un workspace "Interceptor_M"
3. Notez le Workspace ID

### 2. Obtenir la Clé API

1. Allez dans Settings > API
2. Créez une nouvelle clé API
3. Sélectionnez les scopes:
   - `read:issues`
   - `write:issues`
   - `read:labels`
   - `write:labels`
   - `read:projects`
   - `read:users`

### 3. Configurer les Projets

Importez `linear_projects_setup.json` via l'API Linear:

```bash
# Exemple avec curl (à adapter)
curl -X POST "https://api.linear.app/graphql" \
  -H "Authorization: Bearer [LINEAR-API-KEY]" \
  -H "Content-Type: application/json" \
  -d '{"query": "...", "variables": {...}}'
```

Ou configurez manuellement:
- Créez un projet par type d'agent (E1-E3, D1-D3, AM, AC, G1-G2)
- Ajoutez les labels appropriés
- Créez les milestones M1-M8

### 4. Configurer l'Équipe

```bash
# Team ID (trouvable dans les paramètres de l'équipe)
LINEAR_TEAM_ID=INTERCEPTOR-TEAM
```

---

## 🔐 Configuration des Variables d'Environnement

Créez un fichier `.env` à la racine du projet:

```bash
# ===== SUPABASE =====
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# ===== LINEAR =====
LINEAR_API_KEY=lin_api_xxxxx
LINEAR_TEAM_ID=INTERCEPTOR-TEAM
LINEAR_WORKSPACE_ID=INTERCEPTOR-M-WORKSPACE

# ===== GITHUB =====
GITHUB_TOKEN=ghp_xxxxx
GITHUB_OWNER=Commonfields25
GITHUB_REPO=Interceptor_M

# ===== SLACK (Optionnel) =====
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxxxx
SLACK_CHANNEL=#interceptor-alerts

# ===== ALERTES =====
BLOCAGE_THRESHOLD_HOURS=2
INACTIVE_THRESHOLD_HOURS=24

# ===== LOGGING =====
LOG_LEVEL=INFO
```

### Sécurité

⚠️ **IMPORTANT**: Ne jamais commiter le fichier `.env`!

```bash
# Ajouter à .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

---

## 🤖 Scripts d'Automatisation

### 1. Soumission de Rapports Agents

```bash
# Mode interactif
python agent_report_to_supabase.py --interactive

# Mode CLI
python agent_report_to_supabase.py \
  --agent E1 \
  --date 2026-06-30 \
  --actions "Exploration de 200 configurations. Résultats prometteurs sur 3 régions." \
  --blocages "Mémoire GPU insuffisante" \
  --besoins "Upgrade GPU ASAP"

# Depuis un fichier formaté
python agent_report_to_supabase.py \
  --input-file rapport_e1.txt

# Afficher l'historique
python agent_report_to_supabase.py --history E1
```

**Format du fichier**:
```
[E1]|2026-06-30|Exploration de 200 configurations|RAM saturée|Upgrade GPU
```

### 2. Synchronisation GitHub → Linear

```bash
# Synchroniser toutes les issues (mode réel)
python linear_github_sync_script.py

# Mode simulation (dry-run)
python linear_github_sync_script.py --dry-run

# Synchroniser aussi les labels
python linear_github_sync_script.py --sync-labels

# Mode verbose
python linear_github_sync_script.py -v
```

### 3. Monitoring des Alertes

```bash
# Exécution unique
python supabase_alerts.py --once

# Monitoring continu (toutes les 5 minutes)
python supabase_alerts.py --interval 300

# Seuils personnalisés
python supabase_alerts.py --blocage-hours 4 --inactive-hours 48
```

---

## ⚙️ Workflows GitHub Actions

### Workflow: Sync GitHub Issues → Linear

```yaml
# .github/workflows/sync-linear.yml
name: Sync GitHub to Linear

on:
  schedule:
    - cron: '0 */4 * * *'  # Toutes les 4 heures
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      - name: Sync issues
        env:
          LINEAR_API_KEY: ${{ secrets.LINEAR_API_KEY }}
          LINEAR_TEAM_ID: ${{ secrets.LINEAR_TEAM_ID }}
          GITHUB_TOKEN: ${{ secrets.GH_TOKEN }}
          GITHUB_OWNER: ${{ github.repository_owner }}
          GITHUB_REPO: ${{ github.event.repository.name }}
        run: python linear_github_sync_script.py
```

### Workflow: Daily Agent Reports Check

```yaml
# .github/workflows/daily-report-check.yml
name: Daily Report Check

on:
  schedule:
    - cron: '0 8 * * *'  # Chaque jour à 8h
  workflow_dispatch:

jobs:
  check-reports:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      - name: Check alerts
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: python supabase_alerts.py --once
```

### Secrets à Configurer

Dans GitHub > Settings > Secrets:

```
LINEAR_API_KEY=lin_api_xxxxx
LINEAR_TEAM_ID=INTERCEPTOR-TEAM
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxxxx
```

---

## 📈 Dashboard et Monitoring

### Vues SQL Pré-définies

Le schema crée automatiquement ces vues:

1. **`v_agent_daily_status`**: État quotidien des agents
2. **`v_active_tasks`**: Tâches actives par agent
3. **`v_active_blocages`**: Blocages actifs (> 2h)
4. **`v_milestone_progress`**: Progression des milestones

### Requêtes Utiles

```sql
-- Tous les blocages actifs
SELECT * FROM v_active_blocages;

-- Progression des milestones
SELECT * FROM v_milestone_progress;

-- Statistiques globales
SELECT get_project_stats();

-- Rapports du jour
SELECT * FROM agent_reports WHERE report_date = CURRENT_DATE;

-- Agents sans rapport aujourd'hui
SELECT * FROM agents 
WHERE is_active = true 
AND agent_id NOT IN (
  SELECT agent_id FROM agent_reports 
  WHERE report_date = CURRENT_DATE
);
```

### Intégration Metabase (Optionnel)

```bash
# Démarrez Metabase
docker run -d -p 3000:3000 \
  -e MB_DB_TYPE=postgres \
  -e MB_DB_DBNAME=postgres \
  -e MB_DB_PORT=5432 \
  -e MB_DB_USER=postgres \
  -e MB_DB_PASS=[PASSWORD] \
  -e MB_DB_HOST=[HOST] \
  --name metabase metabase/metabase
```

---

## 🎯 Checklist d'Installation

- [ ] Créer un projet Supabase
- [ ] Exécuter `supabase_schema.sql`
- [ ] Importer `supabase_seed_data.json`
- [ ] Créer un workspace Linear
- [ ] Générer une clé API Linear
- [ ] Configurer les secrets GitHub
- [ ] Tester `agent_report_to_supabase.py`
- [ ] Tester `linear_github_sync_script.py --dry-run`
- [ ] Tester `supabase_alerts.py --once`
- [ ] Configurer les workflows GitHub Actions
- [ ] (Optionnel) Configurer Slack webhook
- [ ] (Optionnel) Installer Metabase

---

## 📞 Support

Pour toute question ou problème:
1. Vérifiez les logs dans `linear_sync.log` et `supabase_alerts.log`
2. Vérifiez la console pour les erreurs détaillées
3. Utilisez `--verbose` pour plus de détails

---

*Document généré pour le projet Interceptor_M - Commonfields25*
*Dernière mise à jour: 2026-06-30*
