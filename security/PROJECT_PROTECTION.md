# Project Protection Policy — Interceptor_M

> **Classification:** Confidentiel Projet | **Version:** 1.0 | **Date:** 2026-06-30  
> **Approuvé par:** Direction Générale

---

## 1. Objectif

Ce document définit la politique de protection du projet **Interceptor_M** contre les menaces:
- Exfiltration d'IP (specs stealth, algorithmes RL, BOM)
- Abus de credentials CI/CD
- Publication non-autorisée de code ou données
- Atteinte à l'intégrité du processus de certification (JARUS SORA / EASA)

---

## 2. Protection des Branches Git

### 2.1 Règles de Protection

| Branche | Protection Active | Merge Rule |
|---------|-----------------|------------|
| `main` | ✅ Protégée | 1 approval + signed commits |
| `develop` | ✅ Protégée | 1 approval |
| `feat/*` | Non protégée (transitoire) | Squash merge only |
| `hotfix/*` | ✅ Protégée | Fast-forward vers `main` |

### 2.2 Nettoyage Post-Merge

Les branches mergées doivent être supprimées dans les 48h via:
```bash
# Script de nettoyage
git fetch --prune && \
  git branch -r --merged origin/main | grep -v main | \
  xargs -r git push origin --delete
```

**Commandes DG recommandées** (à exécuter après chaque merge):
```bash
gh pr merge <PR_NUMBER> --admin --merge && \
  gh pr close <PR_NUMBER> --delete-branch
```

---

## 3. Politique PAT GitHub

### 3.1 Principe de Moindre Privilège

| Token | Permissions | Usage |
|-------|------------|-------|
| `DG-PAT` (cetoken) | `repo:full` | Opérations DG uniquement (merge, admin) |
| Agent PATs | `repo:read` | Lecture seule pour les agents AI |
| Deploy Key | `repo:read` (single repo) | Accès lecture cloning |

### 3.2 Rotation des Tokens

| Token | Durée de vie | Rotation |
|-------|-------------|----------|
| DG-PAT | 90 jours | Manuel — DG génère via GitHub Settings → Developer Settings → Personal Access Tokens |
| Agent PATs | 30 jours | Script automatique `scripts/rotate_agent_tokens.sh` |
| Deploy Keys | 365 jours | Renouvellement annuel |

### 3.3 Hygiene des Secrets

```bash
# Vérification proactive (CI intégrée)
- name: Scan for secrets
  uses: trufflesecurity/trufflehog@latest
    with:
      path: ./
      base_depth: 1
```

**Règles absolues — ZERO EXCEPTIONS:**
1. Jamais de secrets dans le code source (`.py`, `.m`, `.js`, `.yml`)
2. Jamais de `GH_TOKEN` dans les logs ou sorties CI
3. Tokens只能在 GitHub Actions Secrets Vault (`repository → Settings → Secrets`)
4. `.env` toujours dans `.gitignore`
5. `.git/hooks/` commit-msg rejettera tout secret détecté

---

## 4. Politique de Non-Publication

### 4.1 Données Interdites de Publication

- [ ] Spécifications de la techno stealth (matériaux RADAR)
- [ ] BOM détaillée avec fournisseurs réels (remplacer par anonymisés)
- [ ] Algorithmes de contrôle RL non-publiés
- [ ] Certificats EASA/JARUS en cours
- [ ] Clés API production (C2-link, telemetry)

### 4.2 Spécifications Techniques

- [x] ISO_UAS_BASELINE.md — publiées (conformité publique)
- [x] README.md — publique (repo public)
- [x] Cahier des Charges Prototype — version publiques uniquement
- [ ] engineering/DI/DI-MARKET-STUDY.md — restriction à vérifier (DG)
- [ ] engineering/DI/ML/swarm_env.py — restriction à vérifier (DG)

---

## 5. Contrôles de Sécurité Opérationnels

### 5.1 CI/CD Security (ISO/IEC 27001 — A.8.19)

```yaml
# .github/workflows/security-hardening.yml
- job: secret_scanning
  uses: trufflesecurity/trufflehog@latest
- job: dependency_audit
  uses: snyk/actions/node@master
- job: branch_protection_enforce
  uses: restfulgithub/branch-protection@latest
```

### 5.2 Monitoring & Alerting

| Canal | Type d'alerte | Destinataires |
|-------|--------------|---------------|
| Supabase Alerting | Tentative de connexion suspecte | DG + Security Team |
| GitHub Security Advisories | CVEs sur dépendances | Développeurs |
| Linear Integration | Tâche automatique sur vulnérabilité détectée | Assigné |

---

## 6. Registre des Incidents

| Date | Incident | Résolution | Statut |
|------|----------|-----------|--------|
| (vide — aucun incident enregistré) | — | — | — |

---

## 7. Révision et Évaluation

- **Révision annuelle:** Juin 2027
- **Évaluation de conformité ISO 27001:** M14 (2027-04-15)
- **Responsable:** Direction Générale

---

*Document généré automatiquement — toute modification doit être validée par la DG.*
