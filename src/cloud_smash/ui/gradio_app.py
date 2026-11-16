"""Enterprise Gradio chat interface with high-tier SaaS design system and live telemetry."""

from collections.abc import AsyncIterator
import html
import logging
import math
from typing import Any

import gradio as gr
import plotly.graph_objects as go

from cloud_smash.clients.pinecone_store import RetrievedChunk
from cloud_smash.config import Settings
from cloud_smash.rag.service import RAGService

logger = logging.getLogger(__name__)

CUSTOM_CSS = """
/* ============================================================
   Cloud Smash Enterprise SaaS Design System
   ============================================================ */

:root {
  --cs-primary: #0284c7;
  --cs-primary-glow: rgba(2, 132, 199, 0.25);
  --cs-accent: #6366f1;
  --cs-emerald: #10b981;
  --cs-bg-card: rgba(30, 41, 59, 0.7);
  --cs-border: rgba(148, 163, 184, 0.15);
  --cs-text-muted: #94a3b8;
  --cs-text-light: #f8fafc;
}

/* Glassmorphism containers */
.cs-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%);
  border: 1px solid var(--cs-border);
  border-radius: 16px;
  backdrop-filter: blur(16px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.25);
  margin-bottom: 14px;
}

.cs-brand-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.cs-logo-svg {
  width: 44px;
  height: 44px;
  filter: drop-shadow(0 0 12px rgba(56, 189, 248, 0.5));
}

.cs-brand-title {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.1;
  margin: 0;
}

.cs-brand-subtitle {
  font-size: 12px;
  color: var(--cs-text-muted);
  font-weight: 500;
  margin-top: 2px;
}

.cs-status-strip {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.cs-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  font-size: 11px;
  font-weight: 600;
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(15, 23, 42, 0.6);
  color: #e2e8f0;
}

.pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.pulse-emerald {
  background-color: #10b981;
  box-shadow: 0 0 8px #10b981;
}

.pulse-indigo {
  background-color: #818cf8;
  box-shadow: 0 0 8px #818cf8;
}

@keyframes pulse-ring {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(1.2); }
}

/* Telemetry flex grid */
.cs-telemetry-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.cs-metric-card {
  padding: 14px 18px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.6) 100%);
  border: 1px solid var(--cs-border);
  border-radius: 14px;
  backdrop-filter: blur(12px);
  transition: transform 0.2s ease, border-color 0.2s ease;
}

.cs-metric-card:hover {
  transform: translateY(-2px);
  border-color: rgba(56, 189, 248, 0.4);
}

.cs-metric-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--cs-text-muted);
  font-weight: 600;
  margin-bottom: 4px;
}

.cs-metric-value {
  font-size: 18px;
  font-weight: 700;
  color: #f1f5f9;
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.cs-metric-detail {
  font-size: 11px;
  color: #38bdf8;
  font-weight: 500;
}

/* Prompt Pills Row */
.cs-pills-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--cs-text-muted);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Retrieved Sources Cards */
.cs-sources-container {
  max-height: 580px;
  overflow-y: auto;
  padding-right: 4px;
}

.cs-sources-container::-webkit-scrollbar {
  width: 5px;
}
.cs-sources-container::-webkit-scrollbar-track {
  background: transparent;
}
.cs-sources-container::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.2);
  border-radius: 4px;
}

.cs-source-card {
  margin-bottom: 12px;
  padding: 14px;
  border-radius: 12px;
  background: rgba(15, 23, 42, 0.75);
  border: 1px solid var(--cs-border);
  transition: all 0.2s ease;
}

.cs-source-card:hover {
  border-color: rgba(56, 189, 248, 0.4);
  box-shadow: 0 4px 14px -2px rgba(2, 132, 199, 0.15);
}

.cs-source-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.provider-badge-gcp {
  background: rgba(66, 133, 244, 0.15);
  color: #60a5fa;
  border: 1px solid rgba(66, 133, 244, 0.3);
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
}

.provider-badge-azure {
  background: rgba(0, 120, 212, 0.15);
  color: #38bdf8;
  border: 1px solid rgba(0, 120, 212, 0.3);
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
}

.cs-score-pill {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 9999px;
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.cs-source-title {
  font-size: 13px;
  font-weight: 600;
  color: #f1f5f9;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 6px;
}

.cs-source-title:hover {
  color: #38bdf8;
  text-decoration: underline;
}

.cs-source-snippet {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 11px;
  line-height: 1.45;
  color: #cbd5e1;
  background: rgba(2, 6, 23, 0.5);
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.cs-empty-sources {
  text-align: center;
  padding: 40px 20px;
  color: var(--cs-text-muted);
}

.cs-radar-icon {
  font-size: 32px;
  margin-bottom: 12px;
  display: inline-block;
  animation: float-icon 3s ease-in-out infinite;
}

@keyframes float-icon {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.cs-blueprint-box {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid var(--cs-border);
  border-radius: 12px;
  padding: 16px;
  font-size: 12px;
  line-height: 1.6;
  color: #cbd5e1;
}

.cs-flow-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin: 12px 0;
  font-weight: 600;
  font-size: 12px;
}

.cs-flow-node {
  padding: 6px 12px;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid var(--cs-border);
  border-radius: 8px;
  color: #e2e8f0;
}

.cs-flow-arrow {
  color: #38bdf8;
}
"""

EMPTY_SOURCES_HTML = """
<div class="cs-empty-sources">
  <div class="cs-radar-icon">📡</div>
  <div style="font-weight: 600; color: #f1f5f9; font-size: 14px; margin-bottom: 4px;">Semantic Vector Mesh Ready</div>
  <div style="font-size: 12px; margin-bottom: 14px;">Ask an infrastructure question to trigger live cosine search against Pinecone Starter.</div>
  <div style="display: flex; gap: 6px; justify-content: center; flex-wrap: wrap;">
    <span class="provider-badge-gcp">GCP VPC</span>
    <span class="provider-badge-gcp">GKE Autopilot</span>
    <span class="provider-badge-gcp">GCP IAM</span>
    <span class="provider-badge-azure">Azure RBAC</span>
    <span class="provider-badge-azure">Azure VNet</span>
    <span class="provider-badge-azure">Azure AKS</span>
  </div>
</div>
"""

HEADER_HTML = """
<div class="cs-header">
  <div class="cs-brand-row">
    <svg class="cs-logo-svg" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="cloudGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#38bdf8"/>
          <stop offset="50%" stop-color="#818cf8"/>
          <stop offset="100%" stop-color="#c084fc"/>
        </linearGradient>
      </defs>
      <path d="M38 34H12C7.58 34 4 30.42 4 26C4 21.84 7.18 18.42 11.26 18.04C12.38 11.22 18.3 6 25.5 6C31.54 6 36.72 9.8 38.64 15.2C42.26 15.84 45 19 45 22.8C45 26.96 41.86 30.34 38 34Z" fill="url(#cloudGrad)" opacity="0.9"/>
      <path d="M26 18L18 29H24L22 38L32 26H25L26 18Z" fill="#ffffff" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.3))"/>
    </svg>
    <div>
      <h1 class="cs-brand-title">CLOUD SMASH</h1>
      <div class="cs-brand-subtitle">Enterprise Cloud Infrastructure Documentation Assistant · Strict Grounding RAG</div>
    </div>
  </div>
  <div class="cs-status-strip">
    <span class="cs-badge"><span class="pulse-dot pulse-emerald"></span> Pinecone Serverless · 50 Chunks</span>
    <span class="cs-badge"><span class="pulse-dot pulse-indigo"></span> Ollama Node · Qwen 2.5 7B</span>
    <span class="cs-badge" style="border-color: rgba(56, 189, 248, 0.3); color: #38bdf8;">⚡ Zero-Billing Tier ($0.00/mo)</span>
  </div>
</div>

<div class="cs-telemetry-grid">
  <div class="cs-metric-card">
    <div class="cs-metric-label">Knowledge Base</div>
    <div class="cs-metric-value">6 Docs <span class="cs-metric-detail">GCP & Azure</span></div>
  </div>
  <div class="cs-metric-card">
    <div class="cs-metric-label">Embedding Dimensions</div>
    <div class="cs-metric-value">768-D <span class="cs-metric-detail">nomic-embed-text</span></div>
  </div>
  <div class="cs-metric-card">
    <div class="cs-metric-label">Vector Store</div>
    <div class="cs-metric-value">Pinecone <span class="cs-metric-detail">AWS us-east-1</span></div>
  </div>
  <div class="cs-metric-card">
    <div class="cs-metric-label">Inference Link</div>
    <div class="cs-metric-value">Cloudflare <span class="cs-metric-detail">Secure Tunnel</span></div>
  </div>
</div>
"""

BLUEPRINT_HTML = """
<div class="cs-blueprint-box">
  <div style="font-weight: 700; color: #f8fafc; font-size: 13px; margin-bottom: 6px;">
    📐 Hybrid Zero-Billing Architecture Blueprint
  </div>
  <div>
    This system enforces a strict <strong>zero-billing constraint</strong> using a decoupled 3-node topology:
  </div>
  <div class="cs-flow-row">
    <span class="cs-flow-node">🌐 User Client</span>
    <span class="cs-flow-arrow">➔</span>
    <span class="cs-flow-node">🤗 Hugging Face Spaces (FastAPI + Gradio)</span>
    <span class="cs-flow-arrow">➔</span>
    <span class="cs-flow-node">🌲 Pinecone Starter (Top-K Cosine)</span>
    <span class="cs-flow-arrow">➔</span>
    <span class="cs-flow-node">🚇 Cloudflare Tunnel</span>
    <span class="cs-flow-arrow">➔</span>
    <span class="cs-flow-node">🖥️ Local GPU Node (Qwen 2.5 7B via Ollama)</span>
  </div>
  <div style="font-size: 11px; color: #94a3b8;">
    <strong>Strict Grounding Contract:</strong> The LLM is locked to retrieved context blocks.
    Hallucinated parameters, fabricated IAM roles, or ungrounded syntax are prohibited;
    unsupported questions trigger explicit out-of-scope notifications.
  </div>
</div>
"""


def _format_sources_html(chunks: list[RetrievedChunk]) -> str:
    """Render retrieved Pinecone chunks as sleek software cards with match scores."""
    if not chunks:
        return EMPTY_SOURCES_HTML

    cards: list[str] = ['<div class="cs-sources-container">']
    for idx, chunk in enumerate(chunks, start=1):
        badge_cls = "provider-badge-gcp" if chunk.provider.lower() == "gcp" else "provider-badge-azure"
        score_pct = round(chunk.score * 100, 1)

        snippet = chunk.text.strip().replace("\r\n", "\n")
        if len(snippet) > 260:
            snippet = snippet[:257].rstrip() + "..."
        safe_snippet = html.escape(snippet)
        safe_title = html.escape(chunk.title or "Documentation Source")
        safe_url = html.escape(chunk.url or "#")

        cards.append(
            f'<div class="cs-source-card">'
            f'  <div class="cs-source-header">'
            f'    <span class="{badge_cls}">SOURCE {idx} · {chunk.provider.upper()}</span>'
            f'    <span class="cs-score-pill">CONFIDENCE {score_pct}%</span>'
            f'  </div>'
            f'  <div>'
            f'    <a class="cs-source-title" href="{safe_url}" target="_blank" rel="noopener noreferrer">'
            f'      {safe_title} <span style="font-size: 11px;">&#8599;</span>'
            f'    </a>'
            f'  </div>'
            f'  <div class="cs-source-snippet">{safe_snippet}</div>'
            f'</div>'
        )
    cards.append("</div>")
    return "\n".join(cards)


# All known documentation sources — used to show un-retrieved chunks in the graph.
_KNOWN_SOURCES: list[dict[str, str]] = [
    {"provider": "gcp",   "topic": "iam",        "title": "GCP IAM Roles"},
    {"provider": "gcp",   "topic": "networking",  "title": "GCP VPC"},
    {"provider": "gcp",   "topic": "kubernetes",  "title": "GKE Autopilot"},
    {"provider": "azure", "topic": "iam",         "title": "Azure RBAC"},
    {"provider": "azure", "topic": "networking",  "title": "Azure VNet"},
    {"provider": "azure", "topic": "kubernetes",  "title": "Azure AKS"},
]

# Colour palette
_PROVIDER_COLOUR = {"gcp": "#4285F4", "azure": "#0078D4"}
_TOPIC_COLOUR    = {"iam": "#c084fc", "networking": "#34d399", "kubernetes": "#fb923c"}


def _build_chunk_graph(
    query: str,
    retrieved_chunks: list[RetrievedChunk],
    present_chunks: list[RetrievedChunk] | None = None,
    view_mode: str = "Unified Flow",
) -> go.Figure:
    """
    Build an interactive graph map supporting unified or separate views:
      • Input Chunk      — user inquiry vector (gold star at origin)
      • Retrieved Chunks — matched chunks with similarity gauges & directional score edges
      • Present Chunks   — all knowledge base chunks in the vector database partitioned by cloud provider
    """
    mode = (view_mode or "Unified Flow").lower()
    show_input = "input" in mode or "unified" in mode or "flow" in mode
    show_retrieved = "retrieved" in mode or "unified" in mode or "flow" in mode
    show_present = "present" in mode or "unified" in mode or "flow" in mode

    all_present = list(present_chunks or [])
    if not all_present:
        all_present = [
            RetrievedChunk(
                id=f"known-{i}",
                score=0.0,
                text=s["title"],
                url="",
                title=s["title"],
                provider=s["provider"],
                topic=s["topic"],
                chunk_index=i,
            )
            for i, s in enumerate(_KNOWN_SOURCES)
        ]

    n_present = len(all_present)
    n_ret = len(retrieved_chunks)
    retrieved_ids = {c.id for c in retrieved_chunks}

    traces = []
    annotations: list[dict] = []

    # ── 1. Present Chunks (Knowledge Base Space) ──────────────────────────────
    if show_present:
        pres_x, pres_y, pres_text, pres_hover, pres_colours, pres_symbols, pres_sizes = (
            [], [], [], [], [], [], []
        )
        gcp_chunks = [c for c in all_present if c.provider.lower() == "gcp"]
        azure_chunks = [c for c in all_present if c.provider.lower() != "gcp"]

        def _place_arc(items: list[RetrievedChunk], start_angle: float, end_angle: float, base_radius: float):
            count = len(items)
            res = []
            for idx, item in enumerate(items):
                fraction = idx / max(count - 1, 1) if count > 1 else 0.5
                angle = start_angle + fraction * (end_angle - start_angle)
                r = base_radius + ((idx % 3) - 1) * 0.35
                res.append((r * math.cos(angle), r * math.sin(angle)))
            return res

        gcp_positions = _place_arc(gcp_chunks, start_angle=0.62 * math.pi, end_angle=1.38 * math.pi, base_radius=3.8)
        azure_positions = _place_arc(azure_chunks, start_angle=-0.38 * math.pi, end_angle=0.38 * math.pi, base_radius=3.8)

        all_items = list(zip(gcp_chunks, gcp_positions)) + list(zip(azure_chunks, azure_positions))

        for chunk, (px, py) in all_items:
            is_ret = chunk.id in retrieved_ids
            pres_x.append(px)
            pres_y.append(py)
            pres_text.append(f"#{chunk.chunk_index}")
            status_desc = "🔥 RETRIEVED FOR CURRENT QUERY" if is_ret else "📦 STORED IN PINECONE INDEX"
            pres_hover.append(
                f"<b>{chunk.title}</b><br>"
                f"Status: <b>{status_desc}</b><br>"
                f"Provider: <b>{chunk.provider.upper()}</b> &nbsp;|&nbsp; Topic: <b>{chunk.topic or 'core'}</b><br>"
                f"Chunk Index: #{chunk.chunk_index} &nbsp;|&nbsp; ID: {chunk.id[:16]}…<br>"
                f"<br><i>{html.escape(chunk.text[:160].strip())}…</i>"
            )
            base_col = _PROVIDER_COLOUR.get(chunk.provider.lower(), "#38bdf8")
            pres_colours.append(base_col if is_ret else (base_col + "66"))
            pres_symbols.append("circle" if chunk.provider.lower() == "gcp" else "diamond")
            pres_sizes.append(22 if is_ret else 14)

        traces.append(
            go.Scatter(
                x=pres_x,
                y=pres_y,
                mode="markers+text",
                name="Present Chunks (Corpus)",
                marker=dict(
                    size=pres_sizes,
                    color=pres_colours,
                    symbol=pres_symbols,
                    line=dict(width=1.5, color="rgba(255,255,255,0.7)"),
                ),
                text=pres_text,
                textposition="top center",
                textfont=dict(size=8, color="rgba(226,232,240,0.7)"),
                hovertemplate="%{customdata}<extra></extra>",
                customdata=pres_hover,
            )
        )

    # ── 2. Retrieval Edges & Scores ──────────────────────────────────────────
    inner_positions = []
    if n_ret > 0:
        for i in range(n_ret):
            angle = math.pi / 2 + 2 * math.pi * i / n_ret
            inner_positions.append((1.8 * math.cos(angle), 1.8 * math.sin(angle)))

    if show_retrieved and n_ret > 0:
        edge_x: list[float | None] = []
        edge_y: list[float | None] = []
        for i, chunk in enumerate(retrieved_chunks):
            px, py = inner_positions[i]
            edge_x += [0.0, px, None]
            edge_y += [0.0, py, None]
            mx, my = px * 0.52, py * 0.52
            score_pct = round(chunk.score * 100, 1)
            annotations.append(
                dict(
                    x=mx,
                    y=my,
                    text=f"<b>{score_pct}%</b>",
                    showarrow=False,
                    font=dict(size=9, color="#10b981"),
                    bgcolor="rgba(15,23,42,0.85)",
                    bordercolor="rgba(16,185,129,0.5)",
                    borderwidth=1,
                    borderpad=2,
                )
            )

        traces.append(
            go.Scatter(
                x=edge_x,
                y=edge_y,
                mode="lines",
                name="Cosine Vector Edges",
                line=dict(width=2, color="rgba(16,185,129,0.7)", dash="dot"),
                hoverinfo="skip",
            )
        )

    # ── 3. Retrieved Chunks Trace ─────────────────────────────────────────────
    if show_retrieved and n_ret > 0:
        ret_x, ret_y, ret_text, ret_hover, ret_colours, ret_sizes = [], [], [], [], [], []
        for i, chunk in enumerate(retrieved_chunks):
            px, py = inner_positions[i]
            score_pct = round(chunk.score * 100, 1)
            base_col = _PROVIDER_COLOUR.get(chunk.provider.lower(), "#38bdf8")
            size = 28 + int(chunk.score * 25)
            short_title = chunk.title[:20] + ("…" if len(chunk.title) > 20 else "")

            ret_x.append(px)
            ret_y.append(py)
            ret_text.append(f"<b>Rank #{i+1}</b><br>{short_title}")
            ret_hover.append(
                f"<b>[RETRIEVED CHUNK #{i+1}]</b><br>"
                f"<b>{chunk.title}</b><br>"
                f"Provider: <b>{chunk.provider.upper()}</b> &nbsp;|&nbsp; Topic: <b>{chunk.topic}</b><br>"
                f"Chunk Index: #{chunk.chunk_index} &nbsp;|&nbsp; Similarity: <b>{score_pct}%</b><br>"
                f"ID: <code>{chunk.id}</code><br>"
                f"<br><i>{html.escape(chunk.text[:220].strip())}…</i>"
            )
            ret_colours.append(base_col)
            ret_sizes.append(size)

        traces.append(
            go.Scatter(
                x=ret_x,
                y=ret_y,
                mode="markers+text",
                name="Retrieved Chunks (Top-K)",
                marker=dict(
                    size=ret_sizes,
                    color=ret_colours,
                    line=dict(width=2.5, color="#ffffff"),
                    symbol="circle",
                ),
                text=ret_text,
                textposition="bottom center",
                textfont=dict(size=10, color="#ffffff"),
                hovertemplate="%{customdata}<extra></extra>",
                customdata=ret_hover,
            )
        )

    # ── 4. Input Query Chunk Node ─────────────────────────────────────────────
    clean_q = (query or "").strip()
    if clean_q and clean_q != "(no query yet)":
        short_q = (clean_q[:32] + "…") if len(clean_q) > 34 else clean_q
    else:
        short_q = "(awaiting query)"

    if show_input:
        traces.append(
            go.Scatter(
                x=[0],
                y=[0],
                mode="markers+text",
                name="Input Chunk (Query)",
                marker=dict(
                    size=54,
                    color="#fbbf24",
                    symbol="star",
                    line=dict(width=3, color="#f59e0b"),
                ),
                text=[f"<b>🔍 INPUT CHUNK</b><br>{short_q}"],
                textposition="top center",
                textfont=dict(size=11, color="#fef08a"),
                hovertemplate=(
                    f"<b>[INPUT CHUNK // QUERY VECTOR]</b><br>"
                    f"Query: <i>{html.escape(clean_q or 'No query active')}</i><br>"
                    f"Embedding Model: <b>nomic-embed-text (768-D)</b><br>"
                    f"Vector Norm: L2-normalized<br>"
                    f"Status: <b>VECTORIZED & SCANNING</b><extra></extra>"
                ),
            )
        )

    # ── Configure Range by Mode ───────────────────────────────────────────────
    if "input" in mode:
        axis_range = [-2.2, 2.2]
        title_suffix = "Input Chunk Stage (Isolated)"
    elif "retrieved" in mode:
        axis_range = [-3.2, 3.2]
        title_suffix = f"Retrieved Chunks Stage ({n_ret} matched chunks)"
    elif "present" in mode:
        axis_range = [-5.2, 5.2]
        title_suffix = f"Present Knowledge Base ({n_present} total chunks in Pinecone)"
    else:
        axis_range = [-5.2, 5.2]
        title_suffix = f"Unified Process Flow ({n_ret} retrieved / {n_present} present in Pinecone)"

    fig = go.Figure(data=traces)
    fig.update_layout(
        title=dict(
            text=f"Process Graph Map — {title_suffix}",
            font=dict(size=14, color="#f8fafc"),
            x=0.01,
        ),
        paper_bgcolor="rgba(10,15,30,0.95)",
        plot_bgcolor="rgba(10,15,30,0.0)",
        font=dict(color="#e2e8f0"),
        showlegend=True,
        legend=dict(
            bgcolor="rgba(15,23,42,0.8)",
            bordercolor="rgba(148,163,184,0.2)",
            borderwidth=1,
            font=dict(size=11),
            x=1.01,
            y=1.0,
        ),
        xaxis=dict(visible=False, range=axis_range),
        yaxis=dict(visible=False, range=axis_range, scaleanchor="x"),
        margin=dict(l=20, r=180, t=55, b=20),
        annotations=annotations,
        height=540,
    )

    if show_present:
        theta = [2 * math.pi * i / 80 for i in range(81)]
        fig.add_trace(
            go.Scatter(
                x=[3.8 * math.cos(t) for t in theta],
                y=[3.8 * math.sin(t) for t in theta],
                mode="lines",
                line=dict(color="rgba(148,163,184,0.12)", width=1, dash="dot"),
                hoverinfo="skip",
                showlegend=False,
            )
        )
    if show_retrieved and n_ret > 0:
        theta = [2 * math.pi * i / 60 for i in range(61)]
        fig.add_trace(
            go.Scatter(
                x=[1.8 * math.cos(t) for t in theta],
                y=[1.8 * math.sin(t) for t in theta],
                mode="lines",
                line=dict(color="rgba(16,185,129,0.18)", width=1, dash="dot"),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    return fig


def _empty_chunk_graph(
    present_chunks: list[RetrievedChunk] | None = None,
    view_mode: str = "Unified Flow",
) -> go.Figure:
    """Placeholder graph shown before the first query."""
    return _build_chunk_graph("(no query yet)", [], present_chunks=present_chunks, view_mode=view_mode)


def _format_chunk_breakdown_html(
    query: str,
    retrieved_chunks: list[RetrievedChunk],
    present_chunks: list[RetrievedChunk] | None = None,
) -> str:
    clean_q = (query or "").strip()
    all_pres = present_chunks or []
    n_pres = len(all_pres)
    gcp_pres = sum(1 for c in all_pres if c.provider.lower() == "gcp")
    azure_pres = n_pres - gcp_pres
    n_ret = len(retrieved_chunks)

    if not retrieved_chunks:
        ret_cards_html = "<div style='color:#94a3b8; font-size:12px; font-style:italic;'>Awaiting query execution to retrieve vector matches.</div>"
    else:
        items = []
        for i, c in enumerate(retrieved_chunks):
            pct = round(c.score * 100, 1)
            prov_col = "#4285F4" if c.provider.lower() == "gcp" else "#0078D4"
            items.append(
                f"<div style='background:rgba(15,23,42,0.8); border:1px solid rgba(148,163,184,0.15); border-left:3px solid {prov_col}; padding:10px; border-radius:6px; margin-bottom:8px;'>"
                f"  <div style='display:flex; justify-content:space-between; align-items:center; font-size:11px; margin-bottom:4px;'>"
                f"    <span style='font-weight:700; color:{prov_col};'>[RANK #{i+1}] {c.provider.upper()} &middot; #{c.chunk_index}</span>"
                f"    <span style='background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.4); padding:1px 6px; border-radius:3px; font-weight:700;'>{pct}% SIMILARITY</span>"
                f"  </div>"
                f"  <div style='font-size:12px; font-weight:600; color:#ffffff; margin-bottom:4px;'>{html.escape(c.title)}</div>"
                f"  <div style='font-size:11px; color:#cbd5e1; line-height:1.4;'>{html.escape(c.text[:180].strip())}…</div>"
                f"</div>"
            )
        ret_cards_html = "".join(items)

    input_text = html.escape(clean_q) if clean_q and clean_q != "(no query yet)" else "Awaiting query directive..."
    token_est = max(1, len(clean_q.split())) if clean_q and clean_q != "(no query yet)" else 0

    return f"""
    <div style='display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px; margin-top:16px; font-family:ui-sans-serif, system-ui, sans-serif;'>
      
      <!-- Box 1: Input Chunk (Separate) -->
      <div style='background:rgba(30,41,59,0.6); border:1px solid rgba(251,191,36,0.3); border-radius:10px; padding:16px;'>
        <div style='display:flex; align-items:center; gap:8px; margin-bottom:12px;'>
          <span style='width:10px; height:10px; border-radius:50%; background:#fbbf24; display:inline-block;'></span>
          <span style='font-size:12px; font-weight:700; color:#fbbf24; text-transform:uppercase; letter-spacing:0.05em;'>[01] Input Chunk (Query)</span>
        </div>
        <div style='background:rgba(15,23,42,0.9); border:1px solid rgba(255,255,255,0.08); padding:12px; border-radius:6px; margin-bottom:10px; font-size:12px; color:#f8fafc; font-style:italic;'>
          "{input_text}"
        </div>
        <div style='font-size:11px; color:#94a3b8; line-height:1.7;'>
          <div>&bull; Token Estimation: <b style='color:#f8fafc;'>{token_est} tokens</b></div>
          <div>&bull; Embedding Vectorizer: <b style='color:#38bdf8;'>nomic-embed-text (768-D)</b></div>
          <div>&bull; Metric: <b style='color:#10b981;'>Cosine Similarity Matrix</b></div>
          <div>&bull; Target Hardware: <b style='color:#c084fc;'>Local GPU Node (Ollama)</b></div>
        </div>
      </div>

      <!-- Box 2: Retrieved Chunks (Separate) -->
      <div style='background:rgba(30,41,59,0.6); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:16px;'>
        <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;'>
          <div style='display:flex; align-items:center; gap:8px;'>
            <span style='width:10px; height:10px; border-radius:50%; background:#10b981; display:inline-block;'></span>
            <span style='font-size:12px; font-weight:700; color:#10b981; text-transform:uppercase; letter-spacing:0.05em;'>[02] Retrieved Chunks ({n_ret})</span>
          </div>
          <span style='font-size:11px; color:#94a3b8;'>Cosine Filtered</span>
        </div>
        <div style='max-height:260px; overflow-y:auto; padding-right:4px;'>
          {ret_cards_html}
        </div>
      </div>

      <!-- Box 3: Present Chunks Knowledge Base (Separate) -->
      <div style='background:rgba(30,41,59,0.6); border:1px solid rgba(56,189,248,0.3); border-radius:10px; padding:16px;'>
        <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;'>
          <div style='display:flex; align-items:center; gap:8px;'>
            <span style='width:10px; height:10px; border-radius:50%; background:#38bdf8; display:inline-block;'></span>
            <span style='font-size:12px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;'>[03] Present Chunks ({n_pres})</span>
          </div>
          <span style='font-size:11px; color:#38bdf8; font-weight:700;'>PINECONE INDEX</span>
        </div>
        <div style='font-size:11px; color:#94a3b8; line-height:1.7; margin-bottom:12px;'>
          <div>&bull; Total Indexed Vectors: <b style='color:#f8fafc;'>{n_pres} chunks</b></div>
          <div>&bull; GCP Corpus: <b style='color:#4285F4;'>{gcp_pres} chunks</b> (IAM, VPC, GKE)</div>
          <div>&bull; Azure Corpus: <b style='color:#0078D4;'>{azure_pres} chunks</b> (RBAC, VNet, AKS)</div>
          <div>&bull; Index Tier: <b style='color:#f8fafc;'>Starter Serverless (AWS us-east-1)</b></div>
        </div>
        <div style='background:rgba(15,23,42,0.9); border:1px solid rgba(255,255,255,0.06); padding:8px 10px; border-radius:6px; font-size:10px; color:#94a3b8;'>
          <i>All chunks are persisted in Pinecone and ready for real-time cosine distance scanning.</i>
        </div>
      </div>

    </div>
    """


def _normalize_history(history: list[dict[str, Any]] | None) -> list[dict[str, str]]:
    """Convert Gradio Chatbot message entries into plain role/content dicts."""
    normalized: list[dict[str, str]] = []
    for entry in history or []:
        role = entry.get("role")
        content = entry.get("content", "")
        if isinstance(content, list):
            content = "".join(
                part.get("text", "") for part in content if isinstance(part, dict)
            )
        if role in {"user", "assistant"} and isinstance(content, str) and content.strip():
            normalized.append({"role": role, "content": content})
    return normalized


def get_gradio_theme() -> gr.themes.ThemeClass:
    """Return the custom Enterprise theme for Cloud Smash."""
    return gr.themes.Soft(
        primary_hue="sky",
        secondary_hue="indigo",
        neutral_hue="slate",
        font=["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
    )


def create_gradio_app(
    rag_service: RAGService,
    settings: Settings,
    pinecone_store: Any | None = None,
) -> gr.Blocks:
    """Build the Gradio Blocks UI with enterprise SaaS styling and separate chunk graph mapping."""
    store = pinecone_store or getattr(rag_service, "_store", None)
    try:
        initial_present_chunks = (
            store.get_all_chunks() if store and hasattr(store, "get_all_chunks") else []
        )
    except Exception:
        initial_present_chunks = []

    with gr.Blocks(title="Cloud Smash — Enterprise Infrastructure Assistant") as demo:
        # Inject custom design system CSS
        gr.HTML(f"<style>{CUSTOM_CSS}</style>")

        # Top Navigation Header & Telemetry Strip
        gr.HTML(HEADER_HTML)

        last_state = gr.State({
            "query": "",
            "retrieved": [],
            "present": initial_present_chunks,
            "mode": "Unified Flow",
        })

        with gr.Tabs():
            # ── Tab 1: Chat ────────────────────────────────────────────────────
            with gr.TabItem("💬 Chat"):
                with gr.Row():
                    # Left Sidebar: Controls & Live Source Inspector
                    with gr.Column(scale=1, min_width=320):
                        with gr.Group():
                            gr.Markdown("### ⚙️ Search Precision & Scope")
                            provider_filter = gr.Radio(
                                choices=["all", "gcp", "azure"],
                                value="all",
                                label="Cloud Provider Filter",
                                info="Constrain Pinecone vector search to specific cloud docs.",
                            )
                            top_k_slider = gr.Slider(
                                minimum=1,
                                maximum=8,
                                value=settings.rag_top_k,
                                step=1,
                                label="Top-K Retrieved Chunks",
                                info="Number of vector context blocks passed to LLM.",
                            )

                        gr.Markdown("### 🎯 Live Grounding Citations")
                        sources_panel = gr.HTML(value=EMPTY_SOURCES_HTML)

                    # Right Main Column: Chatbot & Action Bar
                    with gr.Column(scale=3):
                        chatbot = gr.Chatbot(
                            height=520,
                            label="Grounded Cloud Infrastructure Chatbot",
                            buttons=["copy", "copy_all"],
                            layout="bubble",
                        )

                        # Quick Flex Prompt Pills
                        gr.Markdown("##### ⚡ Instant Technical Prompts")
                        with gr.Row():
                            pill_1 = gr.Button("☸️ GKE Autopilot Nodes", size="sm", variant="secondary")
                            pill_2 = gr.Button("🔐 Azure RBAC Scopes", size="sm", variant="secondary")
                            pill_3 = gr.Button("🌐 GCP VPC Subnets", size="sm", variant="secondary")
                            pill_4 = gr.Button("☁️ Azure AKS Architecture", size="sm", variant="secondary")

                        with gr.Row():
                            query_box = gr.Textbox(
                                placeholder="Ask about GCP IAM, VPC, GKE Autopilot, Azure RBAC, VNet, or AKS...",
                                label="Infrastructure Documentation Query",
                                lines=2,
                                scale=5,
                                autofocus=True,
                            )
                            submit_btn = gr.Button("Ask Assistant ➔", variant="primary", scale=1)

                        with gr.Row():
                            clear_btn = gr.Button("Clear Conversation", variant="secondary", size="sm")

                        # Architecture & Seed Corpus Accordion
                        with gr.Accordion("🏛️ View Grounding Corpus & Architecture Blueprint", open=False):
                            gr.HTML(BLUEPRINT_HTML)
                            gr.Markdown(
                                "**Currently Ingested Seed Documentation (Pinecone Index: `cloud-infra-docs`):**\n"
                                "- 🌐 **GCP VPC:** [`cloud.google.com/vpc/docs/vpc`](https://cloud.google.com/vpc/docs/vpc)\n"
                                "- ☸️ **GCP GKE Autopilot:** [`cloud.google.com/.../autopilot-overview`](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview)\n"
                                "- 🛡️ **GCP IAM Roles:** [`cloud.google.com/iam/docs/roles-overview`](https://cloud.google.com/iam/docs/roles-overview)\n"
                                "- 🔐 **Azure RBAC:** [`MicrosoftDocs/azure-docs/.../overview.md`](https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/articles/role-based-access-control/overview.md)\n"
                                "- 🌐 **Azure VNet:** [`MicrosoftDocs/azure-docs/.../virtual-networks-overview.md`](https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/articles/virtual-network/virtual-networks-overview.md)\n"
                                "- ☸️ **Azure AKS:** [`learn.microsoft.com/en-us/azure/aks/what-is-aks`](https://learn.microsoft.com/en-us/azure/aks/what-is-aks)"
                            )

            # ── Tab 2: Chunk Map ───────────────────────────────────────────────
            with gr.TabItem("🗺️ Chunk Map"):
                gr.Markdown(
                    "### 🗺️ Process Graph Map (Vector Retrieval Lifecycle)\n"
                    "Visualize the full RAG process: see the **Input Chunk**, "
                    "**Retrieved Chunks**, and **All Present Knowledge Base Chunks** in unified or separate views."
                )
                with gr.Row():
                    map_view_mode = gr.Radio(
                        choices=["Unified Flow", "Input Chunk (Separate)", "Retrieved Chunks (Separate)", "Present Chunks (Separate)"],
                        value="Unified Flow",
                        label="Graph Visual Separation Mode",
                        info="Switch between the complete flow or inspect Input Chunk, Retrieved Chunks, and Present Chunks in isolation.",
                    )
                chunk_map_plot = gr.Plot(
                    value=_empty_chunk_graph(present_chunks=initial_present_chunks, view_mode="Unified Flow"),
                    label="Chunk Retrieval Map",
                )
                chunk_details_panel = gr.HTML(
                    value=_format_chunk_breakdown_html("(no query yet)", [], present_chunks=initial_present_chunks)
                )

        # Quick prompt event bindings
        pill_1.click(
            fn=lambda: "What is GKE Autopilot mode and how does it manage nodes?",
            inputs=None,
            outputs=query_box,
        )
        pill_2.click(
            fn=lambda: "What is Azure role-based access control (Azure RBAC) and what are its key components?",
            inputs=None,
            outputs=query_box,
        )
        pill_3.click(
            fn=lambda: "How do subnets, CIDR ranges, and routing work in Google Cloud VPC networks?",
            inputs=None,
            outputs=query_box,
        )
        pill_4.click(
            fn=lambda: "What are the core components and features of Azure Kubernetes Service (AKS)?",
            inputs=None,
            outputs=query_box,
        )

        def change_map_view(mode: str, state_data: dict) -> tuple[go.Figure, str, dict]:
            st = dict(state_data or {})
            st["mode"] = mode
            q = st.get("query", "")
            rets = st.get("retrieved", [])
            pres = st.get("present", initial_present_chunks)
            fig = _build_chunk_graph(q, rets, present_chunks=pres, view_mode=mode)
            html_details = _format_chunk_breakdown_html(q, rets, present_chunks=pres)
            return fig, html_details, st

        map_view_mode.change(
            fn=change_map_view,
            inputs=[map_view_mode, last_state],
            outputs=[chunk_map_plot, chunk_details_panel, last_state],
        )

        async def respond(
            message: str,
            history: list[dict[str, Any]] | None,
            provider: str,
            top_k: int,
            state_data: dict,
        ) -> AsyncIterator[tuple[list[dict[str, Any]], str, str, go.Figure, str, dict]]:
            cleaned = (message or "").strip()
            current_history = list(history or [])
            st = dict(state_data or {})
            current_mode = st.get("mode", "Unified Flow")
            pres = (
                store.get_all_chunks()
                if store and hasattr(store, "get_all_chunks")
                else initial_present_chunks
            )

            if not cleaned:
                empty_fig = _empty_chunk_graph(present_chunks=pres, view_mode=current_mode)
                empty_details = _format_chunk_breakdown_html("", [], present_chunks=pres)
                st.update({"query": "", "retrieved": [], "present": pres})
                yield current_history, EMPTY_SOURCES_HTML, "", empty_fig, empty_details, st
                return

            prior_turns = _normalize_history(current_history)
            updated_history = current_history + [
                {"role": "user", "content": cleaned},
                {"role": "assistant", "content": ""},
            ]

            try:
                chunks, token_stream = await rag_service.prepare_stream(
                    cleaned,
                    top_k=int(top_k),
                    provider=provider,
                    history=prior_turns,
                )
                sources_html = _format_sources_html(chunks)
                chunk_fig = _build_chunk_graph(cleaned, chunks, present_chunks=pres, view_mode=current_mode)
                details_html = _format_chunk_breakdown_html(cleaned, chunks, present_chunks=pres)
                st.update({"query": cleaned, "retrieved": chunks, "present": pres})
                yield updated_history, sources_html, "", chunk_fig, details_html, st

                accumulated = ""
                async for token in token_stream:
                    accumulated += token
                    updated_history[-1] = {"role": "assistant", "content": accumulated}
                    yield updated_history, sources_html, "", chunk_fig, details_html, st
            except Exception as exc:
                logger.exception("Gradio RAG streaming failed: %s", exc)
                updated_history[-1] = {
                    "role": "assistant",
                    "content": f"⚠️ Error querying backend/tunnel: {exc}",
                }
                empty_fig = _empty_chunk_graph(present_chunks=pres, view_mode=current_mode)
                empty_details = _format_chunk_breakdown_html("", [], present_chunks=pres)
                yield updated_history, EMPTY_SOURCES_HTML, "", empty_fig, empty_details, st

        def clear_chat(state_data: dict) -> tuple[list[dict[str, Any]], str, str, go.Figure, str, dict]:
            pres = (
                store.get_all_chunks()
                if store and hasattr(store, "get_all_chunks")
                else initial_present_chunks
            )
            empty_fig = _empty_chunk_graph(present_chunks=pres, view_mode="Unified Flow")
            empty_details = _format_chunk_breakdown_html("", [], present_chunks=pres)
            st = {"query": "", "retrieved": [], "present": pres, "mode": "Unified Flow"}
            return [], EMPTY_SOURCES_HTML, "", empty_fig, empty_details, st

        submit_btn.click(
            fn=respond,
            inputs=[query_box, chatbot, provider_filter, top_k_slider, last_state],
            outputs=[chatbot, sources_panel, query_box, chunk_map_plot, chunk_details_panel, last_state],
        )
        query_box.submit(
            fn=respond,
            inputs=[query_box, chatbot, provider_filter, top_k_slider, last_state],
            outputs=[chatbot, sources_panel, query_box, chunk_map_plot, chunk_details_panel, last_state],
        )
        clear_btn.click(
            fn=clear_chat,
            inputs=[last_state],
            outputs=[chatbot, sources_panel, query_box, chunk_map_plot, chunk_details_panel, last_state],
        )

    return demo

    return demo
