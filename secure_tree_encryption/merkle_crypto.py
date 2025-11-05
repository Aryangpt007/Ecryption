#!/usr/bin/env python3
"""
Secure Tree-Based Encryption System using Merkle Trees
======================================================

This implementation provides cryptographically secure encryption using:
- AES-256-GCM for authenticated encryption
- Merkle trees for data integrity verification
- PBKDF2 for key derivation
- Hierarchical key derivation tree
- SHA-256 for hashing

Author: Educational Implementation
License: MIT
"""

import os
import hashlib
import json
import base64
from typing import List, Optional, Tuple, Dict, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class MerkleNode:
    """
    Node in a Merkle tree for integrity verification.

    Leaf nodes contain encrypted data.
    Internal nodes contain hash of children.
    """

    def __init__(self, data: Optional[bytes] = None, left: Optional['MerkleNode'] = None,
                 right: Optional['MerkleNode'] = None):
        self.data = data
        self.left = left
        self.right = right
        self.hash = self._calculate_hash()

    def _calculate_hash(self) -> bytes:
        """Calculate SHA-256 hash of node."""
        if self.data is not None:
            # Leaf node: hash the data
            return hashlib.sha256(self.data).digest()
        elif self.left and self.right:
            # Internal node: hash concatenation of children
            return hashlib.sha256(self.left.hash + self.right.hash).digest()
        elif self.left:
            # Only left child
            return self.left.hash
        else:
            # Empty node
            return hashlib.sha256(b'').digest()

    def is_leaf(self) -> bool:
        """Check if node is a leaf."""
        return self.data is not None


class KeyDerivationTree:
    """
    Hierarchical key derivation tree.

    Derives unique keys for each data block based on tree position.
    Provides forward secrecy: compromising one key doesn't reveal others.
    """

    def __init__(self, master_key: bytes):
        """
        Initialize key derivation tree.

        Args:
            master_key: 32-byte master key derived from password
        """
        if len(master_key) != 32:
            raise ValueError("Master key must be 32 bytes")
        self.master_key = master_key

    def derive_key(self, path: List[int]) -> bytes:
        """
        Derive key for specific tree position.

        Args:
            path: List of indices representing path in tree (e.g., [0, 1, 2])

        Returns:
            32-byte derived key
        """
        # Use HKDF-like construction: Hash(master_key || path)
        path_bytes = json.dumps(path).encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=path_bytes,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(self.master_key)


class SecureTreeEncryption:
    """
    Main encryption class using Merkle tree structure.

    Features:
    - AES-256-GCM authenticated encryption
    - Merkle tree integrity verification
    - Hierarchical key derivation
    - Chunked encryption for large files
    """

    CHUNK_SIZE = 4096  # 4KB chunks
    NONCE_SIZE = 12    # GCM standard nonce size
    KEY_SIZE = 32      # AES-256 key size
    SALT_SIZE = 16     # Salt for PBKDF2

    def __init__(self, password: str, salt: Optional[bytes] = None):
        """
        Initialize encryption system.

        Args:
            password: User password for key derivation
            salt: Optional salt (generated if not provided)
        """
        self.salt = salt if salt else os.urandom(self.SALT_SIZE)
        self.master_key = self._derive_master_key(password)
        self.kdf_tree = KeyDerivationTree(self.master_key)

    def _derive_master_key(self, password: str) -> bytes:
        """
        Derive master key from password using PBKDF2.

        Args:
            password: User password

        Returns:
            32-byte master key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.KEY_SIZE,
            salt=self.salt,
            iterations=480000,  # OWASP 2023 recommendation
            backend=default_backend()
        )
        return kdf.derive(password.encode('utf-8'))

    def _encrypt_chunk(self, data: bytes, key: bytes) -> Tuple[bytes, bytes]:
        """
        Encrypt single data chunk with AES-256-GCM.

        Args:
            data: Data to encrypt
            key: 32-byte encryption key

        Returns:
            Tuple of (nonce, ciphertext_with_tag)
        """
        nonce = os.urandom(self.NONCE_SIZE)
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, data, None)
        return nonce, ciphertext

    def _decrypt_chunk(self, nonce: bytes, ciphertext: bytes, key: bytes) -> bytes:
        """
        Decrypt single data chunk with AES-256-GCM.

        Args:
            nonce: 12-byte nonce
            ciphertext: Encrypted data with authentication tag
            key: 32-byte encryption key

        Returns:
            Decrypted plaintext

        Raises:
            cryptography.exceptions.InvalidTag: If authentication fails
        """
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext

    def _split_into_chunks(self, data: bytes) -> List[bytes]:
        """Split data into fixed-size chunks."""
        chunks = []
        for i in range(0, len(data), self.CHUNK_SIZE):
            chunks.append(data[i:i + self.CHUNK_SIZE])
        return chunks

    def _build_merkle_tree(self, leaf_data: List[bytes]) -> MerkleNode:
        """
        Build Merkle tree from leaf data.

        Args:
            leaf_data: List of data for leaf nodes

        Returns:
            Root node of Merkle tree
        """
        if not leaf_data:
            return MerkleNode(data=b'')

        # Create leaf nodes
        nodes = [MerkleNode(data=chunk) for chunk in leaf_data]

        # Build tree bottom-up
        while len(nodes) > 1:
            new_level = []
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i + 1] if i + 1 < len(nodes) else None
                parent = MerkleNode(left=left, right=right)
                new_level.append(parent)
            nodes = new_level

        return nodes[0]

    def encrypt(self, plaintext: bytes) -> Dict[str, Any]:
        """
        Encrypt data using tree-based encryption.

        Args:
            plaintext: Data to encrypt

        Returns:
            Dictionary containing:
            - encrypted_chunks: List of encrypted chunks with nonces
            - merkle_root: Root hash for integrity verification
            - salt: Salt used for key derivation
            - metadata: Additional metadata
        """
        # Split data into chunks
        chunks = self._split_into_chunks(plaintext)

        # Encrypt each chunk with derived key
        encrypted_chunks = []
        leaf_hashes = []

        for idx, chunk in enumerate(chunks):
            # Derive unique key for this chunk based on position
            chunk_key = self.kdf_tree.derive_key([idx])

            # Encrypt chunk
            nonce, ciphertext = self._encrypt_chunk(chunk, chunk_key)

            # Store encrypted chunk
            encrypted_chunks.append({
                'nonce': base64.b64encode(nonce).decode('utf-8'),
                'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
                'index': idx
            })

            # Calculate hash for Merkle tree (hash of nonce + ciphertext)
            chunk_data = nonce + ciphertext
            leaf_hashes.append(chunk_data)

        # Build Merkle tree for integrity
        merkle_root = self._build_merkle_tree(leaf_hashes)

        return {
            'version': '1.0',
            'encrypted_chunks': encrypted_chunks,
            'merkle_root': base64.b64encode(merkle_root.hash).decode('utf-8'),
            'salt': base64.b64encode(self.salt).decode('utf-8'),
            'chunk_size': self.CHUNK_SIZE,
            'num_chunks': len(chunks),
            'metadata': {
                'algorithm': 'AES-256-GCM',
                'kdf': 'PBKDF2-SHA256',
                'iterations': 480000,
                'tree_type': 'Merkle'
            }
        }

    def decrypt(self, encrypted_data: Dict[str, Any], verify_integrity: bool = True) -> bytes:
        """
        Decrypt data and verify integrity.

        Args:
            encrypted_data: Dictionary from encrypt() method
            verify_integrity: Whether to verify Merkle tree integrity

        Returns:
            Decrypted plaintext

        Raises:
            ValueError: If integrity check fails
            cryptography.exceptions.InvalidTag: If authentication fails
        """
        # Verify version
        if encrypted_data.get('version') != '1.0':
            raise ValueError("Unsupported encryption version")

        encrypted_chunks = encrypted_data['encrypted_chunks']
        stored_root = base64.b64decode(encrypted_data['merkle_root'])

        # Decrypt chunks
        decrypted_chunks = []
        leaf_hashes = []

        for chunk_info in encrypted_chunks:
            idx = chunk_info['index']
            nonce = base64.b64decode(chunk_info['nonce'])
            ciphertext = base64.b64decode(chunk_info['ciphertext'])

            # Derive same key used for encryption
            chunk_key = self.kdf_tree.derive_key([idx])

            # Decrypt (will raise InvalidTag if tampered)
            plaintext = self._decrypt_chunk(nonce, ciphertext, chunk_key)
            decrypted_chunks.append((idx, plaintext))

            # Store for integrity check
            chunk_data = nonce + ciphertext
            leaf_hashes.append(chunk_data)

        # Verify Merkle tree integrity
        if verify_integrity:
            computed_root = self._build_merkle_tree(leaf_hashes)
            if computed_root.hash != stored_root:
                raise ValueError("Integrity check failed: Merkle root mismatch")

        # Sort by index and concatenate
        decrypted_chunks.sort(key=lambda x: x[0])
        plaintext = b''.join(chunk[1] for chunk in decrypted_chunks)

        return plaintext

    def encrypt_file(self, input_path: str, output_path: str):
        """
        Encrypt file and save to output.

        Args:
            input_path: Path to plaintext file
            output_path: Path to save encrypted file (JSON format)
        """
        with open(input_path, 'rb') as f:
            plaintext = f.read()

        encrypted_data = self.encrypt(plaintext)

        with open(output_path, 'w') as f:
            json.dump(encrypted_data, f, indent=2)

    def decrypt_file(self, input_path: str, output_path: str):
        """
        Decrypt file and save to output.

        Args:
            input_path: Path to encrypted file (JSON format)
            output_path: Path to save decrypted file
        """
        with open(input_path, 'r') as f:
            encrypted_data = json.load(f)

        plaintext = self.decrypt(encrypted_data)

        with open(output_path, 'wb') as f:
            f.write(plaintext)


def main():
    """Example usage and CLI interface."""
    import sys
    import getpass

    if len(sys.argv) < 4:
        print("Usage:")
        print("  Encrypt: python merkle_crypto.py encrypt <input_file> <output_file>")
        print("  Decrypt: python merkle_crypto.py decrypt <input_file> <output_file>")
        sys.exit(1)

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    # Get password securely
    password = getpass.getpass("Enter password: ")

    if mode == 'encrypt':
        print(f"Encrypting {input_file}...")
        encryptor = SecureTreeEncryption(password)
        encryptor.encrypt_file(input_file, output_file)
        print(f"✓ Encrypted file saved to {output_file}")
        print(f"✓ Salt: {base64.b64encode(encryptor.salt).decode()}")
        print("\nKeep this salt safe! You'll need it for decryption.")

    elif mode == 'decrypt':
        print(f"Decrypting {input_file}...")

        # Load salt from encrypted file
        with open(input_file, 'r') as f:
            encrypted_data = json.load(f)

        salt = base64.b64decode(encrypted_data['salt'])
        decryptor = SecureTreeEncryption(password, salt=salt)

        try:
            decryptor.decrypt_file(input_file, output_file)
            print(f"✓ Decrypted file saved to {output_file}")
            print("✓ Integrity verification passed")
        except Exception as e:
            print(f"✗ Decryption failed: {e}")
            sys.exit(1)

    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)


if __name__ == '__main__':
    main()
