"""Pydantic request and response schemas for the Cloud Smash API."""

from typing import Any, Literal

from pydantic import BaseModel, Field

from cloud_smash.clients.pinecone_store import RetrievedChunk


class ChatTurn(BaseModel):
    """Single message turn in conversation history."""

    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """Incoming RAG query payload."""

    query: str = Field(..., min_length=1, max_length=4000)
    provider: Literal["all", "gcp", "azure"] = Field(default="all")
    top_k: int | None = Field(default=None, ge=1, le=10)
    history: list[ChatTurn] = Field(default_factory=list)


class SourceCitation(BaseModel):
    """Metadata and excerpt for a retrieved documentation chunk."""

    id: str
    score: float
    title: str
    url: str
    provider: str
    topic: str = ""
    snippet: str

    @classmethod
    def from_chunk(cls, chunk: RetrievedChunk, max_snippet_chars: int = 320) -> "SourceCitation":
        """Build a SourceCitation from a Pinecone RetrievedChunk."""
        snippet = chunk.text.strip()
        if len(snippet) > max_snippet_chars:
            snippet = snippet[: max_snippet_chars - 3].rstrip() + "..."
        return cls(
            id=chunk.id,
            score=round(chunk.score, 4),
            title=chunk.title,
            url=chunk.url,
            provider=chunk.provider,
            topic=chunk.topic,
            snippet=snippet,
        )


class ChatResponse(BaseModel):
    """Non-streaming RAG response with grounded answer and source citations."""

    answer: str
    sources: list[SourceCitation]


class HealthResponse(BaseModel):
    """Service readiness report for Ollama tunnel and Pinecone."""

    status: Literal["ok", "degraded"]
    ollama: dict[str, Any]
    pinecone: dict[str, Any]
