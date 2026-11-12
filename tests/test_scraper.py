"""Tests for HTML/Markdown extraction and async documentation scraper."""

from pathlib import Path

import httpx

from cloud_smash.ingestion.scraper import (
    AsyncDocScraper,
    DocSource,
    clean_markdown,
    extract_clean_markdown_from_html,
    load_sources_from_yaml,
)


def test_extract_clean_markdown_preserves_code_and_strips_nav() -> None:
    html = """
    <html>
      <head><title>Ignored Title</title></head>
      <body>
        <nav>Home | Pricing | Docs</nav>
        <main>
          <h1>GCP IAM Roles</h1>
          <p>Grant least-privilege roles using gcloud.</p>
          <pre><code class="language-yaml">bindings:
  - role: roles/viewer
    members:
      - user:alice@example.com</code></pre>
          <ul>
            <li>Basic roles</li>
            <li>Predefined roles</li>
          </ul>
        </main>
        <footer>Copyright Cloud</footer>
      </body>
    </html>
    """
    title, md = extract_clean_markdown_from_html(html)
    assert title == "GCP IAM Roles"
    assert "Pricing" not in md
    assert "Copyright Cloud" not in md
    assert "```yaml\nbindings:\n  - role: roles/viewer" in md
    assert "- Basic roles" in md


def test_clean_markdown_strips_frontmatter_and_preserves_indentation() -> None:
    raw = """---
title: Azure RBAC
ms.topic: overview
---

# Azure RBAC


```json
{
  "RoleDefinitionName": "Reader"
}
```
"""
    cleaned = clean_markdown(raw)
    assert "ms.topic" not in cleaned
    assert cleaned.startswith("# Azure RBAC")
    assert '  "RoleDefinitionName": "Reader"' in cleaned


def test_load_sources_from_yaml(tmp_path: Path) -> None:
    cfg = tmp_path / "sources.yaml"
    cfg.write_text(
        """
sources:
  - provider: GCP
    title: VPC Docs
    url: https://cloud.google.com/vpc/docs/vpc
    topic: networking
""",
        encoding="utf-8",
    )
    sources = load_sources_from_yaml(cfg)
    assert len(sources) == 1
    assert sources[0].provider == "gcp"
    assert sources[0].topic == "networking"


async def test_async_doc_scraper_handles_html_md_and_failures() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url).endswith(".md"):
            return httpx.Response(
                200,
                text="---\ntitle: Test\n---\n# Azure AKS\nManaged Kubernetes.",
                headers={"content-type": "text/markdown"},
            )
        if "broken" in str(request.url):
            return httpx.Response(404, text="Not Found")
        return httpx.Response(
            200,
            text="<html><body><main><h1>GCP VPC</h1><p>Virtual network.</p></main></body></html>",
            headers={"content-type": "text/html"},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        scraper = AsyncDocScraper(concurrency=2, http_client=client)
        docs = await scraper.fetch_all(
            [
                DocSource(provider="azure", url="https://example.com/aks.md"),
                DocSource(provider="gcp", url="https://example.com/vpc"),
                DocSource(provider="gcp", url="https://example.com/broken"),
            ]
        )

    assert len(docs) == 2
    assert docs[0].title == "Azure AKS"
    assert "Managed Kubernetes." in docs[0].content
    assert docs[1].title == "GCP VPC"
