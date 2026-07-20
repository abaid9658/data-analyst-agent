"""
Celery tasks for file upload processing, statistical profiling, and PDF indexing.
"""
import asyncio
import logging
import uuid
from asgiref.sync import async_to_sync
from tasks.celery_app import celery_app
from app.database.base import async_session_maker
from app.services.upload_service import UploadService

logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.upload_tasks.parse_dataset_task", bind=True)
def parse_dataset_task(self, dataset_id: str):
    """Background task to parse and profile an uploaded dataset file.
    For PDF files, also indexes their text content into Qdrant.
    """
    logger.info("Starting processing for dataset: %s (task_id=%s)", dataset_id, self.request.id)

    async def _run():
        async with async_session_maker() as db:
            service = UploadService(db)

            # Load the dataset record to check file type
            from app.repositories.dataset_repo import DatasetRepository
            repo = DatasetRepository(db)
            dataset = await repo.get_by_id(uuid.UUID(dataset_id))

            if dataset and dataset.file_type == "pdf":
                # PDF path: download raw bytes from storage, then index into Qdrant
                from app.utils.storage import download_file_from_storage
                from app.services.pdf_service import index_pdf_into_qdrant

                try:
                    content = await download_file_from_storage(dataset.storage_path)
                    total_chunks = await index_pdf_into_qdrant(
                        content=content,
                        dataset_id=dataset_id,
                    )
                    logger.info(
                        "PDF indexed: %d chunks for dataset %s", total_chunks, dataset_id
                    )
                    # Mark PDF datasets as ready immediately (no tabular profiling)
                    dataset.status = "ready"
                    dataset.row_count = total_chunks  # repurpose field as chunk count
                    db.add(dataset)
                    await db.commit()
                    return {"dataset_id": dataset_id, "status": "success", "chunks": total_chunks}
                except Exception as pdf_err:
                    logger.error("PDF indexing failed for %s: %s", dataset_id, pdf_err)
                    dataset.status = "error"
                    dataset.error_message = str(pdf_err)
                    db.add(dataset)
                    await db.commit()
                    raise pdf_err

            # Structured file path (CSV / Excel / JSON)
            profile = await service.profile_dataset(uuid.UUID(dataset_id))
            await db.commit()
            return {
                "dataset_id": dataset_id,
                "status": "success",
                "duplicate_rows": profile.duplicate_rows,
            }

    try:
        result = async_to_sync(_run)()
        return result
    except Exception as e:
        logger.error("Failed to process dataset %s: %s", dataset_id, e)
        async def _mark_error():
            async with async_session_maker() as db:
                from app.repositories.dataset_repo import DatasetRepository
                repo = DatasetRepository(db)
                dataset = await repo.get_by_id(uuid.UUID(dataset_id))
                if dataset:
                    dataset.status = "error"
                    dataset.error_message = str(e)
                    db.add(dataset)
                    await db.commit()
        try:
            async_to_sync(_mark_error)()
        except Exception as db_err:
            logger.error("Failed to save error status to DB for dataset %s: %s", dataset_id, db_err)
        raise e
