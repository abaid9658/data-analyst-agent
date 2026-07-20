"""
Unit tests for PythonTool safe execution sandbox
"""
import pytest
import pandas as pd
from tools.python_tool import PythonTool

py_tool = PythonTool()


@pytest.mark.asyncio
async def test_python_tool_safe_execution():
    """Test basic computations execute successfully."""
    code = "result = 2 + 2"
    res = await py_tool.execute({"code": code})
    assert res["success"] is True
    assert res["output"]["result"] == 4


@pytest.mark.asyncio
async def test_python_tool_unsafe_import():
    """Test that OS module imports are intercepted and blocked."""
    code = "import os\nos.system('ls')"
    res = await py_tool.execute({"code": code})
    assert res["success"] is False
    assert "Import of 'os' is not allowed" in res["error"] or "not allowed" in res["error"]
