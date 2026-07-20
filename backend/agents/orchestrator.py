"""
AI Agent Orchestrator — LangGraph-based multi-step agent
"""
import json
import logging
from typing import AsyncGenerator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

from agents.intent_classifier import classify_intent
from agents.memory import AgentMemory
from agents.planner import create_plan
from agents.state import AgentState, ToolResult
from tools.python_tool import PythonTool
from tools.sql_tool import SQLTool
from tools.statistics_tool import StatisticsTool
from tools.visualization_tool import VisualizationTool
from tools.ml_tool import MLTool
from tools.report_tool import ReportTool
from tools.rag_tool import RAGTool

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


class AgentOrchestrator:
    """
    Main AI agent orchestrator using LangGraph state machine.

    Flow: classify_intent → create_plan → execute_tools → validate → synthesize → respond
    """

    def __init__(self, llm_provider: str = "openai"):
        self.sql_tool = SQLTool()
        self.python_tool = PythonTool()
        self.viz_tool = VisualizationTool()
        self.stats_tool = StatisticsTool()
        self.ml_tool = MLTool()
        self.report_tool = ReportTool()
        self.rag_tool = RAGTool()

        self._graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state machine."""
        graph = StateGraph(AgentState)

        # Add nodes
        graph.add_node("classify_intent", self._node_classify_intent)
        graph.add_node("create_plan", self._node_create_plan)
        graph.add_node("execute_tools", self._node_execute_tools)
        graph.add_node("validate_outputs", self._node_validate_outputs)
        graph.add_node("synthesize_response", self._node_synthesize_response)

        # Define edges
        graph.set_entry_point("classify_intent")
        graph.add_edge("classify_intent", "create_plan")
        graph.add_edge("create_plan", "execute_tools")
        graph.add_edge("execute_tools", "validate_outputs")
        graph.add_conditional_edges(
            "validate_outputs",
            self._route_after_validation,
            {
                "retry": "execute_tools",
                "synthesize": "synthesize_response",
                "error": END,
            },
        )
        graph.add_edge("synthesize_response", END)

        return graph.compile()

    async def _node_classify_intent(self, state: AgentState) -> AgentState:
        """Classify user intent from the message."""
        intent = await classify_intent(
            message=state["user_message"],
            context=state.get("context", {}),
        )
        state["intent"] = intent
        logger.info("Intent classified: %s", intent)
        return state

    async def _node_create_plan(self, state: AgentState) -> AgentState:
        """Create an execution plan from the intent."""
        plan = await create_plan(
            message=state["user_message"],
            intent=state["intent"],
            dataset_schema=state.get("dataset_schema"),
            conversation_history=state.get("history", []),
        )
        state["plan"] = plan
        state["current_step"] = 0
        state["retry_count"] = 0
        logger.info("Plan created: %s steps", len(plan.steps))
        return state

    async def _node_execute_tools(self, state: AgentState) -> AgentState:
        """Execute tools according to the plan."""
        plan = state["plan"]
        results: list[ToolResult] = []

        for step in plan.steps:
            tool_name = step.tool
            logger.info("Executing tool: %s", tool_name)

            try:
                result = await self._call_tool(
                    tool_name=tool_name,
                    parameters=step.parameters,
                    state=state,
                    previous_results=results,
                )
                results.append(ToolResult(
                    tool=tool_name,
                    step=step.description,
                    success=True,
                    output=result,
                ))
            except Exception as e:
                logger.error("Tool %s failed: %s", tool_name, e)
                results.append(ToolResult(
                    tool=tool_name,
                    step=step.description,
                    success=False,
                    error=str(e),
                ))

        state["tool_results"] = results
        return state

    async def _call_tool(
        self,
        tool_name: str,
        parameters: dict,
        state: AgentState,
        previous_results: list[ToolResult],
    ) -> dict:
        """Route to the correct tool and execute it."""
        # Inject context into parameters
        params = {
            **parameters,
            "dataset_id": state.get("dataset_id"),
            "connection_id": state.get("connection_id"),
            "dataset_schema": state.get("dataset_schema"),
            "previous_results": previous_results,
        }

        match tool_name:
            case "sql":
                return await self.sql_tool.execute(params)
            case "python":
                return await self.python_tool.execute(params)
            case "visualization":
                return await self.viz_tool.execute(params)
            case "statistics":
                return await self.stats_tool.execute(params)
            case "ml":
                return await self.ml_tool.execute(params)
            case "report":
                return await self.report_tool.execute(params)
            case "rag":
                # Inject user_message directly so RAGTool can use it
                params["user_message"] = params.get("user_message") or state.get("user_message", "")
                return await self.rag_tool.execute(params)
            case _:
                raise ValueError(f"Unknown tool: {tool_name}")

    async def _node_validate_outputs(self, state: AgentState) -> AgentState:
        """Check tool outputs for errors and decide retry or proceed."""
        results = state.get("tool_results", [])
        failed = [r for r in results if not r.success]

        if failed and state.get("retry_count", 0) < MAX_RETRIES:
            state["retry_count"] = state.get("retry_count", 0) + 1
            state["validation_status"] = "retry"
            logger.warning("Retrying failed tools (attempt %d)", state["retry_count"])
        elif failed and len(failed) == len(results):
            # All tools failed — surface error
            state["validation_status"] = "error"
            state["error"] = f"All tools failed: {[r.error for r in failed]}"
        else:
            state["validation_status"] = "ok"

        return state

    def _route_after_validation(self, state: AgentState) -> str:
        return {
            "retry": "retry",
            "error": "error",
            "ok": "synthesize",
        }.get(state.get("validation_status", "ok"), "synthesize")

    async def _node_synthesize_response(self, state: AgentState) -> AgentState:
        """Combine all tool outputs into a coherent response."""
        from prompts.insights import synthesize_response_prompt
        from app.config import settings

        # Build synthesis prompt
        prompt = synthesize_response_prompt(
            user_message=state["user_message"],
            tool_results=state.get("tool_results", []),
            dataset_schema=state.get("dataset_schema"),
        )

        # Use Gemini (or configured LLM) to generate natural language summary
        llm = settings.get_llm(temperature=0)
        response = await llm.ainvoke([HumanMessage(content=prompt)])

        state["final_text"] = response.content
        return state

    async def stream(
        self,
        message: str,
        session_id: str,
        dataset_id: str | None = None,
        connection_id: str | None = None,
        dataset_schema: dict | None = None,
        history: list | None = None,
    ) -> AsyncGenerator[dict, None]:
        """
        Stream the agent's response as Server-Sent Events chunks.
        Yields dicts with { type, content } to be serialized as SSE.
        """
        initial_state: AgentState = {
            "user_message": message,
            "session_id": session_id,
            "dataset_id": dataset_id,
            "connection_id": connection_id,
            "dataset_schema": dataset_schema or {},
            "history": history or [],
            "intent": None,
            "plan": None,
            "tool_results": [],
            "final_text": None,
            "retry_count": 0,
            "validation_status": "ok",
        }

        yield {"type": "thinking", "content": "Analyzing your request..."}

        # Run graph
        async for event in self._graph.astream(initial_state):
            node_name = list(event.keys())[0]
            node_state = event[node_name]

            if node_name == "classify_intent":
                yield {"type": "intent", "content": node_state.get("intent")}

            elif node_name == "create_plan":
                plan = node_state.get("plan")
                if plan:
                    yield {
                        "type": "plan",
                        "content": {
                            "steps": [s.description for s in plan.steps],
                        },
                    }

            elif node_name == "execute_tools":
                for result in node_state.get("tool_results", []):
                    if result.success:
                        output = result.output
                        if result.tool == "sql":
                            yield {"type": "sql", "content": output.get("sql")}
                            if output.get("table_data"):
                                yield {"type": "table", "content": output["table_data"]}
                        elif result.tool == "python":
                            yield {"type": "code", "content": output.get("code")}
                        elif result.tool == "visualization":
                            yield {"type": "chart", "content": output.get("plotly_spec")}
                        elif result.tool in ("statistics", "ml"):
                            yield {"type": "analysis", "content": output}
                        elif result.tool == "rag":
                            yield {
                                "type": "rag_answer",
                                "content": {
                                    "answer": output.get("answer", ""),
                                    "sources": output.get("sources", []),
                                    "retrieved_chunks": output.get("retrieved_chunks", 0),
                                },
                            }

            elif node_name == "synthesize_response":
                yield {"type": "text", "content": node_state.get("final_text")}

                # Extract insights from tool results
                insights = self._extract_insights(node_state.get("tool_results", []))
                if insights:
                    yield {"type": "insights", "content": insights}

        yield {"type": "done", "content": None}

    def _extract_insights(self, tool_results: list[ToolResult]) -> list[str]:
        """Extract key insights from tool results."""
        insights = []
        for result in tool_results:
            if result.success and isinstance(result.output, dict):
                if "insights" in result.output:
                    insights.extend(result.output["insights"])
        return insights[:5]  # Top 5 insights
