"""Asynchronous HTML and Markdown cloud documentation scraper."""

import asyncio
from dataclasses import dataclass
import logging
from pathlib import Path
import re
from typing import Iterable

from bs4 import BeautifulSoup, Tag
import httpx
import yaml

from cloud_smash.retry import retry_async

logger = logging.getLogger(__name__)

_NOISE_SELECTORS = (
    "script",
    "style",
    "noscript",
    "svg",
    "nav",
    "footer",
    "header",
    "aside",
    "[role='navigation']",
    "[role='banner']",
    "[role='contentinfo']",
    ".devsite-nav",
    ".devsite-header",
    ".devsite-footer",
    ".breadcrumb",
    ".feedback",
)

_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
_MULTI_NEWLINE_RE = re.compile(r"\n{3,}")


@dataclass(frozen=True)
class DocSource:
    """Target documentation URL and its cloud metadata."""

    provider: str
    url: str
    title: str = ""
    topic: str = ""


@dataclass(frozen=True)
class ScrapedDocument:
    """Cleaned documentation page ready for token chunking."""

    url: str
    title: str
    provider: str
    topic: str
    content: str


def load_sources_from_yaml(path: Path) -> list[DocSource]:
    """Load documentation source entries from a YAML configuration file."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    entries = data.get("sources", [])
    return [
        DocSource(
            provider=str(item["provider"]).lower(),
            url=str(item["url"]),
            title=str(item.get("title", "")),
            topic=str(item.get("topic", "")),
        )
        for item in entries
    ]


def clean_markdown(raw_text: str) -> str:
    """Strip YAML frontmatter and normalize excessive blank lines without altering indentation."""
    without_frontmatter = _FRONTMATTER_RE.sub("", raw_text)
    lines = [line.rstrip() for line in without_frontmatter.splitlines()]
    normalized = "\n".join(lines).strip()
    return _MULTI_NEWLINE_RE.sub("\n\n", normalized)


def _detect_code_language(code_tag: Tag) -> str:
    classes = code_tag.get("class") or []
    for cls in classes:
        for prefix in ("language-", "lang-"):
            if cls.startswith(prefix):
                return cls[len(prefix) :]
    return ""


def _render_element_lines(node: Tag) -> list[str]:
    """Convert structural HTML tags into clean Markdown preserving headings and code blocks."""
    lines: list[str] = []
    for el in node.find_all(
        ["h1", "h2", "h3", "h4", "pre", "p", "li", "blockquote"], recursive=True
    ):
        # Skip nested tags already handled inside a <pre> or parent <li>/<p>.
        if el.name != "pre" and el.find_parent("pre") is not None:
            continue
        if el.name == "p" and el.find_parent("li") is not None:
            continue

        if el.name in {"h1", "h2", "h3", "h4"}:
            heading = " ".join(el.get_text(" ", strip=True).split())
            if heading:
                level = int(el.name[1])
                lines.append(f"\n{'#' * level} {heading}")
        elif el.name == "pre":
            code_tag = el.find("code")
            lang = _detect_code_language(code_tag) if isinstance(code_tag, Tag) else ""
            code_text = el.get_text("\n").strip("\n")
            if code_text:
                lines.append(f"\n```{lang}\n{code_text}\n```")
        elif el.name == "li":
            item_text = " ".join(el.get_text(" ", strip=True).split())
            if item_text:
                lines.append(f"- {item_text}")
        elif el.name == "blockquote":
            quote_text = " ".join(el.get_text(" ", strip=True).split())
            if quote_text:
                lines.append(f"> {quote_text}")
        else:
            para_text = " ".join(el.get_text(" ", strip=True).split())
            if para_text:
                lines.append(para_text)
    return lines


def extract_clean_markdown_from_html(html: str, fallback_title: str = "") -> tuple[str, str]:
    """Extract document title and clean Markdown-formatted body from an HTML page."""
    soup = BeautifulSoup(html, "lxml")

    page_title = fallback_title
    if soup.title and soup.title.string:
        page_title = soup.title.string.strip() or fallback_title
    h1 = soup.find("h1")
    if isinstance(h1, Tag):
        h1_text = " ".join(h1.get_text(" ", strip=True).split())
        if h1_text:
            page_title = h1_text

    for selector in _NOISE_SELECTORS:
        for noisy in soup.select(selector):
            noisy.decompose()

    main_container = (
        soup.find("main") or soup.find("article") or soup.find(attrs={"role": "main"}) or soup.body
    )
    if not isinstance(main_container, Tag):
        return page_title or "Untitled", ""

    lines = _render_element_lines(main_container)
    if not lines:
        fallback_text = " ".join(main_container.get_text(" ", strip=True).split())
        return page_title or "Untitled", fallback_text

    content = _MULTI_NEWLINE_RE.sub("\n\n", "\n\n".join(lines)).strip()
    return page_title or "Untitled", content


def _is_retryable_fetch_error(exc: Exception) -> bool:
    if isinstance(exc, (httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in {429, 500, 502, 503, 504}
    return False


class AsyncDocScraper:
    """Concurrent documentation scraper supporting both HTML and raw Markdown URLs."""

    def __init__(
        self,
        concurrency: int = 5,
        timeout_seconds: float = 30.0,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._semaphore = asyncio.Semaphore(concurrency)
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(
            follow_redirects=True,
            timeout=httpx.Timeout(timeout_seconds),
            headers={"User-Agent": "CloudSmash-DocIngestor/0.1 (+https://huggingface.co/spaces)"},
        )

    async def aclose(self) -> None:
        """Close the HTTP client if created by this scraper."""
        if self._owns_client:
            await self._client.aclose()

    async def fetch_source(self, source: DocSource) -> ScrapedDocument | None:
        """Fetch and clean a single documentation URL into a ScrapedDocument."""
        async with self._semaphore:
            try:
                response = await retry_async(
                    lambda: self._get_ok(source.url),
                    is_retryable=_is_retryable_fetch_error,
                    max_attempts=3,
                )
            except Exception as exc:
                logger.error("Failed to fetch %s: %s", source.url, exc)
                return None

        content_type = response.headers.get("content-type", "").lower()
        is_markdown = source.url.lower().endswith((".md", ".mdx", ".txt")) or (
            "text/markdown" in content_type or "text/plain" in content_type
        )

        if is_markdown:
            cleaned = clean_markdown(response.text)
            title = source.title or self._infer_markdown_title(cleaned) or source.url
        else:
            title, cleaned = extract_clean_markdown_from_html(
                response.text, fallback_title=source.title
            )

        if not cleaned:
            logger.warning("No extractable text found at %s", source.url)
            return None

        return ScrapedDocument(
            url=source.url,
            title=title,
            provider=source.provider,
            topic=source.topic,
            content=cleaned,
        )

    async def fetch_all(self, sources: Iterable[DocSource]) -> list[ScrapedDocument]:
        """Scrape all configured documentation sources concurrently."""
        tasks = [self.fetch_source(src) for src in sources]
        results = await asyncio.gather(*tasks)
        return [doc for doc in results if doc is not None]

    async def _get_ok(self, url: str) -> httpx.Response:
        response = await self._client.get(url)
        response.raise_for_status()
        return response

    @staticmethod
    def _infer_markdown_title(markdown_text: str) -> str:
        for line in markdown_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
        return ""
