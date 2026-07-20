"""
Upload Pydantic schemas
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UploadResponse(BaseModel):
    dataset_id: uuid.UUID
    name: str
    status: str
    task_id: str
    message: str


class DatasetResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    original_filename: str | None = None
    file_type: str | None = None
    file_size_bytes: int | None = None
    row_count: int | None = None
    column_count: int | None = None
    schema: dict | None = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DatasetListResponse(BaseModel):
    datasets: list[DatasetResponse]
    total: int
