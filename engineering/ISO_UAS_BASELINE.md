---
action: Fix
agent: Jules
related_gate: G2
status: Validated
timestamp: 2026-07-02 13:27:36+00:00
---

# ISO/UAS Baseline — Interceptor_M

> **Status:** Active Baseline | **Version:** 1.0 | **Date:** 2026-06-30
> **Owner:** Direction Générale | **Classification:** Interne

---

## 1. Cadre Normatif de Référence

| Norme | Domaine | Application Interceptor_M |
|-------|---------|---------------------------|
| ISO 9001:2015 | Systèmes de Management de la Qualité (QMS) | Processus de développement, revue de conception, contrôle change |
| ISO/IEC 27001:2022 | Sécurité de l'information | Protection des IP-Stealth specs, secrets CI/CD, données client |
| ISO/IEC 15408 (Common Criteria) | Évaluation de sécurité IT | Chaîne de confiance du firmware ESC/FC |
| ISO/IEC 42001:2023 | Management de l'IA | Algorithmes swarm RL Isaac Gym, validation autonomía |
| ASTM F3411-24 | Identification et suivi UAS | Protocole Remote ID — numéro de série, position GPS broadcast |
| ASTM F3002-24 | Exigences de conception UAS habité | N/A pour Interceptor_M (UAS autonome) |
| JARUS SORA v2.0 | Analyse de risque operational UAS | Confinement géo-fencé, C2-link loss recovery, fail-safe states |
| EASA SC-DT (MIDO) | Certificationelijke trafic UAS | Autorisation de vol DMZ2/3, intégration space weather |
| ISO 14306 | Échange de données CAO STEP | Conformité export modèles DFMA |

---

## 2. Conformité ISO 9001 — Processus Clés

| Processus ISO 9001 | Artefact Interceptor_M | Statut |
|-------------------|------------------------|--------|
| §7.1.3 Infrastructure | `engineering/INFRASTRUCTURE_REQ.md` | À créer |
| §7.2 Compétence | `agents/*/INSTRUCTIONS_*.md` | ✅ Actif |
| §8.1 Planification CL | `governance/QUALITY_POLICY.md` | ✅ Actif |
| §8.3 Conception & Développement | `docs/Cahier_Charges_Prototype.md` | ✅ Actif |
| §8.4 Approvisionnement | `manufacturing/BOM_consolidee.md` | ✅ Actif |
| §8.5 Production | `manufacturing/BRK-001_gamme_usinage.md` | ✅ Actif |
| §8.7 Non-conformités | `templates/NON_CONFORMANCE_REPORT.md` | ✅ Actif |
| §9.1 Monitoring | `simulation/montecarlo_pintercept.py` | ✅ Actif |
| §10.2 Correctif | `manufacturing/NCR-001_notes.md` | ✅ Actif |

---

## 3. Remote ID & Airworthiness (ASTM F3411 + JARUS SORA)

```yaml
remote_id:
  identifier_type: serial_number
  uas_id_format: UUID_v4
  broadcast_method: Bluetooth_LE_Extended_Advertising
  encryption: AES-256-CBC
  broadcast_interval_sec: 1
  mandatory_fields:
    - uas_id
    - timestamp (UTC, millisecond precision)
    - position (WGS84, ±1m accuracy required)
    - altitude (pressure + geoid corrected)
    - speed (ground track vector)
    - status (airborne / grounded / emergency)
  conformance:
    ASTM_F3411_24: true
    CE_Red_2014_53_EU: pending_antenna_certification
```

---

## 4. Sécurité de l'Information (ISO/IEC 27001)

| Contrôle 27001 | Implémentation Interceptor_M | Priority |
|----------------|------------------------------|----------|
| A.8.1 Responsabilités | PAT GitHub avec permissions minimales (read:repo only pour les agents) | 🔴 Critique |
| A.8.12 Gestion des mots de passe | Secrets stockés dans GitHub Actions vault uniquement | 🔴 Critique |
| A.8.15 Logging | `linear_supabase/supabase_alerts.py` — audit trail Supabase | 🟡 Moyen |
| A.8.3 Accès source | Branches protégées `main`/`develop` — merge requires 1 approval | ✅ En place |
| A.8.16 Surveillance | GitHub Security Advisories + dependabot | ✅ En place |
| A.18.1 Continuité | Fail-safe states JARUS SORA + backup Supabase | 🟡 Moyen |

---

## 5. AI/ML Governance (ISO/IEC 42001 — B-AI)

| Exigence 42001 | Artefact | Statut |
|---------------|---------|--------|
| §6.2.3 Détermination des parties interessées | `agents/AC/INSTRUCTIONS_AC.md` | ✅ |
| §7.2 Compétence IA | `engineering/DI/ML/SWARM-RL-PLAN.md` | ✅ |
| §8.4 Système AIPerson | Validation indépendante des comportements RL (Isaac Gym sim) | 🟡 Partiel |
| §9.1 Monitoring | Monte-Carlo sim + seuil de défaillance < 1e-5 | ✅ |
| §10.3 Non-conformité | NCR-001 — corrective action process | ✅ |

---

## 6. Project Protection Checklist

- [x] PATGitHub: permissions minimales appliquées (`repo` read-only)
- [x] Branch protection: `main` requires signed commits + 1 reviewer
- [x] Token rotation: scheduled every 90 jours (靠 DG)
- [x] No credentials in git history (git-secrets scan dans CI)
- [x] secrets dans GitHub Actions Vault uniquement
- [x] `.env.example` publié — `.env` dans `.gitignore`
- [x] ISO/IEC 27001 controls documentés dans ce fichier
- [x] JARUS SORA fail-safe state documenté
- [x] Remote ID broadcast — conformité ASTM F3411

---

## 7. Artefacts de Traçabilité

| Artefact | Fichier | Lien au MILESTONE_PLAN |
|----------|---------|----------------------|
| BOM Consolidée | `manufacturing/BOM_consolidee.md` | M7 |
| DI Spec Lock | `engineering/DI_SPEC_LOCK.md` | M7 |
| ISO Compliance CI | `.github/workflows/iso-compliance.yml` | M1 |
| Isaac Gym RL | `engineering/DI/ML/isaac_gym/` | W1 |
| Airframe Model | `engineering/DI/NDC/NDC-INTERCEPTOR-DD.md` | W2 |
| 6-DOF Sim | `simulation/sim_6dof.py` | M1 |

---

**Révision:** 1.0 — June 30, 2026
**Approuvé par:** Direction Générale
