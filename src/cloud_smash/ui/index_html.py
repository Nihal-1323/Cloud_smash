"""Awwwards-Inspired Editorial & Architectural Console for Cloud Smash.

Aesthetic: Acid-Minimalism, International Typographic Style, Stark Contrast,
Film Grain Texture, Brutalist Hairline Grids, and Editorial Serif accents.
"""

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CLOUD SMASH — Architectural Documentation Console</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Space Grotesk', '-apple-system', 'sans-serif'],
            serif: ['Instrument Serif', 'Georgia', 'serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
          colors: {
            void: '#060709',
            surface: {
              900: '#0b0d12',
              800: '#11141c',
              700: '#1a1e29',
              600: '#262c3b',
              500: '#384154',
            },
            acid: {
              DEFAULT: '#d4ff00',
              glow: 'rgba(212, 255, 0, 0.25)',
              dim: '#a3c700',
            },
            parchment: '#f4f2ed',
            azure: '#0078d4',
            gcp: '#4285f4',
          }
        }
      }
    }
  </script>
  <style>
    :root {
      --bg: #060709;
      --acid: #d4ff00;
      --line: rgba(255, 255, 255, 0.08);
      --line-bright: rgba(255, 255, 255, 0.16);
    }

    body {
      background-color: var(--bg);
      color: #e5e5e5;
      font-family: 'Space Grotesk', sans-serif;
      letter-spacing: -0.01em;
    }

    /* Architectural Grid Background */
    .grid-mesh {
      background-size: 40px 40px;
      background-image: 
        linear-gradient(to right, rgba(255, 255, 255, 0.025) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
    }

    /* Film Grain Overlay */
    .film-grain {
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.028'/%3E%3C/svg%3E");
      pointer-events: none;
      z-index: 99;
    }

    /* Custom Hairline Borders */
    .hairline-b { border-bottom: 1px solid var(--line); }
    .hairline-t { border-top: 1px solid var(--line); }
    .hairline-r { border-right: 1px solid var(--line); }
    .hairline-l { border-left: 1px solid var(--line); }
    .hairline { border: 1px solid var(--line); }

    /* Crosshair accents */
    .crosshair {
      position: relative;
    }
    .crosshair::before {
      content: '+';
      position: absolute;
      top: -6px; left: -5px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      color: rgba(255, 255, 255, 0.3);
      line-height: 1;
      pointer-events: none;
    }

    /* Kinetic Marquee */
    @keyframes marquee {
      0% { transform: translateX(0%); }
      100% { transform: translateX(-50%); }
    }
    .marquee-track {
      display: flex;
      width: 200%;
      animation: marquee 35s linear infinite;
    }

    /* Markdown Dossier Output */
    .dossier-prose p {
      margin-bottom: 1em;
      line-height: 1.7;
      color: #d1d5db;
      font-size: 0.925rem;
    }
    .dossier-prose h1, .dossier-prose h2, .dossier-prose h3 {
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      color: #ffffff;
      margin-top: 1.3em;
      margin-bottom: 0.5em;
      letter-spacing: -0.02em;
    }
    .dossier-prose h1 { font-size: 1.35rem; }
    .dossier-prose h2 { font-size: 1.15rem; color: #f4f2ed; }
    .dossier-prose h3 { font-size: 1.02rem; color: #d4ff00; }
    .dossier-prose ul {
      list-style-type: none;
      padding-left: 0;
      margin-bottom: 1em;
    }
    .dossier-prose li {
      position: relative;
      padding-left: 1.25rem;
      margin-bottom: 0.4rem;
      font-size: 0.9rem;
    }
    .dossier-prose li::before {
      content: '—';
      position: absolute;
      left: 0;
      color: #d4ff00;
      font-weight: 600;
    }
    .dossier-prose strong {
      color: #ffffff;
      font-weight: 600;
    }
    .dossier-prose code:not(pre code) {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      background: #141720;
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #d4ff00;
      padding: 2px 6px;
      border-radius: 4px;
    }
    .dossier-prose pre {
      background: #08090d;
      border: 1px solid var(--line-bright);
      border-left: 3px solid #d4ff00;
      padding: 14px 16px;
      border-radius: 6px;
      overflow-x: auto;
      margin: 1.2em 0;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      line-height: 1.5;
    }
    .dossier-prose blockquote {
      border-left: 2px solid #d4ff00;
      padding-left: 14px;
      font-family: 'Instrument Serif', serif;
      font-style: italic;
      font-size: 1.05rem;
      color: #f4f2ed;
      margin: 1.2em 0;
    }

    /* Citation Pills */
    .citation-stamp {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      font-weight: 700;
      padding: 1px 7px;
      border-radius: 2px;
      background: rgba(212, 255, 0, 0.12);
      border: 1px solid rgba(212, 255, 0, 0.4);
      color: #d4ff00;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin: 0 2px;
      vertical-align: baseline;
      transition: all 0.15s ease;
      cursor: pointer;
    }
    .citation-stamp:hover {
      background: #d4ff00;
      color: #060709;
      transform: translateY(-1px);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); }
    ::-webkit-scrollbar-thumb:hover { background: #d4ff00; }
  </style>
</head>
<body class="h-screen w-screen overflow-hidden flex flex-col grid-mesh">

  <!-- Grain Filter -->
  <div class="film-grain"></div>

  <!-- ==================== AWWWARDS EDITORIAL TOP BAR ==================== -->
  <header class="h-14 hairline-b bg-void/90 backdrop-blur-md px-6 flex items-center justify-between flex-shrink-0 z-40">
    <div class="flex items-center gap-6">
      
      <!-- Brand Minimalist Mark -->
      <div class="flex items-center gap-3">
        <div class="w-6 h-6 border border-acid flex items-center justify-center font-mono text-[10px] font-bold text-acid bg-acid/10">
          CS
        </div>
        <div class="flex items-baseline gap-2">
          <span class="font-bold tracking-tight text-white text-sm">CLOUD SMASH</span>
          <span class="font-serif italic text-neutral-400 text-xs">/ documentation console</span>
        </div>
      </div>

      <!-- Navigation Matrix -->
      <nav class="hidden md:flex items-center gap-1 font-mono text-xs hairline-l pl-6">
        <button id="nav-btn-console" onclick="switchView('console')" class="px-3 py-1.5 text-acid bg-white/5 border border-acid/40 transition">
          [01] CONSOLE
        </button>
        <button id="nav-btn-corpus" onclick="switchView('corpus')" class="px-3 py-1.5 text-neutral-400 hover:text-white transition">
          [02] CORPUS INDEX
        </button>
        <button id="nav-btn-blueprint" onclick="switchView('blueprint')" class="px-3 py-1.5 text-neutral-400 hover:text-white transition">
          [03] TOPOLOGY
        </button>
        <button id="nav-btn-ingest" onclick="switchView('ingest')" class="px-3 py-1.5 text-neutral-400 hover:text-white transition">
          [04] INGESTION HUB
        </button>
      </nav>
    </div>

    <!-- Live Telemetry Ticker -->
    <div class="flex items-center gap-4 font-mono text-[11px]">
      <div class="hidden lg:flex items-center gap-2 text-neutral-400">
        <span class="inline-block w-1.5 h-1.5 rounded-full bg-acid animate-pulse"></span>
        <span>INDEX // PINECONE_50_RECS</span>
      </div>
      <div class="hidden sm:flex items-center gap-2 text-neutral-400 hairline-l pl-4">
        <span>GPU_INFERENCE // QWEN_2.5_7B</span>
      </div>
      <div class="px-2.5 py-1 text-black bg-acid font-bold text-[10px] uppercase tracking-wider">
        $0.00 / MO
      </div>
      <a href="/gradio" target="_blank" class="text-neutral-400 hover:text-white transition text-xs hairline-l pl-3 hidden sm:inline" title="Switch to Gradio view">
        [GRADIO ↗]
      </a>
    </div>
  </header>

  <!-- ==================== KINETIC MARQUEE TAPE ==================== -->
  <div class="h-6 hairline-b bg-surface-900/60 overflow-hidden flex items-center font-mono text-[10px] text-neutral-500 uppercase tracking-widest select-none flex-shrink-0">
    <div class="marquee-track">
      <span class="px-4">/// ZERO-BILLING RETRIEVAL AUGMENTED GENERATION SYSTEM</span>
      <span class="px-4 text-acid">/// GCP IAM ROLES OVERVIEW (30 CHUNKS)</span>
      <span class="px-4">/// GCP VIRTUAL PRIVATE CLOUD (8 CHUNKS)</span>
      <span class="px-4 text-acid">/// GKE AUTOPILOT ARCHITECTURE (4 CHUNKS)</span>
      <span class="px-4">/// AZURE RBAC GOVERNANCE (3 CHUNKS)</span>
      <span class="px-4 text-acid">/// AZURE VIRTUAL NETWORKS (3 CHUNKS)</span>
      <span class="px-4">/// AZURE KUBERNETES SERVICE (2 CHUNKS)</span>
      <span class="px-4 text-acid">/// NOMIC-EMBED-TEXT 768-DIMENSIONAL COSINE MATRIX</span>
      <!-- Duplicate for seamless infinite loop -->
      <span class="px-4">/// ZERO-BILLING RETRIEVAL AUGMENTED GENERATION SYSTEM</span>
      <span class="px-4 text-acid">/// GCP IAM ROLES OVERVIEW (30 CHUNKS)</span>
      <span class="px-4">/// GCP VIRTUAL PRIVATE CLOUD (8 CHUNKS)</span>
      <span class="px-4 text-acid">/// GKE AUTOPILOT ARCHITECTURE (4 CHUNKS)</span>
      <span class="px-4">/// AZURE RBAC GOVERNANCE (3 CHUNKS)</span>
      <span class="px-4 text-acid">/// AZURE VIRTUAL NETWORKS (3 CHUNKS)</span>
      <span class="px-4">/// AZURE KUBERNETES SERVICE (2 CHUNKS)</span>
      <span class="px-4 text-acid">/// NOMIC-EMBED-TEXT 768-DIMENSIONAL COSINE MATRIX</span>
    </div>
  </div>

  <!-- ==================== MAIN WORKSPACE VIEWPORT ==================== -->
  <div class="flex-1 flex overflow-hidden">

    <!-- ==================== VIEW 1: THE CONSOLE ==================== -->
    <div id="view-console" class="flex-1 flex flex-col md:flex-row overflow-hidden">
      
      <!-- Center Dossier & Query Stream Area -->
      <div class="flex-1 flex flex-col overflow-hidden hairline-r">
        
        <!-- Stream Output Container -->
        <div id="dossier-scroll" class="flex-1 overflow-y-auto p-6 md:p-10 space-y-8">
          
          <!-- Editorial Hero Introduction -->
          <div id="editorial-hero" class="max-w-3xl mx-auto pt-6 pb-4">
            
            <div class="flex items-center gap-3 font-mono text-[11px] text-neutral-400 uppercase tracking-widest mb-4">
              <span class="text-acid">[SPEC 01]</span>
              <span>Cloud Infrastructure Documentation Assistant</span>
              <span>—</span>
              <span class="text-white">Strict Grounding</span>
            </div>

            <h1 class="text-4xl sm:text-6xl font-bold tracking-tight text-white leading-tight mb-4">
              Synthesize cloud docs with <span class="font-serif italic font-normal text-parchment">mathematical precision.</span>
            </h1>

            <p class="text-neutral-400 text-sm leading-relaxed max-w-xl mb-10 font-sans">
              No hallucinations. No invented CLI flags. Pure semantic cosine retrieval over verified GCP and Azure public technical archives.
            </p>

            <!-- Awwwards Style Curated Query Cards -->
            <div class="space-y-2">
              <div class="font-mono text-[10px] uppercase tracking-widest text-neutral-500 mb-3 flex items-center justify-between">
                <span>// SELECT INQUIRY DIRECTIVE</span>
                <span>[04 CURATED VECTORS]</span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                
                <div onclick="executePrompt('What is GKE Autopilot mode and how does it manage nodes dynamically?')" class="p-4 bg-surface-900 hairline hover:border-acid/60 hover:bg-surface-800 transition cursor-pointer group">
                  <div class="flex items-center justify-between font-mono text-[10px] text-neutral-500 mb-2">
                    <span class="text-acid group-hover:underline">VECTOR.01 // GKE</span>
                    <span>GCP</span>
                  </div>
                  <div class="font-bold text-white text-sm mb-1 group-hover:text-acid transition">GKE Autopilot Node Engine</div>
                  <div class="text-xs text-neutral-400 leading-normal">Dynamic node sizing, SLA boundaries, and automated security patch management.</div>
                </div>

                <div onclick="executePrompt('What is Azure role-based access control (Azure RBAC) and what are its key components?')" class="p-4 bg-surface-900 hairline hover:border-acid/60 hover:bg-surface-800 transition cursor-pointer group">
                  <div class="flex items-center justify-between font-mono text-[10px] text-neutral-500 mb-2">
                    <span class="text-acid group-hover:underline">VECTOR.02 // RBAC</span>
                    <span>AZURE</span>
                  </div>
                  <div class="font-bold text-white text-sm mb-1 group-hover:text-acid transition">Azure RBAC Governance Matrix</div>
                  <div class="text-xs text-neutral-400 leading-normal">Security principals, granular role definitions, and hierarchical resource scopes.</div>
                </div>

                <div onclick="executePrompt('How do subnets, CIDR ranges, and routing work in Google Cloud VPC networks?')" class="p-4 bg-surface-900 hairline hover:border-acid/60 hover:bg-surface-800 transition cursor-pointer group">
                  <div class="flex items-center justify-between font-mono text-[10px] text-neutral-500 mb-2">
                    <span class="text-acid group-hover:underline">VECTOR.03 // VPC</span>
                    <span>GCP</span>
                  </div>
                  <div class="font-bold text-white text-sm mb-1 group-hover:text-acid transition">GCP VPC Global Network Fabric</div>
                  <div class="text-xs text-neutral-400 leading-normal">Subnet CIDR blocks, BGP Cloud Routers, and Shared VPC multi-project topologies.</div>
                </div>

                <div onclick="executePrompt('What are the core components and features of Azure Kubernetes Service (AKS)?')" class="p-4 bg-surface-900 hairline hover:border-acid/60 hover:bg-surface-800 transition cursor-pointer group">
                  <div class="flex items-center justify-between font-mono text-[10px] text-neutral-500 mb-2">
                    <span class="text-acid group-hover:underline">VECTOR.04 // AKS</span>
                    <span>AZURE</span>
                  </div>
                  <div class="font-bold text-white text-sm mb-1 group-hover:text-acid transition">Azure AKS Architecture</div>
                  <div class="text-xs text-neutral-400 leading-normal">Hosted control planes, self-healing worker pools, and VNet integration.</div>
                </div>

              </div>
            </div>

          </div>

          <!-- Active Investigation Stream -->
          <div id="investigation-stream" class="space-y-8 max-w-3xl mx-auto"></div>

        </div>

        <!-- ==================== COMMAND INPUT BEAM ==================== -->
        <div class="hairline-t bg-void p-4 md:p-6 flex-shrink-0 z-30">
          <div class="max-w-3xl mx-auto space-y-3">
            
            <!-- Controls Strip (Scope & Top-K) -->
            <div class="flex items-center justify-between font-mono text-xs text-neutral-400">
              <div class="flex items-center gap-2">
                <span class="text-[10px] uppercase text-neutral-500">SCOPE:</span>
                <button onclick="setScope('all')" id="scope-btn-all" class="px-2 py-0.5 text-acid bg-white/5 border border-acid/30 text-[10px]">ALL</button>
                <button onclick="setScope('gcp')" id="scope-btn-gcp" class="px-2 py-0.5 text-neutral-400 hover:text-white border border-transparent text-[10px]">GCP</button>
                <button onclick="setScope('azure')" id="scope-btn-azure" class="px-2 py-0.5 text-neutral-400 hover:text-white border border-transparent text-[10px]">AZURE</button>
              </div>

              <div class="flex items-center gap-2">
                <span class="text-[10px] uppercase text-neutral-500">TOP-K CHUNKS:</span>
                <input type="range" id="top-k-range" min="1" max="8" value="4" oninput="document.getElementById('top-k-label').innerText = this.value" class="w-16 accent-acid cursor-pointer">
                <span id="top-k-label" class="font-bold text-acid text-[10px]">4</span>
              </div>
            </div>

            <!-- Brutalist Search Beam -->
            <div class="relative bg-surface-900 hairline focus-within:border-acid transition p-2">
              <div class="flex items-start gap-3">
                <span class="font-mono text-acid text-sm pt-1 pl-2 select-none">&gt;</span>
                <textarea id="command-input" rows="2" placeholder="Input technical cloud query (e.g., GKE Autopilot node limits or Azure RBAC inheritance)..." class="w-full bg-transparent resize-none outline-none font-mono text-xs text-white placeholder-neutral-500 leading-relaxed max-h-32"></textarea>
                
                <div class="flex flex-col gap-1.5 flex-shrink-0">
                  <button id="btn-execute" onclick="executeCurrentQuery()" class="px-4 py-2 bg-acid hover:bg-acid-dim text-void font-mono font-bold text-xs uppercase tracking-wider transition active:scale-95 flex items-center gap-1.5">
                    <span>EXEC</span>
                    <span>↵</span>
                  </button>
                  <button onclick="clearConsole()" class="p-1 text-neutral-500 hover:text-white font-mono text-[10px] uppercase tracking-wider text-center transition">
                    RESET
                  </button>
                </div>
              </div>
            </div>

            <div class="flex justify-between font-mono text-[10px] text-neutral-500">
              <span>GROUNDING STATUS: LOCKED TO PINECONE KNOWLEDGE BASE</span>
              <span id="exec-latency" class="hidden text-acid">LATENCY: <span id="latency-num">0</span>ms</span>
            </div>

          </div>
        </div>

      </div>

      <!-- Right Archival Evidence Deck -->
      <aside class="w-full md:w-80 lg:w-96 bg-surface-900/60 p-5 flex flex-col flex-shrink-0 overflow-hidden">
        <div class="flex items-center justify-between pb-3 hairline-b mb-4">
          <div class="font-mono text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 bg-acid"></span>
            <span>VERIFIED SOURCE DECK</span>
          </div>
          <span id="deck-count" class="font-mono text-[10px] text-acid">0 ARCHIVES</span>
        </div>

        <div id="evidence-deck" class="flex-1 overflow-y-auto space-y-3">
          <!-- Standby Deck State -->
          <div class="text-center py-20 text-neutral-500 font-mono text-xs space-y-2">
            <div class="text-2xl text-neutral-600">//</div>
            <div class="text-neutral-400 font-bold uppercase tracking-wider">Awaiting Execution</div>
            <p class="text-[10px] leading-relaxed max-w-[200px] mx-auto">Extracted 500-token chunks with exact cosine similarity scores will render here.</p>
          </div>
        </div>
      </aside>

    </div>

    <!-- ==================== VIEW 2: CORPUS INDEX ==================== -->
    <div id="view-corpus" class="flex-1 overflow-y-auto p-6 md:p-12 hidden">
      <div class="max-w-4xl mx-auto space-y-8">
        <div>
          <div class="font-mono text-xs text-acid mb-1">[ARCHIVE CATALOG]</div>
          <h2 class="text-3xl font-bold text-white tracking-tight">Active Cloud Knowledge Base</h2>
          <p class="text-sm text-neutral-400 font-mono mt-1">Pinecone Index <span class="text-white">cloud-infra-docs</span> (AWS us-east-1 // 768-D Vectors)</p>
        </div>

        <div class="space-y-4 font-mono text-xs">
          <!-- GCP Docs -->
          <div class="bg-surface-900 hairline p-5 space-y-3">
            <div class="flex items-center justify-between text-neutral-400 hairline-b pb-2">
              <span class="text-acid font-bold">PROVIDER: GOOGLE CLOUD PLATFORM (GCP)</span>
              <span>3 REPOSITORIES</span>
            </div>
            <div class="grid grid-cols-1 gap-2">
              <div class="p-3 bg-void hairline flex justify-between items-center">
                <div>
                  <div class="font-bold text-white">GCP IAM Roles & Permissions Overview</div>
                  <div class="text-[10px] text-neutral-400">#iam · Primitive, predefined, and custom least-privilege roles</div>
                </div>
                <a href="https://cloud.google.com/iam/docs/roles-overview" target="_blank" class="text-acid hover:underline">VIEW DOC ↗</a>
              </div>
              <div class="p-3 bg-void hairline flex justify-between items-center">
                <div>
                  <div class="font-bold text-white">GCP Virtual Private Cloud (VPC) Overview</div>
                  <div class="text-[10px] text-neutral-400">#networking · Global VPCs, subnet CIDR boundaries, BGP routing</div>
                </div>
                <a href="https://cloud.google.com/vpc/docs/vpc" target="_blank" class="text-acid hover:underline">VIEW DOC ↗</a>
              </div>
              <div class="p-3 bg-void hairline flex justify-between items-center">
                <div>
                  <div class="font-bold text-white">GKE Autopilot Architecture & Concepts</div>
                  <div class="text-[10px] text-neutral-400">#kubernetes · Managed worker provisioning, autoscaling, SLA policies</div>
                </div>
                <a href="https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview" target="_blank" class="text-acid hover:underline">VIEW DOC ↗</a>
              </div>
            </div>
          </div>

          <!-- Azure Docs -->
          <div class="bg-surface-900 hairline p-5 space-y-3">
            <div class="flex items-center justify-between text-neutral-400 hairline-b pb-2">
              <span class="text-acid font-bold">PROVIDER: MICROSOFT AZURE</span>
              <span>3 REPOSITORIES</span>
            </div>
            <div class="grid grid-cols-1 gap-2">
              <div class="p-3 bg-void hairline flex justify-between items-center">
                <div>
                  <div class="font-bold text-white">Azure Role-Based Access Control (RBAC) Overview</div>
                  <div class="text-[10px] text-neutral-400">#iam · Security principals, role definitions, and management scopes</div>
                </div>
                <a href="https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/articles/role-based-access-control/overview.md" target="_blank" class="text-acid hover:underline">VIEW DOC ↗</a>
              </div>
              <div class="p-3 bg-void hairline flex justify-between items-center">
                <div>
                  <div class="font-bold text-white">Azure Virtual Network (VNet) Overview</div>
                  <div class="text-[10px] text-neutral-400">#networking · VNet subnets, Network Security Groups (NSGs), Peering</div>
                </div>
                <a href="https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/articles/virtual-network/virtual-networks-overview.md" target="_blank" class="text-acid hover:underline">VIEW DOC ↗</a>
              </div>
              <div class="p-3 bg-void hairline flex justify-between items-center">
                <div>
                  <div class="font-bold text-white">Azure Kubernetes Service (AKS) Architecture</div>
                  <div class="text-[10px] text-neutral-400">#kubernetes · Hosted control plane, node pools, virtual network overlays</div>
                </div>
                <a href="https://learn.microsoft.com/en-us/azure/aks/what-is-aks" target="_blank" class="text-acid hover:underline">VIEW DOC ↗</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== VIEW 3: TOPOLOGY ==================== -->
    <div id="view-blueprint" class="flex-1 overflow-y-auto p-6 md:p-12 hidden">
      <div class="max-w-4xl mx-auto space-y-8">
        <div>
          <div class="font-mono text-xs text-acid mb-1">[SYSTEM SPECIFICATION]</div>
          <h2 class="text-3xl font-bold text-white tracking-tight">Zero-Billing Hybrid Topology</h2>
          <p class="text-sm text-neutral-400 font-mono mt-1">Decoupled 3-Node Architecture for Enterprise Scale at $0.00 Cost.</p>
        </div>

        <div class="bg-surface-900 hairline p-6 space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
            <div class="p-4 bg-void hairline">
              <div class="text-neutral-500 text-[10px]">NODE 01 // ORCHESTRATION</div>
              <div class="text-white font-bold text-sm mt-1">Hugging Face Spaces</div>
              <div class="text-neutral-400 mt-2">FastAPI Backend + Bespoke Single-Page Interface</div>
              <div class="text-acid font-bold text-[10px] mt-3">FREE TIER: 16GB RAM / 2 vCPU</div>
            </div>

            <div class="p-4 bg-void hairline">
              <div class="text-neutral-500 text-[10px]">NODE 02 // VECTOR STORAGE</div>
              <div class="text-white font-bold text-sm mt-1">Pinecone Serverless</div>
              <div class="text-neutral-400 mt-2">768-D Cosine Metric Serverless Index</div>
              <div class="text-acid font-bold text-[10px] mt-3">STARTER TIER: 2GB STORAGE / 2M WRITES</div>
            </div>

            <div class="p-4 bg-void hairline">
              <div class="text-neutral-500 text-[10px]">NODE 03 // GPU INFERENCE</div>
              <div class="text-white font-bold text-sm mt-1">Local GPU + Tunnel</div>
              <div class="text-neutral-400 mt-2">Qwen 2.5 7B Instruct via Ollama + Cloudflare Tunnel</div>
              <div class="text-acid font-bold text-[10px] mt-3">WORKSTATION: 16GB VRAM (ZERO PER-TOKEN BILLING)</div>
            </div>
          </div>

          <div class="p-4 bg-void hairline font-mono text-xs text-neutral-400 leading-relaxed">
            <div class="text-white font-bold mb-2">// DATA LIFECYCLE & EXECUTION PATHWAY</div>
            [INGESTION]: Asynchronous HTTP scraper fetches HTML/Markdown docs &#8594; TokenChunker enforces 500-token windows (50 overlap) &#8594; nomic-embed-text generates 768-dim vectors &#8594; Pinecone batch upsert.<br><br>
            [RETRIEVAL]: Incoming query vectorized via Ollama &#8594; Cosine similarity search filters top-K chunks &#8594; Assembled into strict grounding XML context blocks.<br><br>
            [SYNTHESIS]: Forwarded over encrypted Cloudflare Tunnel to local Qwen 2.5 7B &#8594; Streamed back word-by-word with [Source N] verified citations.
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== VIEW 4: INGESTION HUB ==================== -->
    <div id="view-ingest" class="flex-1 overflow-y-auto p-6 md:p-12 hidden">
      <div class="max-w-2xl mx-auto space-y-6">
        <div>
          <div class="font-mono text-xs text-acid mb-1">[DIRECT INGESTION ENGINE]</div>
          <h2 class="text-3xl font-bold text-white tracking-tight">Index New Cloud Documentation</h2>
          <p class="text-sm text-neutral-400 font-mono mt-1">Feed live documentation URLs directly into your Pinecone vector database.</p>
        </div>

        <div class="bg-surface-900 hairline p-6 space-y-4 font-mono text-xs">
          <div>
            <label class="block text-neutral-400 uppercase text-[10px] mb-2 font-bold">Documentation URL</label>
            <input type="url" id="ingest-url" placeholder="https://cloud.google.com/... or https://learn.microsoft.com/..." class="w-full bg-void hairline p-3 text-white outline-none focus:border-acid">
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-neutral-400 uppercase text-[10px] mb-2 font-bold">Cloud Provider</label>
              <select id="ingest-provider" class="w-full bg-void hairline p-3 text-white outline-none">
                <option value="gcp">Google Cloud (GCP)</option>
                <option value="azure">Microsoft Azure</option>
              </select>
            </div>
            <div>
              <label class="block text-neutral-400 uppercase text-[10px] mb-2 font-bold">Topic Tag</label>
              <input type="text" id="ingest-topic" placeholder="e.g. security, storage, networking" class="w-full bg-void hairline p-3 text-white outline-none focus:border-acid">
            </div>
          </div>

          <button onclick="triggerIngest()" id="btn-ingest-action" class="w-full py-3 bg-acid hover:bg-acid-dim text-void font-bold uppercase tracking-wider transition">
            [EXECUTE: SCRAPE &#8594; CHUNK &#8594; EMBED &#8594; UPSERT]
          </button>

          <div id="ingest-log-box" class="hidden p-4 bg-void hairline text-[11px] text-neutral-300"></div>
        </div>
      </div>
    </div>

  </div>

  <!-- ==================== JAVASCRIPT ENGINE ==================== -->
  <script>
    let currentScope = 'all';
    let history = [];
    let isExecuting = false;

    // View Switching
    function switchView(viewName) {
      ['console', 'corpus', 'blueprint', 'ingest'].forEach(v => {
        document.getElementById(`view-${v}`).classList.add('hidden');
        const btn = document.getElementById(`nav-btn-${v}`);
        btn.classList.remove('text-acid', 'bg-white/5', 'border', 'border-acid/40');
        btn.classList.add('text-neutral-400');
      });
      document.getElementById(`view-${viewName}`).classList.remove('hidden');
      const activeBtn = document.getElementById(`nav-btn-${viewName}`);
      activeBtn.classList.add('text-acid', 'bg-white/5', 'border', 'border-acid/40');
      activeBtn.classList.remove('text-neutral-400');
    }

    // Scope Selector
    function setScope(scope) {
      currentScope = scope;
      ['all', 'gcp', 'azure'].forEach(s => {
        const btn = document.getElementById(`scope-btn-${s}`);
        if (s === scope) {
          btn.className = 'px-2 py-0.5 text-acid bg-white/5 border border-acid/30 text-[10px]';
        } else {
          btn.className = 'px-2 py-0.5 text-neutral-400 hover:text-white border border-transparent text-[10px]';
        }
      });
    }

    // Input Helpers
    function executePrompt(text) {
      document.getElementById('command-input').value = text;
      executeCurrentQuery();
    }

    document.getElementById('command-input').addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        executeCurrentQuery();
      }
    });

    // Reset Console
    function clearConsole() {
      history = [];
      document.getElementById('editorial-hero').classList.remove('hidden');
      document.getElementById('investigation-stream').innerHTML = '';
      document.getElementById('evidence-deck').innerHTML = `
        <div class="text-center py-20 text-neutral-500 font-mono text-xs space-y-2">
          <div class="text-2xl text-neutral-600">//</div>
          <div class="text-neutral-400 font-bold uppercase tracking-wider">Awaiting Execution</div>
          <p class="text-[10px] leading-relaxed max-w-[200px] mx-auto">Extracted 500-token chunks with exact cosine similarity scores will render here.</p>
        </div>
      `;
      document.getElementById('deck-count').innerText = '0 ARCHIVES';
      document.getElementById('exec-latency').classList.add('hidden');
    }

    // Render Query & Assistant Dossier Block
    function appendDossierBlock(query) {
      document.getElementById('editorial-hero').classList.add('hidden');
      const stream = document.getElementById('investigation-stream');
      const id = 'dossier-body-' + Date.now();

      const card = document.createElement('div');
      card.className = 'bg-surface-900 hairline p-6 space-y-4';
      card.innerHTML = `
        <div class="flex items-center justify-between font-mono text-[11px] hairline-b pb-3 text-neutral-400">
          <div class="flex items-center gap-2">
            <span class="text-acid font-bold">[QUERY DIRECTIVE]</span>
            <span class="text-white font-bold">${escapeHtml(query)}</span>
          </div>
          <span class="text-[10px] uppercase text-acid bg-acid/10 px-2 py-0.5 border border-acid/30">GROUNDED SYNTHESIS</span>
        </div>
        <div id="${id}" class="dossier-prose">
          <div class="font-mono text-xs text-acid animate-pulse flex items-center gap-2">
            <span>&gt; Scanning Pinecone vector mesh and querying local Ollama GPU node...</span>
          </div>
        </div>
      `;
      stream.appendChild(card);
      const scrollContainer = document.getElementById('dossier-scroll');
      scrollContainer.scrollTop = scrollContainer.scrollHeight;
      return id;
    }

    // Render Source Deck (Classified Archival Style)
    function renderEvidenceDeck(sources) {
      const deck = document.getElementById('evidence-deck');
      const count = document.getElementById('deck-count');
      count.innerText = `${sources.length} ARCHIVES`;

      if (!sources || sources.length === 0) {
        deck.innerHTML = `<div class="font-mono text-xs text-neutral-500 text-center py-8">NO MATCHING EVIDENCE LOCATED.</div>`;
        return;
      }

      deck.innerHTML = sources.map((s, idx) => {
        const pct = (s.score * 100).toFixed(1);
        const fillBars = Math.round(s.score * 10);
        const barVisual = '█'.repeat(fillBars) + '░'.repeat(10 - fillBars);

        return `
          <div class="bg-void hairline p-3 font-mono text-xs space-y-2 hover:border-acid transition">
            <div class="flex items-center justify-between text-[10px]">
              <span class="text-acid font-bold">[ARCHIVE 0${idx + 1}]</span>
              <span class="px-1.5 py-0.2 bg-white/5 text-neutral-300 uppercase">${s.provider}</span>
            </div>
            
            <a href="${s.url}" target="_blank" class="font-bold text-white hover:text-acid line-clamp-1 block transition">
              ${escapeHtml(s.title || 'Official Specification')} ↗
            </a>

            <div class="text-[10px] text-neutral-500 flex justify-between">
              <span>SIMILARITY: ${pct}%</span>
              <span class="text-acid">${barVisual}</span>
            </div>

            <div class="p-2 bg-surface-900 hairline text-[10px] text-neutral-400 line-clamp-4 leading-normal">
              ${escapeHtml(s.snippet || '')}
            </div>
          </div>
        `;
      }).join('');
    }

    // Execute Query
    async function executeCurrentQuery() {
      const input = document.getElementById('command-input');
      const query = input.value.trim();
      if (!query || isExecuting) return;

      isExecuting = true;
      input.value = '';
      const topK = parseInt(document.getElementById('top-k-range').value, 10);
      const startTime = performance.now();

      const bodyId = appendDossierBlock(query);
      const bodyEl = document.getElementById(bodyId);

      try {
        const response = await fetch('/api/chat/stream', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: query,
            provider: currentScope,
            top_k: topK,
            history: history.slice(-6)
          })
        });

        if (!response.ok) {
          let errDetail = '';
          try {
            const errJson = await response.json();
            errDetail = errJson.detail || '';
          } catch (_) {}
          throw new Error(errDetail || `API status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let fullAnswer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const blocks = buffer.split('\n\n');
          buffer = blocks.pop();

          for (const block of blocks) {
            const evMatch = block.match(/event:\s*([^\n]+)/);
            const dataMatch = block.match(/data:\s*([^\n]+)/);
            if (!evMatch || !dataMatch) continue;

            const ev = evMatch[1].trim();
            const data = JSON.parse(dataMatch[1]);

            if (ev === 'sources') {
              renderEvidenceDeck(data);
            } else if (ev === 'token') {
              fullAnswer += data.token || '';
              bodyEl.innerHTML = formatDossierMarkdown(fullAnswer);
              const scrollContainer = document.getElementById('dossier-scroll');
              scrollContainer.scrollTop = scrollContainer.scrollHeight;
            } else if (ev === 'done') {
              const elapsed = Math.round(performance.now() - startTime);
              document.getElementById('exec-latency').classList.remove('hidden');
              document.getElementById('latency-num').innerText = elapsed;
            }
          }
        }

        history.push({ role: 'user', content: query });
        history.push({ role: 'assistant', content: fullAnswer });

      } catch (err) {
        bodyEl.innerHTML = `<span class="text-red-400 font-mono font-bold">ERROR: ${escapeHtml(err.message)}</span>`;
      } finally {
        isExecuting = false;
      }
    }

    // Markdown Parser with Citation Stamps
    function formatDossierMarkdown(text) {
      if (!text) return '';
      let parsed = marked.parse(text);
      parsed = parsed.replace(/\[Source\s*(\d+)\]/gi, '<span class="citation-stamp">[SOURCE $1]</span>');
      return parsed;
    }

    function escapeHtml(str) {
      return (str || '').replace(/[&<>'"]/g, tag => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;'
      }[tag] || tag));
    }

    // Ingestion Trigger
    async function triggerIngest() {
      const urlInput = document.getElementById('ingest-url');
      const url = urlInput.value.trim();
      const provider = document.getElementById('ingest-provider').value;
      const topic = document.getElementById('ingest-topic').value.trim();
      const logBox = document.getElementById('ingest-log-box');
      const btn = document.getElementById('btn-ingest-action');

      if (!url) {
        alert('Please specify a documentation URL.');
        return;
      }

      btn.disabled = true;
      btn.innerText = 'PROCESSING INGESTION PIPELINE...';
      logBox.classList.remove('hidden');
      logBox.innerHTML = `<div class="text-acid animate-pulse">&gt; Scraping HTML/Markdown &#8594; Token chunking (500 tokens) &#8594; Embedding via local Ollama...</div>`;

      try {
        const res = await fetch('/api/ingest', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url, provider, topic })
        });
        const data = await res.json();
        if (data.status === 'ok') {
          logBox.innerHTML = `
            <div class="text-acid font-bold mb-1">[SUCCESS] DOCUMENT VECTORIZED AND UPSERTED</div>
            <div>&gt; Documents scraped: ${data.documents_scraped}</div>
            <div>&gt; Chunks generated: ${data.chunks_created}</div>
            <div>&gt; Vectors upserted to Pinecone: ${data.vectors_upserted}</div>
          `;
          urlInput.value = '';
        } else {
          logBox.innerHTML = `<div class="text-red-400 font-bold">[ERROR]: ${data.detail || 'Ingestion failed'}</div>`;
        }
      } catch (err) {
        logBox.innerHTML = `<div class="text-red-400 font-bold">[NETWORK ERROR]: ${err.message}</div>`;
      } finally {
        btn.disabled = false;
        btn.innerText = '[EXECUTE: SCRAPE → CHUNK → EMBED → UPSERT]';
      }
    }

    // Live Health Diagnostic Polling
    async function checkHealth() {
      try {
        const r = await fetch('/api/health');
        const data = await r.json();
        const latencyEl = document.getElementById('exec-latency');
        if (data.status !== 'ok') {
          latencyEl.classList.remove('hidden');
          if (data.ollama && data.ollama.status !== 'ok') {
            latencyEl.innerHTML = `<span class="text-rose-400 font-bold">[WARN: OLLAMA OFFLINE — RUN 'ollama serve']</span>`;
          } else if (data.pinecone && data.pinecone.status !== 'ok') {
            latencyEl.innerHTML = `<span class="text-rose-400 font-bold">[WARN: PINECONE ERROR]</span>`;
          }
        }
      } catch (_) {}
    }
    checkHealth();
    setInterval(checkHealth, 15000);
  </script>
</body>
</html>
"""
