"""
SQL generation prompt templates
"""
import json


SQL_GENERATOR_SYSTEM = """You are an expert SQL query writer.

Given a user's question in plain English and the dataset schema, generate a correct, safe, read-only SQL SELECT query.

Rules:
1. ALWAYS use SELECT only. Never generate INSERT, UPDATE, DELETE, DROP, ALTER.
2. Use proper JOINs based on the schema.
3. Always add LIMIT clause (max 1000 rows).
4. Use aliases for readability.
5. Add ORDER BY when relevant.

Return ONLY a JSON object:
{
  "sql": "Your SQL query here",
  "explanation": "Plain English explanation of what the query does",
  "tables_used": ["table1", "table2"]
}"""


def build_sql_prompt(question: str, schema: dict) -> str:
    """Build the SQL generation prompt with schema context."""
    schema_str = json.dumps(schema, default=str)
    return f"""User Question: {question}

Dataset Schema:
{schema_str}

Generate the SQL query."""
