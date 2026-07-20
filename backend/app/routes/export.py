"""
Export router — export datasets, queries, and charts to raw files
"""
import logging
from fastapi import APIRouter, Depends, status
from app.middleware.auth import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/csv", status_code=status.HTTP_200_OK)
async def export_to_csv(current_user: User = Depends(get_current_user)):
    """Export query or dataset to CSV file format."""
    return {"message": "Export to CSV initiated"}
