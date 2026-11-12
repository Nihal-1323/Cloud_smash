"""RAG service orchestrating query embedding, Pinecone retrieval, and Ollama streaming."""

from collections.abc import AsyncIterator, Sequence
from dataclasses import dataclass

from cloud_smash.clients.ollama import OllamaClient
from cloud_smash.clients.pinecone_store import PineconeStore, RetrievedChunk
from cloud_smash.config import Settings
from cloud_smash.rag.prompts import NO_CONTEXT_RESPONSE, build_rag_messages


@dataclass(frozen=True)
class RAGResult:
    """Complete non-streaming RAG response with retrieved source citations."""

    answer: str
    sources: list[RetrievedChunk]


class RAGService:
    """Executes semantic search against Pinecone and grounded generation via Ollama."""

    def __init__(
        self,
        settings: Settings,
        ollama: OllamaClient,
        pinecone_store: PineconeStore,
    ) -> None:
        self._settings = settings
        self._ollama = ollama
        self._store = pinecone_store

    async def retrieve(
        self,
        query: str,
        *,
        top_k: int | None = None,
        provider: str | None = None,
    ) -> list[RetrievedChunk]:
        """Embed the user query via Ollama and query Pinecone for top-K matching chunks."""
        query_vector = await self._ollama.embed_query(query)
        k = top_k or self._settings.rag_top_k
        return await self._store.aquery(query_vector, top_k=k, provider=provider)

    async def answer(
        self,
        query: str,
        *,
        top_k: int | None = None,
        provider: str | None = None,
        history: Sequence[dict[str, str]] | None = None,
    ) -> RAGResult:
        """Run full RAG and return the complete grounded response plus sources."""
        chunks = await self.retrieve(query, top_k=top_k, provider=provider)
        if not chunks:
            return RAGResult(answer=NO_CONTEXT_RESPONSE, sources=[])

        messages = build_rag_messages(query, chunks, history=history)
        response_text = await self._ollama.chat(messages)
        return RAGResult(answer=response_text, sources=chunks)

    async def prepare_stream(
        self,
        query: str,
        *,
        top_k: int | None = None,
        provider: str | None = None,
        history: Sequence[dict[str, str]] | None = None,
    ) -> tuple[list[RetrievedChunk], AsyncIterator[str]]:
        """Retrieve context chunks first, then return an async token stream."""
        chunks = await self.retrieve(query, top_k=top_k, provider=provider)
        if not chunks:

            async def _empty_stream() -> AsyncIterator[str]:
                yield NO_CONTEXT_RESPONSE

            return [], _empty_stream()

        messages = build_rag_messages(query, chunks, history=history)
        return chunks, self._ollama.stream_chat(messages)
