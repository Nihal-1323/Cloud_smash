"""Enterprise Gradio chat interface with high-tier SaaS design system and live telemetry."""

from collections.abc import AsyncIterator
import html
import logging
from typing import Any

import gradio as gr

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


def create_gradio_app(rag_service: RAGService, settings: Settings) -> gr.Blocks:
    """Build the Gradio Blocks UI with enterprise SaaS styling."""
    with gr.Blocks(title="Cloud Smash — Enterprise Infrastructure Assistant") as demo:
        # Inject custom design system CSS
        gr.HTML(f"<style>{CUSTOM_CSS}</style>")

        # Top Navigation Header & Telemetry Strip
        gr.HTML(HEADER_HTML)

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

        async def respond(
            message: str,
            history: list[dict[str, Any]] | None,
            provider: str,
            top_k: int,
        ) -> AsyncIterator[tuple[list[dict[str, Any]], str, str]]:
            cleaned = (message or "").strip()
            current_history = list(history or [])
            if not cleaned:
                yield current_history, EMPTY_SOURCES_HTML, ""
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
                yield updated_history, sources_html, ""

                accumulated = ""
                async for token in token_stream:
                    accumulated += token
                    updated_history[-1] = {"role": "assistant", "content": accumulated}
                    yield updated_history, sources_html, ""
            except Exception as exc:
                logger.exception("Gradio RAG streaming failed: %s", exc)
                updated_history[-1] = {
                    "role": "assistant",
                    "content": f"⚠️ Error querying backend/tunnel: {exc}",
                }
                yield updated_history, EMPTY_SOURCES_HTML, ""

        def clear_chat() -> tuple[list[dict[str, Any]], str, str]:
            return [], EMPTY_SOURCES_HTML, ""

        submit_btn.click(
            fn=respond,
            inputs=[query_box, chatbot, provider_filter, top_k_slider],
            outputs=[chatbot, sources_panel, query_box],
        )
        query_box.submit(
            fn=respond,
            inputs=[query_box, chatbot, provider_filter, top_k_slider],
            outputs=[chatbot, sources_panel, query_box],
        )
        clear_btn.click(
            fn=clear_chat,
            inputs=None,
            outputs=[chatbot, sources_panel, query_box],
        )

    return demo
