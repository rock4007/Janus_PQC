#!/usr/bin/env python3
"""
Janus PQC CLI
- Generates keys, signs a payload, verifies, and prints status
"""
from janus_core import GlobalSecurityCore

def main():
    security = GlobalSecurityCore()
    payload = b"JANUS_PQC_DEMO_PAYLOAD"
    (c_priv, c_pub), (pq_priv, pq_pub) = security.create_secure_keys()
    envelope, sig_c, sig_pq = security.sign_transmission(payload, c_priv, pq_priv)
    ok = security.verify_integrity(payload, envelope, sig_c, sig_pq, c_pub, pq_pub)
    print("OQS available:", getattr(security.PQSignatureAdapter, "_mode", None))
    print("Verification:", "SUCCESS" if ok else "FAILED")

if __name__ == "__main__":
    main()
