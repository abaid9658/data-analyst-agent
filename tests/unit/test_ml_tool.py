"""
Unit tests for MLTool prediction pipelines
"""
import pytest
import pandas as pd
from tools.ml_tool import MLTool

ml_tool = MLTool()


@pytest.mark.asyncio
async def test_ml_regression_pipeline():
    """Test standard regression problem auto-detection and execution."""
    df = pd.DataFrame({
        "x1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y": [2, 4, 5, 4, 5, 6, 7, 8, 9, 11]
    })
    res = await ml_tool.execute({
        "data": df,
        "problem_type": "regression",
        "target_column": "y",
    })
    assert res["success"] is True
    assert "metrics" in res
    assert "predictions" in res
