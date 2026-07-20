"""
Visualization Tool — Automatic Plotly chart generation
"""
import json
import logging
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.config import settings
from tools.base_tool import BaseTool

logger = logging.getLogger(__name__)


CHART_SELECTOR_PROMPT = """You are a data visualization expert. Choose the best chart type for the given data and question.

User Question: {question}
Data Columns: {columns}
Data Types: {dtypes}
Sample Data: {sample}

Available chart types: bar, line, scatter, pie, histogram, heatmap, boxplot, treemap, sunburst, area

Return ONLY JSON:
{{
  "chart_type": "chosen_type",
  "x_column": "column_name_or_null",
  "y_column": "column_name_or_null",
  "color_column": "column_name_or_null",
  "title": "descriptive chart title",
  "reasoning": "why this chart type was chosen"
}}"""


class VisualizationTool(BaseTool):
    """
    Automatically generates Plotly interactive charts.
    """

    name = "visualization"
    description = "Generate interactive charts and visualizations"

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0,
            response_format={"type": "json_object"},
        )

    async def execute(self, params: dict[str, Any]) -> dict:
        question = params.get("question") or params.get("user_message", "")
        data = params.get("data")  # pandas DataFrame or dict with columns+rows
        chart_type = params.get("chart_type", "auto")

        # Convert data to DataFrame
        df = self._to_dataframe(data)
        if df is None or df.empty:
            return {"success": False, "error": "No data available to visualize"}

        # Auto-select chart type if not specified
        if chart_type == "auto":
            chart_config = await self._select_chart_type(question, df)
        else:
            chart_config = {
                "chart_type": chart_type,
                "x_column": params.get("x_column"),
                "y_column": params.get("y_column"),
                "color_column": params.get("color_column"),
                "title": params.get("title", ""),
                "reasoning": f"{chart_type} chart as requested",
            }

        # Generate Plotly figure
        fig = self._generate_chart(df, chart_config)

        return {
            "success": True,
            "chart_type": chart_config["chart_type"],
            "title": chart_config["title"],
            "plotly_spec": json.loads(fig.to_json()),
            "explanation": chart_config.get("reasoning", ""),
            "insights": self._extract_chart_insights(df, chart_config),
        }

    async def _select_chart_type(self, question: str, df: pd.DataFrame) -> dict:
        """Use LLM to select the best chart type."""
        sample = df.head(3).to_dict(orient="records")
        dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

        response = await self.llm.ainvoke([
            SystemMessage(content=CHART_SELECTOR_PROMPT.format(
                question=question,
                columns=list(df.columns),
                dtypes=dtypes,
                sample=json.dumps(sample, default=str),
            )),
            HumanMessage(content="Select the best chart type"),
        ])

        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback to bar chart
            return {
                "chart_type": "bar",
                "x_column": df.columns[0] if len(df.columns) > 0 else None,
                "y_column": df.columns[1] if len(df.columns) > 1 else None,
                "color_column": None,
                "title": "Data Analysis",
                "reasoning": "Default bar chart",
            }

    def _generate_chart(self, df: pd.DataFrame, config: dict) -> go.Figure:
        """Generate a Plotly figure based on config."""
        chart_type = config["chart_type"]
        x = config.get("x_column")
        y = config.get("y_column")
        color = config.get("color_column")
        title = config.get("title", "")

        # Validate columns exist
        x = x if x and x in df.columns else (df.columns[0] if len(df.columns) > 0 else None)
        y = y if y and y in df.columns else (df.columns[1] if len(df.columns) > 1 else None)
        color = color if color and color in df.columns else None

        kwargs = dict(data_frame=df, x=x, y=y, title=title, color=color)
        # Remove None values
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        match chart_type:
            case "bar":
                fig = px.bar(**kwargs)
            case "line":
                fig = px.line(**kwargs)
            case "scatter":
                fig = px.scatter(**kwargs)
            case "pie":
                fig = px.pie(df, names=x, values=y, title=title)
            case "histogram":
                fig = px.histogram(df, x=x, title=title, color=color)
            case "heatmap":
                numeric_df = df.select_dtypes(include="number")
                corr = numeric_df.corr()
                fig = px.imshow(corr, title=title or "Correlation Matrix", text_auto=True)
            case "boxplot":
                fig = px.box(**kwargs)
            case "treemap":
                path = [col for col in [color, x] if col and col in df.columns]
                fig = px.treemap(df, path=path or [x], values=y, title=title)
            case "sunburst":
                path = [col for col in [color, x] if col and col in df.columns]
                fig = px.sunburst(df, path=path or [x], values=y, title=title)
            case "area":
                fig = px.area(**kwargs)
            case _:
                fig = px.bar(**kwargs)

        # Apply consistent styling
        fig = self._apply_theme(fig)
        return fig

    def _apply_theme(self, fig: go.Figure) -> go.Figure:
        """Apply a consistent dark theme to all charts."""
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(15,15,26,0)",
            plot_bgcolor="rgba(15,15,26,0)",
            font=dict(family="Inter, sans-serif", size=13, color="#C4C6D0"),
            title=dict(font=dict(size=16, color="#E2E3EA"), x=0.02),
            legend=dict(
                bgcolor="rgba(28,28,46,0.8)",
                bordercolor="#252540",
                borderwidth=1,
            ),
            margin=dict(l=40, r=20, t=50, b=40),
        )
        return fig

    def _to_dataframe(self, data: Any) -> pd.DataFrame | None:
        """Convert various data formats to DataFrame."""
        if data is None:
            return None
        if isinstance(data, pd.DataFrame):
            return data
        if isinstance(data, dict) and "columns" in data and "rows" in data:
            return pd.DataFrame(data["rows"], columns=data["columns"])
        if isinstance(data, list):
            return pd.DataFrame(data)
        return None

    def _extract_chart_insights(self, df: pd.DataFrame, config: dict) -> list[str]:
        """Extract simple insights from the chart data."""
        insights = []
        try:
            y_col = config.get("y_column")
            if y_col and y_col in df.columns and pd.api.types.is_numeric_dtype(df[y_col]):
                max_val = df[y_col].max()
                min_val = df[y_col].min()
                x_col = config.get("x_column")
                if x_col and x_col in df.columns:
                    max_label = df.loc[df[y_col].idxmax(), x_col]
                    insights.append(f"Highest {y_col}: {max_label} ({max_val:,.2f})")
                    min_label = df.loc[df[y_col].idxmin(), x_col]
                    insights.append(f"Lowest {y_col}: {min_label} ({min_val:,.2f})")
        except Exception:
            pass
        return insights
