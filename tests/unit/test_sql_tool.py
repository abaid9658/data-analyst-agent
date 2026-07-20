"""
Unit tests for SQLTool safety and validation logic
"""
import pytest
from tools.sql_tool import SQLTool

sql_tool = SQLTool()


def test_sql_validation_safe():
    """Test standard SELECT statements are marked safe."""
    res = sql_tool._validate_sql("SELECT name, revenue FROM sales LIMIT 10")
    assert res["safe"] is True


def test_sql_validation_unsafe_drop():
    """Test DROP statements are intercepted and flagged unsafe."""
    res = sql_tool._validate_sql("DROP TABLE users")
    assert res["safe"] is False
    assert "DROP" in res["reason"]


def test_sql_validation_unsafe_delete():
    """Test DELETE statements are flagged unsafe."""
    res = sql_tool._validate_sql("DELETE FROM transactions")
    assert res["safe"] is False
    assert "DELETE" in res["reason"]
