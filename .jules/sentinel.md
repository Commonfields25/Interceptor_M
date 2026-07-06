# 🛡️ Sentinel Journal

This journal tracks critical security learnings, vulnerability patterns, and architectural gaps discovered in the Interceptor_M codebase.

## 2026-07-02 - Security Theater in Audit Pipelines
**Vulnerability:** The repository's secret audit script (`scripts/audit_secrets.py`) contained a Python syntax error that rendered it non-functional. Furthermore, the CI workflow (`.github/workflows/iso-compliance.yml`) used `|| echo "Audit done"` to mask failures of this script, ensuring the CI would pass even if the security check crashed or found vulnerabilities.
**Learning:** Security controls can easily degrade into "Security Theater" when they are not strictly enforced or when their failure is intentionally suppressed to avoid CI friction. A non-functional security check is worse than no check at all, as it provides a false sense of compliance.
**Prevention:**
1. Never suppress exit codes of security-critical steps in CI/CD pipelines.
2. Security scripts must be included in the project's standard linting and testing suites to catch syntax errors or regressions.
3. Regularly verify that security tools can actually "fail" by testing them with dummy vulnerabilities.

## 2026-07-02 - Ubiquitous Error Suppression in Security Workflows
**Vulnerability:** Beyond the secret audit script, several other security-related workflows (including `hardened-security.yml` and dependency audits) were using `|| echo "issues found"` patterns. This effectively neutralized the security gates, allowing vulnerable code or dependencies to bypass the CI without blocking PRs.
**Learning:** Security tools are often perceived as "noisy" or "brittle," leading developers to suppress their exit codes to keep the CI green. This transforms a security check into a passive notification that is easily ignored.
**Prevention:**
1. Enforce strict exit codes for all security scanning tools.
2. If a tool is too noisy, tune its configuration (e.g., ignore specific non-critical CVEs or paths) rather than suppressing all its failures.
3. Use commit SHAs for GitHub Actions to prevent supply chain attacks on the CI/CD pipeline itself.
