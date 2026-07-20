"""
Query Pydantic schemas
"""
import uuid
from pydantic import BaseModel


class GenerateSQLRequest(BaseModel):
    question: str
    connection_id: uuid.UUID | None = None
    dataset_id: uuid.UUID | None = None


class GenerateSQLResponse(BaseModel):
    sql: str
    explanation: str
    tables_used: list[str]


class ExecuteSQLRequest(BaseModel):
    sql: str
    connection_id: uuid.UUID | None = None
    dataset_id: uuid.UUID | None = None
    limit: int = 1000


class ExecuteSQLResponse(BaseModel):
    columns: list[str]
    rows: list[list]
    row_count: int
    execution_time_ms: int
