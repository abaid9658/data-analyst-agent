"""
Unit tests for VisualizationTool Plotly specification builders
"""
import pytest
import pandas as pd
from tools.visualization_tool import VisualizationTool

viz_tool = VisualizationTool()


@pytest.mark.asyncio
async def test_generate_bar_chart():
    """Test generating standard bar charts with column data mappings."""
    df = pd.DataFrame({
        "category": ["A", "B", "C"],
        "values": [10, 20, 15]
    })
    res = await viz_tool.execute({
        "data": df,
        "chart_type": "bar",
        "x_column": "category",
        "y_column": "values",
        "title": "Test Bar Chart",
    })
    assert res["success"] is True
    assert res["chart_type"] == "bar"
    assert "plotly_spec" in res
    assert res["plotly_spec"]["data"][0]["type"] == "bar"
