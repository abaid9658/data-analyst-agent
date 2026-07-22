"""
Database base — SQLAlchemy async engine and session factory
"""
import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Alias used by Celery task files
async_session_maker = AsyncSessionLocal


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — yields an async DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Create all tables (for dev/testing — use Alembic in production)."""
    from app.models import (  # noqa: F401 — import all models so Base knows them
        user,
        session,
        data_source,
        dataset,
        conversation,
        message,
        generated_query,
        generated_chart,
        generated_report,
        dashboard,
        audit_log,
    )
    async with engine.begin() as conn:
        # In production, rely on Alembic — this is for dev convenience
        if settings.APP_ENV == "development":
            await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")
