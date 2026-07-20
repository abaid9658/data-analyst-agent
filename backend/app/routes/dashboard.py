"""
Dashboard router — auto-generate dashboards from chat insights and manage layouts
"""
import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_db
from app.middleware.auth import get_current_user
from app.models.dashboard import Dashboard, DashboardWidget
from app.models.user import User
from app.schemas.dashboard import DashboardResponse, GenerateDashboardRequest

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/auto-generate", response_model=DashboardResponse, status_code=status.HTTP_201_CREATED)
async def auto_generate_dashboard(
    body: GenerateDashboardRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Auto-generate dashboard widgets from past conversation charts/queries."""
    # Find generated charts/queries in this conversation
    from app.models.generated_chart import GeneratedChart
    from app.models.message import Message

    result = await db.execute(
        select(GeneratedChart)
        .join(Message)
        .where(
            Message.conversation_id == body.session_id,
            GeneratedChart.user_id == current_user.id,
        )
        .limit(6)
    )
    charts = result.scalars().all()

    if not charts:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No charts or visualizations found in conversation history to build dashboard.",
        )

    # Create dashboard
    dashboard = Dashboard(
        user_id=current_user.id,
        title=body.title,
        description=f"Auto-generated from session {body.session_id}",
    )
    db.add(dashboard)
    await db.flush()

    # Create widgets for each chart found
    x = 0
    y = 0
    for chart in charts:
        widget = DashboardWidget(
            dashboard_id=dashboard.id,
            widget_type="chart",
            title=chart.title or "Chart Widget",
            config={"theme": "dark"},
            grid_x=x,
            grid_y=y,
            grid_w=4,
            grid_h=3,
            chart_id=chart.id,
        )
        db.add(widget)
        # Advance layout coordinates
        x += 4
        if x >= 12:
            x = 0
            y += 3

    await db.flush()
    await db.commit()

    # Reload dashboard with widgets
    res = await db.execute(
        select(Dashboard).where(Dashboard.id == dashboard.id)
    )
    dashboard_loaded = res.scalar_one()

    return DashboardResponse(
        dashboard_id=dashboard_loaded.id,
        title=dashboard_loaded.title,
        description=dashboard_loaded.description,
        widgets=dashboard_loaded.widgets,
        layout=dashboard_loaded.layout,
    )
