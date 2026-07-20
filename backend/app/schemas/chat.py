"""
Chat Pydantic schemas
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.auth import UserResponse


class SendMessageRequest(BaseModel):
    message: str
    session_id: uuid.UUID | None = None
    dataset_id: uuid.UUID | None = None
    connection_id: uuid.UUID | None = None
    stream: bool = True


class MessageResponse(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    metadata: dict | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    processing_time_ms: int | None = None
    model_used: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationResponse(BaseModel):
    id: uuid.UUID
    title: str | None = None
    dataset_id: uuid.UUID | None = None
    data_source_id: uuid.UUID | None = None
    message_count: int
    is_pinned: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationListResponse(BaseModel):
    sessions: list[ConversationResponse]


class MessageListResponse(BaseModel):
    session_id: uuid.UUID
    messages: list[MessageResponse]
