param(
    [string]$EmbedModel = $env:OLLAMA_EMBED_MODEL,
    [string]$ChatModel = $env:OLLAMA_CHAT_MODEL,
    [string]$TunnelName = $env:CLOUDFLARED_TUNNEL_NAME
)

if (-not $EmbedModel) { $EmbedModel = "nomic-embed-text" }
if (-not $ChatModel) { $ChatModel = "qwen2.5:7b" }

Write-Host "[1/4] Checking local Ollama server on port 11434..."
try {
    Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 3 | Out-Null
} catch {
    Write-Host "Starting 'ollama serve' in background..."
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

Write-Host "[2/4] Pulling required models ($EmbedModel, $ChatModel)..."
ollama pull $EmbedModel
ollama pull $ChatModel

Write-Host "[3/4] Checking cloudflared..."
if (-not (Get-Command cloudflared -ErrorAction SilentlyContinue)) {
    Write-Error "cloudflared is not installed. Install via: winget install Cloudflare.cloudflared"
    exit 1
}

Write-Host "[4/4] Starting Cloudflare Tunnel to http://localhost:11434..."
if ($TunnelName) {
    cloudflared tunnel run $TunnelName
} else {
    Write-Host "No TunnelName provided; starting a temporary Quick Tunnel (set OLLAMA_BASE_URL in HF Spaces to the printed trycloudflare.com URL)."
    cloudflared tunnel --url http://localhost:11434 --http-host-header localhost:11434
}
