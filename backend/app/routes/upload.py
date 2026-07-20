"""
Upload route — CSV, Excel, JSON file uploads with background processing
"""
import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database.base import get_db
from app.middleware.auth import get_current_user, require_analyst
from app.models.dataset import Dataset
from app.models.user import User
from app.schemas.upload import DatasetListResponse, DatasetResponse, UploadResponse
from app.utils.exceptions import FileTooLargeError, UnsupportedFileTypeError
from app.utils.storage import upload_file_to_storage

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_MIME_TYPES = {
    "text/csv",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/json",
    "text/plain",  # Some CSV files
    "application/pdf",
}

ALLOWED_EXTENSIONS = {".csv", ".xls", ".xlsx", ".json", ".pdf"}

FILE_TYPE_MAP = {
    ".csv": "csv",
    ".xls": "excel",
    ".xlsx": "excel",
    ".json": "json",
    ".pdf": "pdf",
}


@router.post("/file", response_model=UploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_file(
    file: UploadFile = File(...),
    name: str | None = Form(None),
    description: str | None = Form(None),
    current_user: User = Depends(require_analyst),
    db: AsyncSession = Depends(get_db),
):
    """Upload a CSV, Excel, or JSON dataset file."""
    # Validate file extension
    filename = file.filename or ""
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{ext}' not supported. Use: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Read file content and check size
    content = await file.read()
    file_size = len(content)

    if file_size > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB",
        )

    # Create dataset record
    dataset = Dataset(
        user_id=current_user.id,
        name=name or filename,
        description=description,
        original_filename=filename,
        file_type=FILE_TYPE_MAP.get(ext, "unknown"),
        file_size_bytes=file_size,
        status="processing",
    )
    db.add(dataset)
    await db.flush()
    await db.refresh(dataset)

    # Upload to object storage
    storage_path = await upload_file_to_storage(
        content=content,
        filename=f"datasets/{current_user.id}/{dataset.id}{ext}",
    )
    dataset.storage_path = storage_path
    await db.flush()

    # Queue background parsing task
    from tasks.upload_tasks import parse_dataset_task
    task = parse_dataset_task.delay(str(dataset.id))

    logger.info("File uploaded: %s (dataset_id=%s)", filename, dataset.id)

    return UploadResponse(
        dataset_id=dataset.id,
        name=dataset.name,
        status="processing",
        task_id=task.id,
        message="File uploaded successfully. Processing in background.",
    )


@router.get("/status/{task_id}")
async def get_upload_status(
    task_id: str,
    current_user: User = Depends(get_current_user),
):
    """Check the processing status of an uploaded file."""
    from tasks.celery_app import celery_app

    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None,
    }


@router.get("/datasets", response_model=DatasetListResponse)
async def list_datasets(
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all uploaded datasets for the current user."""
    result = await db.execute(
        select(Dataset)
        .where(Dataset.user_id == current_user.id)
        .order_by(Dataset.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    datasets = result.scalars().all()
    return DatasetListResponse(
        datasets=[DatasetResponse.model_validate(d) for d in datasets],
        total=len(datasets),
    )


@router.get("/datasets/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get dataset details."""
    result = await db.execute(
        select(Dataset).where(
            Dataset.id == dataset_id,
            Dataset.user_id == current_user.id,
        )
    )
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return DatasetResponse.model_validate(dataset)


@router.delete("/datasets/{dataset_id}")
async def delete_dataset(
    dataset_id: uuid.UUID,
    current_user: User = Depends(require_analyst),
    db: AsyncSession = Depends(get_db),
):
    """Delete a dataset."""
    result = await db.execute(
        select(Dataset).where(
            Dataset.id == dataset_id,
            Dataset.user_id == current_user.id,
        )
    )
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Delete from storage
    if dataset.storage_path:
        from app.utils.storage import delete_file_from_storage
        await delete_file_from_storage(dataset.storage_path)

    # If this was a PDF dataset, remove its Qdrant vectors too
    if dataset.file_type == "pdf":
        from app.services.qdrant_service import delete_dataset_chunks
        try:
            await delete_dataset_chunks(dataset_id=str(dataset_id))
        except Exception as qdrant_err:
            logger.warning("Qdrant cleanup failed for dataset %s: %s", dataset_id, qdrant_err)

    await db.delete(dataset)
    return {"message": "Dataset deleted successfully"}
