import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class CryptoLayer:
    """
    AES-256 Encryption Layer for Ghost Protocol
    
    Provides password-based encryption using Fernet (AES-128-CBC with HMAC)
    with PBKDF2 key derivation for enhanced security.
    """
    
    def __init__(self, salt_length: int = 32):
        self.salt_length = salt_length
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt(self, plaintext: str, password: str) -> str:
        """
        Encrypt plaintext with password
        
        Args:
            plaintext: Text to encrypt
            password: User password
            
        Returns:
            Encrypted string with salt prepended (base64 encoded)
        """
        # Generate random salt
        salt = os.urandom(self.salt_length)
        
        # Derive key
        key = self._derive_key(password, salt)
        
        # Create Fernet instance
        f = Fernet(key)
        
        # Encrypt
        encrypted = f.encrypt(plaintext.encode('utf-8'))
        
        # Combine salt + encrypted data and encode
        combined = salt + encrypted
        return base64.b64encode(combined).decode('utf-8')
    
    def decrypt(self, encrypted_data: str, password: str) -> str:
        """
        Decrypt ciphertext with password
        
        Args:
            encrypted_data: Encrypted string (base64 encoded with salt)
            password: User password
            
        Returns:
            Decrypted plaintext
        """
        try:
            # Decode and separate salt
            combined = base64.b64decode(encrypted_data.encode('utf-8'))
            salt = combined[:self.salt_length]
            encrypted = combined[self.salt_length:]
            
            # Derive key
            key = self._derive_key(password, salt)
            
            # Decrypt
            f = Fernet(key)
            decrypted = f.decrypt(encrypted)
            
            return decrypted.decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Decryption failed - incorrect password or corrupted data") from e
    
    def generate_password(self, length: int = 32) -> str:
        """Generate a secure random password"""
        return base64.urlsafe_b64encode(os.urandom(length)).decode('utf-8')[:length]
    
    def hash_password(self, password: str) -> str:
        """Create a SHA-256 hash of password for verification"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hash_value: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hash_value
