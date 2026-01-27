# Deploy on iOS (Guidance)

Janus_PQC is a Python prototype. iOS cannot run Docker containers and Python packaging on iOS is limited. For production-grade iOS apps, implement verification in Swift using native crypto (CryptoKit) and optionally integrate post-quantum libraries (liboqs) compiled for iOS.

## Approach A: Swift Client (CryptoKit) for Envelope Verification
- Use Swift + CryptoKit to verify the Ed25519 signature over the canonical envelope JSON.
- Ed448 fallback is not available in CryptoKit; rely on Ed25519 for classical verification.
- PQC (ML-DSA/Dilithium) is not available natively; see Approach B for liboqs.

### Steps
1) Create a Swift Package/App (Xcode) targeting iOS.
2) Define the envelope struct matching Janus_PQC fields: `version`, `algo`, `ts`, `nonce`, `msg_sha256`, and the signatures.
3) Compute SHA-256 over the `msg` payload and compare against `msg_sha256`.
4) Verify the Ed25519 signature with CryptoKit using the serialized envelope bytes.

### Sample Skeleton (Swift)
```swift
import Foundation
import CryptoKit

struct Envelope: Codable {
    let version: String
    let algo: String
    let ts: String
    let nonce: String
    let msg_sha256: String
    let sig_ed25519: String // base64 or hex
    // let sig_pq: String // optional (Approach B)
}

func verifyEd25519(envelope: Envelope, message: Data, publicKeyData: Data) -> Bool {
    // Check message hash
    let digest = SHA256.hash(data: message)
    let msgHashHex = digest.map { String(format: "%02x", $0) }.joined()
    guard msgHashHex == envelope.msg_sha256 else { return false }

    // Serialize canonical envelope (without signatures) as bytes
    // Ensure stable ordering when encoding; use a canonical JSON encoder.
    let encoder = JSONEncoder()
    encoder.outputFormatting = [.sortedKeys]
    guard let envelopeBytes = try? encoder.encode(envelope) else { return false }

    // Verify Ed25519 signature
    guard let signatureData = Data(hexString: envelope.sig_ed25519) else { return false }
    let publicKey = try! Curve25519.Signing.PublicKey(rawRepresentation: publicKeyData)
    return publicKey.isValidSignature(signatureData, for: envelopeBytes)
}
```
Note: Implement `Data(hexString:)` or use base64. Maintain canonical encoding consistent with the server.

## Approach B: PQC via liboqs (Advanced)
- Compile `liboqs` for iOS (arm64) and expose C functions via a Swift bridging header.
- Use ML-DSA/Dilithium for the PQ signature; verify alongside Ed25519.

### High-Level Steps
1) Build liboqs for iOS:
```
# On macOS with Xcode toolchain
# Clone liboqs; configure CMake for iOS arm64; build static library
cmake -S . -B build-ios -DCMAKE_SYSTEM_NAME=iOS -DCMAKE_OSX_ARCHITECTURES=arm64 -DBUILD_SHARED_LIBS=OFF
cmake --build build-ios --config Release
```
2) Add the resulting `liboqs.a` and headers to your Xcode project.
3) Create a Swift wrapper using a bridging header to call verification functions.
4) Verify the PQ signature over the same canonical envelope bytes.

## Alternative: Python on iOS (Prototype Only)
- Frameworks like BeeWare/Briefcase or Pyto can embed Python, but `cryptography` and compiled extensions may not be supported.
- Not recommended for production; use Swift native crypto for iOS apps.

## Operational Notes
- Keep iOS verification stateless; do not store private keys in the app.
- Fetch public keys and envelope payloads securely from your backend.
- Use UTC timestamps and nonce to mitigate replay; enforce server-side windowing.

## Compliance
- Apple platform security requires App Sandbox policies.
- PQC support on iOS requires third-party libraries; ensure license compatibility and performance testing.
