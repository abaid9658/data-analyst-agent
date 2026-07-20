"""
Upload Service handling file ingestion, schema detection, and profiling
"""
import io
import logging
import uuid
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.dataset_repo import DatasetRepository
from app.models.dataset import Dataset, DatasetProfile
from app.utils.storage import download_file_from_storage
from app.utils.exceptions import DatasetNotFoundError

logger = logging.getLogger(__name__)


async def load_dataset_file(dataset_id: str | uuid.UUID) -> pd.DataFrame:
    """Load a dataset file from storage and return as a Pandas DataFrame."""
    # Since we need a DB session or can fetch from storage directly, let's load from storage
    # We will get the dataset record first to know the storage path & type
    # For helper execution, we'll download using storage utility
    from app.database.base import async_session_maker
    async with async_session_maker() as db:
        repo = DatasetRepository(db)
        dataset = await repo.get_by_id(uuid.UUID(str(dataset_id)))
        if not dataset:
            raise DatasetNotFoundError(dataset_id=uuid.UUID(str(dataset_id)))

        file_bytes = await download_file_from_storage(dataset.storage_path)

        if dataset.file_type == "csv":
            return pd.read_csv(io.BytesIO(file_bytes))
        elif dataset.file_type == "excel":
            return pd.read_excel(io.BytesIO(file_bytes))
        elif dataset.file_type == "json":
            return pd.read_json(io.BytesIO(file_bytes))
        else:
            raise ValueError(f"Unsupported file type: {dataset.file_type}")


class UploadService:
    """Service for handling file uploads, schema parsing, and profiling."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = DatasetRepository(db)

    async def get_dataset(self, dataset_id: uuid.UUID) -> Dataset:
        dataset = await self.repo.get_by_id(dataset_id)
        if not dataset:
            raise DatasetNotFoundError(dataset_id=dataset_id)
        return dataset

    async def profile_dataset(self, dataset_id: uuid.UUID) -> DatasetProfile:
        """Perform statistical data profiling on the dataset and save it."""
        dataset = await self.get_dataset(dataset_id)
        df = await load_dataset_file(dataset_id)

        # Basic Stats
        row_count = len(df)
        col_count = len(df.columns)

        # Inferred schema
        schema_cols = []
        data_types = {}
        missing_values = {}
        numeric_stats = {}
        categorical_stats = {}

        for col in df.columns:
            dtype_str = str(df[col].dtype)
            data_types[col] = dtype_str
            null_count = int(df[col].isnull().sum())
            missing_values[col] = null_count

            schema_cols.append({
                "name": col,
                "type": dtype_str,
                "nullable": null_count > 0,
            })

            # Calculate detailed column stats
            if pd.api.types.is_numeric_dtype(df[col]):
                col_clean = df[col].dropna()
                if not col_clean.empty:
                    numeric_stats[col] = {
                        "mean": float(col_clean.mean()),
                        "std": float(col_clean.std()) if len(col_clean) > 1 else 0.0,
                        "min": float(col_clean.min()),
                        "max": float(col_clean.max()),
                        "p25": float(col_clean.quantile(0.25)),
                        "p50": float(col_clean.quantile(0.50)),
                        "p75": float(col_clean.quantile(0.75)),
                    }
            else:
                col_clean = df[col].dropna()
                unique_vals = col_clean.nunique()
                top_vals = col_clean.value_counts().head(5).to_dict()
                categorical_stats[col] = {
                    "unique_count": unique_vals,
                    "top_values": [{"value": str(k), "count": int(v)} for k, v in top_vals.items()],
                }

        # Save profile
        profile = DatasetProfile(
            dataset_id=dataset_id,
            missing_values=missing_values,
            duplicate_rows=int(df.duplicated().sum()),
            data_types=data_types,
            numeric_stats=numeric_stats,
            categorical_stats=categorical_stats,
        )

        dataset.schema = {"columns": schema_cols}
        dataset.row_count = row_count
        dataset.column_count = col_count
        dataset.status = "ready"

        await self.repo.create_profile(profile)
        self.db.add(dataset)
        await self.db.flush()

        logger.info("Dataset profiled successfully: %s", dataset_id)
        return profile
