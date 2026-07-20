"""
Auth routes — registration, login, OAuth, token refresh, logout
"""
import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.base import get_db
from app.database.redis import get_redis
from app.models.session import UserSession
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    UserResponse,
)
from app.utils.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def _make_auth_response(user: User, access_token: str, refresh_token: str) -> AuthResponse:
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


async def _save_session(
    db: AsyncSession,
    user_id: UUID,
    refresh_token: str,
    request: Request | None = None,
) -> None:
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    session = UserSession(
        user_id=user_id,
        refresh_token=refresh_token,
        expires_at=expires_at,
        ip_address=request.client.host if request and request.client else None,
        user_agent=request.headers.get("user-agent") if request else None,
    )
    db.add(session)
    await db.flush()


# ─── Register ────────────────────────────────────────────────────────────────

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user account."""
    # Check email uniqueness
    existing = await db.execute(select(User).where(User.email == body.email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user = User(
        email=body.email,
        full_name=body.full_name,
        password_hash=hash_password(body.password),
        role="analyst",
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    logger.info("New user registered: %s", user.email)
    return UserResponse.model_validate(user)


# ─── Login ────────────────────────────────────────────────────────────────────

@router.post("/login", response_model=AuthResponse)
async def login(
    body: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Login with email and password."""
    result = await db.execute(
        select(User).where(User.email == body.email, User.is_active == True)
    )
    user = result.scalar_one_or_none()

    if not user or not user.password_hash or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Update last login
    await db.execute(
        update(User)
        .where(User.id == user.id)
        .values(last_login=datetime.now(timezone.utc))
    )

    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token()
    await _save_session(db, user.id, refresh_token, request)

    logger.info("User logged in: %s", user.email)
    return _make_auth_response(user, access_token, refresh_token)


# ─── Token Refresh ───────────────────────────────────────────────────────────

@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
    body: RefreshRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token using a valid refresh token (token rotation)."""
    now = datetime.now(timezone.utc)

    result = await db.execute(
        select(UserSession)
        .join(User)
        .where(
            UserSession.refresh_token == body.refresh_token,
            UserSession.is_revoked == False,
            UserSession.expires_at > now,
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    # Revoke old session (rotation)
    await db.execute(
        update(UserSession)
        .where(UserSession.id == session.id)
        .values(is_revoked=True)
    )

    # Get user
    user = await db.get(User, session.user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # Issue new tokens
    new_access = create_access_token(user.id, user.role)
    new_refresh = create_refresh_token()
    await _save_session(db, user.id, new_refresh, request)

    return _make_auth_response(user, new_access, new_refresh)


# ─── Logout ──────────────────────────────────────────────────────────────────

@router.post("/logout")
async def logout(
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """Revoke the current refresh token."""
    await db.execute(
        update(UserSession)
        .where(UserSession.refresh_token == body.refresh_token)
        .values(is_revoked=True)
    )
    return {"message": "Logged out successfully"}


# ─── Google OAuth ─────────────────────────────────────────────────────────────

@router.get("/google")
async def google_login():
    """Redirect to Google OAuth."""
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return RedirectResponse(f"https://accounts.google.com/o/oauth2/v2/auth?{query}")


@router.get("/google/callback")
async def google_callback(
    code: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Handle Google OAuth callback."""
    async with httpx.AsyncClient() as client:
        # Exchange code for tokens
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_resp.json()
        id_token = token_data.get("id_token", "")

        # Get user info
        user_resp = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token_data.get('access_token')}"},
        )
        google_user = user_resp.json()

    google_id = google_user.get("sub")
    email = google_user.get("email")
    name = google_user.get("name", "")
    avatar = google_user.get("picture")

    # Upsert user
    result = await db.execute(select(User).where(User.google_id == google_id))
    user = result.scalar_one_or_none()

    if not user:
        # Check by email
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user:
            user.google_id = google_id
        else:
            user = User(
                email=email,
                full_name=name,
                google_id=google_id,
                avatar_url=avatar,
                is_verified=True,
            )
            db.add(user)
            await db.flush()

    await db.refresh(user)
    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token()
    await _save_session(db, user.id, refresh_token, request)

    # Redirect to frontend with tokens
    return RedirectResponse(
        f"{settings.FRONTEND_URL}/auth/callback"
        f"?access_token={access_token}&refresh_token={refresh_token}"
    )


# ─── GitHub OAuth ────────────────────────────────────────────────────────────

@router.get("/github")
async def github_login():
    """Redirect to GitHub OAuth."""
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
        "scope": "user:email",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return RedirectResponse(f"https://github.com/login/oauth/authorize?{query}")


@router.get("/github/callback")
async def github_callback(
    code: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Handle GitHub OAuth callback."""
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            json={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        token_data = token_resp.json()
        gh_token = token_data.get("access_token")

        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {gh_token}", "Accept": "application/json"},
        )
        email_resp = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"token {gh_token}", "Accept": "application/json"},
        )
        github_user = user_resp.json()
        emails = email_resp.json()

    github_id = str(github_user.get("id"))
    name = github_user.get("name") or github_user.get("login", "")
    avatar = github_user.get("avatar_url")
    primary_email = next(
        (e["email"] for e in emails if e.get("primary") and e.get("verified")),
        None,
    )

    if not primary_email:
        raise HTTPException(status_code=400, detail="No verified email found on GitHub account")

    # Upsert user
    result = await db.execute(select(User).where(User.github_id == github_id))
    user = result.scalar_one_or_none()

    if not user:
        result = await db.execute(select(User).where(User.email == primary_email))
        user = result.scalar_one_or_none()
        if user:
            user.github_id = github_id
        else:
            user = User(
                email=primary_email,
                full_name=name,
                github_id=github_id,
                avatar_url=avatar,
                is_verified=True,
            )
            db.add(user)
            await db.flush()

    await db.refresh(user)
    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token()
    await _save_session(db, user.id, refresh_token, request)

    return RedirectResponse(
        f"{settings.FRONTEND_URL}/auth/callback"
        f"?access_token={access_token}&refresh_token={refresh_token}"
    )
