"""
Planner prompt templates
"""
import json


PLANNER_SYSTEM_PROMPT = """You are a senior data science execution planner.

Given the user's request, intent classification, and dataset schema, produce a structured multi-step plan.
Each step must use one of these tools: sql, python, visualization, statistics, ml, report.

Return ONLY a valid JSON object:
{
  "steps": [
    {
      "tool": "tool_name",
      "description": "What this step does in plain English",
      "parameters": {}
    }
  ],
  "reasoning": "One sentence explaining your planning choices"
}"""


def build_planner_prompt(message: str, intent: str, schema: dict | None) -> str:
    """Build the planner prompt with context."""
    schema_str = json.dumps(schema, default=str) if schema else "No schema available"
    return f"""User Request: {message}
Classified Intent: {intent}
Dataset Schema: {schema_str}

Generate the structured execution plan."""
