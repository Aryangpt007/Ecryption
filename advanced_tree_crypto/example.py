#!/usr/bin/env python3
"""
Simple examples demonstrating Advanced Tree-Based Encryption
"""

from advanced_tree_crypto import AdvancedTreeCrypto, AVLTree, SplayTree


def simple_example():
    """Basic encryption example."""
    print("=" * 60)
    print("Example 1: Simple Text Encryption")
    print("=" * 60)

    password = "MySecretPassword"
    message = b"Hello from Advanced Tree Crypto!"

    print(f"Password: {password}")
    print(f"Message:  {message.decode()}\n")

    # Encrypt
    crypto = AdvancedTreeCrypto(password)
    encrypted = crypto.encrypt(message)

    print("Encryption Details:")
    print(f"  ✓ Algorithm: {encrypted['algorithm']}")
    print(f"  ✓ Blocks: {len(encrypted['blocks'])}")
    print(f"  ✓ Block size: {encrypted['block_size']} bytes")
    print(f"  ✓ First block (first 10 bytes): {encrypted['blocks'][0][:10]}")

    # Decrypt
    decrypted = crypto.decrypt(encrypted)
    print(f"\n✓ Decrypted: {decrypted.decode()}")
    print(f"✓ Match: {message == decrypted}\n")


def tree_structure_example():
    """Show how trees create permutations."""
    print("=" * 60)
    print("Example 2: Tree Structures in Action")
    print("=" * 60)

    print("\n--- AVL Tree (Balanced Permutation) ---")
    avl = AVLTree()
    values = [5, 3, 7, 2, 4, 6, 8, 1, 9]

    print(f"Inserting: {values}")
    for i, val in enumerate(values):
        avl.root = avl.insert(avl.root, val, chr(65 + i))  # A, B, C...

    print(f"Inorder (sorted):  {avl.inorder(avl.root)}")
    print(f"Preorder (root):   {avl.preorder(avl.root)}")
    print(f"Postorder (leaf):  {avl.postorder(avl.root)}")
    print("✓ Different traversals = different permutations!")

    print("\n--- Splay Tree (Dynamic Permutation) ---")
    splay = SplayTree()
    values = [10, 20, 30, 40, 50]

    print(f"Inserting: {values}")
    for i, val in enumerate(values):
        splay.insert(val, chr(65 + i))

    result = splay.inorder(splay.root)
    print(f"Inorder: {result}")
    print("✓ Last inserted value is at root!\n")


def multi_round_example():
    """Demonstrate multi-round encryption."""
    print("=" * 60)
    print("Example 3: Multi-Round Transformation")
    print("=" * 60)

    from advanced_tree_crypto import PermutationNetwork

    password = "demo"
    network = PermutationNetwork(password, rounds=3)

    data = list(b"HELLO123")
    print(f"\nOriginal data: {data}")
    print(f"Characters:    {[chr(b) for b in data]}\n")

    # Show round-by-round encryption
    result = list(data)
    for round_num in range(3):
        round_key = network._key_schedule(round_num)

        print(f"Round {round_num + 1}:")
        print(f"  Before: {result}")

        # Apply transformations
        sbox = network._create_sbox(round_key)
        result = network._substitute(result, sbox)
        print(f"  After S-box: {result}")

        result = network._permute_with_tree(result, round_key)
        print(f"  After permute: {result}")

        result = network._xor_with_key(result, round_key)
        print(f"  After XOR: {result}")

        result = network._diffusion_layer(result)
        print(f"  After diffusion: {result}\n")

    print(f"Final encrypted: {result}")
    print("✓ Notice how data transforms through each round!\n")


def avalanche_example():
    """Demonstrate avalanche effect."""
    print("=" * 60)
    print("Example 4: Avalanche Effect (1 Bit Change)")
    print("=" * 60)

    password = "test"
    crypto = AdvancedTreeCrypto(password)

    # Two messages differing by 1 bit
    msg1 = b"Hello World!"
    msg2 = b"Iello World!"  # Changed 'H' to 'I' (1 bit different)

    encrypted1 = crypto.encrypt(msg1)
    encrypted2 = crypto.encrypt(msg2)

    block1 = encrypted1['blocks'][0]
    block2 = encrypted2['blocks'][0]

    # Count differences
    differences = sum(1 for a, b in zip(block1, block2) if a != b)

    print(f"Message 1: {msg1}")
    print(f"Message 2: {msg2}")
    print(f"Bit difference: 1 bit (H vs I)")
    print(f"\nEncrypted block 1 (first 20): {block1[:20]}")
    print(f"Encrypted block 2 (first 20): {block2[:20]}")
    print(f"\nDifferent bytes: {differences}/{len(block1)}")
    print(f"Percentage: {differences/len(block1)*100:.1f}%")
    print("✓ Small input change → Large output change!\n")


def password_dependency_example():
    """Show password dependency."""
    print("=" * 60)
    print("Example 5: Password Makes the Difference")
    print("=" * 60)

    message = b"Shared secret message"

    passwords = ["password1", "password2", "password3"]
    encrypted_blocks = []

    for pwd in passwords:
        crypto = AdvancedTreeCrypto(pwd)
        encrypted = crypto.encrypt(message)
        encrypted_blocks.append(encrypted['blocks'][0][:15])

    print(f"Same message: {message}\n")
    for i, pwd in enumerate(passwords):
        print(f"Password '{pwd}':")
        print(f"  Encrypted: {encrypted_blocks[i]}")

    print("\n✓ Different passwords → Completely different ciphertexts!\n")


def file_example():
    """File encryption example."""
    print("=" * 60)
    print("Example 6: File Encryption")
    print("=" * 60)

    import os

    # Create sample file
    filename = "demo_file.txt"
    with open(filename, 'w') as f:
        f.write("""Top Secret Document

This document demonstrates file encryption using
advanced tree-based cryptographic techniques.

Features:
- AVL trees for S-boxes
- Splay trees for permutations
- Multi-round encryption (8 rounds)
- CBC mode for blocks

Educational purposes only!
""")

    print(f"✓ Created file: {filename}")

    # Encrypt
    password = "FilePassword123"
    crypto = AdvancedTreeCrypto(password)

    encrypted_file = "demo_file.enc"
    crypto.encrypt_file(filename, encrypted_file)
    print(f"✓ Encrypted: {filename} → {encrypted_file}")

    # Show encrypted file size
    import json
    with open(encrypted_file, 'r') as f:
        enc_data = json.load(f)
    print(f"  - Blocks: {len(enc_data['blocks'])}")
    print(f"  - Block size: {enc_data['block_size']}")

    # Decrypt
    decrypted_file = "demo_file_decrypted.txt"
    crypto.decrypt_file(encrypted_file, decrypted_file)
    print(f"✓ Decrypted: {encrypted_file} → {decrypted_file}")

    # Verify
    with open(filename, 'r') as f1, open(decrypted_file, 'r') as f2:
        if f1.read() == f2.read():
            print("✓ Files match perfectly!\n")

    # Cleanup
    os.remove(filename)
    os.remove(encrypted_file)
    os.remove(decrypted_file)


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "Advanced Tree-Based Crypto - Examples".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    examples = [
        simple_example,
        tree_structure_example,
        multi_round_example,
        avalanche_example,
        password_dependency_example,
        file_example,
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"✗ Example failed: {e}")
            import traceback
            traceback.print_exc()

    print("=" * 60)
    print("✓ All examples completed!")
    print("=" * 60)
    print("\nTry it yourself:")
    print("  python advanced_tree_crypto.py encrypt myfile.txt encrypted.json")
    print("  python advanced_tree_crypto.py decrypt encrypted.json decrypted.txt")
    print()


if __name__ == '__main__':
    main()
