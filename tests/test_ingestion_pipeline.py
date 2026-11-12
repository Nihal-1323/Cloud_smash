"""Tests for end-to-end IngestionPipeline orchestration."""

from cloud_smash.clients.pinecone_store import VectorRecord
from cloud_smash.config import Settings
from cloud_smash.ingestion.pipeline import IngestionPipeline
from cloud_smash.ingestion.scraper import DocSource, ScrapedDocument


class _StubScraper:
    async def fetch_all(self, sources: list[DocSource]) -> list[ScrapedDocument]:
        return [
            ScrapedDocument(
                url=src.url,
                title=src.title or "Doc",
                provider=src.provider,
                topic=src.topic,
                content="# Title\n\nConfigure VPC subnet CIDR blocks carefully.",
            )
            for src in sources
        ]


class _StubOllamaEmbedder:
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [[0.1, 0.2, 0.3] for _ in texts]


class _StubPinecone:
    def __init__(self) -> None:
        self.ensured = False
        self.upserted: list[VectorRecord] = []

    def ensure_index(self) -> None:
        self.ensured = True

    async def aupsert_records(self, records: list[VectorRecord], batch_size: int | None = None) -> int:
        self.upserted.extend(records)
        return len(records)


async def test_ingestion_pipeline_dry_run_skips_external_writes() -> None:
    store = _StubPinecone()
    pipeline = IngestionPipeline(
        Settings(),
        scraper=_StubScraper(),
        ollama=_StubOllamaEmbedder(),
        pinecone_store=store,
    )
    summary = await pipeline.run(
        [DocSource(provider="gcp", url="https://cloud.google.com/vpc/docs/vpc")],
        dry_run=True,
    )
    assert summary.documents_scraped == 1
    assert summary.chunks_created == 1
    assert summary.vectors_upserted == 0
    assert not store.ensured


async def test_ingestion_pipeline_upserts_embedded_chunks() -> None:
    store = _StubPinecone()
    pipeline = IngestionPipeline(
        Settings(),
        scraper=_StubScraper(),
        ollama=_StubOllamaEmbedder(),
        pinecone_store=store,
    )
    summary = await pipeline.run(
        [DocSource(provider="azure", url="https://learn.microsoft.com/vnet")]
    )
    assert summary.documents_scraped == 1
    assert summary.chunks_created == 1
    assert summary.vectors_upserted == 1
    assert store.ensured
    assert store.upserted[0].values == [0.1, 0.2, 0.3]
