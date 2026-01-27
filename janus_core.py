"""
Janus PQC Core Module
- Exposes GlobalSecurityCore for import by CLI and tests
- Uses oqs when available; falls back to Ed448 otherwise
"""
try:
    import oqs
    OQS_AVAILABLE = True
except Exception:
    oqs = None
    OQS_AVAILABLE = False

from cryptography.hazmat.primitives.asymmetric import ed25519, ed448
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
import hashlib
import secrets
import time
from typing import Tuple

class GlobalSecurityCore:
    def __init__(self):
        self.pq_algorithm = "ML-DSA-65"

    class PQSignatureAdapter:
        def __init__(self, algorithm: str):
            self.algorithm = algorithm
            self.secret_key = None
            self._mode = "oqs" if OQS_AVAILABLE else "fallback"
            self._oqs_sig = oqs.Signature(algorithm) if OQS_AVAILABLE else None
            self._priv_obj = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self._oqs_sig is not None:
                try:
                    self._oqs_sig.close()
                except Exception:
                    pass

        def generate_keypair(self):
            if self._mode == "oqs":
                pub = self._oqs_sig.generate_keypair()
                try:
                    self._cached_secret = self._oqs_sig.export_secret_key()
                except Exception:
                    self._cached_secret = None
                return pub
            else:
                priv = ed448.Ed448PrivateKey.generate()
                pub = priv.public_key()
                self._priv_obj = priv
                self._cached_secret = priv.private_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PrivateFormat.Raw,
                    encryption_algorithm=serialization.NoEncryption()
                )
                pub_bytes = pub.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw
                )
                return pub_bytes

        def export_secret_key(self):
            if self._mode == "oqs":
                return self._oqs_sig.export_secret_key()
            return self._cached_secret

        def sign(self, message: bytes) -> bytes:
            if self._mode == "oqs":
                if self.secret_key is not None:
                    try:
                        self._oqs_sig.secret_key = self.secret_key
                    except Exception:
                        pass
                return self._oqs_sig.sign(message)
            else:
                priv = ed448.Ed448PrivateKey.from_private_bytes(self.secret_key or self._cached_secret)
                return priv.sign(message)

        def verify(self, message: bytes, signature: bytes, public_key_bytes: bytes) -> bool:
            if self._mode == "oqs":
                return self._oqs_sig.verify(message, signature, public_key_bytes)
            else:
                try:
                    pub = ed448.Ed448PublicKey.from_public_bytes(public_key_bytes)
                    pub.verify(signature, message)
                    return True
                except InvalidSignature:
                    return False

    def create_secure_keys(self) -> Tuple[Tuple[ed25519.Ed25519PrivateKey, ed25519.Ed25519PublicKey], Tuple[bytes, bytes]]:
        classic_priv = ed25519.Ed25519PrivateKey.generate()
        classic_pub = classic_priv.public_key()
        with self.PQSignatureAdapter(self.pq_algorithm) as pq_signer:
            pq_public_key = pq_signer.generate_keypair()
            pq_private_key = pq_signer.export_secret_key()
        return (classic_priv, classic_pub), (pq_private_key, pq_public_key)

    def _build_envelope(self, message: bytes) -> bytes:
        digest = hashlib.sha256(message).hexdigest()
        envelope = {
            "version": "1.0",
            "algo": f"Ed25519+{self.pq_algorithm}",
            "ts": int(time.time()),
            "nonce": secrets.token_hex(16),
            "msg_sha256": digest,
        }
        import json
        return json.dumps(envelope, separators=(",", ":"), sort_keys=True).encode("utf-8")

    def sign_transmission(self, message: bytes, c_priv: ed25519.Ed25519PrivateKey, pq_priv: bytes):
        envelope = self._build_envelope(message)
        sig_classic = c_priv.sign(envelope)
        with self.PQSignatureAdapter(self.pq_algorithm) as pq_signer:
            pq_signer.secret_key = pq_priv
            sig_pq = pq_signer.sign(envelope)
        return envelope, sig_classic, sig_pq

    def verify_integrity(self, message: bytes, envelope: bytes, sig_c: bytes, sig_pq: bytes, pub_c: ed25519.Ed25519PublicKey, pub_pq: bytes) -> bool:
        import json
        try:
            env = json.loads(envelope.decode("utf-8"))
            expected_digest = hashlib.sha256(message).hexdigest()
            if env.get("msg_sha256") != expected_digest:
                return False
        except Exception:
            return False
        try:
            pub_c.verify(sig_c, envelope)
            classical_valid = True
        except InvalidSignature:
            classical_valid = False
        with self.PQSignatureAdapter(self.pq_algorithm) as pq_verifier:
            pq_valid = pq_verifier.verify(envelope, sig_pq, pub_pq)
        return classical_valid and pq_valid
