---
title: Cloud Smash
emoji: ☁️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Cloud Smash — Cloud Infrastructure Documentation Assistant

A **zero-billing** Retrieval-Augmented Generation (RAG) assistant for querying and summarizing **GCP** and **Azure** infrastructure documentation.

## Architecture

| Component | Technology | Zero-Billing Strategy |
| --- | --- | --- |
| **Backend & UI** | FastAPI + Gradio | Single-process app on port `7860`, ready for **Hugging Face Spaces** free tier (16GB RAM, 2 vCPU). |
| **Vector DB** | Pinecone Serverless | **Pinecone Starter Tier** perpetual free index (`768` dims, `cosine` similarity). |
| **Embeddings** | `nomic-embed-text` | Served by local Ollama (`768`-dim vectors) for both ingestion and query embedding. |
| **LLM Inference** | `qwen2.5:7b` (Qwen 2.5 7B) | Executed on local GPU hardware via Ollama and exposed securely over **Cloudflare Tunnel**. |
| **Packaging** | `uv` / `pip-tools` | Reproducible dependencies via `pyproject.toml`, `requirements.in`, and `requirements.txt`. |

## Project Structure

```text
├── configs/sources.yaml          # Curated GCP & Azure public documentation seed URLs
├── deploy/                       # Local Ollama + Cloudflare Tunnel scripts & config
├── src/cloud_smash/
│   ├── api/                      # FastAPI routes (/api/health, /api/chat, /api/chat/stream)
│   ├── clients/                  # Async Ollama client & Pinecone store with exponential backoff
│   ├── ingestion/                # Async HTML/Markdown scraper, 500-token chunker, ingestion CLI
│   ├── rag/                      # Strict grounding system prompt & streaming RAG service
│   └── ui/                       # Gradio UI mounted at `/`
├── tests/                        # Unit & API tests (mocked HTTP/Pinecone, no external calls)
├── Dockerfile                    # Hugging Face Spaces container image (port 7860)
└── requirements.in / .txt        # pip-tools / uv dependency manifests
```

## Quick Start (Local Development)

### 1. Environment Setup

Using `uv`:

```bash
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

Or using standard `venv` + `pip`:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

To regenerate `requirements.txt` from `requirements.in`:

```bash
pip-compile requirements.in -o requirements.txt
# or: uv pip compile requirements.in -o requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Set `PINECONE_API_KEY` (from Pinecone Starter Tier) and `OLLAMA_BASE_URL` (e.g. `http://localhost:11434` locally, or your Cloudflare Tunnel HTTPS URL in Hugging Face Spaces).

### 3. Pull Local Ollama Models

```bash
ollama pull nomic-embed-text
ollama pull qwen2.5:7b
```

### 4. Ingest Cloud Documentation

Run a dry-run first (scrapes & chunks at 500 tokens / 50-token overlap without writing to Pinecone):

```bash
cloud-smash-ingest --dry-run
```

Run full ingestion (embeds locally with `nomic-embed-text` and batch-upserts into Pinecone):

```bash
cloud-smash-ingest
```

Ingest a single extra documentation URL:

```bash
cloud-smash-ingest --url https://cloud.google.com/vpc/docs/vpc --provider gcp --topic networking
```

### 5. Run the Server & UI

```bash
cloud-smash-server
```

- Gradio UI: `http://localhost:7860/`
- Health Check: `http://localhost:7860/api/health`
- Sync Chat API: `POST http://localhost:7860/api/chat`
- Streaming SSE Chat API: `POST http://localhost:7860/api/chat/stream`

## Phase 4: Cloudflare Tunnel & Hugging Face Spaces Deployment

1. **Start Local Node & Tunnel**
   - Linux/macOS: `./deploy/start_local_node.sh`
   - Windows PowerShell: `.\deploy\start_local_node.ps1`
   - For a persistent custom hostname, configure `~/.cloudflared/config.yml` based on `deploy/cloudflared-config.example.yml`.

2. **Deploy to Hugging Face Spaces**
   - Create a **Docker** Space on Hugging Face Spaces.
   - Push this repository (including `Dockerfile`, `requirements.txt`, `pyproject.toml`, `configs/`, and `src/`).
   - Add Space Secrets/Variables:
     - `PINECONE_API_KEY`
     - `PINECONE_INDEX_NAME`
     - `OLLAMA_BASE_URL` (your `https://...` Cloudflare Tunnel URL)
     - Optional Cloudflare Access headers: `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET`

## Running Tests

```bash
pytest
```
