"""
SQL Tool — Natural language to SQL generation, validation, and execution
"""
import logging
import re
from typing import Any

from app.config import settings
from langchain_core.messages import HumanMessage, SystemMessage
from sqlalchemy import text

from app.config import settings
from tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

# ─── SQL Injection / Safety Patterns ─────────────────────────────────────────

DANGEROUS_SQL_PATTERNS = [
    r"\bDROP\s+(TABLE|DATABASE|INDEX)\b",
    r"\bTRUNCATE\b",
    r"\bDELETE\s+FROM\b(?!\s+\w+\s+WHERE)",  # DELETE without WHERE
    r"\bUPDATE\b(?!.*\bWHERE\b)",             # UPDATE without WHERE
    r"\bINSERT\s+INTO\b",
    r"\bALTER\s+TABLE\b",
    r"\bCREATE\s+(TABLE|DATABASE)\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bEXEC\b",
    r"\bEXECUTE\b",
    r";\s*--",                                 # Comment after semicolon
    r"'[^']*'\s*OR\s*'[^']*'\s*=\s*'[^']*'", # Classic OR injection
]


SQL_GENERATOR_PROMPT = """You are an expert SQL analyst. Convert the user's natural language question into a clean, optimized SQL query.

Dataset Schema:
{schema}

Rules:
- Generate only SELECT queries (read-only)
- Use proper JOINs when needed
- Always add appropriate LIMIT (default 1000 unless user asks for all)
- Use date functions appropriate to the database type
- Format SQL cleanly with proper indentation
- Do NOT include any DML/DDL (INSERT, UPDATE, DELETE, DROP, CREATE, ALTER)

Return ONLY valid JSON with this exact structure:
{{
  "sql": "the SQL query",
  "explanation": "plain English explanation of what this query does",
  "tables_used": ["table1", "table2"],
  "estimated_complexity": "simple|medium|complex"
}}"""


class SQLTool(BaseTool):
    """
    Tool that converts natural language to SQL, validates it, and executes it.
    """

    name = "sql"
    description = "Convert natural language to SQL queries and execute them"

    def __init__(self):
        self.llm = settings.get_llm(temperature=0)

    async def execute(self, params: dict[str, Any]) -> dict:
        question = params.get("question") or params.get("user_message", "")
        schema = params.get("dataset_schema") or {}
        connection_id = params.get("connection_id")
        dataset_id = params.get("dataset_id")

        # Step 1: Generate SQL
        sql_result = await self._generate_sql(question, schema)

        # Step 2: Validate SQL
        validation = self._validate_sql(sql_result["sql"])
        if not validation["safe"]:
            return {
                "success": False,
                "error": f"Generated SQL failed safety check: {validation['reason']}",
                "sql": sql_result["sql"],
            }

        # Step 3: Execute SQL (if connection available)
        table_data = None
        if connection_id or dataset_id:
            try:
                table_data = await self._execute_sql(sql_result["sql"], connection_id, dataset_id)
            except Exception as e:
                logger.error("SQL execution failed: %s", e)
                return {
                    "success": True,
                    "sql": sql_result["sql"],
                    "explanation": sql_result["explanation"],
                    "execution_error": str(e),
                }

        return {
            "success": True,
            "sql": sql_result["sql"],
            "explanation": sql_result["explanation"],
            "tables_used": sql_result.get("tables_used", []),
            "table_data": table_data,
            "insights": self._generate_sql_insights(table_data),
        }

    async def _generate_sql(self, question: str, schema: dict) -> dict:
        """Use LLM to generate SQL from natural language."""
        schema_str = self._format_schema(schema)
        prompt = SQL_GENERATOR_PROMPT.format(schema=schema_str)

        response = await self.llm.ainvoke([
            SystemMessage(content=prompt),
            HumanMessage(content=question),
        ])

        import json
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback: extract SQL from text
            return {
                "sql": response.content,
                "explanation": "SQL generated from your question",
                "tables_used": [],
            }

    def _validate_sql(self, sql: str) -> dict:
        """Check SQL for dangerous patterns."""
        sql_upper = sql.upper()
        for pattern in DANGEROUS_SQL_PATTERNS:
            if re.search(pattern, sql_upper, re.IGNORECASE | re.MULTILINE):
                return {"safe": False, "reason": f"Pattern matched: {pattern}"}
        return {"safe": True, "reason": ""}

    async def _execute_sql(
        self, sql: str, connection_id: str | None, dataset_id: str | None
    ) -> dict:
        """Execute SQL against the appropriate data source."""
        # For dataset files — load into pandas and use pandasql
        if dataset_id and not connection_id:
            return await self._execute_on_dataset(sql, dataset_id)

        # For live database connections
        if connection_id:
            return await self._execute_on_connection(sql, connection_id)

        return {"columns": [], "rows": [], "row_count": 0}

    async def _execute_on_dataset(self, sql: str, dataset_id: str) -> dict:
        """Execute SQL on an uploaded dataset using DuckDB."""
        import duckdb
        from app.services.upload_service import load_dataset_file

        df = await load_dataset_file(dataset_id)
        conn = duckdb.connect()
        conn.register("data", df)

        # Replace common table names with "data"
        result = conn.execute(sql).fetchdf()
        return {
            "columns": result.columns.tolist(),
            "rows": result.values.tolist()[:1000],
            "row_count": len(result),
        }

    async def _execute_on_connection(self, sql: str, connection_id: str) -> dict:
        """Execute SQL on a live database connection."""
        from app.services.database_service import get_connection_engine

        engine = await get_connection_engine(connection_id)
        async with engine.connect() as conn:
            result = await conn.execute(text(sql))
            columns = list(result.keys())
            rows = [list(row) for row in result.fetchmany(1000)]
            return {
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
            }

    def _format_schema(self, schema: dict) -> str:
        """Format schema dict as readable string for the LLM."""
        if not schema:
            return "No schema available."
        lines = []
        for table, info in schema.items():
            lines.append(f"Table: {table}")
            if isinstance(info, dict) and "columns" in info:
                for col in info["columns"]:
                    name = col.get("name", col) if isinstance(col, dict) else col
                    dtype = col.get("type", "unknown") if isinstance(col, dict) else "unknown"
                    lines.append(f"  - {name}: {dtype}")
        return "\n".join(lines)

    def _generate_sql_insights(self, table_data: dict | None) -> list[str]:
        """Generate basic insights from query result."""
        if not table_data or not table_data.get("rows"):
            return []
        insights = [f"Query returned {table_data['row_count']} rows"]
        return insights
