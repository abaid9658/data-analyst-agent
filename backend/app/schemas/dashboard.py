"""
Dashboard Pydantic schemas
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WidgetResponse(BaseModel):
    id: uuid.UUID
    widget_type: str
    title: str | None = None
    config: dict
    grid_x: int
    grid_y: int
    grid_w: int
    grid_h: int
    chart_id: uuid.UUID | None = None
    query_id: uuid.UUID | None = None

    model_config = ConfigDict(from_attributes=True)


class GenerateDashboardRequest(BaseModel):
    session_id: uuid.UUID
    title: str


class DashboardResponse(BaseModel):
    dashboard_id: uuid.UUID
    title: str
    description: str | None = None
    widgets: list[WidgetResponse]
    layout: dict | None = None

    model_config = ConfigDict(from_attributes=True)
