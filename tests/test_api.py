"""Tests for FastAPI endpoints (/api/health, /api/chat, /api/chat/stream) and Gradio mount."""

from collections.abc import AsyncIterator
import json

from fastapi.testclient import TestClient

from cloud_smash.api.app import create_app
from cloud_smash.clients.pinecone_store import RetrievedChunk
from cloud_smash.config import Settings
from cloud_smash.rag.service import RAGResult


class _FakeOllama:
    async def health_check(self) -> dict:
        return {"status": "ok", "models": ["qwen2.5:7b-instruct", "nomic-embed-text"]}

    async def aclose(self) -> None:
        return None


class _FakeStore:
    def __init__(self, fail_health: bool = False) -> None:
        self._fail_health = fail_health

    def health_check(self) -> dict:
        if self._fail_health:
            raise RuntimeError("Pinecone unreachable")
        return {"status": "ok", "index": "cloud-infra-docs", "total_vector_count": 42}


class _FakeRAGService:
    def __init__(self) -> None:
        self._chunk = RetrievedChunk(
            id="doc-1",
            score=0.94,
            text="GKE Autopilot manages cluster nodes automatically.",
            url="https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview",
            title="GKE Autopilot Overview",
            provider="gcp",
            topic="kubernetes",
        )

    async def answer(self, query: str, **kwargs: object) -> RAGResult:
        return RAGResult(
            answer="GKE Autopilot automatically provisions and manages nodes [Source 1].",
            sources=[self._chunk],
        )

    async def prepare_stream(
        self, query: str, **kwargs: object
    ) -> tuple[list[RetrievedChunk], AsyncIterator[str]]:
        async def _gen() -> AsyncIterator[str]:
            yield "GKE Autopilot "
            yield "[Source 1]."

        return [self._chunk], _gen()


def test_health_endpoint_ok_and_degraded() -> None:
    app_ok = create_app(
        Settings(),
        ollama=_FakeOllama(),
        pinecone_store=_FakeStore(),
        rag_service=_FakeRAGService(),
        mount_ui=False,
    )
    with TestClient(app_ok) as client:
        resp = client.get("/api/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert body["pinecone"]["total_vector_count"] == 42

    app_degraded = create_app(
        Settings(),
        ollama=_FakeOllama(),
        pinecone_store=_FakeStore(fail_health=True),
        rag_service=_FakeRAGService(),
        mount_ui=False,
    )
    with TestClient(app_degraded) as client:
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "degraded"


def test_chat_endpoint_returns_answer_and_sources() -> None:
    app = create_app(
        Settings(),
        ollama=_FakeOllama(),
        pinecone_store=_FakeStore(),
        rag_service=_FakeRAGService(),
        mount_ui=False,
    )
    with TestClient(app) as client:
        resp = client.post("/api/chat", json={"query": "What is GKE Autopilot?", "provider": "gcp"})
        assert resp.status_code == 200
        data = resp.json()
        assert "[Source 1]" in data["answer"]
        assert len(data["sources"]) == 1
        assert data["sources"][0]["provider"] == "gcp"


def test_chat_stream_endpoint_emits_sse_events() -> None:
    app = create_app(
        Settings(),
        ollama=_FakeOllama(),
        pinecone_store=_FakeStore(),
        rag_service=_FakeRAGService(),
        mount_ui=False,
    )
    with TestClient(app) as client:
        with client.stream(
            "POST",
            "/api/chat/stream",
            json={"query": "Explain GKE Autopilot", "provider": "all"},
        ) as resp:
            assert resp.status_code == 200
            raw_text = "".join(resp.iter_text())

    assert "event: sources" in raw_text
    assert "event: token" in raw_text
    assert "event: done" in raw_text
    assert json.dumps({"token": "GKE Autopilot "}) in raw_text


def test_enterprise_ui_and_gradio_mount() -> None:
    app = create_app(
        Settings(),
        ollama=_FakeOllama(),
        pinecone_store=_FakeStore(),
        rag_service=_FakeRAGService(),
        mount_ui=True,
    )
    with TestClient(app) as client:
        resp = client.get("/")
        assert resp.status_code == 200
        assert "CLOUD SMASH" in resp.text
        assert "documentation console" in resp.text

        gradio_resp = client.get("/gradio")
        assert gradio_resp.status_code == 200
