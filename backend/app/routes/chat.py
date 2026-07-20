"""
Chat route — SSE streaming AI responses
"""
import json
import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from agents.orchestrator import AgentOrchestrator
from app.database.base import get_db
from app.middleware.auth import get_current_user
from app.models.conversation import Conversation, Message
from app.models.dataset import Dataset
from app.models.user import User
from app.schemas.chat import (
    ConversationListResponse,
    ConversationResponse,
    MessageListResponse,
    SendMessageRequest,
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Single orchestrator instance (stateless — state is per-request)
orchestrator = AgentOrchestrator()


# ─── Send Message (SSE Streaming) ────────────────────────────────────────────

@router.post("/message")
async def send_message(
    body: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send a message and receive a streaming AI response via Server-Sent Events.
    """
    # Validate or create conversation
    if body.session_id:
        result = await db.execute(
            select(Conversation).where(
                Conversation.id == body.session_id,
                Conversation.user_id == current_user.id,
            )
        )
        conversation = result.scalar_one_or_none()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(
            user_id=current_user.id,
            title=body.message[:50],
            dataset_id=body.dataset_id,
        )
        db.add(conversation)
        await db.flush()

    # Save user message
    user_msg = Message(
        conversation_id=conversation.id,
        role="user",
        content=body.message,
    )
    db.add(user_msg)
    await db.flush()

    # Get conversation history
    history_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
        .limit(20)  # Last 20 messages for context
    )
    history = [
        {"role": m.role, "content": m.content}
        for m in history_result.scalars().all()
    ]

    # Get dataset schema if dataset is linked
    dataset_schema = {}
    if body.dataset_id:
        ds_result = await db.execute(
            select(Dataset).where(Dataset.id == body.dataset_id)
        )
        dataset = ds_result.scalar_one_or_none()
        if dataset and dataset.schema:
            dataset_schema = dataset.schema

    await db.commit()

    # ─── Streaming SSE response ───────────────────────────────────────────────
    async def event_generator():
        """Generate SSE events from the agent stream."""
        full_response_parts = []
        metadata = {}

        try:
            async for chunk in orchestrator.stream(
                message=body.message,
                session_id=str(conversation.id),
                dataset_id=str(body.dataset_id) if body.dataset_id else None,
                connection_id=str(body.connection_id) if body.connection_id else None,
                dataset_schema=dataset_schema,
                history=history,
            ):
                # Yield SSE event
                event_data = json.dumps(chunk, default=str)
                yield f"data: {event_data}\n\n"

                # Collect parts for saving
                chunk_type = chunk.get("type")
                if chunk_type == "text":
                    full_response_parts.append(chunk["content"] or "")
                elif chunk_type == "sql":
                    metadata["sql_query"] = chunk["content"]
                elif chunk_type == "chart":
                    metadata["chart_spec"] = chunk["content"]
                elif chunk_type == "insights":
                    metadata["insights"] = chunk["content"]

        except Exception as e:
            logger.error("Agent streaming error: %s", e)
            error_event = json.dumps({"type": "error", "content": str(e)})
            yield f"data: {error_event}\n\n"

        finally:
            # Save assistant message to DB
            try:
                async with db.begin():
                    assistant_msg = Message(
                        conversation_id=conversation.id,
                        role="assistant",
                        content="\n".join(full_response_parts),
                        metadata=metadata if metadata else None,
                        model_used="gpt-4o",
                    )
                    db.add(assistant_msg)
                    await db.execute(
                        update(Conversation)
                        .where(Conversation.id == conversation.id)
                        .values(
                            updated_at=datetime.now(timezone.utc),
                            message_count=Conversation.message_count + 2,
                        )
                    )
            except Exception as e:
                logger.error("Failed to save assistant message: %s", e)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ─── List Sessions ────────────────────────────────────────────────────────────

@router.get("/sessions", response_model=ConversationListResponse)
async def list_sessions(
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Conversation)
        .where(
            Conversation.user_id == current_user.id,
            Conversation.is_archived == False,
        )
        .order_by(Conversation.updated_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    conversations = result.scalars().all()
    return ConversationListResponse(
        sessions=[ConversationResponse.model_validate(c) for c in conversations]
    )


# ─── Get Session Messages ────────────────────────────────────────────────────

@router.get("/sessions/{session_id}/messages", response_model=MessageListResponse)
async def get_session_messages(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify ownership
    conv_result = await db.execute(
        select(Conversation).where(
            Conversation.id == session_id,
            Conversation.user_id == current_user.id,
        )
    )
    if not conv_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Conversation not found")

    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == session_id)
        .order_by(Message.created_at)
    )
    messages = result.scalars().all()
    return MessageListResponse(
        session_id=session_id,
        messages=messages,
    )


# ─── Delete Session ──────────────────────────────────────────────────────────

@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == session_id,
            Conversation.user_id == current_user.id,
        )
    )
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    await db.delete(conversation)
    return {"message": "Conversation deleted"}
