"""Pinecone vector store client with Starter-tier serverless setup and retry backoff."""

import asyncio
from dataclasses import dataclass
import logging
from typing import Any

from pinecone import Pinecone, ServerlessSpec

from cloud_smash.config import Settings
from cloud_smash.retry import retry_sync

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class VectorRecord:
    """Single embedded document chunk prepared for Pinecone upsert."""

    id: str
    values: list[float]
    metadata: dict[str, Any]


@dataclass(frozen=True)
class RetrievedChunk:
    """Retrieved document chunk with similarity score and source metadata."""

    id: str
    score: float
    text: str
    url: str
    title: str
    provider: str
    topic: str = ""
    chunk_index: int = 0


def _is_retryable_pinecone_error(exc: Exception) -> bool:
    """Detect Pinecone rate-limit (429), 5xx, or transient transport failures."""
    status = getattr(exc, "status", None)
    if isinstance(status, int) and status in {429, 500, 502, 503, 504}:
        return True
    message = str(exc).lower()
    return any(
        hint in message
        for hint in ("429", "rate limit", "too many requests", "timeout", "temporarily unavailable")
    )


class PineconeStore:
    """Wrapper around Pinecone Starter-tier serverless index operations."""

    def __init__(
        self,
        settings: Settings,
        client: Any | None = None,
        index: Any | None = None,
    ) -> None:
        self._settings = settings
        self._index_name = settings.pinecone_index_name
        self._namespace = settings.pinecone_namespace
        self._dimension = settings.pinecone_embed_dimension
        self._client = client
        self._index = index
        self._cached_chunks: list[RetrievedChunk] | None = None
        self._cache_time: float = 0.0
        self._cache_ttl: float = 300.0

    def _get_client(self) -> Any:
        if self._client is None:
            if not self._settings.pinecone_api_key:
                raise RuntimeError("PINECONE_API_KEY is not configured.")
            self._client = Pinecone(api_key=self._settings.pinecone_api_key)
        return self._client

    def _get_index(self) -> Any:
        if self._index is None:
            self._index = self._get_client().Index(self._index_name)
        return self._index

    def ensure_index(self) -> None:
        """Create the Pinecone serverless index if it does not already exist."""
        client = self._get_client()
        existing = client.list_indexes()
        names = (
            existing.names()
            if hasattr(existing, "names")
            else [item["name"] if isinstance(item, dict) else item.name for item in existing]
        )
        if self._index_name in names:
            logger.info("Pinecone index '%s' already exists.", self._index_name)
            return

        logger.info(
            "Creating Pinecone serverless index '%s' (dim=%d, metric=cosine).",
            self._index_name,
            self._dimension,
        )
        retry_sync(
            lambda: client.create_index(
                name=self._index_name,
                dimension=self._dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=self._settings.pinecone_cloud,
                    region=self._settings.pinecone_region,
                ),
            ),
            is_retryable=_is_retryable_pinecone_error,
        )

    def upsert_records(self, records: list[VectorRecord], batch_size: int | None = None) -> int:
        """Upsert vector records in batches with exponential backoff on rate limits."""
        if not records:
            return 0

        size = batch_size or self._settings.upsert_batch_size
        index = self._get_index()
        total_upserted = 0

        for start in range(0, len(records), size):
            batch = records[start : start + size]
            vectors = [
                {"id": rec.id, "values": rec.values, "metadata": rec.metadata} for rec in batch
            ]
            retry_sync(
                lambda payload=vectors: index.upsert(vectors=payload, namespace=self._namespace),
                is_retryable=_is_retryable_pinecone_error,
            )
            total_upserted += len(batch)

        self._cached_chunks = None
        return total_upserted

    def query(
        self,
        vector: list[float],
        top_k: int | None = None,
        provider: str | None = None,
    ) -> list[RetrievedChunk]:
        """Execute cosine similarity search against Pinecone with retry backoff."""
        k = top_k or self._settings.rag_top_k
        index = self._get_index()
        metadata_filter = (
            {"provider": {"$eq": provider.lower()}}
            if provider and provider.lower() != "all"
            else None
        )

        response = retry_sync(
            lambda: index.query(
                vector=vector,
                top_k=k,
                namespace=self._namespace,
                include_metadata=True,
                filter=metadata_filter,
            ),
            is_retryable=_is_retryable_pinecone_error,
        )
        matches = (
            response.get("matches", [])
            if isinstance(response, dict)
            else getattr(response, "matches", [])
        )

        chunks: list[RetrievedChunk] = []
        for match in matches:
            meta = (
                match.get("metadata", {})
                if isinstance(match, dict)
                else getattr(match, "metadata", {}) or {}
            )
            match_id = match["id"] if isinstance(match, dict) else match.id
            score = float(match["score"] if isinstance(match, dict) else match.score)
            chunks.append(
                RetrievedChunk(
                    id=match_id,
                    score=score,
                    text=str(meta.get("text", "")),
                    url=str(meta.get("url", "")),
                    title=str(meta.get("title", "Untitled")),
                    provider=str(meta.get("provider", "unknown")),
                    topic=str(meta.get("topic", "")),
                    chunk_index=int(meta.get("chunk_index", 0)),
                )
            )
        return chunks

    async def aupsert_records(
        self, records: list[VectorRecord], batch_size: int | None = None
    ) -> int:
        """Async wrapper around batch upsert for async ingestion pipelines."""
        return await asyncio.to_thread(self.upsert_records, records, batch_size)

    async def aquery(
        self,
        vector: list[float],
        top_k: int | None = None,
        provider: str | None = None,
    ) -> list[RetrievedChunk]:
        """Async wrapper around Pinecone query so FastAPI event loops stay non-blocking."""
        return await asyncio.to_thread(self.query, vector, top_k, provider)

    def health_check(self) -> dict[str, Any]:
        """Check Pinecone index connectivity and return vector count stats."""
        stats = retry_sync(
            lambda: self._get_index().describe_index_stats(),
            is_retryable=_is_retryable_pinecone_error,
        )
        total_vectors = (
            stats.get("total_vector_count", 0)
            if isinstance(stats, dict)
            else getattr(stats, "total_vector_count", 0)
        )
        return {
            "status": "ok",
            "index": self._index_name,
            "namespace": self._namespace,
            "total_vector_count": total_vectors,
        }

    def get_all_chunks(self, force_refresh: bool = False, max_chunks: int = 200) -> list[RetrievedChunk]:
        """Fetch all vector chunks present in the index with in-memory caching."""
        import time

        now = time.time()
        if not force_refresh and self._cached_chunks is not None and (now - self._cache_time) < self._cache_ttl:
            return list(self._cached_chunks)

        try:
            index = self._get_index()
            response = retry_sync(
                lambda: index.query(
                    vector=[0.0] * self._dimension,
                    top_k=max_chunks,
                    namespace=self._namespace,
                    include_metadata=True,
                ),
                is_retryable=_is_retryable_pinecone_error,
            )
            matches = (
                response.get("matches", [])
                if isinstance(response, dict)
                else getattr(response, "matches", [])
            )
            chunks: list[RetrievedChunk] = []
            for match in matches:
                meta = (
                    match.get("metadata", {})
                    if isinstance(match, dict)
                    else getattr(match, "metadata", {}) or {}
                )
                match_id = match["id"] if isinstance(match, dict) else match.id
                chunks.append(
                    RetrievedChunk(
                        id=match_id,
                        score=0.0,
                        text=str(meta.get("text", "")),
                        url=str(meta.get("url", "")),
                        title=str(meta.get("title", "Untitled")),
                        provider=str(meta.get("provider", "unknown")),
                        topic=str(meta.get("topic", "")),
                        chunk_index=int(meta.get("chunk_index", 0)),
                    )
                )
            chunks.sort(key=lambda c: (c.provider, c.topic, c.chunk_index))
            self._cached_chunks = chunks
            self._cache_time = now
            return list(chunks)
        except Exception as exc:
            logger.warning("Could not fetch all chunks from Pinecone: %s", exc)
            if self._cached_chunks is not None:
                return list(self._cached_chunks)
            return []

    async def aget_all_chunks(
        self, force_refresh: bool = False, max_chunks: int = 200
    ) -> list[RetrievedChunk]:
        """Async wrapper around get_all_chunks."""
        return await asyncio.to_thread(self.get_all_chunks, force_refresh, max_chunks)
