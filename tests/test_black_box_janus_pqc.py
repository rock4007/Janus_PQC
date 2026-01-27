import os
import random
from janus_core import GlobalSecurityCore

def test_many_random_messages(n=50):
    security = GlobalSecurityCore()
    for _ in range(n):
        msg = os.urandom(random.randint(16, 256))
        (c_priv, c_pub), (pq_priv, pq_pub) = security.create_secure_keys()
        envelope, sig_c, sig_pq = security.sign_transmission(msg, c_priv, pq_priv)
        assert security.verify_integrity(msg, envelope, sig_c, sig_pq, c_pub, pq_pub)

def test_tamper_detection():
    security = GlobalSecurityCore()
    msg = b"HELLO_WORLD"
    (c_priv, c_pub), (pq_priv, pq_pub) = security.create_secure_keys()
    envelope, sig_c, sig_pq = security.sign_transmission(msg, c_priv, pq_priv)
    # Tamper with message
    tampered_msg = b"HELLO_WORLD!"
    assert not security.verify_integrity(tampered_msg, envelope, sig_c, sig_pq, c_pub, pq_pub)
