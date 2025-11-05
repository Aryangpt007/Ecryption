# Architecture Overview

## System Design

This document explains the architecture of the Secure Tree-Based Encryption system.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Input                          │
│              (Password + Plaintext/File)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Key Derivation Layer                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Password + Salt → PBKDF2(480k iter) → Master Key    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Processing Layer                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Plaintext → Split into 4KB chunks                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│            Hierarchical Key Derivation Tree                 │
│                                                             │
│              Master Key                                     │
│              /         \                                    │
│          Key[0]      Key[1]      ...                        │
│          /    \       /    \                                │
│      Key[0,0] ...  Key[1,0] ...                            │
│                                                             │
│  Each chunk gets unique derived key                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Encryption Layer                          │
│                                                             │
│  For each chunk[i]:                                         │
│    1. Generate random nonce (12 bytes)                      │
│    2. Encrypt: AES-256-GCM(chunk, key[i], nonce)           │
│    3. Output: nonce + ciphertext + auth_tag (16 bytes)     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Merkle Tree Layer                          │
│                                                             │
│                   Root Hash                                 │
│                  /          \                               │
│            H(c0+c1)      H(c2+c3)                          │
│            /    \         /    \                            │
│         H(c0)  H(c1)  H(c2)  H(c3)                         │
│          |      |      |      |                             │
│       chunk0  chunk1  chunk2  chunk3                       │
│     (encrypted)                                             │
│                                                             │
│  Provides integrity verification                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      Output Layer                           │
│                                                             │
│  {                                                          │
│    encrypted_chunks: [...]                                  │
│    merkle_root: "..."                                       │
│    salt: "..."                                              │
│    metadata: {...}                                          │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. SecureTreeEncryption (Main Class)

**Responsibilities:**
- Orchestrate entire encryption/decryption process
- Manage master key derivation
- Handle file I/O operations
- Coordinate between subcomponents

**Key Methods:**
- `encrypt(plaintext)` → encrypted_data
- `decrypt(encrypted_data)` → plaintext
- `encrypt_file(in, out)` → void
- `decrypt_file(in, out)` → void

---

### 2. KeyDerivationTree

**Responsibilities:**
- Derive unique keys for each data chunk
- Implement hierarchical key structure
- Provide forward secrecy

**Algorithm:**
```python
def derive_key(path: [int]) -> bytes:
    # path example: [0], [1], [0,0], [0,1], etc.
    path_bytes = json.dumps(path).encode()
    return PBKDF2(master_key, salt=path_bytes, iterations=100k)
```

**Benefits:**
- Each chunk has unique key
- Compromising one key doesn't reveal others
- Hierarchical structure allows nested encryption

---

### 3. MerkleNode & Merkle Tree

**Responsibilities:**
- Organize encrypted chunks into tree structure
- Calculate hashes for integrity verification
- Provide efficient tamper detection

**Structure:**
```python
class MerkleNode:
    data: Optional[bytes]  # Encrypted chunk (leaf only)
    left: Optional[MerkleNode]
    right: Optional[MerkleNode]
    hash: bytes  # SHA-256 hash
```

**Hash Calculation:**
- Leaf: `hash = SHA256(encrypted_chunk)`
- Internal: `hash = SHA256(left.hash + right.hash)`

---

## Data Flow

### Encryption Flow

```
1. Input Processing
   └─> Password → PBKDF2(480k) → Master Key (32 bytes)
   └─> Plaintext → Split into chunks (4KB each)

2. Chunk Encryption
   For chunk[i]:
   ├─> Derive key[i] from master key + path[i]
   ├─> Generate random nonce (12 bytes)
   ├─> AES-256-GCM encrypt
   └─> Output: nonce || ciphertext || tag

3. Integrity Protection
   ├─> Build Merkle tree from encrypted chunks
   ├─> Calculate root hash
   └─> Store root hash with encrypted data

4. Output
   └─> JSON with: chunks + root_hash + salt + metadata
```

### Decryption Flow

```
1. Input Validation
   ├─> Load encrypted data (JSON)
   ├─> Extract salt
   └─> Verify version compatibility

2. Key Derivation
   └─> Password + Salt → PBKDF2(480k) → Master Key

3. Chunk Decryption
   For chunk[i]:
   ├─> Derive same key[i] from master key + path[i]
   ├─> AES-256-GCM decrypt with nonce
   ├─> Verify authentication tag
   └─> Output: plaintext chunk

4. Integrity Verification
   ├─> Rebuild Merkle tree from encrypted chunks
   ├─> Compare computed root vs stored root
   └─> Fail if mismatch (data tampered)

5. Output
   └─> Concatenate decrypted chunks → plaintext
```

---

## Security Layers

### Layer 1: Password Security
```
Password (user input)
    ↓
PBKDF2-SHA256 (480,000 iterations)
    ↓
Master Key (32 bytes)
```
**Protects against:** Brute force, dictionary attacks

### Layer 2: Key Derivation
```
Master Key + Path[i]
    ↓
PBKDF2-SHA256 (100,000 iterations)
    ↓
Chunk Key[i] (32 bytes, unique per chunk)
```
**Protects against:** Key reuse, forward secrecy violations

### Layer 3: Authenticated Encryption
```
Plaintext + Key + Nonce (random)
    ↓
AES-256-GCM
    ↓
Ciphertext + Authentication Tag
```
**Protects against:** Eavesdropping, tampering, forgery

### Layer 4: Integrity Verification
```
Encrypted Chunks
    ↓
Merkle Tree Construction
    ↓
Root Hash
```
**Protects against:** Data corruption, chunk reordering, deletion

---

## Cryptographic Primitives

### AES-256-GCM

**Mode:** Galois/Counter Mode (authenticated encryption)
**Key Size:** 256 bits
**Nonce Size:** 96 bits (12 bytes)
**Tag Size:** 128 bits (16 bytes)

**Properties:**
- Confidentiality: Encrypts data
- Authentication: Verifies data integrity
- Efficiency: Hardware acceleration available
- Security: Semantically secure

### PBKDF2-SHA256

**Purpose:** Key derivation from password
**Hash:** SHA-256
**Iterations:** 480,000 (master) / 100,000 (chunks)
**Salt Size:** 128 bits (16 bytes)

**Properties:**
- Slow computation (intentional)
- Unique keys per salt
- Prevents rainbow tables
- Resists brute force

### SHA-256

**Purpose:** Merkle tree hashing
**Output:** 256 bits (32 bytes)
**Properties:**
- Collision resistant
- Pre-image resistant
- Fast computation
- Widely standardized

---

## File Format

### Encrypted File Structure (JSON)

```json
{
  "version": "1.0",
  "encrypted_chunks": [
    {
      "index": 0,
      "nonce": "base64_encoded_nonce",
      "ciphertext": "base64_encoded_ciphertext_and_tag"
    },
    ...
  ],
  "merkle_root": "base64_encoded_root_hash",
  "salt": "base64_encoded_salt",
  "chunk_size": 4096,
  "num_chunks": 5,
  "metadata": {
    "algorithm": "AES-256-GCM",
    "kdf": "PBKDF2-SHA256",
    "iterations": 480000,
    "tree_type": "Merkle"
  }
}
```

**Why JSON?**
- Human readable (for education)
- Easy to parse
- Cross-platform compatible
- Includes metadata

**Production alternatives:**
- Binary format (more efficient)
- Protocol Buffers
- MessagePack

---

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Key Derivation | O(iterations) | ~0.5s for 480k iterations |
| Chunk Encryption | O(n) | Linear in data size |
| Merkle Tree Build | O(n) | n = number of chunks |
| Merkle Tree Verify | O(n) | Full tree reconstruction |

### Space Complexity

| Component | Space | Notes |
|-----------|-------|-------|
| Encrypted Data | ~n + overhead | n = plaintext size |
| Overhead | ~50 bytes/chunk | Nonce + tag + metadata |
| Merkle Tree | O(n chunks) | Stored as root hash only |

### Bottlenecks

1. **PBKDF2 iterations** - Intentionally slow for security
2. **AES operations** - Fast with hardware acceleration
3. **File I/O** - Can be significant for large files

---

## Threat Model

### What We Protect Against

✅ **Eavesdropping** - Data is encrypted with AES-256
✅ **Tampering** - GCM auth tags + Merkle root detect changes
✅ **Password Guessing** - PBKDF2 iterations make it expensive
✅ **Data Corruption** - Merkle tree verifies all chunks
✅ **Partial Decryption** - Each chunk authenticated separately

### What We Don't Protect Against

❌ **Side-channel attacks** - Timing attacks may reveal info
❌ **Malware on system** - Can steal keys from memory
❌ **Weak passwords** - Still vulnerable to brute force
❌ **Social engineering** - Attacker tricks user for password
❌ **Quantum computers** - AES-256 reduced to ~128-bit security

---

## Future Enhancements

### Potential Improvements

1. **Post-Quantum Cryptography**
   - Add Kyber/Dilithium for quantum resistance

2. **Streaming Encryption**
   - Process large files without loading entirely

3. **Parallel Processing**
   - Encrypt/decrypt chunks in parallel

4. **Compression**
   - Add optional compression before encryption

5. **Key Rotation**
   - Support for re-encryption with new key

6. **Metadata Encryption**
   - Encrypt filename, size, timestamps

---

## References

- [NIST AES](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
- [GCM Mode](https://csrc.nist.gov/publications/detail/sp/800-38d/final)
- [PBKDF2 RFC](https://tools.ietf.org/html/rfc2898)
- [Merkle Trees](https://en.wikipedia.org/wiki/Merkle_tree)
- [Python Cryptography](https://cryptography.io/)

---

**Document Version:** 1.0
**Last Updated:** 2025-01-05
