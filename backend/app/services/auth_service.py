"""
Auth Service handling business logic for authentication
"""
import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.session import UserSession
from app.repositories.user_repo import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, UserResponse
from app.utils.exceptions import InvalidCredentialsError, EmailAlreadyExistsError
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.config import settings

logger = logging.getLogger(__name__)


class AuthService:
    """Service for handling Authentication business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register(self, data: RegisterRequest) -> User:
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise EmailAlreadyExistsError()

        user = User(
            email=data.email,
            full_name=data.full_name,
            password_hash=hash_password(data.password),
            role="analyst",
        )
        await self.user_repo.create(user)
        logger.info("Registered user: %s", user.email)
        return user

    async def login(self, data: LoginRequest, ip_address: str | None = None, user_agent: str | None = None) -> AuthResponse:
        user = await self.user_repo.get_by_email(data.email)
        if not user or not user.is_active or not user.password_hash:
            raise InvalidCredentialsError()

        if not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsError()

        user.last_login = datetime.now(timezone.utc)
        self.db.add(user)

        access_token = create_access_token(user.id, user.role)
        refresh_token = create_refresh_token()

        # Save session
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        session = UserSession(
            user_id=user.id,
            refresh_token=refresh_token,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(session)
        await self.db.flush()

        logger.info("User login success: %s", user.email)
        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user),
        )
