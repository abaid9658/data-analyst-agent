"""
GeneratedChart ORM Model
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class GeneratedChart(Base):
    __tablename__ = "generated_charts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    message_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
    )

    chart_type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # bar, line, scatter, pie, etc.
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    plotly_spec: Mapped[dict] = mapped_column(JSONB, nullable=False)  # full Plotly figure spec
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Storage paths for exports
    png_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    svg_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    user = relationship("User")
    message = relationship("Message", back_populates="generated_charts")
