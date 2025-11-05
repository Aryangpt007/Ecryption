# Advanced Tree & Data Structure Based Encryption

An educational implementation demonstrating how **tree and graph data structures** can be used to create encryption through **permutations, substitutions, and diffusion** - without relying on standard encryption algorithms like AES.

## ⚠️ EDUCATIONAL PURPOSE ONLY

**This is a sophisticated educational project** showing advanced data structure applications in cryptography. However:

❌ **NOT cryptographically secure for production use**
❌ **Custom algorithms cannot match proven standards**
✅ **Excellent for learning data structures**
✅ **Demonstrates cryptographic principles**

For real security, use AES, ChaCha20, or other standardized algorithms.

---

## 🎓 What Makes This Advanced?

Unlike the original simple implementation, this uses:

### **Multiple Tree Types**
- **AVL Trees** → Self-balancing for consistent permutations
- **Splay Trees** → Dynamic restructuring based on access patterns
- **Complete Binary Trees** → Diffusion layer mixing

### **Sophisticated Techniques**
- **8-round Feistel-like network** (similar to DES/AES structure)
- **Tree-based S-boxes** (substitution boxes from AVL trees)
- **Key-dependent permutations** (splay tree transformations)
- **Diffusion layer** (tree-based mixing for avalanche effect)
- **CBC mode** (Cipher Block Chaining for blocks)

### **Real Cryptographic Principles**
- **Confusion** → S-boxes hide plaintext-ciphertext relationship
- **Diffusion** → Each bit affects many others
- **Key scheduling** → Different keys per round
- **Multiple rounds** → Increases security exponentially

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   PLAINTEXT                         │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │ Split into 64-byte  │
         │      blocks         │
         └──────────┬──────────┘
                    │
        ┌───────────▼──────────┐
        │   CBC Chaining       │ (XOR with prev block)
        └───────────┬──────────┘
                    │
    ┌───────────────▼────────────────┐
    │      8-ROUND ENCRYPTION        │
    │                                │
    │  Round 1:                      │
    │    1. AVL Tree S-box           │ ← Substitution
    │    2. Splay Tree Permutation   │ ← Permutation
    │    3. XOR with Round Key       │ ← Key Mixing
    │    4. Tree Diffusion           │ ← Diffusion
    │                                │
    │  Round 2-8: (repeat)           │
    │                                │
    └───────────────┬────────────────┘
                    │
                    ▼
          ┌─────────────────┐
          │   CIPHERTEXT    │
          └─────────────────┘
```

---

## 🌳 How Trees Provide Encryption

### 1. AVL Tree → S-Box Generation

```python
# Create permutation from balanced tree

Key = "secret"  →  Seed: 12345
                    ↓
        Shuffled insertion: [42, 7, 99, 15, ...]
                    ↓
            Build AVL Tree:
                   42
                  /  \
                7     99
                     /
                   15
                    ↓
        Inorder traversal: [7, 42, 15, 99, ...]
                    ↓
            S-Box permutation!
```

**Why AVL?**
- Self-balancing ensures same structure for same key
- Different keys → different tree structures
- Inorder traversal creates permutation
- 256 values → 256! possible permutations

### 2. Splay Tree → Dynamic Permutation

```python
# Access pattern creates permutation

Values: [10, 20, 30, 40]  with Key-based access order
                    ↓
         Each insert splays to root
                    ↓
            Final structure depends on:
            - Insertion order (from key)
            - Splay operations (rotations)
                    ↓
            Inorder gives permuted output
```

**Why Splay?**
- Recently accessed moves to root (key-dependent)
- Rotations create complex transformations
- No two keys produce same structure
- Self-adjusting property adds confusion

### 3. Complete Binary Tree → Diffusion

```python
# Parent-child mixing spreads bits

Array: [A, B, C, D, E, F, G]
              ↓
        Tree structure:
              A
            /   \
           B     C
          / \   / \
         D   E F   G
              ↓
    Mix: A = A + B + C
         B = B + D + E
         C = C + F + G
              ↓
    One bit change affects entire tree!
```

**Why Tree Mixing?**
- Parent influenced by all descendants
- Siblings affect each other
- Creates avalanche effect
- O(n) complexity, efficient

---

## 🔧 How It Works

### Encryption Process

```
1. PASSWORD → SHA-256 → Key Schedule
   └─> 8 round keys generated

2. PLAINTEXT → Pad to 64-byte blocks
   └─> Split: [Block0, Block1, ...]

3. FOR EACH BLOCK:

   CBC Chaining:
   └─> Block ⊕ Previous Ciphertext

   Round 1:
   ├─> Substitution (AVL S-box)
   ├─> Permutation (Splay tree)
   ├─> XOR (Round key)
   └─> Diffusion (Tree mixing)

   Rounds 2-8: (repeat)

4. OUTPUT: Encrypted blocks
```

### Decryption Process

```
1. Load encrypted blocks + IV

2. FOR EACH BLOCK (reverse order):

   Reverse Round 8:
   ├─> Reverse diffusion
   ├─> XOR (Round key 8)
   ├─> Reverse permutation
   └─> Reverse substitution (Inverse S-box)

   Reverse Rounds 7-1: (repeat)

   CBC Unchaining:
   └─> Result ⊕ Previous Ciphertext

3. Remove padding → PLAINTEXT
```

---

## 📊 Components Explained

### AVLTree Class

**Purpose:** Generate key-dependent substitution boxes

**Methods:**
- `insert(value, data)` - Insert with auto-balancing
- `inorder(node)` - Extract permutation
- `_rotate_left/right()` - Balance operations

**Security Role:** Creates 256-byte permutation table

### SplayTree Class

**Purpose:** Create dynamic, key-dependent permutations

**Methods:**
- `insert(value, data)` - Insert and splay to root
- `_splay(root, value)` - Perform rotations
- `inorder(node)` - Extract permutation

**Security Role:** Permutes data based on access patterns

### PermutationNetwork Class

**Purpose:** Multi-round encryption engine

**Key Methods:**
- `_create_sbox(key)` - AVL tree S-box generation
- `_permute_with_tree(data, key)` - Splay permutation
- `_diffusion_layer(data)` - Tree-based mixing
- `encrypt_block()` / `decrypt_block()` - Main cipher

**Security Role:** Implements 8-round SPN (Substitution-Permutation Network)

### AdvancedTreeCrypto Class

**Purpose:** High-level encryption interface

**Methods:**
- `encrypt(plaintext)` - Full encryption with padding
- `decrypt(ciphertext)` - Full decryption
- `encrypt_file()` / `decrypt_file()` - File operations

**Security Role:** Orchestrates block cipher with CBC mode

---

## 🚀 Usage

### Installation

No external dependencies! Pure Python 3.

```bash
cd advanced_tree_crypto
python --version  # Requires Python 3.6+
```

### Command Line

```bash
# Encrypt file
python advanced_tree_crypto.py encrypt input.txt encrypted.json

# Decrypt file
python advanced_tree_crypto.py decrypt encrypted.json output.txt
```

### Python API

```python
from advanced_tree_crypto import AdvancedTreeCrypto

# Initialize
crypto = AdvancedTreeCrypto("MyPassword123")

# Encrypt
plaintext = b"Secret message"
encrypted = crypto.encrypt(plaintext)

# Decrypt
decrypted = crypto.decrypt(encrypted)
print(decrypted)  # b"Secret message"
```

### Run Tests

```bash
python test_crypto.py
```

---

## 🧪 Test Suite

The test suite includes:

1. **AVL Tree Structure** - Verify balancing works
2. **Splay Tree Transformations** - Check dynamic restructuring
3. **Basic Encryption** - Round-trip test
4. **Large Data** - Multi-block encryption
5. **Password Dependency** - Different passwords → different output
6. **Wrong Password** - Detect incorrect decryption
7. **S-Box Generation** - Verify permutations
8. **File Encryption** - File I/O operations
9. **Diffusion** - Avalanche effect test

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| **Block Size** | 64 bytes |
| **Rounds** | 8 |
| **S-Box Size** | 256 bytes (8-bit) |
| **Key Schedule** | SHA-256 based |
| **Mode** | CBC (Cipher Block Chaining) |
| **Padding** | PKCS#7 |

**Speed (approximate):**
- Small files (<1KB): < 0.1s
- Medium files (100KB): ~1s
- Large files (1MB): ~10s

*Note: Pure Python, no optimization*

---

## 🔐 Security Analysis

### Strengths (vs Original Implementation)

✅ **Multiple Rounds** - 8 rounds vs 2 (exponentially stronger)
✅ **Proper Diffusion** - Avalanche effect through tree mixing
✅ **Key Scheduling** - Different keys per round
✅ **CBC Mode** - Blocks depend on previous (pattern hiding)
✅ **Non-Deterministic IV** - Same plaintext → different ciphertext
✅ **Larger Block Size** - 64 bytes vs character-by-character

### Weaknesses (vs Real Crypto)

❌ **No Security Proof** - Not mathematically proven secure
❌ **Weak S-Boxes** - Not cryptographically optimal
❌ **Deterministic Key Schedule** - No true randomness in round keys
❌ **Limited Diffusion** - Not as complete as AES MixColumns
❌ **Vulnerable to Analysis** - Susceptible to differential/linear cryptanalysis
❌ **No Authentication** - No MAC/HMAC (can be tampered)
❌ **Implementation Attacks** - Timing, side-channels possible

---

## 🆚 Comparison Matrix

| Feature | Original | This (Advanced) | AES-256 |
|---------|----------|-----------------|---------|
| **Rounds** | 2 | 8 | 14 |
| **Block Size** | 1 char | 64 bytes | 16 bytes |
| **S-Box** | None | Tree-based | Rijndael |
| **Diffusion** | Minimal | Tree mixing | MixColumns |
| **Key Schedule** | None | SHA-256 | Rijndael |
| **Mode** | None | CBC | GCM/CBC/CTR |
| **Security** | Very Weak | Weak-Medium | Strong |
| **Production Ready** | ❌ | ❌ | ✅ |
| **Educational Value** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎓 Learning Objectives

### Data Structures Covered

1. **AVL Trees**
   - Self-balancing rotations
   - Height maintenance
   - Balanced insertion

2. **Splay Trees**
   - Splaying operations
   - Zig-zig, zig-zag patterns
   - Amortized analysis

3. **Complete Binary Trees**
   - Parent-child relationships
   - Level-order properties
   - Array representation

### Cryptography Concepts

1. **Substitution-Permutation Networks**
   - S-boxes (substitution)
   - P-boxes (permutation)
   - Multiple rounds

2. **Confusion & Diffusion**
   - Shannon's principles
   - Avalanche effect
   - Non-linearity

3. **Block Ciphers**
   - Fixed block size
   - Padding schemes
   - Chaining modes (CBC)

4. **Key Scheduling**
   - Round key derivation
   - Hash-based generation
   - Key expansion

---

## 💡 Educational Insights

### Why Trees for Encryption?

**Pros:**
- ✅ Create complex, key-dependent permutations
- ✅ Natural hierarchical mixing (diffusion)
- ✅ Interesting educational example
- ✅ Shows data structure applications

**Cons:**
- ❌ Not optimized for cryptography
- ❌ Permutations not cryptographically strong
- ❌ Slower than bitwise operations
- ❌ Hard to prove security properties

### What Real Crypto Uses Instead

| Component | This Project | Real Crypto (AES) |
|-----------|-------------|-------------------|
| **S-Box** | AVL tree permutation | Carefully designed lookup table |
| **Permutation** | Splay tree | Bit-level permutations |
| **Diffusion** | Tree mixing | Polynomial multiplication (GF) |
| **Rounds** | 8 | 10-14 (key-dependent) |
| **Optimization** | Python loops | Hardware instructions (AES-NI) |

---

## 🔬 Advanced Topics

### Extending This Project

**Ideas for improvement:**
1. Add authentication (tree-based MAC)
2. Implement counter mode (CTR)
3. Use Red-Black trees for S-boxes
4. Add parallel processing
5. Optimize with Cython/C
6. Implement GCM mode
7. Add key derivation (PBKDF2)

### Research Questions

1. Can tree depth affect security?
2. What's the optimal number of rounds?
3. How to analyze differential properties?
4. Can graph structures improve diffusion?
5. What's the entropy of tree-based S-boxes?

---

## ⚠️ Security Warnings

### DO NOT USE FOR:

❌ Protecting sensitive data (use AES-256-GCM)
❌ Financial transactions (use industry standards)
❌ Password storage (use bcrypt/Argon2)
❌ Network security (use TLS/SSL)
❌ Any production system

### ACCEPTABLE FOR:

✅ Learning data structures
✅ Understanding encryption principles
✅ Academic projects
✅ Algorithm research
✅ Educational demonstrations

---

## 📚 Further Reading

### Data Structures
- [AVL Trees](https://en.wikipedia.org/wiki/AVL_tree)
- [Splay Trees](https://en.wikipedia.org/wiki/Splay_tree)
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms)

### Cryptography
- [Substitution-Permutation Networks](https://en.wikipedia.org/wiki/Substitution%E2%80%93permutation_network)
- [Block Cipher Modes](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)
- [Applied Cryptography by Bruce Schneier](https://www.schneier.com/books/applied-cryptography/)

### Why Custom Crypto Fails
- [Don't Roll Your Own Crypto](https://security.stackexchange.com/questions/18197)
- [Cryptographic Failures](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure)

---

## 🤝 Contributing

Improvements welcome for educational purposes:
- Better tree algorithms
- Additional test cases
- Performance optimizations
- Documentation improvements
- Visual demonstrations

**Note:** This is intentionally NOT production-ready. Don't try to "fix" it to be secure - use AES instead!

---

## 📄 License

MIT License - Educational use

---

## 🎯 Summary

This project demonstrates:

✅ **Advanced data structures** (AVL, Splay trees)
✅ **Cryptographic principles** (Confusion, Diffusion, Multiple rounds)
✅ **Algorithm design** (SPN structure, Key scheduling)
✅ **Why standardized crypto matters** (Limitations of custom algorithms)

**Key Takeaway:** Trees and data structures can create interesting transformations, but **cryptographically secure encryption requires decades of research, mathematical proofs, and peer review**. Always use established standards in production!

---

**Built with:** Python, AVL Trees, Splay Trees, Binary Trees, and Cryptographic Curiosity 🌳🔐
