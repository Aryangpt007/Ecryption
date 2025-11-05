#!/usr/bin/env python3
"""
Advanced Tree & Data Structure Based Encryption
===============================================

This is an EDUCATIONAL implementation showing how multiple data structures
can be combined for encryption. It uses:

- AVL Trees for balanced permutations
- Splay Trees for dynamic transformations
- Binary Search Trees for substitution
- Graph structures for diffusion
- Multi-round Feistel-like network
- Tree-based S-boxes

⚠️ EDUCATIONAL ONLY - NOT CRYPTOGRAPHICALLY SECURE ⚠️

This demonstrates advanced data structure concepts, but custom
encryption algorithms cannot match the security of proven standards.

Author: Educational Implementation
"""

import hashlib
import json
import random
from typing import List, Tuple, Optional


class TreeNode:
    """Generic tree node for various tree types."""
    def __init__(self, value: int, data: int = 0):
        self.value = value
        self.data = data
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None
        self.height = 1


class AVLTree:
    """
    AVL Tree for creating balanced permutations.
    Self-balancing property ensures consistent transformations.
    """

    def __init__(self):
        self.root: Optional[TreeNode] = None

    def _height(self, node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return node.height

    def _balance(self, node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y: TreeNode) -> TreeNode:
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = max(self._height(y.left), self._height(y.right)) + 1
        x.height = max(self._height(x.left), self._height(x.right)) + 1
        return x

    def _rotate_left(self, x: TreeNode) -> TreeNode:
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = max(self._height(x.left), self._height(x.right)) + 1
        y.height = max(self._height(y.left), self._height(y.right)) + 1
        return y

    def insert(self, node: Optional[TreeNode], value: int, data: int = 0) -> TreeNode:
        """Insert value and rebalance tree."""
        if not node:
            return TreeNode(value, data)

        if value < node.value:
            node.left = self.insert(node.left, value, data)
        else:
            node.right = self.insert(node.right, value, data)

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._balance(node)

        # Left Left
        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)

        # Right Right
        if balance < -1 and value > node.right.value:
            return self._rotate_left(node)

        # Left Right
        if balance > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Left
        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def inorder(self, node: Optional[TreeNode]) -> List[int]:
        """Get inorder traversal."""
        if not node:
            return []
        return self.inorder(node.left) + [node.data] + self.inorder(node.right)

    def preorder(self, node: Optional[TreeNode]) -> List[int]:
        """Get preorder traversal."""
        if not node:
            return []
        return [node.data] + self.preorder(node.left) + self.preorder(node.right)

    def postorder(self, node: Optional[TreeNode]) -> List[int]:
        """Get postorder traversal."""
        if not node:
            return []
        return self.postorder(node.left) + self.postorder(node.right) + [node.data]


class SplayTree:
    """
    Splay Tree for dynamic transformations.
    Recently accessed elements move to root, creating key-dependent structure.
    """

    def __init__(self):
        self.root: Optional[TreeNode] = None

    def _right_rotate(self, x: TreeNode) -> TreeNode:
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x: TreeNode) -> TreeNode:
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root: Optional[TreeNode], value: int) -> Optional[TreeNode]:
        """Bring value to root through rotations."""
        if not root or root.value == value:
            return root

        if value < root.value:
            if not root.left:
                return root

            # Zig-Zig (Left Left)
            if value < root.left.value:
                root.left.left = self._splay(root.left.left, value)
                root = self._right_rotate(root)
            # Zig-Zag (Left Right)
            elif value > root.left.value:
                root.left.right = self._splay(root.left.right, value)
                if root.left.right:
                    root.left = self._left_rotate(root.left)

            return self._right_rotate(root) if root.left else root

        else:
            if not root.right:
                return root

            # Zag-Zag (Right Right)
            if value > root.right.value:
                root.right.right = self._splay(root.right.right, value)
                root = self._left_rotate(root)
            # Zag-Zig (Right Left)
            elif value < root.right.value:
                root.right.left = self._splay(root.right.left, value)
                if root.right.left:
                    root.right = self._right_rotate(root.right)

            return self._left_rotate(root) if root.right else root

    def insert(self, value: int, data: int = 0):
        """Insert and splay to root."""
        if not self.root:
            self.root = TreeNode(value, data)
            return

        self.root = self._splay(self.root, value)

        if self.root.value == value:
            return

        new_node = TreeNode(value, data)
        if value < self.root.value:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node

    def inorder(self, node: Optional[TreeNode]) -> List[int]:
        """Get inorder traversal."""
        if not node:
            return []
        return self.inorder(node.left) + [node.data] + self.inorder(node.right)


class PermutationNetwork:
    """
    Creates permutations using tree structures.
    Multiple rounds of tree-based transformations.
    """

    def __init__(self, key: str, rounds: int = 8):
        self.key = key
        self.rounds = rounds
        self.key_hash = hashlib.sha256(key.encode()).digest()

    def _key_schedule(self, round_num: int) -> bytes:
        """Generate round-specific key."""
        data = self.key_hash + round_num.to_bytes(4, 'big')
        return hashlib.sha256(data).digest()

    def _create_sbox(self, round_key: bytes) -> List[int]:
        """
        Create substitution box using tree structure.
        Build AVL tree with key-dependent order, extract permutation.
        """
        # Use key to determine insertion order
        seed_value = int.from_bytes(round_key[:8], 'big')
        random.seed(seed_value)

        insertion_order = list(range(256))
        random.shuffle(insertion_order)

        # Build AVL tree
        avl = AVLTree()
        for idx, val in enumerate(insertion_order):
            avl.root = avl.insert(avl.root, val, idx)

        # Extract permutation via traversal
        sbox = avl.inorder(avl.root)

        # Ensure it's a valid permutation
        if len(sbox) != 256:
            sbox.extend([i for i in range(256) if i not in sbox])

        return sbox[:256]

    def _substitute(self, data: List[int], sbox: List[int]) -> List[int]:
        """Apply S-box substitution."""
        return [sbox[byte] for byte in data]

    def _permute_with_tree(self, data: List[int], round_key: bytes) -> List[int]:
        """
        Permute data using splay tree.
        Access pattern depends on key, creating unique permutation.
        """
        if len(data) == 0:
            return data

        # Build splay tree with key-dependent access pattern
        seed = int.from_bytes(round_key[8:16], 'big')
        random.seed(seed)

        splay = SplayTree()
        indices = list(range(len(data)))
        random.shuffle(indices)

        for idx in indices:
            splay.insert(idx, data[idx])

        # Extract permuted data
        result = splay.inorder(splay.root)

        # Ensure correct length
        while len(result) < len(data):
            result.append(0)

        return result[:len(data)]

    def _xor_with_key(self, data: List[int], round_key: bytes) -> List[int]:
        """XOR data with expanded round key."""
        key_expanded = list(round_key * (len(data) // len(round_key) + 1))
        return [(data[i] ^ key_expanded[i]) % 256 for i in range(len(data))]

    def _diffusion_layer(self, data: List[int]) -> List[int]:
        """
        Mix data using tree-based diffusion.
        Each byte influenced by multiple others via tree structure.
        """
        if len(data) < 2:
            return data

        # Build complete binary tree
        result = list(data)
        n = len(data)

        # Parent-child mixing
        for i in range(n // 2):
            left_child = 2 * i + 1
            right_child = 2 * i + 2

            if left_child < n:
                result[i] = (result[i] + result[left_child]) % 256
            if right_child < n:
                result[i] = (result[i] + result[right_child]) % 256

        # Sibling mixing
        for i in range(0, n - 1, 2):
            temp = (result[i] + result[i + 1]) % 256
            result[i] = (result[i] - result[i + 1]) % 256
            result[i + 1] = temp

        return result

    def encrypt_block(self, data: List[int]) -> List[int]:
        """
        Encrypt data block using multi-round tree transformations.

        Each round:
        1. Substitution (tree-based S-box)
        2. Permutation (splay tree)
        3. XOR with round key
        4. Diffusion (tree mixing)
        """
        result = list(data)

        for round_num in range(self.rounds):
            round_key = self._key_schedule(round_num)

            # Substitution
            sbox = self._create_sbox(round_key)
            result = self._substitute(result, sbox)

            # Permutation
            result = self._permute_with_tree(result, round_key)

            # Key mixing
            result = self._xor_with_key(result, round_key)

            # Diffusion
            result = self._diffusion_layer(result)

        return result

    def decrypt_block(self, data: List[int]) -> List[int]:
        """
        Decrypt by reversing operations in reverse order.
        """
        result = list(data)

        # Reverse each round
        for round_num in range(self.rounds - 1, -1, -1):
            round_key = self._key_schedule(round_num)

            # Reverse diffusion
            result = self._reverse_diffusion(result)

            # Reverse key mixing
            result = self._xor_with_key(result, round_key)

            # Reverse permutation
            result = self._reverse_permute(result, round_key)

            # Reverse substitution
            sbox = self._create_sbox(round_key)
            inv_sbox = self._invert_sbox(sbox)
            result = self._substitute(result, inv_sbox)

        return result

    def _reverse_diffusion(self, data: List[int]) -> List[int]:
        """Reverse the diffusion layer."""
        if len(data) < 2:
            return data

        result = list(data)
        n = len(data)

        # Reverse sibling mixing
        for i in range(0, n - 1, 2):
            temp = result[i + 1]
            result[i + 1] = (result[i + 1] - result[i]) % 256
            result[i] = (result[i] - temp) % 256

        # Reverse parent-child mixing
        for i in range(n // 2 - 1, -1, -1):
            left_child = 2 * i + 1
            right_child = 2 * i + 2

            if right_child < n:
                result[i] = (result[i] - result[right_child]) % 256
            if left_child < n:
                result[i] = (result[i] - result[left_child]) % 256

        return result

    def _reverse_permute(self, data: List[int], round_key: bytes) -> List[int]:
        """Reverse tree-based permutation."""
        if len(data) == 0:
            return data

        # Recreate same splay tree
        seed = int.from_bytes(round_key[8:16], 'big')
        random.seed(seed)

        indices = list(range(len(data)))
        random.shuffle(indices)

        # Create inverse mapping
        splay = SplayTree()
        for idx in indices:
            splay.insert(idx, 0)  # Dummy data

        permuted_indices = splay.inorder(splay.root)

        # Create inverse permutation
        result = [0] * len(data)
        for i, perm_idx in enumerate(permuted_indices[:len(data)]):
            if perm_idx < len(data):
                result[perm_idx] = data[i]

        return result

    def _invert_sbox(self, sbox: List[int]) -> List[int]:
        """Create inverse S-box."""
        inv_sbox = [0] * 256
        for i, val in enumerate(sbox):
            if val < 256:
                inv_sbox[val] = i
        return inv_sbox


class AdvancedTreeCrypto:
    """
    Main encryption class using advanced tree and data structures.

    Features:
    - Multi-round permutation network
    - Tree-based S-boxes
    - Diffusion through tree mixing
    - Key-dependent structure transformations
    """

    BLOCK_SIZE = 64  # bytes

    def __init__(self, password: str):
        self.password = password
        # Use hash for IV generation
        self.iv = hashlib.sha256(password.encode()).digest()[:16]
        self.network = PermutationNetwork(password, rounds=8)

    def _pad(self, data: bytes) -> bytes:
        """PKCS#7 padding."""
        pad_len = self.BLOCK_SIZE - (len(data) % self.BLOCK_SIZE)
        return data + bytes([pad_len] * pad_len)

    def _unpad(self, data: bytes) -> bytes:
        """Remove PKCS#7 padding."""
        pad_len = data[-1]
        return data[:-pad_len]

    def encrypt(self, plaintext: bytes) -> dict:
        """Encrypt data using tree-based cipher."""
        # Pad data
        padded = self._pad(plaintext)

        # Split into blocks
        blocks = [padded[i:i+self.BLOCK_SIZE]
                  for i in range(0, len(padded), self.BLOCK_SIZE)]

        encrypted_blocks = []
        prev_block = list(self.iv)

        # CBC mode
        for block in blocks:
            block_list = list(block)

            # XOR with previous ciphertext (CBC)
            chained = [(block_list[i] ^ prev_block[i % len(prev_block)]) % 256
                      for i in range(len(block_list))]

            # Encrypt block
            encrypted = self.network.encrypt_block(chained)
            encrypted_blocks.append(encrypted)
            prev_block = encrypted

        return {
            'version': '1.0',
            'algorithm': 'Advanced Tree Crypto',
            'blocks': encrypted_blocks,
            'block_size': self.BLOCK_SIZE,
            'iv': list(self.iv)
        }

    def decrypt(self, encrypted_data: dict) -> bytes:
        """Decrypt data."""
        blocks = encrypted_data['blocks']
        iv = encrypted_data['iv']

        decrypted_blocks = []
        prev_block = iv

        for encrypted_block in blocks:
            # Decrypt block
            decrypted = self.network.decrypt_block(encrypted_block)

            # XOR with previous ciphertext (CBC)
            unchained = [(decrypted[i] ^ prev_block[i % len(prev_block)]) % 256
                        for i in range(len(decrypted))]

            decrypted_blocks.append(bytes(unchained))
            prev_block = encrypted_block

        # Concatenate and unpad
        plaintext = b''.join(decrypted_blocks)
        return self._unpad(plaintext)

    def encrypt_file(self, input_path: str, output_path: str):
        """Encrypt file."""
        with open(input_path, 'rb') as f:
            plaintext = f.read()

        encrypted = self.encrypt(plaintext)

        with open(output_path, 'w') as f:
            json.dump(encrypted, f, indent=2)

    def decrypt_file(self, input_path: str, output_path: str):
        """Decrypt file."""
        with open(input_path, 'r') as f:
            encrypted = json.load(f)

        plaintext = self.decrypt(encrypted)

        with open(output_path, 'wb') as f:
            f.write(plaintext)


def main():
    """CLI interface."""
    import sys
    import getpass

    if len(sys.argv) < 4:
        print("Advanced Tree-Based Encryption")
        print("=" * 50)
        print("\nUsage:")
        print("  Encrypt: python advanced_tree_crypto.py encrypt <input> <output>")
        print("  Decrypt: python advanced_tree_crypto.py decrypt <input> <output>")
        print("\n⚠️  EDUCATIONAL ONLY - NOT CRYPTOGRAPHICALLY SECURE")
        sys.exit(1)

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    password = getpass.getpass("Enter password: ")

    crypto = AdvancedTreeCrypto(password)

    if mode == 'encrypt':
        print(f"Encrypting {input_file}...")
        crypto.encrypt_file(input_file, output_file)
        print(f"✓ Encrypted to {output_file}")
    elif mode == 'decrypt':
        print(f"Decrypting {input_file}...")
        try:
            crypto.decrypt_file(input_file, output_file)
            print(f"✓ Decrypted to {output_file}")
        except Exception as e:
            print(f"✗ Decryption failed: {e}")
            sys.exit(1)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)


if __name__ == '__main__':
    main()
