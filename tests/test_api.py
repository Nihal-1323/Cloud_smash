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

    async def embed(self, text: str) -> list[float]:
        return [0.1] * 768

    async def embed_query(self, text: str) -> list[float]:
        return [0.1] * 768

    async def aclose(self) -> None:
        return None


class _FakeStore:
    def __init__(self, fail_health: bool = False) -> None:
        self._fail_health = fail_health
        self._chunk = RetrievedChunk(
            id="doc-1",
            score=0.94,
            text="GKE Autopilot manages cluster nodes automatically.",
            url="https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview",
            title="GKE Autopilot Overview",
            provider="gcp",
            topic="kubernetes",
        )

    def health_check(self) -> dict:
        if self._fail_health:
            raise RuntimeError("Pinecone unreachable")
        return {"status": "ok", "index": "cloud-infra-docs", "total_vector_count": 42}

    def get_all_chunks(self, force_refresh: bool = False, max_chunks: int = 200) -> list[RetrievedChunk]:
        return [self._chunk]

    async def aget_all_chunks(self, force_refresh: bool = False, max_chunks: int = 200) -> list[RetrievedChunk]:
        return [self._chunk]

    async def aquery(self, vector: list[float], top_k: int | None = None, provider: str | None = None) -> list[RetrievedChunk]:
        return [self._chunk]


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


def test_chunks_endpoint() -> None:
    app = create_app(
        Settings(),
        ollama=_FakeOllama(),
        pinecone_store=_FakeStore(),
        rag_service=_FakeRAGService(),
        mount_ui=False,
    )
    with TestClient(app) as client:
        resp = client.get("/api/chunks")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_count"] == 1
        assert data["chunks"][0]["id"] == "doc-1"
        assert data["provider_counts"]["gcp"] == 1


def test_graph_endpoints_get_and_post() -> None:
    app = create_app(
        Settings(),
        ollama=_FakeOllama(),
        pinecone_store=_FakeStore(),
        rag_service=_FakeRAGService(),
        mount_ui=False,
    )
    with TestClient(app) as client:
        # GET default graph (no query yet)
        get_resp = client.get("/api/graph")
        assert get_resp.status_code == 200
        get_data = get_resp.json()
        assert get_data["input_chunk"] is None
        assert get_data["total_present_count"] == 1

        # POST with query
        post_resp = client.post("/api/graph", json={"query": "What is GKE Autopilot?", "top_k": 2})
        assert post_resp.status_code == 200
        post_data = post_resp.json()
        assert post_data["input_chunk"] is not None
        assert post_data["input_chunk"]["query"] == "What is GKE Autopilot?"
        assert post_data["input_chunk"]["status"] == "vectorized"
        assert len(post_data["retrieved_chunks"]) == 1
        assert post_data["retrieved_chunks"][0]["id"] == "doc-1"
        # The present chunk should be marked is_retrieved=True
        assert post_data["present_chunks"][0]["is_retrieved"] is True
