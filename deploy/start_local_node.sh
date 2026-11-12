#!/usr/bin/env bash
set -euo pipefail

EMBED_MODEL="${OLLAMA_EMBED_MODEL:-nomic-embed-text}"
CHAT_MODEL="${OLLAMA_CHAT_MODEL:-qwen2.5:7b}"
TUNNEL_NAME="${CLOUDFLARED_TUNNEL_NAME:-}"

echo "[1/4] Checking Ollama daemon..."
if ! curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "Starting Ollama serve in background..."
  nohup ollama serve >/tmp/ollama.log 2>&1 &
  sleep 3
fi

echo "[2/4] Ensuring models are pulled ($EMBED_MODEL, $CHAT_MODEL)..."
ollama pull "$EMBED_MODEL"
ollama pull "$CHAT_MODEL"

echo "[3/4] Checking cloudflared..."
if ! command -v cloudflared >/dev/null 2>&1; then
  echo "ERROR: cloudflared is not installed. Install it from https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
  exit 1
fi

echo "[4/4] Starting Cloudflare Tunnel to http://localhost:11434..."
if [[ -n "$TUNNEL_NAME" ]]; then
  exec cloudflared tunnel run "$TUNNEL_NAME"
else
  echo "No CLOUDFLARED_TUNNEL_NAME set; starting a temporary Quick Tunnel (URL changes on restart)."
  exec cloudflared tunnel --url http://localhost:11434 --http-host-header localhost:11434
fi
