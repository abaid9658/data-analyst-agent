"""
Query router — NL to SQL generation and execution
"""
import logging
import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_db
from app.middleware.auth import get_current_user, require_analyst
from app.models.user import User
from app.schemas.query import (
    ExecuteSQLRequest,
    ExecuteSQLResponse,
    GenerateSQLRequest,
    GenerateSQLResponse,
)
from tools.sql_tool import SQLTool

logger = logging.getLogger(__name__)
router = APIRouter()
sql_tool = SQLTool()


@router.post("/generate", response_model=GenerateSQLResponse)
async def generate_sql(
    body: GenerateSQLRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate SQL from natural language description."""
    # Obtain dataset schema if dataset_id provided
    schema = {}
    if body.dataset_id:
        from app.models.dataset import Dataset
        dataset = await db.get(Dataset, body.dataset_id)
        if dataset and dataset.schema:
            schema = dataset.schema

    try:
        result = await sql_tool._generate_sql(body.question, schema)
        return GenerateSQLResponse(
            sql=result["sql"],
            explanation=result["explanation"],
            tables_used=result.get("tables_used", []),
        )
    except Exception as e:
        logger.error("SQL generation failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to generate SQL: {e}",
        )


@router.post("/execute", response_model=ExecuteSQLResponse)
async def execute_sql(
    body: ExecuteSQLRequest,
    current_user: User = Depends(require_analyst),
):
    """Execute a raw SQL query safely with read-only validation."""
    # Validate safety
    val = sql_tool._validate_sql(body.sql)
    if not val["safe"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Safety check failed: {val['reason']}",
        )

    start_time = time.time()
    try:
        result = await sql_tool._execute_sql(
            sql=body.sql,
            connection_id=str(body.connection_id) if body.connection_id else None,
            dataset_id=str(body.dataset_id) if body.dataset_id else None,
        )
        latency = int((time.time() - start_time) * 1000)

        return ExecuteSQLResponse(
            columns=result.get("columns", []),
            rows=result.get("rows", []),
            row_count=result.get("row_count", 0),
            execution_time_ms=latency,
        )
    except Exception as e:
        logger.error("SQL execution failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Execution error: {e}",
        )
