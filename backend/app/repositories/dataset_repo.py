"""
Dataset Repository for database access
"""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dataset import Dataset, DatasetProfile


class DatasetRepository:
    """Repository for managing Dataset and DatasetProfile DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, dataset_id: uuid.UUID) -> Dataset | None:
        result = await self.db.execute(select(Dataset).where(Dataset.id == dataset_id))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: uuid.UUID, page: int = 1, limit: int = 20) -> list[Dataset]:
        result = await self.db.execute(
            select(Dataset)
            .where(Dataset.user_id == user_id)
            .order_by(Dataset.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, dataset: Dataset) -> Dataset:
        self.db.add(dataset)
        await self.db.flush()
        return dataset

    async def create_profile(self, profile: DatasetProfile) -> DatasetProfile:
        self.db.add(profile)
        await self.db.flush()
        return profile

    async def delete(self, dataset: Dataset) -> None:
        await self.db.delete(dataset)
        await self.db.flush()
