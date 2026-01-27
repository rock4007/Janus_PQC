# Janus PQC Overview

Janus provides hybrid signatures over a tamper-evident envelope combining Ed25519 and ML-DSA-65 (via oqs when available). It falls back to Ed448 on platforms without oqs, ensuring portability.
