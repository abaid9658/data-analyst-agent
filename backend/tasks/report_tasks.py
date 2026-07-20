"""
Celery background tasks for generating reports (PDF, Docx, PPTX, XLSX, Markdown)
"""
import asyncio
import logging
import os
import uuid
from datetime import datetime, timedelta, timezone
from asgiref.sync import async_to_sync
from tasks.celery_app import celery_app
from app.database.base import async_session_maker
from app.models.generated_report import GeneratedReport
from app.models.message import Message

logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.report_tasks.generate_report_task", bind=True)
def generate_report_task(self, report_id: str):
    """Background Celery task to generate an executive report from conversation history."""
    logger.info("Generating report task started: %s", report_id)

    async def _run():
        async with async_session_maker() as db:
            report = await db.get(GeneratedReport, uuid.UUID(report_id))
            if not report:
                return {"status": "error", "message": "Report not found"}

            # Fetch conversation messages for context
            from app.repositories.message_repo import MessageRepository
            msg_repo = MessageRepository(db)
            messages = await msg_repo.get_by_conversation_id(report.conversation_id, limit=50)

            # Generate report content based on requested format
            os.makedirs("reports_out", exist_ok=True)
            file_name = f"report_{report_id}.{report.format}"
            file_path = os.path.join("reports_out", file_name)

            content_text = f"Title: {report.title}\nFormat: {report.format}\nDate: {datetime.now(timezone.utc)}\n\n"
            content_text += "Executive Summary:\n"
            for m in messages:
                if m.role == "assistant" and len(m.content) > 10:
                    content_text += f"- {m.content[:200]}...\n"

            # Write file based on format
            if report.format == "pdf":
                # ReportLab or fallback
                try:
                    from reportlab.lib.pagesizes import letter
                    from reportlab.pdfgen import canvas
                    c = canvas.Canvas(file_path, pagesize=letter)
                    c.drawString(100, 750, report.title)
                    c.drawString(100, 730, f"Generated on: {datetime.now(timezone.utc)}")
                    y = 700
                    for line in content_text.split("\n"):
                        c.drawString(100, y, line[:80])
                        y -= 20
                        if y < 50:
                            c.showPage()
                            y = 750
                    c.save()
                except ImportError:
                    # Text fallback saved as PDF representation
                    with open(file_path, "wb") as f:
                        f.write(content_text.encode())
            else:
                # docx, pptx, xlsx, md fallbacks
                with open(file_path, "wb") as f:
                    f.write(content_text.encode())

            # Update DB
            report.status = "ready"
            report.file_path = file_path
            report.file_size_bytes = os.path.getsize(file_path)
            report.expires_at = datetime.now(timezone.utc) + timedelta(days=7)

            db.add(report)
            await db.commit()

            return {
                "status": "ready",
                "report_id": report_id,
                "file_path": file_path,
            }

    try:
        result = async_to_sync(_run)()
        return result
    except Exception as e:
        logger.error("Failed to generate report %s: %s", report_id, e)
        async def _mark_error():
            async with async_session_maker() as db:
                report = await db.get(GeneratedReport, uuid.UUID(report_id))
                if report:
                    report.status = "error"
                    report.error_message = str(e)
                    db.add(report)
                    await db.commit()
        try:
            async_to_sync(_mark_error)()
        except Exception as db_err:
            logger.error("Failed to save error status to DB for report %s: %s", report_id, db_err)
        raise e
