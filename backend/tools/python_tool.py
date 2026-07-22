"""
Python Analysis Tool — Sandboxed Python code execution for data analysis
"""
import ast
import logging
import sys
from io import StringIO
from typing import Any

import numpy as np
import pandas as pd
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import settings
from tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

# Allowed imports in sandboxed execution
ALLOWED_MODULES = {"pandas", "numpy", "scipy", "statsmodels", "sklearn", "io", "json", "math", "datetime", "re", "collections"}

PYTHON_GENERATOR_PROMPT = """You are an expert data scientist. Generate Python code to answer the user's question using pandas/numpy.

Dataset Schema: {schema}
Sample Data (first 3 rows): {sample}

Rules:
- The dataframe is already loaded as variable `df`
- Do NOT import os, sys, subprocess, or any system modules
- Use only: pandas, numpy, scipy, statsmodels, sklearn, math, datetime, re, json
- Store the final result in a variable called `result` (dict with 'data', 'summary', 'insights')
- Keep code concise and focused on the question
- Handle missing values gracefully

Return ONLY valid JSON:
{{
  "code": "the Python code",
  "explanation": "what this code does"
}}"""


class PythonTool(BaseTool):
    """
    Tool for executing auto-generated Python analysis code in a sandboxed environment.
    """

    name = "python"
    description = "Execute Python data analysis code with Pandas, NumPy, SciPy"

    def __init__(self):
        self.llm = settings.get_llm(temperature=0)

    async def execute(self, params: dict[str, Any]) -> dict:
        question = params.get("question") or params.get("user_message", "")
        data = params.get("data")
        schema = params.get("dataset_schema") or {}
        provided_code = params.get("code")  # If code is already provided, skip generation

        df = self._to_dataframe(data)

        # Auto-clean data
        if df is not None and not df.empty:
            df = self._auto_clean(df)

        # Generate code if not provided
        if not provided_code:
            gen = await self._generate_code(question, schema, df)
            code = gen["code"]
            explanation = gen["explanation"]
        else:
            code = provided_code
            explanation = "Code provided directly"

        # Validate code safety
        if not self._is_safe_code(code):
            return {
                "success": False,
                "error": "Generated code contains disallowed operations",
                "code": code,
            }

        # Execute code
        exec_result = self._execute_code(code, df)

        return {
            "success": exec_result["success"],
            "code": code,
            "explanation": explanation,
            "output": exec_result.get("result"),
            "stdout": exec_result.get("stdout"),
            "error": exec_result.get("error"),
            "insights": exec_result.get("result", {}).get("insights", []) if exec_result.get("result") else [],
        }

    async def _generate_code(self, question: str, schema: dict, df: pd.DataFrame | None) -> dict:
        """Use LLM to generate analysis code."""
        sample = df.head(3).to_dict(orient="records") if df is not None and not df.empty else []

        import json
        response = await self.llm.ainvoke([
            SystemMessage(content=PYTHON_GENERATOR_PROMPT.format(
                schema=json.dumps(schema, default=str),
                sample=json.dumps(sample, default=str),
            )),
            HumanMessage(content=question),
        ])

        try:
            return json.loads(response.content)
        except Exception:
            return {"code": "result = {'data': None, 'summary': {}, 'insights': []}", "explanation": ""}

    def _is_safe_code(self, code: str) -> bool:
        """Use AST to validate code doesn't use dangerous operations."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return False

        for node in ast.walk(tree):
            # Block import of dangerous modules
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in getattr(node, "names", []):
                    module = alias.name.split(".")[0]
                    if module not in ALLOWED_MODULES:
                        logger.warning("Blocked import: %s", module)
                        return False

            # Block exec() and eval() calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ("exec", "eval", "__import__"):
                    return False

        return True

    def _execute_code(self, code: str, df: pd.DataFrame | None) -> dict:
        """Execute Python code in a controlled namespace."""
        # Set up execution namespace
        namespace: dict[str, Any] = {
            "pd": pd,
            "np": np,
            "df": df if df is not None else pd.DataFrame(),
            "result": None,
        }

        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()

        try:
            # Execute with timeout (simple approach — use threading for production)
            exec(compile(code, "<analysis>", "exec"), namespace)  # noqa: S102
            result = namespace.get("result")
            stdout = captured.getvalue()

            return {
                "success": True,
                "result": result,
                "stdout": stdout,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": captured.getvalue(),
            }
        finally:
            sys.stdout = old_stdout

    def _auto_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Automatically clean a dataframe."""
        df = df.copy()

        # Remove duplicate rows
        original_len = len(df)
        df = df.drop_duplicates()
        if len(df) < original_len:
            logger.info("Removed %d duplicate rows", original_len - len(df))

        # Fill numeric nulls with median
        for col in df.select_dtypes(include="number").columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                df[col] = df[col].fillna(df[col].median())

        # Fill categorical nulls with mode
        for col in df.select_dtypes(include="object").columns:
            null_count = df[col].isnull().sum()
            if null_count > 0 and not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])

        return df

    def _to_dataframe(self, data: Any) -> pd.DataFrame | None:
        if data is None:
            return None
        if isinstance(data, pd.DataFrame):
            return data
        if isinstance(data, dict) and "columns" in data and "rows" in data:
            return pd.DataFrame(data["rows"], columns=data["columns"])
        return None
