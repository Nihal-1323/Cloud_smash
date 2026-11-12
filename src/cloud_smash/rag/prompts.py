"""Strict grounding system prompts and retrieved-context formatting."""

from collections.abc import Sequence

from cloud_smash.clients.pinecone_store import RetrievedChunk

SYSTEM_PROMPT = """You are a Cloud Infrastructure Documentation Assistant specializing in GCP and Azure.

STRICT GROUNDING RULES:
1. Answer ONLY using facts, CLI flags, YAML configurations, and IAM policies explicitly stated in the <context> blocks below.
2. Do NOT rely on outside knowledge, guess missing parameters, or fabricate resource names, IAM roles, or syntax.
3. If the <context> does not contain enough information to answer the question, state clearly:
   "I cannot find enough information in the retrieved documentation to answer that."
4. Cite your sources inline using [Source 1], [Source 2], etc., matching the source numbers in <context>."""

NO_CONTEXT_RESPONSE = (
    "I cannot find any relevant documentation chunks in the knowledge base to answer that. "
    "Try ingesting the relevant GCP or Azure documentation first or broadening your query."
)


def format_context(chunks: Sequence[RetrievedChunk]) -> str:
    """Format retrieved Pinecone chunks into numbered XML-style context blocks."""
    blocks: list[str] = []
    for idx, chunk in enumerate(chunks, start=1):
        blocks.append(
            f"[Source {idx}]\n"
            f"Provider: {chunk.provider.upper()}\n"
            f"Title: {chunk.title}\n"
            f"URL: {chunk.url}\n"
            f"Score: {chunk.score:.4f}\n"
            f"Content:\n{chunk.text}"
        )
    return "\n\n---\n\n".join(blocks)


def build_rag_messages(
    query: str,
    chunks: Sequence[RetrievedChunk],
    history: Sequence[dict[str, str]] | None = None,
    max_history_turns: int = 4,
) -> list[dict[str, str]]:
    """Assemble Ollama chat messages with strict grounding instructions and retrieved context."""
    messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        recent = list(history)[-(max_history_turns * 2) :]
        for turn in recent:
            role = turn.get("role")
            content = turn.get("content", "").strip()
            if role in {"user", "assistant"} and content:
                messages.append({"role": role, "content": content})

    context_block = format_context(chunks)
    user_prompt = (
        f"<context>\n{context_block}\n</context>\n\n"
        f"Question: {query}\n\n"
        "Answer using only the provided <context> and cite [Source N] where applicable."
    )
    messages.append({"role": "user", "content": user_prompt})
    return messages
