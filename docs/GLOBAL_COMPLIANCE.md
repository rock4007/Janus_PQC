# Global Cybersecurity Compliance Overview

Janus_PQC is a cryptographic verification prototype. Deployment compliance depends on your environment, controls, and validated crypto modules. This document summarizes common frameworks and how this project supports compliance readiness.

## Baseline Security & Governance
- **ISO/IEC 27001 + 27002:** Information security management and controls.
- **NIST CSF / SP 800-53:** Identify/Protect/Detect/Respond/Recover; control families (AC, AU, CM, IA, etc.).
- **CIS Critical Security Controls:** Implementation-friendly baseline for hardening and monitoring.
- **SOC 2 (Trust Services Criteria):** Security, Availability, Confidentiality; audit reporting.

## Privacy & Data Protection
- **GDPR (EU):** Lawful basis, data minimization, integrity, accountability.
- **CCPA/CPRA (California):** Consumer rights and protections.
- **PIPEDA (Canada):** Consent, safeguards, accuracy, accountability.
- **Australia Privacy Act:** Principles and security safeguards.

## Sectoral & Regulatory
- **HIPAA (US healthcare):** Protect PHI; integrity controls; audit trails.
- **PCI DSS (payments):** Secure development, change control, logging, vulnerability management.
- **NIS2 (EU):** Risk management, incident reporting, supply-chain security (SBOM).
- **ISM / Essential Eight (Australia):** Hardening strategies and baseline controls.

## How Janus_PQC Supports Readiness
- **Integrity & Tamper-Evidence:** Dual signatures (Ed25519 + ML-DSA/Ed448) over a canonical envelope (timestamp, nonce, SHA-256) help detect tampering and replay.
- **Supply Chain Transparency:** CI produces CycloneDX SBOM and signed checksums in releases; non-blocking `bandit` security scans and `pip-audit` available.
- **Restricted Use & Licensing:** Proprietary license and Acceptable Use Policy limit unauthorized/illegal use.
- **Documentation:** Regional guidance for EU/UK/Ireland; compliance and security policy docs included.

## Required Operational Controls (Deployers)
- **Validated Crypto Modules:** For government/regulatory use, operate only with FIPS 140-3 validated modules (FIPS mode). Default wheels may not be validated.
- **Key Management:** Store private keys in HSM/KMS (AWS KMS, Azure Key Vault, GCP KMS). Apply RBAC and auditing.
- **Logging & Monitoring:** Redact sensitive data; maintain audit trails; monitor integrity outcomes.
- **Vulnerability Management:** Track SBOMs; patch dependencies; run static analysis and dependency audits.
- **Change Management:** Use PRs, reviews, branch protection, and signed commits for provenance.

## Exports & Legal
- Comply with export controls (e.g., EAR) and sanctions. Do not deploy for illegal or unauthorized purposes.

## Disclaimers
- This repository is a reference implementation. Formal accreditation and certification are the deployer’s responsibility.
- Compliance depends on your chosen environment, validated cryptographic modules, and organizational controls.
