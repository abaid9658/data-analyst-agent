"""
Message ORM Model
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # user, assistant, system
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Rich metadata for assistant messages (SQL, charts, insights, plan)
    msg_metadata: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    @property
    def metadata(self) -> dict | None:
        return self.msg_metadata

    @metadata.setter
    def metadata(self, value: dict | None) -> None:
        self.msg_metadata = value

    # Token usage
    prompt_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completion_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Processing info
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    generated_queries = relationship("GeneratedQuery", back_populates="message", cascade="all, delete-orphan")
    generated_charts = relationship("GeneratedChart", back_populates="message", cascade="all, delete-orphan")
