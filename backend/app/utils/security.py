"""
Security utilities — password hashing, JWT tokens, encryption
"""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from cryptography.fernet import Fernet
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

# ─── Password Hashing ────────────────────────────────────────────────────────

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ─── JWT Tokens ───────────────────────────────────────────────────────────────

def create_access_token(user_id: UUID, role: str) -> str:
    """Create a short-lived access token."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token() -> str:
    """Create a cryptographically secure refresh token."""
    return secrets.token_urlsafe(64)


def decode_access_token(token: str) -> dict:
    """Decode and validate an access token."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        if payload.get("type") != "access":
            raise JWTError("Invalid token type")
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {e}") from e


# ─── Fernet Encryption (for DB credentials) ──────────────────────────────────

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


# ─── Utilities ────────────────────────────────────────────────────────────────

def generate_fernet_key() -> str:
    """Generate a new Fernet encryption key — use for ENCRYPTION_KEY env var."""
    return Fernet.generate_key().decode()
