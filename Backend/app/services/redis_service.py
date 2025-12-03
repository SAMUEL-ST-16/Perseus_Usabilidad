"""
Redis Service
Handles caching operations with Redis for improved performance
"""

import json
import hashlib
from typing import Optional, Any, Callable
from functools import wraps
import asyncio
from app.core.logger import get_logger

logger = get_logger(__name__)


class RedisService:
    """
    Service for Redis caching operations

    Provides async caching with automatic serialization/deserialization
    and fallback to no-cache if Redis is unavailable.
    """

    def __init__(self):
        """Initialize Redis service with lazy connection"""
        self.redis_client = None
        self.enabled = False
        logger.info("Initializing Redis Service (lazy connection)")

    async def _ensure_connected(self):
        """Ensure Redis connection is established"""
        if self.redis_client is None:
            try:
                import redis.asyncio as redis
                from app.core.config import settings

                # Try to connect to Redis
                self.redis_client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2
                )

                # Test connection
                await self.redis_client.ping()
                self.enabled = True
                logger.info(f"✓ Redis connected: {settings.REDIS_HOST}:{settings.REDIS_PORT}")

            except ImportError:
                logger.warning("redis package not installed - caching disabled")
                self.enabled = False
            except Exception as e:
                logger.warning(f"Redis connection failed: {e} - caching disabled")
                self.enabled = False
                self.redis_client = None

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Generate cache key from prefix and arguments

        Args:
            prefix: Key prefix (e.g., "llm_desc", "scraping")
            *args: Positional arguments to hash
            **kwargs: Keyword arguments to hash

        Returns:
            Cache key string
        """
        # Create consistent hash from arguments
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_json = json.dumps(key_data, sort_keys=True, ensure_ascii=False)
        key_hash = hashlib.md5(key_json.encode()).hexdigest()

        return f"perseus:{prefix}:{key_hash}"

    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/error
        """
        if not self.enabled:
            await self._ensure_connected()

        if not self.enabled:
            return None

        try:
            value = await self.redis_client.get(key)
            if value:
                logger.debug(f"Cache HIT: {key[:50]}...")
                return json.loads(value)
            logger.debug(f"Cache MISS: {key[:50]}...")
            return None
        except Exception as e:
            logger.warning(f"Cache get error for {key}: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = 3600):
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl: Time to live in seconds (default: 1 hour)
        """
        if not self.enabled:
            await self._ensure_connected()

        if not self.enabled:
            return

        try:
            value_json = json.dumps(value, ensure_ascii=False)
            await self.redis_client.setex(key, ttl, value_json)
            logger.debug(f"Cache SET: {key[:50]}... (TTL: {ttl}s)")
        except Exception as e:
            logger.warning(f"Cache set error for {key}: {e}")

    async def delete(self, key: str):
        """Delete key from cache"""
        if not self.enabled:
            return

        try:
            await self.redis_client.delete(key)
            logger.debug(f"Cache DELETE: {key[:50]}...")
        except Exception as e:
            logger.warning(f"Cache delete error for {key}: {e}")

    async def clear_pattern(self, pattern: str):
        """
        Clear all keys matching pattern

        Args:
            pattern: Redis pattern (e.g., "perseus:llm_desc:*")
        """
        if not self.enabled:
            return

        try:
            keys = await self.redis_client.keys(pattern)
            if keys:
                await self.redis_client.delete(*keys)
                logger.info(f"Cleared {len(keys)} keys matching: {pattern}")
        except Exception as e:
            logger.warning(f"Cache clear error for {pattern}: {e}")

    async def get_stats(self) -> dict:
        """Get Redis statistics"""
        if not self.enabled:
            await self._ensure_connected()

        if not self.enabled:
            return {"enabled": False, "status": "disconnected"}

        try:
            info = await self.redis_client.info()
            return {
                "enabled": True,
                "status": "connected",
                "used_memory": info.get("used_memory_human", "N/A"),
                "connected_clients": info.get("connected_clients", 0),
                "total_keys": await self.redis_client.dbsize()
            }
        except Exception as e:
            return {"enabled": False, "status": f"error: {e}"}

    def cached(self, prefix: str, ttl: int = 3600):
        """
        Decorator for caching async function results

        Args:
            prefix: Cache key prefix
            ttl: Time to live in seconds

        Example:
            @redis_service.cached("llm_desc", ttl=7200)
            async def generate_description(comment, subchar):
                return await llm_call(comment, subchar)
        """
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = self._generate_key(prefix, *args, **kwargs)

                # Try to get from cache
                cached_result = await self.get(cache_key)
                if cached_result is not None:
                    return cached_result

                # Call original function
                result = await func(*args, **kwargs)

                # Store in cache
                await self.set(cache_key, result, ttl=ttl)

                return result
            return wrapper
        return decorator

    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            try:
                await self.redis_client.close()
                logger.info("Redis connection closed")
            except Exception as e:
                logger.warning(f"Error closing Redis: {e}")


# Global service instance
redis_service = RedisService()
