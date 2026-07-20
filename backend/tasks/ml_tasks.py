"""
Celery ML background tasks — forecasting, clustering, anomaly detection
"""
import asyncio
import logging
import uuid
from asgiref.sync import async_to_sync
from tasks.celery_app import celery_app
from app.database.base import async_session_maker

logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.ml_tasks.run_ml_analysis_task", bind=True)
def run_ml_analysis_task(self, dataset_id: str, problem_type: str, target_column: str | None = None):
    """Background Celery task to run ML analysis on a dataset asynchronously."""
    logger.info(
        "Starting ML task: dataset=%s problem=%s target=%s (task_id=%s)",
        dataset_id, problem_type, target_column, self.request.id
    )

    async def _run():
        from app.services.upload_service import load_dataset_file
        from tools.ml_tool import MLTool

        # Load dataset
        df = await load_dataset_file(dataset_id)
        ml_tool = MLTool()

        # Execute ML pipeline
        result = await ml_tool.execute({
            "data": df,
            "problem_type": problem_type,
            "target_column": target_column,
        })

        return {
            "dataset_id": dataset_id,
            "problem_type": problem_type,
            "status": "success" if result.get("success") else "error",
            "metrics": result.get("metrics", {}),
            "predictions_count": len(result.get("predictions", [])),
        }

    try:
        return async_to_sync(_run)()
    except Exception as e:
        logger.error("ML task failed for dataset %s: %s", dataset_id, e)
        raise e
