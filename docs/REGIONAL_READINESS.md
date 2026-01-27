# Regional Readiness

This document summarizes considerations for deploying Janus_PQC in the EU, USA, Canada, and Australia. Janus_PQC is a cryptographic verification prototype; it does not process personal data by itself. Regulatory alignment depends on the environment and cryptographic modules you choose.

## Common Requirements
- Use validated cryptographic modules (e.g., FIPS 140-3) where required.
- Provide SBOM, signed artifacts, and reproducible build evidence.
- Maintain access controls, auditability, and incident response procedures.
- Avoid handling PII unless necessary; if handling PII, apply regional privacy controls.

## European Union (EU)
- **GDPR:** If used with personal data, ensure lawful basis, data minimization, integrity, and access controls.
- **NIS2:** For essential/important entities, ensure security measures, incident reporting, and supply-chain transparency (SBOM).
- **ENISA Guidance:** Follow best practices for crypto implementations and key management.
- **Data Residency:** Host keys/artifacts within EU when required by policy.

## United States (USA)
- **FIPS 140-3:** Government use requires crypto operations via validated modules in FIPS mode.
- **NIST SP 800-53/63:** Align identity, access control, and integrity controls as applicable.
- **FedRAMP:** For cloud service authorization, provide SBOM, signed artifacts, vulnerability management, and logging.
- **HIPAA / CCPA/CPRA:** If touching PHI/PII, enforce privacy and security safeguards; Janus_PQC itself does not store data.

## Canada
- **PIPEDA:** For private-sector personal data use, ensure consent, safeguards, accuracy, and accountability.
- **CyberSecure Canada / ITSG-33:** Follow baseline cyber controls; ensure crypto and integrity controls meet guidance.
- **Residency & Sovereignty:** Host keys and artifacts in Canadian regions where policy requires.

## Australia
- **ASD Essential Eight / ISM:** Apply hardening strategies; ensure integrity controls and key management.
- **Privacy Act:** If handling personal data, ensure privacy principles and security safeguards.
- **Sovereign Hosting:** Use Australian regions when mandated.

## Export Controls & Legal
- Comply with applicable export controls for cryptographic software.
- Do not deploy for illegal or unauthorized use; see ACCEPTABLE_USE_POLICY.md.

## Implementation Notes
- **Validated Modules:** On Windows, default wheels may not be FIPS validated; use environments with validated OpenSSL.
- **SBOM & Signing:** CI generates CycloneDX SBOM and signed checksums in releases.
- **Key Storage:** Prefer HSMs or managed KMS (AWS KMS, Azure Key Vault) with RBAC and auditing.

## Disclaimer
This repository is a reference implementation. Accreditation and compliance depend on your deployment environment and validated crypto modules.
