"""
Encryption utilities using Cryptography Fernet
"""
from cryptography.fernet import Fernet
from app.config import settings


def get_fernet() -> Fernet:
    """Get Fernet instance using the configured encryption key."""
    key = settings.ENCRYPTION_KEY.encode()
    return Fernet(key)


def encrypt_data(data: str) -> bytes:
    """Encrypt a string and return ciphertext bytes."""
    f = get_fernet()
    return f.encrypt(data.encode())


def decrypt_data(ciphertext: bytes) -> str:
    """Decrypt ciphertext bytes and return the original string."""
    f = get_fernet()
    return f.decrypt(ciphertext).decode()
