"""Token-aware document chunker preserving YAML configurations and IAM policy blocks."""

from dataclasses import dataclass
import hashlib
from typing import Any

import tiktoken

from cloud_smash.ingestion.scraper import ScrapedDocument

_DEFAULT_SEPARATORS = ("\n## ", "\n### ", "\n```", "\n\n", "\n", " ")


@dataclass(frozen=True)
class DocumentChunk:
    """Single token-bounded chunk with deterministic ID and Pinecone-ready metadata."""

    id: str
    text: str
    token_count: int
    chunk_index: int
    metadata: dict[str, Any]


class TokenChunker:
    """Splits cleaned Markdown/YAML docs into fixed token windows with overlap."""

    def __init__(
        self,
        chunk_size_tokens: int = 500,
        chunk_overlap_tokens: int = 50,
        encoding_name: str = "cl100k_base",
    ) -> None:
        if chunk_overlap_tokens >= chunk_size_tokens:
            raise ValueError("chunk_overlap_tokens must be smaller than chunk_size_tokens.")
        self._chunk_size = chunk_size_tokens
        self._chunk_overlap = chunk_overlap_tokens
        self._encoding = tiktoken.get_encoding(encoding_name)

    def count_tokens(self, text: str) -> int:
        """Count exact tokens using the configured tiktoken encoding."""
        return len(self._encoding.encode(text, disallowed_special=()))

    def _split_by_tokens(self, text: str) -> list[str]:
        """Fallback hard split on exact token boundaries when no separator fits."""
        token_ids = self._encoding.encode(text, disallowed_special=())
        step = self._chunk_size - self._chunk_overlap
        pieces: list[str] = []
        for start in range(0, len(token_ids), step):
            window = token_ids[start : start + self._chunk_size]
            decoded = self._encoding.decode(window).strip()
            if decoded:
                pieces.append(decoded)
            if start + self._chunk_size >= len(token_ids):
                break
        return pieces

    def _recursive_split(self, text: str, separators: tuple[str, ...]) -> list[str]:
        """Break text into atomic segments each <= chunk_size tokens."""
        stripped = text.strip()
        if not stripped:
            return []
        if self.count_tokens(stripped) <= self._chunk_size:
            return [stripped]
        if not separators:
            return self._split_by_tokens(stripped)

        sep = separators[0]
        parts = stripped.split(sep)
        if len(parts) == 1:
            return self._recursive_split(stripped, separators[1:])

        segments: list[str] = []
        for idx, part in enumerate(parts):
            rebuilt = part if idx == 0 else f"{sep.lstrip('\n')}{part}" if sep.startswith("\n") else f"{sep}{part}"
            rebuilt = rebuilt.strip()
            if not rebuilt:
                continue
            if self.count_tokens(rebuilt) <= self._chunk_size:
                segments.append(rebuilt)
            else:
                segments.extend(self._recursive_split(rebuilt, separators[1:]))
        return segments

    def _merge_with_overlap(self, segments: list[str]) -> list[str]:
        """Pack segments up to chunk_size_tokens while carrying chunk_overlap_tokens forward."""
        chunks: list[str] = []
        current_parts: list[str] = []

        for seg in segments:
            candidate = "\n\n".join(current_parts + [seg]) if current_parts else seg
            if self.count_tokens(candidate) <= self._chunk_size:
                current_parts.append(seg)
                continue

            if current_parts:
                emitted = "\n\n".join(current_parts).strip()
                chunks.append(emitted)
                current_parts = self._overlap_tail(emitted, seg)
            else:
                chunks.append(seg)
                current_parts = []

        if current_parts:
            chunks.append("\n\n".join(current_parts).strip())
        return chunks

    def _overlap_tail(self, previous_chunk: str, next_segment: str) -> list[str]:
        """Extract up to chunk_overlap_tokens from the end of previous_chunk before next_segment."""
        if self._chunk_overlap <= 0:
            return [next_segment]
        prev_tokens = self._encoding.encode(previous_chunk, disallowed_special=())
        tail_text = self._encoding.decode(prev_tokens[-self._chunk_overlap :]).strip()
        if tail_text:
            combined = f"{tail_text}\n\n{next_segment}"
            if self.count_tokens(combined) <= self._chunk_size:
                return [tail_text, next_segment]
        return [next_segment]

    def split_text(self, text: str) -> list[str]:
        """Split raw markdown/YAML text into overlapping token-bounded chunks."""
        segments = self._recursive_split(text, _DEFAULT_SEPARATORS)
        if not segments:
            return []
        return self._merge_with_overlap(segments)

    def chunk_document(self, doc: ScrapedDocument) -> list[DocumentChunk]:
        """Split a ScrapedDocument into overlapping token-bounded DocumentChunks."""
        raw_chunks = self.split_text(doc.content)
        chunks: list[DocumentChunk] = []
        for idx, text in enumerate(raw_chunks):
            chunk_id = self._deterministic_id(doc.url, idx)
            chunks.append(
                DocumentChunk(
                    id=chunk_id,
                    text=text,
                    token_count=self.count_tokens(text),
                    chunk_index=idx,
                    metadata={
                        "url": doc.url,
                        "title": doc.title,
                        "provider": doc.provider,
                        "topic": doc.topic,
                        "chunk_index": idx,
                        "text": text,
                    },
                )
            )
        return chunks

    def chunk_documents(self, docs: list[ScrapedDocument]) -> list[DocumentChunk]:
        """Chunk a collection of ScrapedDocuments."""
        all_chunks: list[DocumentChunk] = []
        for doc in docs:
            all_chunks.extend(self.chunk_document(doc))
        return all_chunks

    @staticmethod
    def _deterministic_id(url: str, chunk_index: int) -> str:
        digest = hashlib.sha256(f"{url}::{chunk_index}".encode("utf-8")).hexdigest()
        return digest[:24]
