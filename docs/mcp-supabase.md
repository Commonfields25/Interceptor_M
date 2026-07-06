---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# Supabase MCP — Connexion Agents (R/W)

## Objectif

Donner aux agents IA (Jules / Linear) un accès **lecture + écriture** à la base Postgres Supabase du projet via le **Model Context Protocol (MCP)**.

> ⚠️ **Sécurité — R/W enabled** : l'accès est en lecture **et** écriture. Un token Supabase avec permissions d'écriture permet à un agent d'exécuter des requêtes INSERT/UPDATE/DELETE. Ne partagez jamais le token.

---

## Prérequis

- Un projet Supabase actif : [https://app.supabase.com](https://app.supabase.com)
- Un **Personal Access Token** (PAT) Supabase
- Accès au dépôt GitHub `Commonfields25/Interceptor_M`

---

## Étape 1 — Créer un Personal Access Token (PAT) Supabase

1. Se connecter sur [app.supabase.com](https://app.supabase.com)
2. Aller dans **Settings → Access Tokens**
3. Cliquer **Generate new token**
4. Nommer le token (ex. `mcp-agents-rw`)
5. Choisir les scopes nécessaires : `PROJECTS_READ`, `PROJECTS_WRITE`, `DATABASES_READ`, `DATABASES_WRITE`
6. **Copier le token immédiatement** — il ne sera plus affiché après fermeture

---

## Étape 2 — Stocker le token dans GitHub Secrets (recommandé)

> Ne jamais commiter le token. Toujours passer par un secret GitHub / Vercel.

### GitHub Secrets

1. Ouvrir le dépôt → **Settings → Secrets and variables → Actions**
2. Cliquer **New repository secret**
3. Ajouter ces 3 secrets :

| Nom du secret | Valeur |
|---|---|
| `SUPABASE_ACCESS_TOKEN` | Le PAT généré à l'étape 1 |
| `SUPABASE_PROJECT_REF` | L'ID du projet visible dans les paramètres Supabase (Settings → API) |
| `SUPABASE_URL` | L'URL du projet Supabase (ex. `https://abcdefgh.supabase.co`) |

### Vercel Secrets (si déployé sur Vercel)

1. Ouvrir le projet sur [vercel.com](https://vercel.com)
2. **Settings → Environment Variables**
3. Ajouter les 3 variables ci-dessus pour les environnements `Development`, `Preview`, `Production`

> Les agents qui tournent sur Vercel liront ces variables d'environnement automatiquement.

---

## Étape 3 — Configurer le serveur MCP Supabase

Le fichier `.mcp/supabase.json` à la racine du projet déclare le serveur MCP Supabase :

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase",
        "--project-ref",
        "${SUPABASE_PROJECT_REF}"
      ],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}",
        "SUPABASE_PROJECT_REF": "${SUPABASE_PROJECT_REF}"
      }
    }
  }
}
```

Ce fichier est **déjà commité** dans la branche `feat/supabase-mcp`. Il est lu par les clients MCP compatibles (Cursor, Claude Desktop, etc.).

- `SUPABASE_ACCESS_TOKEN` → secret GitHub (ou variable d'environnement)
- `SUPABASE_PROJECT_REF` → secret GitHub (ou variable d'environnement)
- **Pas de flag `--read-only`** → écriture autorisée

---

## Étape 4 — Brancher les agents

### Jules

Dans la configuration de l'agent Jules (fichier `agents/agent_manager/config.json` ou équivalent), ajouter :

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase", "--project-ref", "${SUPABASE_PROJECT_REF}"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}",
        "SUPABASE_PROJECT_REF": "${SUPABASE_PROJECT_REF}"
      }
    }
  }
}
```

### Linear

Même configuration dans le fichier de config Linear / MCP de l'agent dédié (`agents/D1/` ou équivalent).

> Les agents utilisent les variables d'environnement injectées par l'environnement d'exécution. Aucune valeur secrète n'est stockée dans le code source.

---

## Étape 5 — Vérifier la connexion

Depuis un terminal avec Node.js ≥ 18 :

```bash
npx -y @supabase/mcp-server-supabase --project-ref <YOUR_PROJECT_REF>
# puis tester avec un outil MCP-compatible (Cursor, Claude Desktop, etc.)
```

Ou depuis Python (via `supabase` SDK) :

```python
from supabase import create_client, Client

client: Client = create_client(
    supabase_url=os.environ["SUPABASE_URL"],
    supabase_key=os.environ["SUPABASE_ACCESS_TOKEN"]
)

# Test lecture
result = client.table("agents").select("*").execute()
print(result.data)
```

---

## Sécurité — Points de vigilance

| Risque | Mitigation |
|---|---|
| Token exposé dans les logs | Ne jamais logger `SUPABASE_ACCESS_TOKEN` ; les secrets GitHub ne sont pas affichés dans les logs CI |
| Agent qui modifie la prod | Limiter le scope du PAT aux bases нужные ; utiliser des policies RLS Supabase |
| Commit accidentel du token | `.env` est dans `.gitignore` ; le `.env.example` ne contient que des placeholders |
| Accès non autorisé au projet | Révoquer le token depuis Supabase Dashboard → Settings → Access Tokens |

---

## Dépannage

| Erreur | Cause probable | Solution |
|---|---|---|
| `401 Unauthorized` | Token expiré ou mal copié | Régénérer le PAT dans Supabase Dashboard |
| `project not found` | `SUPABASE_PROJECT_REF` incorrect | Vérifier dans Settings → API du projet Supabase |
| MCP server not found | `npx` non disponible | S'assurer que Node.js ≥ 18 est installé dans l'environnement de l'agent |
| `PERMISSION DENIED` sur table | RLS policy Supabase | Ajuster les policies sur les tables Postgres dans le dashboard Supabase |

---

*Dernière mise à jour : PR #145 — feat: Supabase MCP connection for agents (read/write)*
