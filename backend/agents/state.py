"""
Agent State — LangGraph TypedDict state definition
"""
from typing import Any, TypedDict

from pydantic import BaseModel


class PlanStep(BaseModel):
    """A single step in the execution plan."""
    tool: str           # sql | python | visualization | statistics | ml | report
    description: str    # Human-readable step description
    parameters: dict[str, Any] = {}


class ExecutionPlan(BaseModel):
    """The full execution plan."""
    steps: list[PlanStep]
    reasoning: str      # Why this plan was chosen


class ToolResult(BaseModel):
    """Result from a single tool execution."""
    tool: str
    step: str
    success: bool
    output: dict[str, Any] | None = None
    error: str | None = None


class AgentState(TypedDict):
    """LangGraph state — passed through all nodes."""
    user_message: str
    session_id: str
    dataset_id: str | None
    connection_id: str | None
    dataset_schema: dict
    history: list

    # Set during execution
    intent: str | None
    plan: ExecutionPlan | None
    tool_results: list[ToolResult]
    final_text: str | None

    # Control flow
    retry_count: int
    validation_status: str
    error: str | None
    current_step: int
