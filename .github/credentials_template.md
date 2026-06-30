# 🔐 Credentials Template

> **Ce fichier est un TEMPLATE — il ne doit JAMAIS contenir de credentials réels.**
> Utilisez `credentials_example.md` (ou `.env.example`) pour les vrais identifiants dans un fichier séparé, ignoré par Git.

---

## 1. Structure des credentials

| Catégorie | Clé | Description | Exemple |
|-----------|-----|-------------|---------|
| `github` | `token` | Personal Access Token (PAT) GitHub | `ghp_xxxxxxxxxxxx` |
| `github` | `url` | URL du dépôt GitHub | `https://github.com/org/repo` |
| `api` | `key` | Clé API (service externe) | `sk-xxxxxxxxxxxx` |
| `api` | `url` | URL de base de l'API | `https://api.example.com/v1` |
| `db` | `host` | Hôte de la base de données | `localhost` |
| `db` | `port` | Port | `5432` |
| `db` | `user` | Nom d'utilisateur | `admin` |
| `db` | `password` | Mot de passe (NE JAMAIS en clair) | `${DB_PASSWORD}` |
| `deploy` | `ssh_key_path` | Chemin vers la clé SSH | `~/.ssh/id_rsa` |
| `deploy` | `server` | Adresse du serveur | `user@server.com` |

---

## 2. Comment ajouter un accès

### Via variables d'environnement (recommandé)

```bash
# .env (À METTRE DANS .gitignore)
export GITHUB_TOKEN="ghp_votre_token_ici"
export API_KEY="sk-votre-cle-api-ici"
export DB_PASSWORD="votre_mot_de_passe"
```

Chargez dans votre shell :
```bash
source .env
```

### Via GitHub Secrets (CI/CD)

Pour les workflows GitHub Actions, ajoutez les secrets via :

```
Repository → Settings → Secrets and variables → Actions → New repository secret
```

Référencez-les dans le workflow :
```yaml
jobs:
  deploy:
    steps:
      - name: Deploy
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Via un fichier `.env.local`

```bash
# .gitignore doit contenir :
.env.local
.env.*.local
credentials_local.md
```

---

## 3. Format recommandé pour tokens et URLs

### Token GitHub

```yaml
github:
  pat:
    prefix: "ghp_"              # Préfixe standard GitHub PAT
    scopes: ["repo", "workflow"] # Scope minimum requis
    expiry: "90 jours"          # Rotation recommandée
  ssh_key:
    path: "~/.ssh/id_ed25519"   # Clé SSH préfèree (plus sécurisée)
    comment: "user@hostname"    # Commentaire identifiable
```

### URLs standardisées

```yaml
repositories:
  main: "https://github.com/Commonfields25/Interceptor_M"
  api: "https://api.github.com/repos/Commonfields25/Interceptor_M"
  raw: "https://raw.githubusercontent.com/Commonfields25/Interceptor_M/main"
```

---

## 4. Bonnes pratiques de sécurité

### ✅ Bonnes pratiques

- **Nunca commiter de credentials en clair** — Vérifiez toujours `.gitignore`
  ```bash
  # Vérifier avant chaque commit :
  git diff --cached | grep -i "token\|password\|secret\|key"
  ```
- **Utiliser des variables d'environnement** — Jamais de secrets dans le code source
- **Rotation régulière des tokens** — PAT GitHub : tous les 90 jours
- **Principe du moindre privilège** — Accorder uniquement les scopes nécessaires
- **Audit régulier des accès** — Révoquer les tokens inutilisés
- **Stocker les secrets dans un coffre-fort** — 1Password, Bitwarden, Vault, etc.
- **Utiliser SSH plutôt que HTTPS** pour les opérations Git
- **Activer l'authentification 2FA** sur tous les comptes

### ❌ Erreurs à éviter

- Pousser un `.env` ou `config.py` avec des secrets sur GitHub
- Partager des tokens dans des messages de commit ou PR
- Stocker des mots de passe en dur dans des scripts
- Utiliser le même token pour plusieurs services
- Laisser des credentials dans des commentaires de code

---

## 5. Checklist avant push

```bash
# 1. Vérifier .gitignore
cat .gitignore | grep -E "env|credentials|secret|key"

# 2. Scanner les secrets potentiels
grep -rE "ghp_|sk_|password\s*=\s*['\"]" --include="*.py" --include="*.yaml" --include="*.md"

# 3. Vérifier les fichiers暂（staged）
git diff --cached --name-only

# 4. Nettoyer les variables d'environnement en local après usage
unset GITHUB_TOKEN API_KEY DB_PASSWORD
```

---

## 6. Templates concrets

### `.env.example`

```bash
# GitHub
GITHUB_TOKEN=
GITHUB_USER=

# API Keys
OPENAI_API_KEY=
HF_TOKEN=

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=interceptor_db
DB_USER=
DB_PASSWORD=

# Deployment
DEPLOY_SSH_KEY_PATH=~/.ssh/id_ed25519
DEPLOY_SERVER=
```

### `.gitignore` minimal (credentials)

```
# Secrets & credentials
.env
.env.local
.env.*.local
.env.example
credentials_local.md
credentials.md
*.pem
*.key

# GitHub secrets (workflows)
.secrets
.github/secrets/
```

---

*Ce template a été créé pour standardiser la gestion des identifiants dans le projet Interceptor_M.*
*Dernière mise à jour : 2026-06-28*
