"""
Intent Classifier agent node — classifies user query to target tools
✅ Uses Gemini (free) via settings.get_llm()
"""
import logging
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import settings

logger = logging.getLogger(__name__)

CLASSIFY_INTENT_PROMPT = """You are an intent classifier for a data analysis system.
Categorize the user's message into exactly one of the following categories:
- sql: Requesting SQL query generation/execution, database tables overview, or database selection.
- python: Requesting complex calculations, data transformations, custom Pandas/NumPy operations.
- visualization: Requesting charts, plots, line graphs, bar charts, heatmaps.
- statistics: Requesting descriptive stats, hypothesis testing, t-tests, correlation matrices.
- ml: Requesting forecasting, prediction, K-means clustering, random forest models.
- report: Requesting PDF/Word summary, KPI tiles, or business recommendations file generation.
- rag: Asking questions about the CONTENT of an uploaded PDF, document, or text report (e.g. "what does section 3 say?", "summarize this document", "find X in the report").
- general: General conversation, greeting, explaining capabilities, or unrelated requests.

Return ONLY the lowercase category name."""


async def classify_intent(message: str, context: dict = None) -> str:
    """Classify user intent using LLM (Gemini by default)."""
    llm = settings.get_llm(temperature=0)
    response = await llm.ainvoke([
        SystemMessage(content=CLASSIFY_INTENT_PROMPT),
        HumanMessage(content=message)
    ])
    intent = response.content.strip().lower()
    if intent not in ("sql", "python", "visualization", "statistics", "ml", "report", "rag"):
        return "general"
    return intent
