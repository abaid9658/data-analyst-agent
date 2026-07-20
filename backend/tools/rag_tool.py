"""
RAG Tool — Retrieval-Augmented Generation over indexed PDF documents.
Uses Qdrant semantic search to retrieve relevant context, then synthesizes
an answer with Google Gemini LLM.

✅ Uses Gemini (free) for answer generation + Local HuggingFace embeddings.
"""
import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from app.config import settings
from tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

RAG_SYSTEM_PROMPT = """You are a precise document analyst. You have been given relevant excerpts from a PDF document.
Answer the user's question using ONLY the provided context. If the context does not contain enough information
to fully answer the question, say so clearly.

Rules:
- Cite which page(s) the information came from when possible.
- Be concise and factual — do not hallucinate.
- If multiple excerpts are relevant, synthesize them into one coherent answer.
- Format the response in clean Markdown.
"""


class RAGTool(BaseTool):
    """
    Tool that performs semantic search over indexed PDF documents in Qdrant
    and generates a Gemini-powered answer grounded in the retrieved context.
    """

    @property
    def name(self) -> str:
        return "rag"

    @property
    def description(self) -> str:
        return (
            "Retrieves and answers questions from uploaded PDF documents using "
            "semantic search and a language model. Use when the user asks about "
            "the contents of a PDF, report, or document they have uploaded."
        )

    async def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Retrieve top-k relevant chunks from Qdrant and synthesize an answer.

        Expected params keys:
            user_message (str): The user's question.
            dataset_id (str | None): Target dataset/document UUID.
            top_k (int): Number of chunks to retrieve (default 5).
            score_threshold (float): Minimum similarity score (default 0.35).
        """
        from app.services.qdrant_service import search_similar_chunks

        user_message: str = params.get("user_message", "")
        dataset_id: str | None = params.get("dataset_id")
        top_k: int = int(params.get("top_k", 5))
        score_threshold: float = float(params.get("score_threshold", 0.35))

        if not dataset_id:
            return {
                "answer": "No document dataset selected. Please upload a PDF and select it.",
                "sources": [],
                "insights": ["No PDF dataset was linked to the conversation."],
            }

        # ── Semantic retrieval ──────────────────────────────────────────────
        chunks = await search_similar_chunks(
            query=user_message,
            dataset_id=dataset_id,
            top_k=top_k,
            score_threshold=score_threshold,
        )

        if not chunks:
            return {
                "answer": (
                    "I could not find relevant information in the uploaded document "
                    "for your question. Please try rephrasing or check that the correct "
                    "document is selected."
                ),
                "sources": [],
                "insights": ["No matching context found in the document."],
            }

        # ── Build context string ────────────────────────────────────────────
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(
                f"[Excerpt {i} — Page {chunk['page'] + 1} "
                f"(relevance: {chunk['score']:.2f})]:\n{chunk['text']}"
            )
        context = "\n\n---\n\n".join(context_parts)

        # ── LLM answer synthesis (Gemini) ───────────────────────────────────
        llm = settings.get_llm(temperature=0)
        prompt = (
            f"Context from the document:\n\n{context}\n\n"
            f"User question: {user_message}\n\n"
            "Please answer the question based on the context above."
        )

        response = await llm.ainvoke(
            [
                SystemMessage(content=RAG_SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]
        )

        answer: str = response.content

        # Collect unique page references as sources
        sources = sorted({chunk["page"] + 1 for chunk in chunks})

        return {
            "answer": answer,
            "sources": sources,
            "retrieved_chunks": len(chunks),
            "insights": [
                f"Found {len(chunks)} relevant document sections.",
                f"Sources: Page(s) {', '.join(str(p) for p in sources)}.",
            ],
        }
