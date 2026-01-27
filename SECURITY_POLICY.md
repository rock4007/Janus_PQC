# Security Policy

## Supported Versions
- Main branch is maintained. Tags are recommended for deployment.

## Reporting a Vulnerability
- Email: soumodeepguha22@gmail.com
- Include: environment details, reproduction steps, logs sans secrets.
- We aim to acknowledge within 3 business days.

## Handling Sensitive Information
- Do not include secrets or private keys in reports.
- If disclosure is sensitive, request an encrypted channel.

## Hardening Guidance
- Use HSMs or managed KMS for key storage.
- Run with least privilege; restrict filesystem and network access.
- Enable integrity checks: validate both signatures and envelope fields.
- Prefer FIPS-validated crypto modules for regulated environments.

## Dependency Security
- Maintain SBOM (CycloneDX) and run static analysis (Bandit) in CI.
- Pin dependencies and update regularly.

## Incident Response
- Collect minimal logs; redact sensitive data.
- Document timeline and actions; update advisories.
