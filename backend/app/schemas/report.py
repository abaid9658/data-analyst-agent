"""
Report Pydantic schemas
"""
import uuid
from datetime import datetime
from pydantic import BaseModel


class GenerateReportRequest(BaseModel):
    session_id: uuid.UUID
    format: str = "pdf"  # pdf, docx, pptx, xlsx, markdown
    title: str
    include_sections: list[str] = ["summary", "charts", "insights", "recommendations"]


class GenerateReportResponse(BaseModel):
    report_id: uuid.UUID
    status: str
    task_id: str


class ReportStatusResponse(BaseModel):
    report_id: uuid.UUID
    status: str
    format: str
    title: str
    download_url: str | None = None
    created_at: datetime
    expires_at: datetime | None = None
