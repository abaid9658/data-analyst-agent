"""
Settings router — manage user profile, theme, and application preferences
"""
import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.base import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.auth import UserResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()


class UpdateProfileRequest(BaseModel):
    full_name: str | None = None
    preferences: dict | None = None


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Retrieve current user profile data and preferences."""
    return UserResponse.model_validate(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    body: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update profile details and dashboard/chart preferences."""
    if body.full_name is not None:
        current_user.full_name = body.full_name

    if body.preferences is not None:
        # Merge dicts
        current_user.preferences = {**current_user.preferences, **body.preferences}

    db.add(current_user)
    await db.flush()
    await db.commit()

    return UserResponse.model_validate(current_user)
