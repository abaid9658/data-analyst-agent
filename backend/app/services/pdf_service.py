"""
PDF Service
Extracts text from uploaded PDFs, chunks it, and indexes it into Qdrant.
"""
import io
import logging
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)


def _chunk_text(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[str]:
    """
    Split a long text string into overlapping fixed-size chunks.
    Uses a simple sliding-window approach — no external splitter needed.
    """
    chunks: list[str] = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= text_len:
            break
        start += chunk_size - chunk_overlap

    return chunks


def extract_text_from_pdf(content: bytes) -> list[dict[str, Any]]:
    """
    Extract text from a PDF binary blob page by page.

    Returns a list of dicts:
        { "page": int, "text": str }

    Tries `pypdf` first; falls back to `pdfplumber` for scanned PDFs with
    embedded text layers.
    """
    pages: list[dict[str, Any]] = []

    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(content))
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            text = text.strip()
            if text:
                pages.append({"page": page_num, "text": text})

    except Exception as pypdf_err:
        logger.warning(
            "pypdf extraction failed (%s), trying pdfplumber.", pypdf_err
        )
        try:
            import pdfplumber

            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = (page.extract_text() or "").strip()
                    if text:
                        pages.append({"page": page_num, "text": text})

        except Exception as plumber_err:
            logger.error("pdfplumber also failed: %s", plumber_err)
            raise RuntimeError(
                f"Could not extract text from PDF. pypdf: {pypdf_err}. pdfplumber: {plumber_err}"
            )

    return pages


async def index_pdf_into_qdrant(
    content: bytes,
    dataset_id: str,
) -> int:
    """
    Full pipeline: extract → chunk → embed → upsert into Qdrant.

    Returns the total number of vector points upserted.
    """
    from app.services.qdrant_service import upsert_document_chunks

    chunk_size = settings.EMBEDDING_CHUNK_SIZE
    chunk_overlap = settings.EMBEDDING_CHUNK_OVERLAP

    pages = extract_text_from_pdf(content)
    logger.info(
        "Extracted %d pages from PDF for dataset_id='%s'.", len(pages), dataset_id
    )

    all_chunks: list[dict[str, Any]] = []
    for page_data in pages:
        page_num = page_data["page"]
        page_text = page_data["text"]

        text_chunks = _chunk_text(page_text, chunk_size, chunk_overlap)
        for idx, chunk_text in enumerate(text_chunks):
            all_chunks.append(
                {
                    "text": chunk_text,
                    "dataset_id": dataset_id,
                    "page": page_num,
                    "chunk_index": idx,
                }
            )

    logger.info(
        "Indexing %d total chunks from PDF for dataset_id='%s'.",
        len(all_chunks),
        dataset_id,
    )
    total_upserted = await upsert_document_chunks(all_chunks)
    return total_upserted
