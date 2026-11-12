"""End-to-end document ingestion pipeline: scrape -> chunk -> embed -> Pinecone upsert."""

import argparse
import asyncio
from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Sequence

from cloud_smash.clients.ollama import OllamaClient
from cloud_smash.clients.pinecone_store import PineconeStore, VectorRecord
from cloud_smash.config import Settings, get_settings
from cloud_smash.ingestion.chunker import DocumentChunk, TokenChunker
from cloud_smash.ingestion.scraper import AsyncDocScraper, DocSource, load_sources_from_yaml

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class IngestionSummary:
    """Statistics produced by an ingestion pipeline run."""

    documents_scraped: int
    chunks_created: int
    vectors_upserted: int


class IngestionPipeline:
    """Coordinates async scraping, token chunking, local embedding, and Pinecone batch upserts."""

    def __init__(
        self,
        settings: Settings,
        scraper: AsyncDocScraper | None = None,
        chunker: TokenChunker | None = None,
        ollama: OllamaClient | None = None,
        pinecone_store: PineconeStore | None = None,
    ) -> None:
        self._settings = settings
        self._scraper = scraper or AsyncDocScraper(concurrency=settings.scrape_concurrency)
        self._owns_scraper = scraper is None
        self._chunker = chunker or TokenChunker(
            chunk_size_tokens=settings.chunk_size_tokens,
            chunk_overlap_tokens=settings.chunk_overlap_tokens,
        )
        self._ollama = ollama or OllamaClient(settings)
        self._owns_ollama = ollama is None
        self._store = pinecone_store or PineconeStore(settings)

    async def aclose(self) -> None:
        """Release resources owned by the pipeline."""
        if self._owns_scraper:
            await self._scraper.aclose()
        if self._owns_ollama:
            await self._ollama.aclose()

    async def run(
        self,
        sources: Sequence[DocSource],
        *,
        dry_run: bool = False,
        embed_batch_size: int = 32,
    ) -> IngestionSummary:
        """Execute ingestion across the provided sources."""
        docs = await self._scraper.fetch_all(sources)
        chunks = self._chunker.chunk_documents(docs)
        logger.info("Scraped %d documents into %d chunks.", len(docs), len(chunks))

        if dry_run or not chunks:
            return IngestionSummary(
                documents_scraped=len(docs),
                chunks_created=len(chunks),
                vectors_upserted=0,
            )

        await asyncio.to_thread(self._store.ensure_index)
        records = await self._embed_chunks(chunks, batch_size=embed_batch_size)
        upserted = await self._store.aupsert_records(records)
        logger.info("Upserted %d vectors into Pinecone.", upserted)

        return IngestionSummary(
            documents_scraped=len(docs),
            chunks_created=len(chunks),
            vectors_upserted=upserted,
        )

    async def _embed_chunks(
        self, chunks: list[DocumentChunk], *, batch_size: int
    ) -> list[VectorRecord]:
        records: list[VectorRecord] = []
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start : start + batch_size]
            embeddings = await self._ollama.embed_texts([chunk.text for chunk in batch])
            for chunk, vector in zip(batch, embeddings, strict=True):
                records.append(
                    VectorRecord(id=chunk.id, values=vector, metadata=chunk.metadata)
                )
        return records


async def _run_cli(args: argparse.Namespace) -> IngestionSummary:
    settings = get_settings()
    if args.url:
        sources = [
            DocSource(
                provider=args.provider.lower(),
                url=args.url,
                title=args.title or "",
                topic=args.topic or "",
            )
        ]
    else:
        sources = load_sources_from_yaml(Path(args.sources or settings.sources_config_path))

    pipeline = IngestionPipeline(settings)
    try:
        return await pipeline.run(sources, dry_run=args.dry_run)
    finally:
        await pipeline.aclose()


def main() -> None:
    """CLI entry point for scraping, chunking, embedding, and upserting docs."""
    parser = argparse.ArgumentParser(description="Ingest cloud docs into Pinecone.")
    parser.add_argument("--sources", type=str, default=None, help="Path to sources.yaml")
    parser.add_argument("--url", type=str, default=None, help="Single documentation URL to ingest")
    parser.add_argument("--provider", type=str, default="gcp", help="Provider for --url (gcp|azure)")
    parser.add_argument("--title", type=str, default="", help="Optional title override for --url")
    parser.add_argument("--topic", type=str, default="", help="Optional topic tag for --url")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scrape and chunk only; skip Ollama embedding and Pinecone upsert.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    summary = asyncio.run(_run_cli(args))
    print(
        f"Ingestion complete: docs={summary.documents_scraped}, "
        f"chunks={summary.chunks_created}, upserted={summary.vectors_upserted}"
    )


if __name__ == "__main__":
    main()
