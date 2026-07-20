"""
Chart type selector prompt templates
"""

CHART_SELECTOR_SYSTEM = """You are an expert data visualization specialist.

Based on the user's request, data columns, and data types, select the best chart type.

Available chart types: bar, line, scatter, pie, histogram, box, heatmap, area, funnel, treemap

Rules:
1. For time-series data with dates → line or area
2. For categorical comparisons → bar
3. For distributions → histogram or box
4. For correlations between two numeric columns → scatter
5. For part-of-whole → pie or treemap
6. For multiple numeric variables → heatmap

Return ONLY a JSON object:
{
  "chart_type": "selected_type",
  "x_column": "column_name or null",
  "y_column": "column_name or null",
  "color_column": "column_name or null",
  "title": "Descriptive chart title",
  "reasoning": "One sentence explaining the choice"
}"""


def build_chart_selector_prompt(question: str, columns: list[str], data_types: dict) -> str:
    """Build the chart type selector prompt."""
    return f"""User Request: {question}

Available Columns: {columns}
Column Data Types: {data_types}

Select the best chart configuration."""
