"""Tests for PineconeStore batch upserts, retry backoff, and cosine query filtering."""

from cloud_smash.clients.pinecone_store import PineconeStore, VectorRecord
from cloud_smash.config import Settings


class _FakeRateLimitError(Exception):
    def __init__(self) -> None:
        super().__init__("429 Too Many Requests")
        self.status = 429


class _FakeIndex:
    def __init__(self, fail_first_upsert: bool = False) -> None:
        self.upsert_calls: list[dict] = []
        self.query_calls: list[dict] = []
        self._fail_first_upsert = fail_first_upsert
        self._attempts = 0

    def upsert(self, *, vectors: list[dict], namespace: str) -> None:
        self._attempts += 1
        if self._fail_first_upsert and self._attempts == 1:
            raise _FakeRateLimitError()
        self.upsert_calls.append({"vectors": vectors, "namespace": namespace})

    def query(self, **kwargs: object) -> dict:
        self.query_calls.append(kwargs)
        return {
            "matches": [
                {
                    "id": "chunk-1",
                    "score": 0.9123,
                    "metadata": {
                        "text": "Azure RBAC uses role assignments.",
                        "url": "https://learn.microsoft.com/rbac",
                        "title": "Azure RBAC",
                        "provider": "azure",
                        "topic": "iam",
                        "chunk_index": 0,
                    },
                }
            ]
        }


def test_upsert_batches_and_retries_on_rate_limit(monkeypatch) -> None:
    monkeypatch.setattr("time.sleep", lambda _: None)
    fake_index = _FakeIndex(fail_first_upsert=True)
    settings = Settings(pinecone_api_key="test-key", upsert_batch_size=2)
    store = PineconeStore(settings, index=fake_index)

    records = [
        VectorRecord(id=f"id-{i}", values=[0.1, 0.2], metadata={"text": f"chunk {i}"})
        for i in range(3)
    ]
    total = store.upsert_records(records)

    assert total == 3
    assert len(fake_index.upsert_calls) == 2
    assert len(fake_index.upsert_calls[0]["vectors"]) == 2
    assert len(fake_index.upsert_calls[1]["vectors"]) == 1


def test_query_applies_provider_filter_and_maps_chunks() -> None:
    fake_index = _FakeIndex()
    settings = Settings(pinecone_api_key="test-key", rag_top_k=3)
    store = PineconeStore(settings, index=fake_index)

    results = store.query([0.1, 0.2], top_k=4, provider="azure")

    assert len(results) == 1
    assert results[0].provider == "azure"
    assert results[0].score == 0.9123
    assert fake_index.query_calls[0]["filter"] == {"provider": {"$eq": "azure"}}
    assert fake_index.query_calls[0]["top_k"] == 4


def test_get_all_chunks_and_caching() -> None:
    fake_index = _FakeIndex()
    settings = Settings(pinecone_api_key="test-key", pinecone_embed_dimension=2)
    store = PineconeStore(settings, index=fake_index)

    chunks = store.get_all_chunks()
    assert len(chunks) == 1
    assert chunks[0].id == "chunk-1"
    assert chunks[0].provider == "azure"

    # Second call should use cache
    call_count_before = len(fake_index.query_calls)
    cached = store.get_all_chunks()
    assert len(cached) == 1
    assert len(fake_index.query_calls) == call_count_before
