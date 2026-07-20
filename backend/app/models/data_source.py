"""
DataSource ORM Model
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, LargeBinary, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # postgresql, mysql, sqlite, sqlserver, mongodb

    # Encrypted connection details (Fernet encrypted JSON)
    encrypted_config: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    # Metadata
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")  # active, error, disabled
    last_connected: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    tables_cache: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user = relationship("User", back_populates="data_sources")

    def __repr__(self) -> str:
        return f"<DataSource id={self.id} name={self.name} type={self.type}>"
