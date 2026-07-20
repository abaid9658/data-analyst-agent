"""
Qdrant Vector Database Service
Handles collection management, document embedding, and semantic search for RAG.

✅ Uses FREE local HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2)
   — No OpenAI API key required.
"""
import logging
import uuid
from typing import Any

from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import AsyncQdrantClient, models as qmodels

from app.config import settings

logger = logging.getLogger(__name__)

# ── Singleton embedding model (loaded once, reused) ──────────────────────────
_embeddings_instance: HuggingFaceEmbeddings | None = None


def _get_embeddings() -> HuggingFaceEmbeddings:
    """
    Return a singleton HuggingFace embeddings model.
    ✅ Free, local, no API key needed.
    Model is downloaded once from HuggingFace Hub and cached locally.
    """
    global _embeddings_instance
    if _embeddings_instance is None:
        logger.info(
            "Loading local embedding model: %s on device=%s",
            settings.EMBEDDING_MODEL,
            settings.EMBEDDING_DEVICE,
        )
        _embeddings_instance = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={"device": settings.EMBEDDING_DEVICE},
            encode_kwargs={"normalize_embeddings": True},
        )
        logger.info("Embedding model loaded successfully.")
    return _embeddings_instance


def _get_client() -> AsyncQdrantClient:
    """Create and return an async Qdrant client."""
    return AsyncQdrantClient(url=settings.QDRANT_URL)


async def ensure_collection_exists(collection_name: str | None = None) -> None:
    """Create the Qdrant collection if it does not yet exist."""
    name = collection_name or settings.QDRANT_COLLECTION_NAME
    client = _get_client()
    try:
        existing = await client.get_collections()
        existing_names = [c.name for c in existing.collections]
        if name not in existing_names:
            await client.create_collection(
                collection_name=name,
                vectors_config=qmodels.VectorParams(
                    size=settings.EMBEDDING_DIMENSION,  # 384 for MiniLM / bge-small
                    distance=qmodels.Distance.COSINE,
                ),
            )
            logger.info("Qdrant collection '%s' created (dim=%d).", name, settings.EMBEDDING_DIMENSION)
        else:
            logger.debug("Qdrant collection '%s' already exists.", name)
    finally:
        await client.close()


async def upsert_document_chunks(
    chunks: list[dict[str, Any]],
    collection_name: str | None = None,
) -> int:
    """
    Embed and upsert a list of text chunks into Qdrant.

    Each chunk must have:
        text: str          — The raw text content to embed.
        dataset_id: str    — UUID of the parent dataset.
        page: int          — The source PDF page number (0-indexed).
        chunk_index: int   — Index of this chunk within the page.

    Returns the number of points upserted.
    """
    if not chunks:
        return 0

    name = collection_name or settings.QDRANT_COLLECTION_NAME
    embeddings_model = _get_embeddings()
    client = _get_client()

    try:
        await ensure_collection_exists(name)

        texts = [c["text"] for c in chunks]
        # HuggingFaceEmbeddings.embed_documents is synchronous — run via asyncio
        import asyncio
        vectors = await asyncio.get_event_loop().run_in_executor(
            None, embeddings_model.embed_documents, texts
        )

        points = [
            qmodels.PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk["text"],
                    "dataset_id": chunk["dataset_id"],
                    "page": chunk.get("page", 0),
                    "chunk_index": chunk.get("chunk_index", 0),
                },
            )
            for chunk, vector in zip(chunks, vectors)
        ]

        await client.upsert(collection_name=name, points=points)
        logger.info("Upserted %d chunks into Qdrant collection '%s'.", len(points), name)
        return len(points)

    finally:
        await client.close()


async def search_similar_chunks(
    query: str,
    dataset_id: str,
    top_k: int = 5,
    score_threshold: float = 0.35,
    collection_name: str | None = None,
) -> list[dict[str, Any]]:
    """
    Embed the query and search Qdrant for the top-k most similar document chunks
    that belong to the specified dataset.

    Returns a list of dicts with keys: text, page, chunk_index, score.
    """
    import asyncio

    name = collection_name or settings.QDRANT_COLLECTION_NAME
    embeddings_model = _get_embeddings()
    client = _get_client()

    try:
        query_vector = await asyncio.get_event_loop().run_in_executor(
            None, embeddings_model.embed_query, query
        )

        results = await client.search(
            collection_name=name,
            query_vector=query_vector,
            query_filter=qmodels.Filter(
                must=[
                    qmodels.FieldCondition(
                        key="dataset_id",
                        match=qmodels.MatchValue(value=dataset_id),
                    )
                ]
            ),
            limit=top_k,
            score_threshold=score_threshold,
            with_payload=True,
        )

        return [
            {
                "text": hit.payload["text"],
                "page": hit.payload.get("page", 0),
                "chunk_index": hit.payload.get("chunk_index", 0),
                "score": hit.score,
            }
            for hit in results
        ]

    finally:
        await client.close()


async def delete_dataset_chunks(
    dataset_id: str,
    collection_name: str | None = None,
) -> None:
    """Remove all Qdrant vectors that belong to a given dataset."""
    name = collection_name or settings.QDRANT_COLLECTION_NAME
    client = _get_client()
    try:
        await client.delete(
            collection_name=name,
            points_selector=qmodels.FilterSelector(
                filter=qmodels.Filter(
                    must=[
                        qmodels.FieldCondition(
                            key="dataset_id",
                            match=qmodels.MatchValue(value=dataset_id),
                        )
                    ]
                )
            ),
        )
        logger.info("Deleted all Qdrant vectors for dataset_id='%s'.", dataset_id)
    finally:
        await client.close()
