# Janus Security Design

- Tamper-Evident Envelope: `version`, `algo`, `ts`, `nonce`, `msg_sha256` signed by both algorithms.
- Dual Verification: Both signatures must verify the same envelope; mismatch fails.
- OQS Adapter: Uses ML-DSA-65 when available; Ed448 fallback otherwise.
- Defense-in-Depth: Timestamp + nonce limits replay; SHA-256 binds signature to the exact payload.
