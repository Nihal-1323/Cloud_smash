"""Exponential backoff retry helpers for rate-limited or transient API calls."""

import asyncio
import logging
import random
import time
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")
logger = logging.getLogger(__name__)


def _compute_delay(attempt: int, base_delay: float, max_delay: float) -> float:
    """Compute exponential backoff delay with full jitter."""
    ceiling = min(max_delay, base_delay * (2**attempt))
    return random.uniform(ceiling * 0.5, ceiling)


def retry_sync(
    operation: Callable[[], T],
    *,
    is_retryable: Callable[[Exception], bool],
    max_attempts: int = 4,
    base_delay: float = 0.5,
    max_delay: float = 16.0,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> T:
    """Execute a synchronous callable with exponential backoff on retryable exceptions."""
    last_error: Exception | None = None
    for attempt in range(max_attempts):
        try:
            return operation()
        except Exception as exc:
            last_error = exc
            if attempt >= max_attempts - 1 or not is_retryable(exc):
                raise
            delay = _compute_delay(attempt, base_delay, max_delay)
            logger.warning(
                "Retryable error on attempt %d/%d (%s). Retrying in %.2fs.",
                attempt + 1,
                max_attempts,
                exc,
                delay,
            )
            sleep_fn(delay)
    assert last_error is not None  # pragma: no cover
    raise last_error


async def retry_async(
    operation: Callable[[], Awaitable[T]],
    *,
    is_retryable: Callable[[Exception], bool],
    max_attempts: int = 4,
    base_delay: float = 0.5,
    max_delay: float = 16.0,
    sleep_fn: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> T:
    """Execute an async callable with exponential backoff on retryable exceptions."""
    last_error: Exception | None = None
    for attempt in range(max_attempts):
        try:
            return await operation()
        except Exception as exc:
            last_error = exc
            if attempt >= max_attempts - 1 or not is_retryable(exc):
                raise
            delay = _compute_delay(attempt, base_delay, max_delay)
            logger.warning(
                "Retryable async error on attempt %d/%d (%s). Retrying in %.2fs.",
                attempt + 1,
                max_attempts,
                exc,
                delay,
            )
            await sleep_fn(delay)
    assert last_error is not None  # pragma: no cover
    raise last_error
