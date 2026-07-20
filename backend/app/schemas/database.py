"""
Database connections Pydantic schemas
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ConnectionConfig(BaseModel):
    host: str
    port: int
    database: str
    username: str
    password: str
    ssl: bool = False


class ConnectRequest(BaseModel):
    name: str
    type: str = Field(..., description="postgresql, mysql, sqlite, sqlserver, mongodb")
    config: ConnectionConfig


class TestConnectionRequest(BaseModel):
    type: str
    config: ConnectionConfig


class TestConnectionResponse(BaseModel):
    status: str
    latency_ms: int | None = None
    tables_count: int


class ConnectionResponse(BaseModel):
    id: uuid.UUID
    name: str
    type: str
    status: str
    last_connected: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ConnectionListResponse(BaseModel):
    connections: list[ConnectionResponse]
