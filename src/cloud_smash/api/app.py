"""FastAPI backend exposing RAG endpoints and mounting the Gradio UI."""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import json
import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
import gradio as gr
from pydantic import BaseModel, Field
import uvicorn

from cloud_smash.api.schemas import (
    ChatRequest,
    ChatResponse,
    ChunksResponse,
    GraphMapRequest,
    GraphMapResponse,
    HealthResponse,
    InputChunkInfo,
    PresentChunkInfo,
    SourceCitation,
)
from cloud_smash.clients.ollama import OllamaClient
from cloud_smash.clients.pinecone_store import PineconeStore
from cloud_smash.config import Settings, get_settings
from cloud_smash.ingestion.pipeline import IngestionPipeline
from cloud_smash.ingestion.scraper import DocSource
from cloud_smash.rag.service import RAGService
from cloud_smash.ui.gradio_app import create_gradio_app, get_gradio_theme
from cloud_smash.ui.index_html import INDEX_HTML

logger = logging.getLogger(__name__)


class IngestPayload(BaseModel):
    """Payload for live documentation ingestion via API or UI."""

    url: str = Field(..., min_length=5)
    provider: str = Field(default="gcp")
    title: str = Field(default="")
    topic: str = Field(default="")


def _sse_event(event: str, data: object) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def _format_upstream_error(exc: Exception, base_url: str) -> str:
    err_str = str(exc)
    exc_name = type(exc).__name__
    if "11434" in err_str or "ConnectError" in exc_name or "connect" in err_str.lower():
        return (
            f"Cannot connect to Ollama at {base_url}. Please ensure 'ollama serve' is running in a terminal."
        )
    if "pinecone" in err_str.lower() or "401" in err_str or "unauthenticated" in err_str.lower():
        return f"Pinecone vector database error: {exc}. Verify your PINECONE_API_KEY in .env."
    return f"Upstream RAG error: {exc}"


def create_app(
    settings: Settings | None = None,
    *,
    ollama: OllamaClient | None = None,
    pinecone_store: PineconeStore | None = None,
    rag_service: RAGService | None = None,
    mount_ui: bool = True,
) -> FastAPI:
    """Create and configure the FastAPI + Gradio Cloud Smash application."""
    cfg = settings or get_settings()
    ollama_client = ollama or OllamaClient(cfg)
    owns_ollama = ollama is None
    store = pinecone_store or PineconeStore(cfg)
    rag = rag_service or RAGService(cfg, ollama=ollama_client, pinecone_store=store)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            if owns_ollama:
                await ollama_client.aclose()

    app = FastAPI(
        title="Cloud Smash API",
        version="0.1.0",
        description="Zero-billing hybrid RAG assistant for GCP and Azure documentation.",
        lifespan=lifespan,
    )

    @app.get("/api/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        ollama_status: dict[str, object]
        pinecone_status: dict[str, object]

        try:
            ollama_status = await ollama_client.health_check()
        except Exception as exc:
            ollama_status = {"status": "error", "detail": str(exc)}

        try:
            pinecone_status = await asyncio.to_thread(store.health_check)
        except Exception as exc:
            pinecone_status = {"status": "error", "detail": str(exc)}

        overall = (
            "ok"
            if ollama_status.get("status") == "ok" and pinecone_status.get("status") == "ok"
            else "degraded"
        )
        return HealthResponse(status=overall, ollama=ollama_status, pinecone=pinecone_status)

    @app.post("/api/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest) -> ChatResponse:
        history = [turn.model_dump() for turn in request.history]
        try:
            result = await rag.answer(
                request.query,
                top_k=request.top_k,
                provider=request.provider,
                history=history,
            )
        except Exception as exc:
            logger.exception("Chat request failed: %s", exc)
            detail = _format_upstream_error(exc, cfg.ollama_base_url)
            raise HTTPException(status_code=502, detail=detail) from exc

        return ChatResponse(
            answer=result.answer,
            sources=[SourceCitation.from_chunk(chunk) for chunk in result.sources],
        )

    @app.post("/api/chat/stream")
    async def chat_stream(request: ChatRequest) -> StreamingResponse:
        history = [turn.model_dump() for turn in request.history]
        try:
            chunks, token_stream = await rag.prepare_stream(
                request.query,
                top_k=request.top_k,
                provider=request.provider,
                history=history,
            )
        except Exception as exc:
            logger.exception("Streaming RAG setup failed: %s", exc)
            detail = _format_upstream_error(exc, cfg.ollama_base_url)
            raise HTTPException(status_code=502, detail=detail) from exc

        citations = [SourceCitation.from_chunk(chunk).model_dump() for chunk in chunks]

        async def event_generator() -> AsyncIterator[str]:
            yield _sse_event("sources", citations)
            try:
                async for token in token_stream:
                    yield _sse_event("token", {"token": token})
                yield _sse_event("done", {})
            except Exception as exc:
                logger.exception("Error during SSE token stream: %s", exc)
                yield _sse_event("error", {"detail": str(exc)})

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    @app.post("/api/ingest")
    async def ingest_doc(payload: IngestPayload) -> dict[str, object]:
        try:
            pipeline = IngestionPipeline(
                cfg,
                ollama=ollama_client,
                pinecone_store=store,
            )
            source = DocSource(
                provider=payload.provider.lower(),
                url=payload.url,
                title=payload.title,
                topic=payload.topic,
            )
            summary = await pipeline.run([source])
            return {
                "status": "ok",
                "documents_scraped": summary.documents_scraped,
                "chunks_created": summary.chunks_created,
                "vectors_upserted": summary.vectors_upserted,
            }
        except Exception as exc:
            logger.exception("Live ingestion failed: %s", exc)
            raise HTTPException(status_code=500, detail=f"Ingestion error: {exc}") from exc

    @app.get("/api/chunks", response_model=ChunksResponse)
    async def get_present_chunks() -> ChunksResponse:
        chunks = await store.aget_all_chunks()
        present = [PresentChunkInfo.from_chunk(c) for c in chunks]
        prov_counts: dict[str, int] = {}
        top_counts: dict[str, int] = {}
        for c in chunks:
            prov_counts[c.provider] = prov_counts.get(c.provider, 0) + 1
            if c.topic:
                top_counts[c.topic] = top_counts.get(c.topic, 0) + 1
        return ChunksResponse(
            chunks=present,
            total_count=len(present),
            provider_counts=prov_counts,
            topic_counts=top_counts,
        )

    @app.get("/api/graph", response_model=GraphMapResponse)
    async def get_graph_default() -> GraphMapResponse:
        chunks = await store.aget_all_chunks()
        present = [PresentChunkInfo.from_chunk(c) for c in chunks]
        prov_counts: dict[str, int] = {}
        top_counts: dict[str, int] = {}
        for c in chunks:
            prov_counts[c.provider] = prov_counts.get(c.provider, 0) + 1
            if c.topic:
                top_counts[c.topic] = top_counts.get(c.topic, 0) + 1
        return GraphMapResponse(
            input_chunk=None,
            retrieved_chunks=[],
            present_chunks=present,
            total_present_count=len(present),
            provider_counts=prov_counts,
            topic_counts=top_counts,
        )

    @app.post("/api/graph", response_model=GraphMapResponse)
    async def compute_graph_map(request: GraphMapRequest) -> GraphMapResponse:
        query_text = (request.query or "").strip()
        all_chunks = await store.aget_all_chunks()
        prov_counts: dict[str, int] = {}
        top_counts: dict[str, int] = {}
        for c in all_chunks:
            prov_counts[c.provider] = prov_counts.get(c.provider, 0) + 1
            if c.topic:
                top_counts[c.topic] = top_counts.get(c.topic, 0) + 1

        if not query_text:
            present = [PresentChunkInfo.from_chunk(c) for c in all_chunks]
            return GraphMapResponse(
                input_chunk=None,
                retrieved_chunks=[],
                present_chunks=present,
                total_present_count=len(present),
                provider_counts=prov_counts,
                topic_counts=top_counts,
            )

        try:
            import tiktoken
            enc = tiktoken.get_encoding("cl100k_base")
            token_count = len(enc.encode(query_text))
        except Exception:
            token_count = max(1, len(query_text.split()))

        try:
            vector = await ollama_client.embed_query(query_text)
            top_k = request.top_k or cfg.rag_top_k
            retrieved = await store.aquery(vector, top_k=top_k, provider=request.provider)
        except Exception as exc:
            logger.exception("Graph vector retrieval failed: %s", exc)
            detail = _format_upstream_error(exc, cfg.ollama_base_url)
            raise HTTPException(status_code=502, detail=detail) from exc

        retrieved_citations = [SourceCitation.from_chunk(c) for c in retrieved]
        retrieved_map = {c.id: (c.score, idx + 1) for idx, c in enumerate(retrieved)}

        present = [
            PresentChunkInfo.from_chunk(
                c,
                is_retrieved=c.id in retrieved_map,
                score=retrieved_map[c.id][0] if c.id in retrieved_map else None,
                rank=retrieved_map[c.id][1] if c.id in retrieved_map else None,
            )
            for c in all_chunks
        ]

        input_chunk = InputChunkInfo(
            query=query_text,
            token_count=token_count,
            embed_model=cfg.ollama_embed_model,
            embed_dimension=cfg.pinecone_embed_dimension,
            status="vectorized",
        )

        return GraphMapResponse(
            input_chunk=input_chunk,
            retrieved_chunks=retrieved_citations,
            present_chunks=present,
            total_present_count=len(present),
            provider_counts=prov_counts,
            topic_counts=top_counts,
        )

    @app.get("/", response_class=HTMLResponse)
    async def index() -> HTMLResponse:
        return HTMLResponse(content=INDEX_HTML)

    if mount_ui:
        demo = create_gradio_app(rag, cfg, pinecone_store=store)
        app = gr.mount_gradio_app(app, demo, path="/gradio", theme=get_gradio_theme())

    return app


def main() -> None:
    """Launch the FastAPI + Gradio server via Uvicorn."""
    cfg = get_settings()
    logging.basicConfig(
        level=getattr(logging, cfg.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    app = create_app(cfg, mount_ui=True)
    uvicorn.run(app, host=cfg.app_host, port=cfg.app_port)


if __name__ == "__main__":
    main()
