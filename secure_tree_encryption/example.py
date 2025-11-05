#!/usr/bin/env python3
"""
Simple example demonstrating secure tree-based encryption
"""

from merkle_crypto import SecureTreeEncryption

def simple_example():
    """Basic encryption and decryption example."""

    print("Simple Encryption Example")
    print("=" * 50)

    # Your secret message
    message = "This is a secret message that needs protection!"

    # Your password (in real use, get from user input)
    password = "MySecurePassword123!"

    print(f"\n1. Original message: {message}")

    # Encrypt
    print("\n2. Encrypting...")
    encryptor = SecureTreeEncryption(password)
    encrypted_data = encryptor.encrypt(message.encode('utf-8'))

    print(f"   ✓ Encrypted into {encrypted_data['num_chunks']} chunks")
    print(f"   ✓ Algorithm: {encrypted_data['metadata']['algorithm']}")
    print(f"   ✓ Merkle root: {encrypted_data['merkle_root'][:40]}...")

    # Decrypt
    print("\n3. Decrypting...")
    decryptor = SecureTreeEncryption(password, salt=encryptor.salt)
    decrypted_bytes = decryptor.decrypt(encrypted_data)
    decrypted_message = decrypted_bytes.decode('utf-8')

    print(f"   ✓ Decrypted message: {decrypted_message}")

    # Verify
    print("\n4. Verification:")
    if message == decrypted_message:
        print("   ✓ SUCCESS: Messages match!")
    else:
        print("   ✗ ERROR: Messages don't match!")

    print("\n" + "=" * 50)


def file_example():
    """File encryption example."""

    print("\nFile Encryption Example")
    print("=" * 50)

    # Create a test file
    test_file = "secret_document.txt"
    encrypted_file = "secret_document.enc"
    decrypted_file = "secret_document_decrypted.txt"

    # Create content
    content = """TOP SECRET DOCUMENT

This document contains sensitive information that must be encrypted.

Project: Secure Tree Encryption
Status: Active
Classification: Confidential

Please handle with care.
"""

    # Write test file
    print(f"\n1. Creating test file: {test_file}")
    with open(test_file, 'w') as f:
        f.write(content)
    print(f"   ✓ File created ({len(content)} bytes)")

    # Encrypt file
    password = "FileEncryptionPassword456!"
    print(f"\n2. Encrypting file...")
    encryptor = SecureTreeEncryption(password)
    encryptor.encrypt_file(test_file, encrypted_file)
    print(f"   ✓ Encrypted: {test_file} → {encrypted_file}")

    # Decrypt file
    print(f"\n3. Decrypting file...")
    decryptor = SecureTreeEncryption(password, salt=encryptor.salt)
    decryptor.decrypt_file(encrypted_file, decrypted_file)
    print(f"   ✓ Decrypted: {encrypted_file} → {decrypted_file}")

    # Verify
    print("\n4. Verification:")
    with open(test_file, 'r') as f1, open(decrypted_file, 'r') as f2:
        if f1.read() == f2.read():
            print("   ✓ SUCCESS: Files match perfectly!")
        else:
            print("   ✗ ERROR: Files don't match!")

    # Cleanup
    print("\n5. Cleanup:")
    import os
    os.remove(test_file)
    os.remove(encrypted_file)
    os.remove(decrypted_file)
    print("   ✓ Test files removed")

    print("\n" + "=" * 50)


def security_demo():
    """Demonstrate security features."""

    print("\nSecurity Features Demo")
    print("=" * 50)

    password = "DemoPassword789"
    message = b"Sensitive data"

    # Non-deterministic encryption
    print("\n1. Non-Deterministic Encryption:")
    print("   (Same input → different output each time)")

    enc1 = SecureTreeEncryption(password)
    encrypted1 = enc1.encrypt(message)

    enc2 = SecureTreeEncryption(password)
    encrypted2 = enc2.encrypt(message)

    cipher1 = encrypted1['encrypted_chunks'][0]['ciphertext']
    cipher2 = encrypted2['encrypted_chunks'][0]['ciphertext']

    print(f"   Encryption 1: {cipher1[:40]}...")
    print(f"   Encryption 2: {cipher2[:40]}...")
    print(f"   ✓ Different: {cipher1 != cipher2}")

    # Wrong password detection
    print("\n2. Wrong Password Detection:")
    encryptor = SecureTreeEncryption("correct_password")
    encrypted = encryptor.encrypt(message)

    try:
        wrong_decryptor = SecureTreeEncryption("wrong_password", salt=encryptor.salt)
        wrong_decryptor.decrypt(encrypted)
        print("   ✗ ERROR: Should have failed!")
    except Exception as e:
        print(f"   ✓ Authentication failed (as expected)")

    # Tamper detection
    print("\n3. Tamper Detection:")
    encryptor = SecureTreeEncryption(password)
    encrypted = encryptor.encrypt(message)

    # Tamper with data
    original = encrypted['encrypted_chunks'][0]['ciphertext']
    encrypted['encrypted_chunks'][0]['ciphertext'] = original[:-4] + "XXXX"

    try:
        decryptor = SecureTreeEncryption(password, salt=encryptor.salt)
        decryptor.decrypt(encrypted)
        print("   ✗ ERROR: Should have detected tampering!")
    except Exception as e:
        print(f"   ✓ Tampering detected (as expected)")

    print("\n" + "=" * 50)


if __name__ == '__main__':
    print("\n")
    print("╔" + "═" * 48 + "╗")
    print("║" + " " * 48 + "║")
    print("║" + "  Secure Tree-Based Encryption Examples".center(48) + "║")
    print("║" + " " * 48 + "║")
    print("╚" + "═" * 48 + "╝")

    simple_example()
    file_example()
    security_demo()

    print("\n✓ All examples completed successfully!")
    print("\nTry it yourself:")
    print("  python merkle_crypto.py encrypt myfile.txt encrypted.json")
    print("  python merkle_crypto.py decrypt encrypted.json decrypted.txt")
    print()
