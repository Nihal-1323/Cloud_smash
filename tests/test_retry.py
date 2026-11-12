"""Tests for exponential backoff retry helpers."""

import pytest

from cloud_smash.retry import retry_async, retry_sync


def test_retry_sync_succeeds_after_transient_errors() -> None:
    calls = 0
    delays: list[float] = []

    def flaky() -> str:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RuntimeError("429 rate limit")
        return "ok"

    result = retry_sync(
        flaky,
        is_retryable=lambda e: "429" in str(e),
        max_attempts=4,
        base_delay=0.1,
        sleep_fn=delays.append,
    )
    assert result == "ok"
    assert calls == 3
    assert len(delays) == 2


def test_retry_sync_does_not_retry_fatal_error() -> None:
    calls = 0

    def fatal() -> str:
        nonlocal calls
        calls += 1
        raise ValueError("bad request")

    with pytest.raises(ValueError, match="bad request"):
        retry_sync(fatal, is_retryable=lambda _: False, max_attempts=4, sleep_fn=lambda _: None)
    assert calls == 1


async def test_retry_async_exhausts_attempts() -> None:
    calls = 0
    delays: list[float] = []

    async def always_fails() -> None:
        nonlocal calls
        calls += 1
        raise TimeoutError("timed out")

    async def fake_sleep(seconds: float) -> None:
        delays.append(seconds)

    with pytest.raises(TimeoutError):
        await retry_async(
            always_fails,
            is_retryable=lambda e: isinstance(e, TimeoutError),
            max_attempts=3,
            base_delay=0.1,
            sleep_fn=fake_sleep,
        )
    assert calls == 3
    assert len(delays) == 2
