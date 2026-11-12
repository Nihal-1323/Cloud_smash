"""Asynchronous Ollama client supporting embeddings, streaming chat, and tunnel headers."""

from collections.abc import AsyncIterator, Sequence
import json
import logging
from typing import Any

import httpx

from cloud_smash.config import Settings
from cloud_smash.retry import retry_async

logger = logging.getLogger(__name__)

_RETRYABLE_STATUS_CODES = {429, 502, 503, 504}


def _is_retryable_http_error(exc: Exception) -> bool:
    if isinstance(exc, (httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in _RETRYABLE_STATUS_CODES
    return False


class OllamaClient:
    """Async client for Ollama's REST API (local or exposed via Cloudflare Tunnel)."""

    def __init__(
        self,
        settings: Settings,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._base_url = settings.ollama_base_url.rstrip("/")
        self._embed_model = settings.ollama_embed_model
        self._chat_model = settings.ollama_chat_model
        self._temperature = settings.llm_temperature
        self._headers = settings.ollama_headers()
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(
            base_url=self._base_url,
            headers=self._headers,
            timeout=httpx.Timeout(settings.ollama_timeout_seconds, connect=15.0),
        )

    async def aclose(self) -> None:
        """Close the underlying HTTP client if owned by this instance."""
        if self._owns_client:
            await self._client.aclose()

    def _url(self, path: str) -> str:
        # Support injected MockTransport clients with or without base_url configured.
        if str(self._client.base_url):
            return path
        return f"{self._base_url}{path}"

    async def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        """Generate vector embeddings for one or more texts using `nomic-embed-text`."""
        if not texts:
            return []

        async def _call_batch_embed() -> list[list[float]]:
            response = await self._client.post(
                self._url("/api/embed"),
                json={"model": self._embed_model, "input": list(texts)},
                headers=self._headers,
            )
            if response.status_code == 404:
                return await self._embed_legacy(texts)
            response.raise_for_status()
            payload = response.json()
            embeddings = payload.get("embeddings")
            if not isinstance(embeddings, list) or len(embeddings) != len(texts):
                raise ValueError("Unexpected Ollama /api/embed response payload.")
            return embeddings

        return await retry_async(_call_batch_embed, is_retryable=_is_retryable_http_error)

    async def _embed_legacy(self, texts: Sequence[str]) -> list[list[float]]:
        """Fallback to Ollama's legacy single-prompt /api/embeddings endpoint."""
        vectors: list[list[float]] = []
        for text in texts:
            response = await self._client.post(
                self._url("/api/embeddings"),
                json={"model": self._embed_model, "prompt": text},
                headers=self._headers,
            )
            response.raise_for_status()
            vectors.append(response.json()["embedding"])
        return vectors

    async def embed_query(self, query: str) -> list[float]:
        """Generate an embedding vector for a single search query."""
        vectors = await self.embed_texts([query])
        return vectors[0]

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """Send a non-streaming chat completion request to Ollama."""

        async def _call_chat() -> str:
            response = await self._client.post(
                self._url("/api/chat"),
                json=self._chat_payload(messages, stream=False),
                headers=self._headers,
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            return data.get("message", {}).get("content", "")

        return await retry_async(_call_chat, is_retryable=_is_retryable_http_error)

    async def stream_chat(self, messages: list[dict[str, str]]) -> AsyncIterator[str]:
        """Stream assistant response tokens from Ollama's /api/chat endpoint."""
        async with self._client.stream(
            "POST",
            self._url("/api/chat"),
            json=self._chat_payload(messages, stream=True),
            headers=self._headers,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                chunk = json.loads(line)
                token = chunk.get("message", {}).get("content", "")
                if token:
                    yield token
                if chunk.get("done"):
                    break

    async def health_check(self) -> dict[str, Any]:
        """Verify Ollama reachability (including through Cloudflare Tunnel) and list models."""
        response = await self._client.get(self._url("/api/tags"), headers=self._headers)
        response.raise_for_status()
        models = [m.get("name") for m in response.json().get("models", []) if m.get("name")]
        return {"status": "ok", "base_url": self._base_url, "models": models}

    def _chat_payload(self, messages: list[dict[str, str]], *, stream: bool) -> dict[str, Any]:
        return {
            "model": self._chat_model,
            "messages": messages,
            "stream": stream,
            "options": {"temperature": self._temperature},
        }
