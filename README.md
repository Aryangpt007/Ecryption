# Two-Level Encryption System

An educational encryption program demonstrating the application of data structures (binary trees) and ASCII manipulation for creating a custom cipher.

## ⚠️ Educational Purpose Only

**This is an educational project demonstrating algorithm design and data structures. It is NOT cryptographically secure and should NEVER be used to protect real-world sensitive data.**

For production use, always use industry-standard encryption libraries like AES, RSA, or libsodium.

---

## 📚 What You'll Learn

This project demonstrates:
- **Binary tree construction and traversal** (inorder, preorder, level-order)
- **Tree manipulation algorithms** (reversing alternate levels)
- **ASCII character encoding/decoding**
- **Stack implementation** using linked lists
- **File I/O operations** in C++
- **Algorithm design** for transformations
- **Why custom cryptography is dangerous** in real-world applications

---

## 🔧 How It Works

### Algorithm Overview

The encryption uses a **two-level transformation approach**:

#### **Level 1: ASCII Position-Swap Cipher**

1. Convert each character to its ASCII value
2. Create a position array: `[1, 2, 3, 4, 5, 6, ...]`
3. Swap adjacent positions: `[2, 1, 4, 3, 6, 5, ...]`
4. Add ASCII value + swapped position for each character
5. Convert results back to characters

**Example:**
```
Input:  'I'
ASCII:  73
Position: 1 → swapped to 2
Result: 73 + 2 = 75 = 'K'
```

#### **Level 2: Binary Tree Permutation**

1. Build a binary tree using **level-order insertion**
2. **Reverse alternate tree levels** (odd levels: 1, 3, 5, ...)
3. Extract **encrypted text** via **inorder traversal**
4. Extract **encryption key** via **preorder traversal**

**Tree Structure Example:**
```
Original:        After Reversing Level 1:
     A                    C
    / \                  / \
   B   C                B   A
  / \                  / \
 D   E                D   E
```

### Complete Example

```
Plaintext:  "I have a big House. Its number is 703."
            ↓ First Level (ASCII + Position Swap)
            ↓ Second Level (Tree Manipulation)
Ciphertext: "K! jzhb c! dk#j Jyvkp3 Kw#u pqekvw kt 9711"
Key:        [Preorder traversal of tree]
```

---

## 🚀 Compilation and Usage

### Requirements
- C++ compiler (g++, clang++)
- C++11 or later

### Compile
```bash
g++ -o enc enc.cpp
```

### Run
```bash
./enc
```

### Menu Options

```
1. Encrypt
   - Encrypt Text: Enter a string to encrypt
   - Encrypt File: Provide file path

2. Decrypt
   - Decrypt Text: Enter ciphertext and key
   - Decrypt File: Provide encrypted file and key file paths

3. Exit
```

### File Encryption Example

**Input File (`abc.txt`):**
```
I have a big House. Its number is 703.
```

**After encryption:**
- `abc_enc.txt` - Contains encrypted text
- `key.txt` - Contains encryption key

**To decrypt:**
- Use both `abc_enc.txt` and `key.txt` to recover original text
- Output saved to `Converted_file.txt`

---

## 📊 Code Structure

### Key Classes

```cpp
class node {
    char data;
    node* left;
    node* right;
};

class List : public node1 {
    void push(node *num);    // Stack push
    node* pop();             // Stack pop
};
```

### Main Functions

| Function | Purpose |
|----------|---------|
| `First_lvl()` | ASCII + position swap transformation |
| `Second_lvl()` | Binary tree encryption + key generation |
| `First_lvld()` | Rebuild tree from traversals, reverse levels |
| `Second_lvld()` | Reverse ASCII transformation |
| `encrypt()` | Complete encryption pipeline |
| `decrypt()` | Complete decryption pipeline |
| `reverseAlternate()` | Reverse odd-level tree nodes |
| `inorder()` | Generate encrypted text |
| `preorder()` | Generate encryption key |

---

## 🎓 Learning Exercises

Try these to deepen your understanding:

1. **Trace the Algorithm**: Manually encrypt "HELLO" step-by-step
2. **Modify the Pattern**: Change position swap from adjacent to every 3rd position
3. **Add Complexity**: Implement reversing even levels instead of odd
4. **Frequency Analysis**: Analyze character frequency in encrypted vs plaintext
5. **Break It**: Try to decrypt without the key using statistical analysis

---

## 🔐 Security Analysis (Educational)

### Why This Is NOT Secure

#### ❌ **Vulnerabilities**

1. **Deterministic Encryption**
   - Same input always produces same output
   - No randomness or initialization vector (IV)
   - Vulnerable to pattern detection

2. **Predictable Transformations**
   - Position swap pattern is fixed: `[2,1,4,3,6,5,...]`
   - Can be reverse-engineered with 1-2 known plaintext samples

3. **Length Preservation**
   - Ciphertext length = plaintext length
   - Leaks information about message size

4. **Weak Key Derivation**
   - Key is derived from ciphertext structure
   - Not truly independent from encrypted data

5. **No Integrity Protection**
   - No MAC (Message Authentication Code)
   - No protection against tampering

6. **Statistical Weaknesses**
   - Character relationships partially preserved
   - Vulnerable to frequency analysis

#### 🎯 **Attack Vectors**

| Attack Type | Difficulty | Time Required |
|-------------|-----------|---------------|
| Known Plaintext | Trivial | Minutes |
| Ciphertext-Only | Easy | Hours |
| Brute Force | Easy | Seconds-Minutes |

---

## 🏆 Comparison to Real Cryptography

| Feature | This Project | AES-256 (Industry Standard) |
|---------|--------------|----------------------------|
| Security | Educational only | Military-grade |
| Randomness | None | Cryptographically secure |
| Key Size | Variable (~text length) | 256 bits (fixed) |
| Standardized | No | NIST FIPS 197 |
| Peer Reviewed | No | Decades of analysis |
| Time to Break | Minutes | Computationally infeasible |

---

## 💡 Key Takeaways

### What This Project Teaches

✅ **Data structures matter** - Trees enable complex transformations
✅ **Algorithm design** - Breaking problems into steps
✅ **Encoding concepts** - ASCII manipulation and character mapping
✅ **File processing** - Reading/writing encrypted data

### What Real Cryptography Requires

✅ **Randomness** - Non-deterministic encryption (use IV/nonce)
✅ **Mathematical proofs** - Security guarantees
✅ **Key independence** - Keys derived from secure sources
✅ **Integrity** - Authentication tags (HMAC, GCM)
✅ **Standards compliance** - Peer-reviewed algorithms
✅ **Side-channel resistance** - Protection against timing attacks

---

## 🛡️ Security Best Practices

**For real-world encryption, use:**

```cpp
// Modern C++ Encryption (Example with libsodium)
#include <sodium.h>

// AES-256-GCM encryption
crypto_aead_aes256gcm_encrypt(
    ciphertext, ciphertext_len,
    plaintext, plaintext_len,
    additional_data, additional_data_len,
    NULL, nonce, key
);
```

**Recommended Libraries:**
- **libsodium** - Easy-to-use crypto library
- **OpenSSL** - Industry standard
- **Crypto++** - Comprehensive C++ crypto
- **Botan** - Modern C++ cryptography

**Golden Rule:** 🚫 **Never roll your own crypto for production!**

---

## 📖 Further Reading

### Cryptography Fundamentals
- [Introduction to Modern Cryptography](https://www.cs.umd.edu/~jkatz/imc.html) - Katz & Lindell
- [Applied Cryptography](https://www.schneier.com/books/applied-cryptography/) - Bruce Schneier
- [Cryptography Engineering](https://www.schneier.com/books/cryptography-engineering/) - Ferguson, Schneier, Kohno

### Why Custom Crypto Fails
- [Don't Roll Your Own Crypto](https://security.stackexchange.com/questions/18197/why-shouldnt-we-roll-our-own)
- [Lessons from Poor Crypto Implementations](https://www.nccgroup.com/us/research-blog/)

### Standard Algorithms
- [NIST Cryptographic Standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)
- [AES Specification](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)

---

## 🤝 Contributing

This is an educational project. Feel free to:
- Add more encryption levels
- Implement different tree structures
- Create visualization tools
- Add automated testing
- Improve code quality (fix buffer overflow risks, use modern C++)

**Note:** Contributions should maintain the educational focus. Don't attempt to make this "secure" - use it to teach concepts instead.

---

## 📝 License

This project is for educational purposes. Use at your own risk.

---

## 🙏 Acknowledgments

This project demonstrates:
- Classic data structure applications
- Why security requires specialized expertise
- The importance of using tested, standardized cryptography

**Remember:** Great programmers know when to build from scratch and when to use proven solutions. For encryption, always choose proven solutions. 🔒

---

## ⚡ Quick Start Example

```bash
# Compile
g++ -o enc enc.cpp

# Run
./enc

# Select: 1 (Encrypt) → 1 (Encrypt Text)
# Enter: Hello World
# Output:
#   Encrypted: [ciphertext]
#   Key: [key string]

# Select: 2 (Decrypt) → 1 (Decrypt Text)
# Enter encrypted text and key to recover original
```

---

**Built with:** C++, Binary Trees, ASCII Magic, and Educational Intent 🎓
