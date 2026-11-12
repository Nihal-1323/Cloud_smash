"""Tests for RAGService grounding, empty-context handling, and streaming."""

from collections.abc import AsyncIterator

from cloud_smash.clients.pinecone_store import RetrievedChunk
from cloud_smash.config import Settings
from cloud_smash.rag.prompts import NO_CONTEXT_RESPONSE, build_rag_messages
from cloud_smash.rag.service import RAGService


class _StubOllama:
    def __init__(self) -> None:
        self.last_messages: list[dict[str, str]] = []

    async def embed_query(self, query: str) -> list[float]:
        return [0.25, 0.75]

    async def chat(self, messages: list[dict[str, str]]) -> str:
        self.last_messages = messages
        return "Use `gcloud iam` [Source 1]."

    async def stream_chat(self, messages: list[dict[str, str]]) -> AsyncIterator[str]:
        self.last_messages = messages
        for tok in ["Use ", "`gcloud iam` ", "[Source 1]."]:
            yield tok


class _StubStore:
    def __init__(self, chunks: list[RetrievedChunk]) -> None:
        self._chunks = chunks

    async def aquery(
        self, vector: list[float], top_k: int | None = None, provider: str | None = None
    ) -> list[RetrievedChunk]:
        return self._chunks


async def test_rag_service_grounds_prompt_and_returns_citations() -> None:
    chunk = RetrievedChunk(
        id="c1",
        score=0.95,
        text="Run `gcloud iam roles list` to inspect predefined roles.",
        url="https://cloud.google.com/iam/docs/roles-overview",
        title="IAM Roles",
        provider="gcp",
    )
    ollama = _StubOllama()
    service = RAGService(Settings(), ollama=ollama, pinecone_store=_StubStore([chunk]))

    result = await service.answer("How do I list IAM roles?", provider="gcp")

    assert "[Source 1]" in result.answer
    assert result.sources == [chunk]
    assert "STRICT GROUNDING RULES" in ollama.last_messages[0]["content"]
    assert "<context>" in ollama.last_messages[-1]["content"]


async def test_rag_service_handles_empty_retrieval_without_hallucination() -> None:
    ollama = _StubOllama()
    service = RAGService(Settings(), ollama=ollama, pinecone_store=_StubStore([]))

    chunks, stream = await service.prepare_stream("Unknown topic")
    tokens = [tok async for tok in stream]

    assert chunks == []
    assert "".join(tokens) == NO_CONTEXT_RESPONSE
    assert ollama.last_messages == []


def test_build_rag_messages_bounds_history() -> None:
    history = [{"role": "user", "content": f"q{i}"} for i in range(12)]
    msgs = build_rag_messages("latest?", [], history=history, max_history_turns=2)
    # system + max 4 history messages + final user prompt
    assert len(msgs) == 6
    assert msgs[1]["content"] == "q8"
