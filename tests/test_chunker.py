"""Tests for 500-token chunking with 50-token overlap."""

import pytest

from cloud_smash.ingestion.chunker import TokenChunker
from cloud_smash.ingestion.scraper import ScrapedDocument


def test_chunker_enforces_token_bounds_and_deterministic_ids() -> None:
    chunker = TokenChunker(chunk_size_tokens=500, chunk_overlap_tokens=50)
    # Build a synthetic multi-section YAML/Markdown document > 1200 tokens
    section = (
        "## IAM Policy Binding\n\n"
        "Configure least-privilege access for service accounts in GCP:\n\n"
        "```yaml\n"
        "bindings:\n"
        "  - role: roles/storage.objectViewer\n"
        "    members:\n"
        "      - serviceAccount:app-reader@my-project.iam.gserviceaccount.com\n"
        "```\n\n"
    )
    doc = ScrapedDocument(
        url="https://cloud.google.com/iam/docs/overview",
        title="IAM Overview",
        provider="gcp",
        topic="iam",
        content=section * 25,
    )

    chunks = chunker.chunk_document(doc)
    assert len(chunks) >= 3
    for idx, chunk in enumerate(chunks):
        assert 1 <= chunk.token_count <= 500
        assert chunk.chunk_index == idx
        assert chunk.metadata["provider"] == "gcp"
        assert chunk.metadata["url"] == doc.url
        assert chunk.metadata["text"] == chunk.text

    # Deterministic IDs across repeated runs
    repeat_chunks = chunker.chunk_document(doc)
    assert [c.id for c in chunks] == [c.id for c in repeat_chunks]


def test_chunker_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError, match="smaller than"):
        TokenChunker(chunk_size_tokens=100, chunk_overlap_tokens=100)
