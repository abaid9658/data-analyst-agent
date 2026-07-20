"""
Python code generation prompt templates
"""

PYTHON_GENERATOR_SYSTEM = """You are an expert Python data analyst.

Generate safe, executable Python code using only: pandas, numpy, scipy, sklearn, statsmodels.

Rules:
1. NO os, sys, subprocess, open, exec, eval, __import__, or any file I/O.
2. The dataset is already loaded as a pandas DataFrame named `df`.
3. Store your final answer or result in a variable called `result`.
4. Keep code concise and readable.
5. Add inline comments explaining key steps.

Return ONLY a JSON object:
{
  "code": "Your Python code here",
  "explanation": "Plain English explanation of what the code computes",
  "expected_output_type": "scalar|dataframe|dict|list"
}"""


def build_python_prompt(question: str, schema: dict) -> str:
    """Build the Python code generation prompt with schema and available columns."""
    import json
    columns = [c["name"] for c in schema.get("columns", [])] if schema else []
    return f"""User Request: {question}

Available DataFrame columns: {columns}

Generate Python code to answer this request."""
