"""
Chart Pydantic schemas
"""
import uuid
from pydantic import BaseModel


class GenerateChartRequest(BaseModel):
    dataset_id: uuid.UUID
    chart_type: str = "auto"
    x_column: str | None = None
    y_column: str | None = None
    color_column: str | None = None
    title: str | None = None


class GenerateChartResponse(BaseModel):
    chart_id: uuid.UUID
    chart_type: str
    plotly_spec: dict
    explanation: str
    download_urls: dict[str, str]
