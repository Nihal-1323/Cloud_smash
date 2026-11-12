"""Application configuration loaded from environment variables and .env files."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for ingestion, Pinecone storage, Ollama inference, and FastAPI."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Pinecone (Starter Tier)
    pinecone_api_key: str = Field(default="", description="Pinecone API key.")
    pinecone_index_name: str = Field(default="cloud-infra-docs")
    pinecone_namespace: str = Field(default="default")
    pinecone_cloud: str = Field(default="aws")
    pinecone_region: str = Field(default="us-east-1")
    pinecone_embed_dimension: int = Field(default=768, ge=1)

    # Ollama (Local node or Cloudflare Tunnel HTTPS endpoint)
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_embed_model: str = Field(default="nomic-embed-text")
    ollama_chat_model: str = Field(default="qwen2.5:7b")
    ollama_timeout_seconds: float = Field(default=120.0, gt=0)

    # Optional tunnel protection headers
    cf_access_client_id: Optional[str] = Field(default=None)
    cf_access_client_secret: Optional[str] = Field(default=None)
    ollama_bearer_token: Optional[str] = Field(default=None)

    # Chunking & RAG
    chunk_size_tokens: int = Field(default=500, ge=50)
    chunk_overlap_tokens: int = Field(default=50, ge=0)
    rag_top_k: int = Field(default=4, ge=1, le=10)
    llm_temperature: float = Field(default=0.1, ge=0.0, le=2.0)

    # Ingestion
    sources_config_path: Path = Field(default=Path("configs/sources.yaml"))
    scrape_concurrency: int = Field(default=5, ge=1, le=20)
    upsert_batch_size: int = Field(default=50, ge=1, le=200)

    # Server
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=7860, ge=1, le=65535)
    log_level: str = Field(default="INFO")

    def ollama_headers(self) -> dict[str, str]:
        """Build optional authentication headers for requests sent through Cloudflare Tunnel."""
        headers: dict[str, str] = {}
        if self.cf_access_client_id and self.cf_access_client_secret:
            headers["CF-Access-Client-Id"] = self.cf_access_client_id
            headers["CF-Access-Client-Secret"] = self.cf_access_client_secret
        if self.ollama_bearer_token:
            headers["Authorization"] = f"Bearer {self.ollama_bearer_token}"
        return headers


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
