"""
History router — fetch analysis activity history
"""
import logging
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.base import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.generated_query import GeneratedQuery

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("")
async def get_history(
    page: int = 1,
    limit: int = 20,
    search: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve historical queries and activities run by the user."""
    query = select(GeneratedQuery).where(GeneratedQuery.user_id == current_user.id)
    if search:
        query = query.where(GeneratedQuery.natural_language.ilike(f"%{search}%"))

    query = query.order_by(GeneratedQuery.created_at.desc()).offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    # Map to expected schema format
    formatted_items = []
    for item in items:
        formatted_items.append({
            "id": str(item.id),
            "type": "query",
            "question": item.natural_language,
            "dataset_name": item.sql_query[:100],  # Quick preview
            "created_at": item.created_at.isoformat(),
        })

    return {
        "items": formatted_items,
        "total": len(formatted_items),
        "page": page,
        "limit": limit,
    }
