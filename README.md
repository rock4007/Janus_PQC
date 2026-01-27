# Janus_PQC [![CI](https://github.com/rock4007/Janus_PQC/actions/workflows/janus-pqc-tests.yml/badge.svg)](https://github.com/rock4007/Janus_PQC/actions/workflows/janus-pqc-tests.yml)

The transition to "Cloud 3.0" and the "Year of Truth for AI" requires data integrity that can survive early quantum decryption attempts.

A hybrid-signature prototype combining classical Ed25519 with post-quantum ML-DSA-65 (via `oqs` if available, otherwise Ed448 fallback) to provide resilient dual-layer verification.

## Features
- Dual-signature over a tamper-evident envelope (timestamp, nonce, SHA-256)
- Uses `oqs` on compatible systems; Ed448 fallback for Windows
- Black-box test suite to validate success and tamper detection
- Minimal Docker image for portable runs

## Architecture
- **Envelope:** Canonical JSON with `version`, `algo`, `ts`, `nonce`, `msg_sha256` binds signatures to the exact payload and thwarts replay.
- **Hybrid Signatures:** Ed25519 + ML-DSA-65 (or Ed448 fallback) both sign the same envelope; verification requires both to pass.
- **Adapter:** `PQSignatureAdapter` auto-selects `oqs` when available; otherwise uses Ed448 so Windows users can run without liboqs.

## Quick Start (Windows)
```powershell
python Janus_PQC
python run_tests_janus_pqc.py
```

## Installation
```powershell
python -m pip install -r requirements.txt
```
Notes:
- `cryptography` installs on Windows/macOS/Linux.
- `python-oqs` (liboqs bindings) is optional and not on PyPI for Windows; use WSL/Linux and follow the official guide.

## Optional: Linux/WSL with oqs
- Follow https://github.com/open-quantum-safe/liboqs-python
- When `oqs` is present, the adapter uses ML-DSA-65 instead of Ed448 fallback.

## Docker
```bash
docker build -t janus-pqc .
docker run --rm janus-pqc
```

## CI (Optional)
Example GitHub Actions job to run black-box tests:
```yaml
name: janus-pqc-tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m pip install -r requirements.txt
      - run: python run_tests_janus_pqc.py
```

## Files
- `Janus_PQC`: runnable script with envelope signing
- `janus_core.py`: importable core module for CLI/tests
- `janus_cli.py`: CLI runner
- `tests/test_black_box_janus_pqc.py`: black-box tests
- `run_tests_janus_pqc.py`: test harness
- `requirements.txt`: dependencies
- `Dockerfile`: containerization

## Security Notes
- Both signatures must verify the same envelope or verification fails.
- The SHA-256 digest inside the envelope ensures payload immutability.
- Timestamp and nonce reduce replay risk; consider persistence or windowing in production.

## Contact
- For questions or access, email: soumodeepguha22@gmail.com

## Compliance
- NIST PQC-aligned (ML-DSA/Dilithium via `oqs` when available); treat as experimental unless using validated modules.
- For government use, operate only with FIPS 140-3 validated crypto modules and approved algorithms in FIPS mode.
- SBOM and CI checks available; see [docs/COMPLIANCE.md](docs/COMPLIANCE.md) and [SECURITY_POLICY.md](SECURITY_POLICY.md).

## Regional Readiness
- EU (GDPR/NIS2), USA (FIPS 140-3/NIST/FedRAMP), Canada (PIPEDA/CyberSecure), Australia (ASD Essential Eight/ISM).
- Details and guidance in [docs/REGIONAL_READINESS.md](docs/REGIONAL_READINESS.md).

## Regional Deployment (UK, Ireland, EU)
- See [docs/DEPLOY_EU.md](docs/DEPLOY_EU.md) for step-by-step commands for AWS (eu-west-1/eu-west-2/eu-central-1), Azure (westeurope/northeurope/uksouth), and GCP (europe-west*).

## Project Separation
- Janus_PQC is independent and not affiliated with any other project.
- Do not mix code, configurations, or releases with Crypto-Shield.
- This repository stands alone for PQC verification work.

## Global Deployment
- Worldwide guidance for AWS, Azure, and GCP in [docs/DEPLOY_GLOBAL.md](docs/DEPLOY_GLOBAL.md), including US, Canada, APAC, and EU regions.

## License
- Proprietary — All Rights Reserved. See [LICENSE](LICENSE).
- Usage is subject to the [Acceptable Use Policy](ACCEPTABLE_USE_POLICY.md).

## Releases
- Tagged releases (`v*`) publish signed artifacts via GitHub Actions.
- Artifacts include: `sbom.json` (signed), `checksums.txt` (signed), and a source zip.
- How to create a release:
  - Tag locally and push:
    - `git tag -a v0.1.0 -m "Initial release"`
    - `git push origin v0.1.0`
  - The workflow in [.github/workflows/release.yml](.github/workflows/release.yml) will build and attach artifacts.

## Real-World Validation
- Environment: Windows 11, Python 3.14.2.
- Runtime output (local execution):
  ```
  [NOTICE] Use restricted. See LICENSE and ACCEPTABLE_USE_POLICY.md.
  [SUCCESS] Data Integrity Verified: System is Quantum-Safe and Uncompromisable.
  ```
- Tests: `All Janus_PQC black-box tests passed.`
- SBOM: Generated in CI for releases; local generation via `requirements-dev.txt` and `tools/generate_sbom.py`.
