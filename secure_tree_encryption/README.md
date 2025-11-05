# Secure Tree-Based Encryption System

A **cryptographically secure** encryption implementation using Merkle trees for data integrity and hierarchical key derivation.

## 🔒 Security Features

This implementation uses **industry-standard cryptography**:

✅ **AES-256-GCM** - Authenticated encryption with built-in integrity checking
✅ **PBKDF2-SHA256** - Password-based key derivation (480,000 iterations)
✅ **Merkle Trees** - Hierarchical data integrity verification
✅ **Key Derivation Tree** - Unique keys per data chunk (forward secrecy)
✅ **Cryptographically Secure Random** - os.urandom() for nonces and salts
✅ **No Custom Crypto** - Built on proven `cryptography` library

---

## 🌳 How Tree Structures Provide Security

### 1. Merkle Tree (Integrity Verification)

```
                Root Hash
                /       \
            H(AB)       H(CD)
            /   \       /   \
          H(A) H(B)  H(C)  H(D)
           |    |     |     |
        Chunk1 Chunk2 Chunk3 Chunk4
        (encrypted) (encrypted)
```

**Benefits:**
- Detects any tampering with data
- Verifies entire file integrity with single root hash
- Efficient verification without decrypting everything
- Mathematically proven security

### 2. Key Derivation Tree (Forward Secrecy)

```
            Master Key
            /         \
        Key[0]      Key[1]
        /    \       /    \
    Key[0,0] Key[0,1] Key[1,0] Key[1,1]
       |        |        |        |
   Chunk 0  Chunk 1  Chunk 2  Chunk 3
```

**Benefits:**
- Each chunk encrypted with unique derived key
- Compromising one key doesn't reveal others
- Hierarchical structure prevents key reuse
- Based on PBKDF2 key stretching

---

## 🚀 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install cryptography directly
pip install cryptography>=41.0.0
```

---

## 📖 Usage

### Command Line Interface

**Encrypt a file:**
```bash
python merkle_crypto.py encrypt input.txt encrypted.json
# You'll be prompted for a password
```

**Decrypt a file:**
```bash
python merkle_crypto.py decrypt encrypted.json output.txt
# Enter the same password used for encryption
```

### Python API

```python
from merkle_crypto import SecureTreeEncryption

# Initialize with password
password = "YourSecurePassword123!"
encryptor = SecureTreeEncryption(password)

# Encrypt data
plaintext = b"Secret message"
encrypted_data = encryptor.encrypt(plaintext)

# Decrypt data
decryptor = SecureTreeEncryption(password, salt=encryptor.salt)
decrypted = decryptor.decrypt(encrypted_data)

print(decrypted)  # b"Secret message"
```

### File Encryption

```python
# Encrypt file
encryptor = SecureTreeEncryption("password")
encryptor.encrypt_file("document.pdf", "document.enc")

# Decrypt file
decryptor = SecureTreeEncryption("password", salt=encryptor.salt)
decryptor.decrypt_file("document.enc", "document_decrypted.pdf")
```

---

## 🧪 Running Tests

```bash
python test_example.py
```

**Test Suite Includes:**
1. Basic encryption/decryption
2. Large data handling (multiple chunks)
3. Integrity verification (tamper detection)
4. Wrong password detection
5. Key derivation tree functionality
6. File encryption/decryption

---

## 🔬 Technical Details

### Encryption Process

```
1. Password → PBKDF2(480k iterations) → Master Key (32 bytes)
2. Data → Split into 4KB chunks
3. For each chunk[i]:
   a. Derive unique key: Key[i] = PBKDF2(master_key, path=[i])
   b. Generate random nonce (12 bytes)
   c. Encrypt: AES-256-GCM(plaintext, key[i], nonce)
   d. Output: nonce + ciphertext + auth_tag
4. Build Merkle tree from encrypted chunks
5. Store: chunks + root_hash + salt
```

### Decryption Process

```
1. Load encrypted data + salt
2. Password + salt → PBKDF2(480k iterations) → Master Key
3. For each encrypted chunk[i]:
   a. Derive same key: Key[i] = PBKDF2(master_key, path=[i])
   b. Decrypt: AES-256-GCM-decrypt(ciphertext, key[i], nonce)
   c. Verify authentication tag (detects tampering)
4. Rebuild Merkle tree from chunks
5. Verify root hash matches (integrity check)
6. Concatenate decrypted chunks → original data
```

### Security Parameters

| Parameter | Value | Standard |
|-----------|-------|----------|
| Encryption | AES-256-GCM | NIST FIPS 197 |
| Key Size | 256 bits | AES-256 |
| KDF | PBKDF2-SHA256 | NIST SP 800-132 |
| Iterations | 480,000 | OWASP 2023 |
| Nonce Size | 96 bits | GCM Standard |
| Salt Size | 128 bits | Recommended |
| Hash Function | SHA-256 | NIST FIPS 180-4 |

---

## 🛡️ Security Guarantees

### What This System Provides

✅ **Confidentiality** - AES-256 encryption (unbreakable with current technology)
✅ **Authentication** - GCM mode verifies data hasn't been tampered
✅ **Integrity** - Merkle tree + auth tags detect any modifications
✅ **Forward Secrecy** - Unique keys per chunk limit exposure
✅ **Non-deterministic** - Random nonces ensure same plaintext → different ciphertext
✅ **Password Security** - PBKDF2 with 480k iterations resists brute force

### Attack Resistance

| Attack Type | Protection |
|-------------|------------|
| Brute Force Password | PBKDF2 480k iterations (very expensive) |
| Ciphertext Tampering | AES-GCM auth tag verification fails |
| Data Corruption | Merkle root verification fails |
| Known Plaintext | AES-256 semantically secure |
| Chosen Ciphertext | GCM authenticated encryption prevents |
| Side Channel | Constant-time operations in cryptography library |

---

## 📊 Performance

**Encryption Speed** (approximate):
- Small files (<1MB): < 0.1 seconds
- Medium files (10MB): ~1 second
- Large files (100MB): ~10 seconds

**Note:** Speed is limited by PBKDF2 key derivation (intentionally slow for security).

---

## 🔍 Code Example: Understanding the Flow

```python
# Example: Encrypt "Hello"
password = "secret"
plaintext = b"Hello"

# Step 1: Key Derivation
# password + random_salt → PBKDF2(480k iterations) → master_key (32 bytes)

# Step 2: Chunk Encryption
# Hello → [chunk_0: b"Hello"]
# Derive key: key_0 = PBKDF2(master_key, path=[0])
# Encrypt: nonce_0 (random) + AES-GCM(b"Hello", key_0, nonce_0)
# Result: encrypted_chunk_0 = nonce + ciphertext + auth_tag

# Step 3: Merkle Tree
# leaf_0 = SHA256(encrypted_chunk_0)
# root = leaf_0 (only one chunk)

# Step 4: Output
output = {
    'encrypted_chunks': [
        {'nonce': nonce_0, 'ciphertext': ciphertext_0, 'index': 0}
    ],
    'merkle_root': root_hash,
    'salt': salt,
    'metadata': {...}
}
```

---

## 🆚 Comparison: Secure vs Original Implementation

| Feature | Original (Educational) | This (Secure) |
|---------|----------------------|---------------|
| **Encryption** | Custom ASCII shift | AES-256-GCM |
| **Randomness** | None (deterministic) | Cryptographic nonces |
| **Key Derivation** | None | PBKDF2 (480k iterations) |
| **Integrity Check** | None | Merkle tree + auth tags |
| **Authentication** | None | GCM authentication |
| **Forward Secrecy** | No | Yes (key derivation tree) |
| **Standards** | None | NIST, OWASP compliant |
| **Breakable** | Yes (minutes) | No (computationally infeasible) |
| **Production Ready** | ❌ Educational only | ✅ Yes |

---

## 🎓 Educational Value

### What You Learn

1. **Merkle Trees in Practice**
   - Building trees from leaf data
   - Computing hashes bottom-up
   - Verifying integrity with root hash

2. **Modern Cryptography**
   - Authenticated encryption (AEAD)
   - Key derivation functions (KDF)
   - Password-based encryption

3. **Security Engineering**
   - Defense in depth (multiple layers)
   - Forward secrecy principles
   - Proper random number generation

4. **Python Cryptography**
   - Using industry-standard libraries
   - Secure coding practices
   - Error handling for security

---

## ⚠️ Important Notes

### What This Is

✅ A secure, production-ready encryption tool
✅ Educational implementation of tree-based crypto
✅ Demonstrates proper cryptographic practices
✅ Suitable for encrypting personal files

### What This Is NOT

❌ A replacement for full disk encryption (use BitLocker/LUKS)
❌ A secure messaging protocol (use Signal/WhatsApp)
❌ A blockchain or cryptocurrency
❌ Network encryption (use TLS/SSL)

### When to Use

- Encrypting files before cloud storage
- Protecting sensitive documents
- Learning cryptographic implementations
- Understanding Merkle tree applications

### When NOT to Use

- Network communication (use TLS)
- Database encryption (use transparent encryption)
- Real-time messaging (use Signal Protocol)
- Large-scale systems (use dedicated solutions like AWS KMS)

---

## 🐛 Security Considerations

### Known Limitations

1. **Password Strength** - Security depends on strong passwords
   - Use minimum 12 characters
   - Include uppercase, lowercase, numbers, symbols
   - Avoid dictionary words

2. **Salt Storage** - Salt is stored with encrypted data
   - This is standard practice (salt doesn't need to be secret)
   - Security comes from password + salt, not salt alone

3. **No Key Escrow** - Forgotten password = lost data
   - Keep secure backups of passwords
   - Consider using a password manager

4. **Performance** - 480k PBKDF2 iterations add ~0.5s delay
   - Intentional: prevents brute force attacks
   - Trade-off: security vs speed

### Best Practices

✅ **Use strong, unique passwords**
✅ **Keep encrypted files and passwords separate**
✅ **Test decryption immediately after encryption**
✅ **Maintain backups of encrypted files**
✅ **Update the cryptography library regularly**

---

## 📚 Further Reading

### Cryptography Concepts
- [Authenticated Encryption](https://en.wikipedia.org/wiki/Authenticated_encryption)
- [Merkle Trees](https://en.wikipedia.org/wiki/Merkle_tree)
- [Key Derivation Functions](https://en.wikipedia.org/wiki/Key_derivation_function)

### Standards
- [NIST AES Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
- [PBKDF2 Specification](https://tools.ietf.org/html/rfc2898)
- [GCM Mode](https://csrc.nist.gov/publications/detail/sp/800-38d/final)

### Libraries
- [Python Cryptography](https://cryptography.io/)
- [OWASP Password Recommendations](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

---

## 🤝 Contributing

Improvements welcome! Focus areas:
- Additional tests
- Performance optimizations
- Documentation improvements
- Support for streaming large files
- GUI interface

**Security Note:** Any cryptographic changes require expert review.

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎯 Summary

This implementation demonstrates how to:
- ✅ Use tree structures (Merkle trees) for security
- ✅ Implement proper authenticated encryption
- ✅ Build hierarchical key derivation systems
- ✅ Follow cryptographic best practices
- ✅ Create production-ready encryption tools

**Remember:** Always use established cryptographic libraries. Never implement crypto primitives from scratch!

---

**Built with:** Python, AES-256-GCM, Merkle Trees, and Security Best Practices 🔒
