"""
Report router — trigger, track, and download generated PDF/Docx/PPTX reports
"""
import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_db
from app.middleware.auth import get_current_user
from app.models.generated_report import GeneratedReport
from app.models.user import User
from app.schemas.report import (
    GenerateReportRequest,
    GenerateReportResponse,
    ReportStatusResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate", response_model=GenerateReportResponse, status_code=status.HTTP_202_ACCEPTED)
async def generate_report(
    body: GenerateReportRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Trigger background report generation task."""
    report = GeneratedReport(
        user_id=current_user.id,
        conversation_id=body.session_id,
        title=body.title,
        format=body.format,
        status="generating",
        sections={"included": body.include_sections},
    )
    db.add(report)
    await db.flush()

    # Queue background task (Celery)
    from tasks.report_tasks import generate_report_task
    task = generate_report_task.delay(str(report.id))

    await db.commit()

    return GenerateReportResponse(
        report_id=report.id,
        status="generating",
        task_id=task.id,
    )


@router.get("/{report_id}", response_model=ReportStatusResponse)
async def get_report_status(
    report_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve the generation status of a report."""
    report = await db.get(GeneratedReport, report_id)
    if not report or report.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Report not found")

    download_url = None
    if report.status == "ready":
        download_url = f"/report/{report.id}/download"

    return ReportStatusResponse(
        report_id=report.id,
        status=report.status,
        format=report.format,
        title=report.title,
        download_url=download_url,
        created_at=report.created_at,
        expires_at=report.expires_at,
    )


@router.get("/{report_id}/download")
async def download_report(
    report_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Download a completed report file."""
    report = await db.get(GeneratedReport, report_id)
    if not report or report.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.status != "ready" or not report.file_path:
        raise HTTPException(status_code=400, detail="Report is not ready for download")

    return FileResponse(
        path=report.file_path,
        filename=f"{report.title.replace(' ', '_')}.{report.format}",
    )
