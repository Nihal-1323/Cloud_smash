"""Tests for async Ollama client (embeddings, fallback, streaming chat, tunnel headers)."""

import json

import httpx

from cloud_smash.clients.ollama import OllamaClient
from cloud_smash.config import Settings


def _test_settings() -> Settings:
    return Settings(
        ollama_base_url="https://ollama.example.com",
        cf_access_client_id="cf-id",
        cf_access_client_secret="cf-secret",
        ollama_bearer_token="secret-token",
    )


async def test_embed_texts_and_tunnel_headers() -> None:
    captured_headers: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_headers.update(dict(request.headers))
        assert request.url.path == "/api/embed"
        return httpx.Response(200, json={"embeddings": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        client = OllamaClient(_test_settings(), http_client=http)
        vectors = await client.embed_texts(["first", "second"])

    assert vectors == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    assert captured_headers.get("cf-access-client-id") == "cf-id"
    assert captured_headers.get("cf-access-client-secret") == "cf-secret"
    assert captured_headers.get("authorization") == "Bearer secret-token"


async def test_embed_falls_back_to_legacy_endpoint_on_404() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/embed":
            return httpx.Response(404, json={"error": "not found"})
        if request.url.path == "/api/embeddings":
            return httpx.Response(200, json={"embedding": [0.9, 0.8]})
        raise AssertionError(f"Unexpected path {request.url.path}")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        client = OllamaClient(_test_settings(), http_client=http)
        vec = await client.embed_query("vpc peering")

    assert vec == [0.9, 0.8]


async def test_stream_chat_yields_tokens() -> None:
    ndjson = "\n".join(
        [
            json.dumps({"message": {"content": "Use "}, "done": False}),
            json.dumps({"message": {"content": "VPC"}, "done": False}),
            json.dumps({"message": {"content": ""}, "done": True}),
        ]
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/chat"
        return httpx.Response(200, text=ndjson)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        client = OllamaClient(_test_settings(), http_client=http)
        tokens = [tok async for tok in client.stream_chat([{"role": "user", "content": "hi"}])]

    assert "".join(tokens) == "Use VPC"
