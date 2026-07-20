"""
Database Service handling external database connections
"""
import json
import logging
import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from app.utils.encryption import decrypt_data
from app.database.base import async_session_maker
from app.models.data_source import DataSource
from app.utils.exceptions import ConnectionTestFailedError

logger = logging.getLogger(__name__)


async def get_connection_engine(connection_id: str | uuid.UUID) -> AsyncEngine:
    """Decrypt DataSource configuration and return a SQLAlchemy AsyncEngine."""
    from app.database.base import async_session_maker
    async with async_session_maker() as db:
        result = await db.get(DataSource, uuid.UUID(str(connection_id)))
        if not result:
            raise ConnectionTestFailedError("Connection source not found")

        # Decrypt config
        decrypted_json = decrypt_data(result.encrypted_config)
        config = json.loads(decrypted_json)

        # Build url based on database type
        db_type = result.type
        host = config.get("host")
        port = config.get("port")
        username = config.get("username")
        password = config.get("password")
        database = config.get("database")

        if db_type == "postgresql":
            url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "mysql":
            url = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "sqlite":
            url = f"sqlite+aiosqlite:///{database}"
        elif db_type == "sqlserver":
            url = f"mssql+pyodbc://{username}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
        else:
            raise ValueError(f"Unsupported connection type: {db_type}")

        return create_async_engine(url, pool_pre_ping=True)


class DatabaseService:
    """Service for handling testing and CRUD operations on database connections."""

    @staticmethod
    async def test_connection(config: dict, db_type: str) -> dict:
        """Test database connection without saving."""
        host = config.get("host")
        port = config.get("port")
        username = config.get("username")
        password = config.get("password")
        database = config.get("database")

        # Select async driver for testing
        if db_type == "postgresql":
            url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "mysql":
            url = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "sqlite":
            url = f"sqlite+aiosqlite:///{database}"
        elif db_type == "sqlserver":
            url = f"mssql+pyodbc://{username}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
        else:
            raise ConnectionTestFailedError("Unsupported connection type")

        try:
            # We create an async engine, connect, and execute a simple query
            engine = create_async_engine(url, connect_args={"timeout": 5} if db_type == "postgresql" else {})
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            await engine.dispose()
            return {"status": "success", "tables_count": 0}
        except Exception as e:
            logger.error("Database connection test failed: %s", e)
            raise ConnectionTestFailedError(str(e))
