"""
Shared Redis client module.

Provides a module-level singleton Redis connection with explicit
init/get/close lifecycle management.
"""

import os

import redis.asyncio as redis

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

_client: redis.Redis | None = None


async def init(url: str | None = None) -> redis.Redis:
    """Initialize the shared Redis client. Safe to call multiple times."""
    global _client
    if _client is None:
        _client = redis.from_url(url or REDIS_URL, decode_responses=True)
    return _client


def get() -> redis.Redis:
    """Return the shared Redis client. Raises if not initialized."""
    if _client is None:
        raise RuntimeError(
            "Redis client not initialized. Call 'await redis_client.init()' first."
        )
    return _client


async def close() -> None:
    """Close the shared Redis client and reset state."""
    global _client
    if _client:
        await _client.aclose()
        _client = None
