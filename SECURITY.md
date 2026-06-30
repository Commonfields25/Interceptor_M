# Security Policy — Interceptor_M

## 1. Reporting a Vulnerability

We take the security of our counter-UAS systems seriously. If you discover a vulnerability, please report it immediately:

- **Primary Contact**: Director General (DG)
- **Method**: Secure message or PGP-encrypted email (Internal only).
- **Response Time**: We acknowledge reports within 24 hours and provide an initial assessment within 72 hours.

## 2. Secure Development Standards

All agents must adhere to the following:
- **No Hardcoded Secrets**: Use GitHub Secrets/Environment Variables.
- **Dependency Audit**: Regular `pip audit` and `npm audit`.
- **Namespace Isolation**: Do not bypass agent scope boundaries.

## 3. Data Classification

Data within this repository is classified under the following scheme:

| Class | Label | Description | Storage Requirement |
|---|---|---|---|
| **L1** | PUBLIC | Marketing, General Documentation | No restrictions |
| **L2** | INTERNAL | Operational plans, non-ITAR engineering | Repository access restricted |
| **L3** | CONFIDENTIAL | Defense (DD) Engineering, Logic | High-grade encryption required |

---
*UAV Venture Security Protocol v1.0*
