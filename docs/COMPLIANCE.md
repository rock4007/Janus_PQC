# Compliance Overview

This project provides a prototype for dual-layer signature verification aligned with NIST PQC selections. It is intended for R&D and integration testing. Production deployments in regulated environments must use validated cryptographic modules and adhere to jurisdictional requirements.

## Standards Alignment
- **NIST PQC (Signatures):** ML-DSA (Dilithium) — the project uses `oqs` ML-DSA-65 when available. Note: Library and module validations are ongoing; treat as experimental unless using a validated distribution.
- **NIST SP 800-56/57 (Key Management):** Follow robust key lifecycle management and rotation policies; store private keys in HSM or OS keyring with least privilege.
- **NIST SP 800-131A (Transition):** Strong hash (SHA-256) used in the envelope; plan for minimum 112-bit security equivalence.
- **FIPS 140-3:** Requires cryptographic operations to be performed by a validated module in FIPS mode. The default Windows `cryptography` wheel and `oqs` are not FIPS-validated. For government use, run in environments with FIPS-validated OpenSSL and use approved algorithms/modules.

## Government Readiness Notes
- **Procurement:** Provide SBOM and build provenance; pin dependencies; enforce reproducible builds.
- **Data Protection:** No plaintext secrets are stored. Envelope includes `msg_sha256`, `ts`, and `nonce` to resist tampering and replay.
- **Logging & Privacy:** Do not log private keys or raw payload; redact sensitive data from logs.
- **Policy & Notices:** PQC support is experimental. Do not represent outputs as FIPS-compliant unless built/linked with validated modules.

## Operational Guidance
- **Key Storage:** Use HSMs or enterprise key vaults (Azure Key Vault, AWS KMS, HashiCorp Vault). Ensure audit trails and access controls (RBAC).
- **Build Provenance:** Use CI-generated artifacts with checksums; sign releases (git tag signing, release asset signatures).
- **Risk Management:** Keep a deprecation plan for non-approved algorithms; monitor NIST and vendor advisories.

## Required Artifacts
- **SBOM:** CycloneDX JSON.
- **Test Evidence:** Black-box success and tamper-detection runs.
- **Policy Docs:** Security policy and support contact.

## Disclaimer
This repository is a reference implementation. Government or regulated deployments must undergo formal accreditation and operate only with FIPS-validated cryptographic modules.
