"""
Agent Memory — manages short-term and long-term conversation context
"""
import json
import logging
from typing import Any

import redis.asyncio as aioredis
from app.config import settings

logger = logging.getLogger(__name__)

MEMORY_TTL_SECONDS = 60 * 60 * 2  # 2 hours


class AgentMemory:
    """
    Manages conversation context for the LangGraph agent.
    Uses Redis for short-term session memory and provides a structured
    interface for reading/writing per-session state.
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self._redis: aioredis.Redis | None = None

    async def _get_redis(self) -> aioredis.Redis:
        if self._redis is None:
            self._redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        return self._redis

    def _key(self, suffix: str) -> str:
        return f"agent:memory:{self.session_id}:{suffix}"

    async def save_context(self, context: dict[str, Any]) -> None:
        """Save agent execution context to Redis with TTL."""
        redis = await self._get_redis()
        try:
            await redis.setex(self._key("context"), MEMORY_TTL_SECONDS, json.dumps(context, default=str))
            logger.debug("Saved context for session %s", self.session_id)
        except Exception as e:
            logger.warning("Failed to save agent context: %s", e)

    async def load_context(self) -> dict[str, Any]:
        """Load agent execution context from Redis."""
        redis = await self._get_redis()
        try:
            data = await redis.get(self._key("context"))
            if data:
                return json.loads(data)
        except Exception as e:
            logger.warning("Failed to load agent context: %s", e)
        return {}

    async def append_message(self, role: str, content: str) -> None:
        """Append a message to the session's in-memory history list."""
        redis = await self._get_redis()
        try:
            message = json.dumps({"role": role, "content": content})
            await redis.rpush(self._key("history"), message)
            await redis.expire(self._key("history"), MEMORY_TTL_SECONDS)
            # Keep last 40 messages only to avoid token overflow
            length = await redis.llen(self._key("history"))
            if length > 40:
                await redis.ltrim(self._key("history"), -40, -1)
        except Exception as e:
            logger.warning("Failed to append message to memory: %s", e)

    async def get_history(self) -> list[dict]:
        """Retrieve recent conversation history from Redis."""
        redis = await self._get_redis()
        try:
            raw_list = await redis.lrange(self._key("history"), 0, -1)
            return [json.loads(item) for item in raw_list]
        except Exception as e:
            logger.warning("Failed to retrieve memory history: %s", e)
            return []

    async def clear(self) -> None:
        """Clear all memory keys for this session."""
        redis = await self._get_redis()
        keys = await redis.keys(f"agent:memory:{self.session_id}:*")
        if keys:
            await redis.delete(*keys)
        logger.debug("Cleared memory for session %s", self.session_id)
