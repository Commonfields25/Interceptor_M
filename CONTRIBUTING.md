# Contributing to Interceptor_M

## 🗂️ Repository Structure

| Path | Purpose |
|------|---------|
| `agents/D{1,2,3}/` | Domain agent definitions (D1=Design, D2=Aero, D3=Struct) |
| `agents/E{1,2,3}/` | Engineering agent definitions |
| `agents/agent_manager/` | Agent Manager rules, decision log, gate audits |
| `engineering/DI/ML/` | Swarm RL training (MAPPO, Isaac Gym) |
| `engineering/DC/` | Airframe sizing |
| `engineering/DI/NDC/` | Market & NDC studies |
| `governance/` | Policies, CI checks, BOT guidelines |
| `simulation/` | 6-DOF flight simulator |
| `docs/` | Technical documentation |

## 🚀 Development Workflow

1. **Branch** from `main` → `feat/<AGENT>/<short-description>`
2. **Implement** within your namespace only (see `governance/NAMESPACE-ISOLATION.md`)
3. **Run CI locally** before pushing:
   ```bash
   python3 governance/ci_checks/namespace_isolation.py --changed-files "file1.md file2.py" --author-agent D2
   ```
4. **Open PR** → auto-labeling + governance CI run automatically
5. **PR reviewed** → merge to main

## 🏷️ Labels You Should Know

| Label | Meaning |
|-------|---------|
| `area:swarm-rl` | Changes to ML/Swarm RL code |
| `area:dc` | Changes to DC airframe sizing |
| `area:governance` | Changes to policies/CI |
| `red-flag:rf1` | Blocked: no trained baseline |
| `priority:critical` | Must resolve before next gate |

## ✅ PR Checklist

- [ ] Changes are within your agent namespace
- [ ] Smoke test passes (`python -c import swarm_env`)
- [ ] Relevant labels added
- [ ] Milestone assigned
- [ ] Docs updated if behavior changed

## 🔗 Key Docs

- `governance/NAMESPACE-ISOLATION.md` — who's allowed to touch what
- `governance/AUTO-APPROVAL-POLICY.md` — KPI thresholds for auto-approval
- `engineering/DI/ML/SWARM-RL-PLAN.md` — RL training roadmap
- `docs/INSIGHTS_REPORT.md` — weekly metrics and improvement tracking

