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


class InputChunkInfo(BaseModel):
    """Metadata and vector details for the user input query chunk."""

    query: str
    token_count: int
    embed_model: str
    embed_dimension: int
    status: str = "vectorized"


class PresentChunkInfo(BaseModel):
    """Representation of an ingested document chunk present in the Pinecone index."""

    id: str
    provider: str
    topic: str = ""
    title: str
    url: str
    chunk_index: int = 0
    snippet: str
    is_retrieved: bool = False
    score: float | None = None
    retrieval_rank: int | None = None

    @classmethod
    def from_chunk(
        cls,
        chunk: RetrievedChunk,
        is_retrieved: bool = False,
        score: float | None = None,
        rank: int | None = None,
        max_snippet_chars: int = 320,
    ) -> "PresentChunkInfo":
        snippet = chunk.text.strip()
        if len(snippet) > max_snippet_chars:
            snippet = snippet[: max_snippet_chars - 3].rstrip() + "..."
        return cls(
            id=chunk.id,
            provider=chunk.provider,
            topic=chunk.topic,
            title=chunk.title,
            url=chunk.url,
            chunk_index=chunk.chunk_index,
            snippet=snippet,
            is_retrieved=is_retrieved,
            score=round(score, 4) if score is not None else None,
            retrieval_rank=rank,
        )


class GraphMapRequest(BaseModel):
    """Payload to request graph mapping for a specific query."""

    query: str = Field(default="", max_length=4000)
    provider: Literal["all", "gcp", "azure"] = Field(default="all")
    top_k: int | None = Field(default=None, ge=1, le=12)


class GraphMapResponse(BaseModel):
    """Comprehensive graph data separating input chunk, retrieved chunks, and all present chunks."""

    input_chunk: InputChunkInfo | None = None
    retrieved_chunks: list[SourceCitation] = Field(default_factory=list)
    present_chunks: list[PresentChunkInfo] = Field(default_factory=list)
    total_present_count: int = 0
    provider_counts: dict[str, int] = Field(default_factory=dict)
    topic_counts: dict[str, int] = Field(default_factory=dict)


class ChunksResponse(BaseModel):
    """Response containing all present chunks currently in the vector database."""

    chunks: list[PresentChunkInfo]
    total_count: int
    provider_counts: dict[str, int]
    topic_counts: dict[str, int]
