"""
Database Connection router — save, test, list, delete connections
"""
import json
import logging
import time
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_db
from app.middleware.auth import get_current_user, require_analyst
from app.models.data_source import DataSource
from app.models.user import User
from app.schemas.database import (
    ConnectRequest,
    ConnectionListResponse,
    ConnectionResponse,
    TestConnectionRequest,
    TestConnectionResponse,
)
from app.services.database_service import DatabaseService
from app.utils.encryption import encrypt_data

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/connect", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
async def connect_database(
    body: ConnectRequest,
    current_user: User = Depends(require_analyst),
    db: AsyncSession = Depends(get_db),
):
    """Test and save a new database connection."""
    # Test connection first
    config_dict = body.config.model_dump()
    try:
        await DatabaseService.test_connection(config_dict, body.type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Connection test failed: {e}",
        )

    # Encrypt connection details
    encrypted_config = encrypt_data(json.dumps(config_dict))

    # Save to DB
    data_source = DataSource(
        user_id=current_user.id,
        name=body.name,
        type=body.type,
        encrypted_config=encrypted_config,
        status="active",
    )
    db.add(data_source)
    await db.flush()
    await db.commit()

    return ConnectionResponse.model_validate(data_source)


@router.post("/test", response_model=TestConnectionResponse)
async def test_database_connection(
    body: TestConnectionRequest,
    current_user: User = Depends(require_analyst),
):
    """Test database connection parameters without saving."""
    start_time = time.time()
    try:
        result = await DatabaseService.test_connection(body.config.model_dump(), body.type)
        latency = int((time.time() - start_time) * 1000)
        return TestConnectionResponse(
            status="success",
            latency_ms=latency,
            tables_count=result.get("tables_count", 0),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.get("/connections", response_model=ConnectionListResponse)
async def list_connections(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all saved database connections for current user."""
    result = await db.execute(
        select(DataSource).where(DataSource.user_id == current_user.id)
    )
    data_sources = result.scalars().all()
    return ConnectionListResponse(
        connections=[ConnectionResponse.model_validate(ds) for ds in data_sources]
    )


@router.delete("/connections/{connection_id}")
async def delete_connection(
    connection_id: uuid.UUID,
    current_user: User = Depends(require_analyst),
    db: AsyncSession = Depends(get_db),
):
    """Delete a saved connection."""
    result = await db.execute(
        select(DataSource).where(
            DataSource.id == connection_id,
            DataSource.user_id == current_user.id,
        )
    )
    data_source = result.scalar_one_or_none()
    if not data_source:
        raise HTTPException(status_code=404, detail="Connection not found")

    await db.delete(data_source)
    await db.commit()
    return {"message": "Connection deleted"}
