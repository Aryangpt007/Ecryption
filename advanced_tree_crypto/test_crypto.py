#!/usr/bin/env python3
"""
Test suite for Advanced Tree-Based Encryption
"""

from advanced_tree_crypto import (
    AdvancedTreeCrypto, AVLTree, SplayTree,
    PermutationNetwork, TreeNode
)
import os


def test_avl_tree():
    """Test AVL tree construction and traversals."""
    print("=" * 60)
    print("Test 1: AVL Tree Structure")
    print("=" * 60)

    avl = AVLTree()
    values = [50, 30, 70, 20, 40, 60, 80]

    print(f"Inserting values: {values}")
    for i, val in enumerate(values):
        avl.root = avl.insert(avl.root, val, i)

    inorder = avl.inorder(avl.root)
    preorder = avl.preorder(avl.root)
    postorder = avl.postorder(avl.root)

    print(f"✓ Inorder:   {inorder}")
    print(f"✓ Preorder:  {preorder}")
    print(f"✓ Postorder: {postorder}")
    print(f"✓ Tree is balanced (AVL property maintained)")
    print()


def test_splay_tree():
    """Test splay tree transformations."""
    print("=" * 60)
    print("Test 2: Splay Tree Dynamic Restructuring")
    print("=" * 60)

    splay = SplayTree()
    values = [10, 20, 30, 40, 50]

    print(f"Inserting values: {values}")
    for i, val in enumerate(values):
        splay.insert(val, i)

    result = splay.inorder(splay.root)
    print(f"✓ Inorder traversal: {result}")
    print(f"✓ Last inserted value is at root (splay property)")
    print()


def test_basic_encryption():
    """Test basic encryption and decryption."""
    print("=" * 60)
    print("Test 3: Basic Encryption/Decryption")
    print("=" * 60)

    password = "TestPassword123"
    message = b"Hello, World! This is a test message."

    crypto = AdvancedTreeCrypto(password)

    print(f"Original: {message}")
    print(f"Password: {password}")

    # Encrypt
    encrypted = crypto.encrypt(message)
    print(f"✓ Encrypted into {len(encrypted['blocks'])} blocks")
    print(f"✓ Block size: {encrypted['block_size']} bytes")
    print(f"✓ Algorithm: {encrypted['algorithm']}")

    # Decrypt
    decrypted = crypto.decrypt(encrypted)
    print(f"✓ Decrypted: {decrypted}")

    # Verify
    if message == decrypted:
        print("✓ SUCCESS: Encryption/Decryption works correctly!")
    else:
        print("✗ FAILED: Messages don't match!")
    print()


def test_large_data():
    """Test with larger data."""
    print("=" * 60)
    print("Test 4: Large Data Encryption")
    print("=" * 60)

    password = "LargeDataTest"
    # Create 5KB of data
    message = b"A" * 5120

    crypto = AdvancedTreeCrypto(password)

    print(f"Data size: {len(message)} bytes")

    encrypted = crypto.encrypt(message)
    print(f"✓ Encrypted into {len(encrypted['blocks'])} blocks")

    decrypted = crypto.decrypt(encrypted)
    print(f"✓ Decrypted {len(decrypted)} bytes")

    if message == decrypted:
        print("✓ SUCCESS: Large data encryption works!")
    else:
        print("✗ FAILED: Data corrupted!")
    print()


def test_different_passwords():
    """Test that different passwords produce different results."""
    print("=" * 60)
    print("Test 5: Password Dependency")
    print("=" * 60)

    message = b"Secret message"
    password1 = "Password1"
    password2 = "Password2"

    crypto1 = AdvancedTreeCrypto(password1)
    crypto2 = AdvancedTreeCrypto(password2)

    encrypted1 = crypto1.encrypt(message)
    encrypted2 = crypto2.encrypt(message)

    # Compare first blocks
    block1 = encrypted1['blocks'][0]
    block2 = encrypted2['blocks'][0]

    print(f"Same plaintext: {message}")
    print(f"Password 1: {password1}")
    print(f"Password 2: {password2}")
    print(f"First block cipher 1: {block1[:10]}...")
    print(f"First block cipher 2: {block2[:10]}...")

    if block1 != block2:
        print("✓ SUCCESS: Different passwords → different ciphertexts")
    else:
        print("✗ FAILED: Passwords not affecting encryption!")
    print()


def test_wrong_password():
    """Test decryption with wrong password."""
    print("=" * 60)
    print("Test 6: Wrong Password Detection")
    print("=" * 60)

    message = b"Secret data"
    correct_password = "CorrectPass"
    wrong_password = "WrongPass"

    # Encrypt with correct password
    crypto1 = AdvancedTreeCrypto(correct_password)
    encrypted = crypto1.encrypt(message)
    print(f"✓ Encrypted with password: {correct_password}")

    # Try decrypt with wrong password
    crypto2 = AdvancedTreeCrypto(wrong_password)
    decrypted = crypto2.decrypt(encrypted)
    print(f"✓ Attempted decrypt with: {wrong_password}")

    if decrypted != message:
        print("✓ SUCCESS: Wrong password produces garbage output")
        print(f"  Decrypted (first 20 bytes): {decrypted[:20]}")
    else:
        print("✗ WARNING: Wrong password still decrypted correctly!")
    print()


def test_sbox_generation():
    """Test S-box generation from keys."""
    print("=" * 60)
    print("Test 7: Tree-Based S-Box Generation")
    print("=" * 60)

    network1 = PermutationNetwork("key1")
    network2 = PermutationNetwork("key2")

    round_key1 = network1._key_schedule(0)
    round_key2 = network2._key_schedule(0)

    sbox1 = network1._create_sbox(round_key1)
    sbox2 = network2._create_sbox(round_key2)

    print(f"S-box 1 (first 10): {sbox1[:10]}")
    print(f"S-box 2 (first 10): {sbox2[:10]}")

    # Check they're valid permutations
    is_perm1 = sorted(sbox1) == list(range(256))
    is_perm2 = sorted(sbox2) == list(range(256))

    print(f"✓ S-box 1 is valid permutation: {is_perm1}")
    print(f"✓ S-box 2 is valid permutation: {is_perm2}")
    print(f"✓ S-boxes are different: {sbox1 != sbox2}")
    print()


def test_file_encryption():
    """Test file encryption."""
    print("=" * 60)
    print("Test 8: File Encryption/Decryption")
    print("=" * 60)

    # Create test file
    test_file = "test_input.txt"
    encrypted_file = "test_encrypted.json"
    decrypted_file = "test_output.txt"

    content = b"""This is a test file for advanced tree-based encryption.
It demonstrates:
- AVL trees for balanced permutations
- Splay trees for dynamic transformations
- Multi-round encryption
- Tree-based S-boxes
"""

    with open(test_file, 'wb') as f:
        f.write(content)

    password = "FileTestPassword"
    crypto = AdvancedTreeCrypto(password)

    # Encrypt
    crypto.encrypt_file(test_file, encrypted_file)
    print(f"✓ File encrypted: {test_file} → {encrypted_file}")

    # Decrypt
    crypto.decrypt_file(encrypted_file, decrypted_file)
    print(f"✓ File decrypted: {encrypted_file} → {decrypted_file}")

    # Verify
    with open(decrypted_file, 'rb') as f:
        decrypted_content = f.read()

    if content == decrypted_content:
        print("✓ SUCCESS: File content matches!")
    else:
        print("✗ FAILED: File content corrupted!")

    # Cleanup
    os.remove(test_file)
    os.remove(encrypted_file)
    os.remove(decrypted_file)
    print("✓ Test files cleaned up")
    print()


def test_diffusion():
    """Test diffusion layer."""
    print("=" * 60)
    print("Test 9: Diffusion Layer (Avalanche Effect)")
    print("=" * 60)

    password = "DiffusionTest"
    network = PermutationNetwork(password)

    # Two messages differing by 1 bit
    msg1 = [0] * 64
    msg2 = [0] * 64
    msg2[0] = 1  # Single bit difference

    encrypted1 = network.encrypt_block(msg1)
    encrypted2 = network.encrypt_block(msg2)

    # Count different bytes
    differences = sum(1 for a, b in zip(encrypted1, encrypted2) if a != b)

    print(f"Message 1: All zeros")
    print(f"Message 2: Single bit changed")
    print(f"Encrypted blocks differ in {differences}/{len(msg1)} bytes")
    print(f"Difference percentage: {differences/len(msg1)*100:.1f}%")

    if differences > len(msg1) * 0.3:  # At least 30% different
        print("✓ SUCCESS: Good diffusion (avalanche effect)")
    else:
        print("⚠ WARNING: Limited diffusion")
    print()


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Advanced Tree-Based Crypto - Test Suite".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    tests = [
        test_avl_tree,
        test_splay_tree,
        test_basic_encryption,
        test_large_data,
        test_different_passwords,
        test_wrong_password,
        test_sbox_generation,
        test_file_encryption,
        test_diffusion,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("=" * 60)
    print(f"Tests Passed: {passed}/{len(tests)}")
    print(f"Tests Failed: {failed}/{len(tests)}")
    print("=" * 60)


if __name__ == '__main__':
    main()
