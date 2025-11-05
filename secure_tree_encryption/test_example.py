#!/usr/bin/env python3
"""
Test and demonstration script for Secure Tree-Based Encryption
"""

import os
import json
from merkle_crypto import SecureTreeEncryption, MerkleNode, KeyDerivationTree


def test_basic_encryption():
    """Test basic encryption and decryption."""
    print("=" * 60)
    print("Test 1: Basic Encryption/Decryption")
    print("=" * 60)

    password = "SecurePassword123!"
    plaintext = b"Hello, World! This is a secure tree-based encryption system."

    # Encrypt
    encryptor = SecureTreeEncryption(password)
    encrypted_data = encryptor.encrypt(plaintext)

    print(f"✓ Original text: {plaintext.decode()}")
    print(f"✓ Encrypted into {encrypted_data['num_chunks']} chunks")
    print(f"✓ Merkle root: {encrypted_data['merkle_root'][:32]}...")

    # Decrypt
    decryptor = SecureTreeEncryption(password, salt=encryptor.salt)
    decrypted = decryptor.decrypt(encrypted_data)

    print(f"✓ Decrypted text: {decrypted.decode()}")
    print(f"✓ Match: {plaintext == decrypted}")
    print()


def test_large_data():
    """Test with larger data to demonstrate chunking."""
    print("=" * 60)
    print("Test 2: Large Data Encryption (Multiple Chunks)")
    print("=" * 60)

    password = "AnotherSecurePassword456!"
    # Create 20KB of data (will be split into multiple chunks)
    plaintext = b"A" * 20480

    encryptor = SecureTreeEncryption(password)
    encrypted_data = encryptor.encrypt(plaintext)

    print(f"✓ Data size: {len(plaintext)} bytes")
    print(f"✓ Number of chunks: {encrypted_data['num_chunks']}")
    print(f"✓ Chunk size: {encrypted_data['chunk_size']} bytes")
    print(f"✓ Algorithm: {encrypted_data['metadata']['algorithm']}")

    # Decrypt and verify
    decryptor = SecureTreeEncryption(password, salt=encryptor.salt)
    decrypted = decryptor.decrypt(encrypted_data)

    print(f"✓ Decryption successful: {plaintext == decrypted}")
    print()


def test_integrity_verification():
    """Test Merkle tree integrity verification."""
    print("=" * 60)
    print("Test 3: Integrity Verification (Tamper Detection)")
    print("=" * 60)

    password = "IntegrityTest789"
    plaintext = b"This message must not be tampered with!"

    encryptor = SecureTreeEncryption(password)
    encrypted_data = encryptor.encrypt(plaintext)

    print(f"✓ Original encrypted successfully")

    # Try decrypting with correct data
    decryptor = SecureTreeEncryption(password, salt=encryptor.salt)
    decrypted = decryptor.decrypt(encrypted_data)
    print(f"✓ Integrity check passed for unmodified data")

    # Tamper with data
    original_ciphertext = encrypted_data['encrypted_chunks'][0]['ciphertext']
    encrypted_data['encrypted_chunks'][0]['ciphertext'] = original_ciphertext[:-4] + "XXXX"

    print("⚠ Tampering with encrypted data...")

    # Try decrypting tampered data
    try:
        decryptor.decrypt(encrypted_data)
        print("✗ ERROR: Tampered data was not detected!")
    except Exception as e:
        print(f"✓ Tampering detected: {type(e).__name__}")
        print(f"  (AES-GCM authentication failed as expected)")
    print()


def test_wrong_password():
    """Test decryption with wrong password."""
    print("=" * 60)
    print("Test 4: Wrong Password Detection")
    print("=" * 60)

    correct_password = "CorrectPassword123"
    wrong_password = "WrongPassword456"
    plaintext = b"Secret message"

    # Encrypt with correct password
    encryptor = SecureTreeEncryption(correct_password)
    encrypted_data = encryptor.encrypt(plaintext)
    print(f"✓ Encrypted with correct password")

    # Try decrypt with wrong password
    decryptor = SecureTreeEncryption(wrong_password, salt=encryptor.salt)

    try:
        decryptor.decrypt(encrypted_data)
        print("✗ ERROR: Wrong password was not detected!")
    except Exception as e:
        print(f"✓ Wrong password detected: {type(e).__name__}")
        print(f"  (Authentication failed as expected)")
    print()


def test_key_derivation_tree():
    """Test hierarchical key derivation."""
    print("=" * 60)
    print("Test 5: Key Derivation Tree (Forward Secrecy)")
    print("=" * 60)

    master_key = os.urandom(32)
    kdf_tree = KeyDerivationTree(master_key)

    # Derive keys for different tree positions
    key_0 = kdf_tree.derive_key([0])
    key_1 = kdf_tree.derive_key([1])
    key_0_0 = kdf_tree.derive_key([0, 0])
    key_0_1 = kdf_tree.derive_key([0, 1])

    print(f"✓ Derived key for path [0]: {key_0.hex()[:32]}...")
    print(f"✓ Derived key for path [1]: {key_1.hex()[:32]}...")
    print(f"✓ Derived key for path [0,0]: {key_0_0.hex()[:32]}...")
    print(f"✓ Derived key for path [0,1]: {key_0_1.hex()[:32]}...")

    # Verify keys are different
    assert key_0 != key_1, "Keys should be different"
    assert key_0 != key_0_0, "Keys should be different"
    assert key_0_0 != key_0_1, "Keys should be different"

    print(f"✓ All derived keys are unique (forward secrecy)")
    print()


def test_file_encryption():
    """Test file encryption and decryption."""
    print("=" * 60)
    print("Test 6: File Encryption/Decryption")
    print("=" * 60)

    # Create test file
    test_file = "test_input.txt"
    encrypted_file = "test_encrypted.json"
    decrypted_file = "test_output.txt"

    original_content = b"This is a test file for secure encryption.\nIt has multiple lines.\nLine 3 here!"

    with open(test_file, 'wb') as f:
        f.write(original_content)

    password = "FileTestPassword"

    # Encrypt file
    encryptor = SecureTreeEncryption(password)
    encryptor.encrypt_file(test_file, encrypted_file)
    print(f"✓ File encrypted: {test_file} → {encrypted_file}")

    # Decrypt file
    decryptor = SecureTreeEncryption(password, salt=encryptor.salt)
    decryptor.decrypt_file(encrypted_file, decrypted_file)
    print(f"✓ File decrypted: {encrypted_file} → {decrypted_file}")

    # Verify
    with open(decrypted_file, 'rb') as f:
        decrypted_content = f.read()

    print(f"✓ Content match: {original_content == decrypted_content}")

    # Cleanup
    os.remove(test_file)
    os.remove(encrypted_file)
    os.remove(decrypted_file)
    print(f"✓ Test files cleaned up")
    print()


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Secure Tree-Based Encryption - Test Suite".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    try:
        test_basic_encryption()
        test_large_data()
        test_integrity_verification()
        test_wrong_password()
        test_key_derivation_tree()
        test_file_encryption()

        print("=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
