"""
Dataset Factory for generating test Dataset records
"""
import uuid
from app.models.dataset import Dataset


class DatasetFactory:
    """Helper factory class to build Dataset instances for tests."""

    @staticmethod
    def build(
        user_id: uuid.UUID,
        name: str = "test_data",
        file_type: str = "csv",
        status: str = "ready",
    ) -> Dataset:
        return Dataset(
            id=uuid.uuid4(),
            user_id=user_id,
            name=name,
            file_type=file_type,
            status=status,
            row_count=100,
            column_count=5,
        )
