"""
User Factory for generating test User records
"""
import uuid
from app.models.user import User


class UserFactory:
    """Helper factory class to build User instances for tests."""

    @staticmethod
    def build(
        email: str = "test@example.com",
        full_name: str = "Test User",
        password_hash: str = "hashed_pass",
        role: str = "analyst",
    ) -> User:
        return User(
            id=uuid.uuid4(),
            email=email,
            full_name=full_name,
            password_hash=password_hash,
            role=role,
            is_active=True,
            is_verified=True,
        )
