# Compliance — engineering/simulation

This folder contains ISO compliance documentation for the Interceptor_M simulation namespace.

---

## 📋 Index

| Document | Standard | Description |
|---|---|---|
| `ISO9001_traceability.md` | ISO 9001:2015 | Requirements traceability, test records, document control |
| `ISO27001_security.md` | ISO 27001:2022 | Secure parameter handling, access control, token hygiene |
| `ISO15288_process.md` | ISO 15288:2023 | Systems engineering lifecycle alignment for simulation |
| `ISO_compliance_matrix.md` | All three | Unified table mapping scripts/files to ISO clauses |
| `README.md` | — | This file — index and verification checklist |

---

## ✅ Verification Checklist

### ISO 9001:2015
- [ ] Every `.m` script has a header (name, rev, date, author) → `ISO9001_traceability.md §7.5.1a`
- [ ] Revision status tracked via Git → `ISO9001_traceability.md §7.5.1b`
- [ ] Changes approved via PR review → `ISO9001_traceability.md §7.5.2b`
- [ ] Simulation logs retained ≥ 3 years → `ISO9001_traceability.md §7.5.4`
- [ ] Nonconformance reports (NCRs) filed for any test failure → `ISO9001_traceability.md §3.3`

### ISO 27001:2022
- [ ] No secrets, tokens, or PII in simulation files → `ISO27001_security.md §5`
- [ ] Tokens passed via stdin only (never hardcoded) → `ISO27001_security.md §4`
- [ ] Branch protection + PR review on main/develop → `ISO27001_security.md §A.9.1`
- [ ] Incident response plan understood → `ISO27001_security.md §7`

### ISO 15288:2023
- [ ] All REQ-* requirements mapped to scripts → `ISO15288_process.md §2.2`
- [ ] Architecture follows modular script model → `ISO15288_process.md §2.3`
- [ ] Verification via Octave CI automated → `ISO15288_process.md §2.5`
- [ ] Validation via `constraint_test_runner.m` thresholds → `ISO15288_process.md §2.6`
- [ ] Configuration management via Git → `ISO15288_process.md §3`

### General
- [ ] CI workflow `.github/workflows/octave-sim-ci.yml` runs on every push/PR
- [ ] All scripts syntax-compatible with GNU Octave 8.x+ and MATLAB R2023b+
- [ ] No files modified outside `engineering/simulation/` and `.github/workflows/`

---

## 🔍 Quick Compliance Scan

```bash
# Verify no secrets in simulation namespace
grep -rP 'ghp_|token:|password:|api_key' engineering/simulation/ .github/workflows/
# Expected output: (empty)

# Verify all scripts have headers
grep -l "## " engineering/simulation/scripts/*.m engineering/simulation/tests/*.m
# Expected output: list of all .m files

# Verify ISO docs are present
ls -1 engineering/simulation/compliance/
# Expected: ISO9001_traceability.md ISO27001_security.md ISO15288_process.md ISO_compliance_matrix.md README.md
```

---

## 📞 Contacts

- **Simulation Team Owner**: Engineering / E3 Team
- **Compliance Owner**: Engineering Lead
- **ISO 9001 questions**: See `ISO9001_traceability.md`
- **ISO 27001 questions**: See `ISO27001_security.md`
- **ISO 15288 questions**: See `ISO15288_process.md`

---

*Last reviewed: 2026-06-30 | Next review: 2027-06-30*
