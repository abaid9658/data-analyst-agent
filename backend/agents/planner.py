"""
Agent Planner node — planning execution steps
✅ Uses Gemini (free) via settings.get_llm()
"""
import json
import logging
import re
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import settings
from agents.state import ExecutionPlan, PlanStep

logger = logging.getLogger(__name__)

PLANNER_PROMPT = """You are a senior data science planner. Break down the user's request into a structured sequence of execution steps.

User Request: {message}
Intent: {intent}
Dataset Schema: {schema}

Available Tools:
- sql: Run database queries, aggregates, joins.
- python: Run complex calculations, cleaning, statistical formulas.
- visualization: Render interactive Plotly charts.
- statistics: Descriptive summaries, hypothesis tests, distributions.
- ml: Clustering, time series forecasting, regressions.
- report: Build summaries, business recommendations.

Return ONLY a JSON object matching this schema:
{{
  "steps": [
    {{
      "tool": "tool_name",
      "description": "Short human readable description of the step",
      "parameters": {{}}
    }}
  ],
  "reasoning": "Brief explanation of the plan"
}}"""


async def create_plan(
    message: str,
    intent: str,
    dataset_schema: dict | None = None,
    conversation_history: list | None = None,
) -> ExecutionPlan:
    """Create an execution plan using LLM (Gemini by default)."""
    # Note: Gemini uses plain text; we ask it to return JSON inside the prompt
    llm = settings.get_llm(temperature=0)

    schema_str = json.dumps(dataset_schema, default=str) if dataset_schema else "None"
    prompt = PLANNER_PROMPT.format(message=message, intent=intent, schema=schema_str)

    response = await llm.ainvoke([
        SystemMessage(content=prompt),
        HumanMessage(content="Generate the execution plan as a JSON object.")
    ])

    # Extract JSON from response (handle markdown code fences if present)
    content = response.content
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', content)
    if json_match:
        content = json_match.group(1).strip()
    else:
        # Try to find raw JSON object
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            content = json_match.group(0)

    try:
        data = json.loads(content)
        steps = [
            PlanStep(
                tool=s.get("tool", "python"),
                description=s.get("description", "Execute code"),
                parameters=s.get("parameters", {}),
            )
            for s in data.get("steps", [])
        ]
        return ExecutionPlan(
            steps=steps,
            reasoning=data.get("reasoning", "Sequential execution plan"),
        )
    except Exception as e:
        logger.error("Planner failed to parse JSON: %s. Using fallback.", e)
        # Fallback plan
        return ExecutionPlan(
            steps=[PlanStep(tool=intent if intent != "general" else "python", description=message)],
            reasoning="Fallback plan",
        )
