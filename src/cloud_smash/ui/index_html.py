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
        <button id="nav-btn-graph" onclick="switchView('graph')" class="px-3 py-1.5 text-neutral-400 hover:text-white transition">
          [02] CHUNK GRAPH MAP
        </button>
        <button id="nav-btn-corpus" onclick="switchView('corpus')" class="px-3 py-1.5 text-neutral-400 hover:text-white transition">
          [03] CORPUS INDEX
        </button>
        <button id="nav-btn-blueprint" onclick="switchView('blueprint')" class="px-3 py-1.5 text-neutral-400 hover:text-white transition">
          [04] TOPOLOGY
        </button>
        <button id="nav-btn-ingest" onclick="switchView('ingest')" class="px-3 py-1.5 text-neutral-400 hover:text-white transition">
          [05] INGESTION HUB
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

    <!-- ==================== VIEW 2: PROCESS GRAPH MAP ==================== -->
    <div id="view-graph" class="flex-1 flex flex-col md:flex-row overflow-hidden hidden">
      
      <!-- Center Graph Area -->
      <div class="flex-1 flex flex-col overflow-hidden hairline-r">
        
        <!-- Graph Control Header Bar -->
        <div class="hairline-b bg-surface-900/80 px-6 py-3 flex-shrink-0 flex flex-wrap items-center justify-between gap-3 font-mono text-xs z-20">
          
          <!-- Mode Switcher: Unified vs Separate -->
          <div class="flex items-center gap-1.5 flex-wrap">
            <span class="text-[10px] text-neutral-500 uppercase tracking-wider mr-1">PROCESS VIEW:</span>
            <button id="graph-mode-unified" onclick="setGraphMode('unified')" class="px-2.5 py-1 text-acid bg-white/5 border border-acid/40 text-[10px] font-bold transition">
              [UNIFIED FLOW]
            </button>
            <button id="graph-mode-input" onclick="setGraphMode('input')" class="px-2.5 py-1 text-neutral-400 hover:text-white border border-transparent text-[10px] transition">
              [01: INPUT CHUNK]
            </button>
            <button id="graph-mode-retrieved" onclick="setGraphMode('retrieved')" class="px-2.5 py-1 text-neutral-400 hover:text-white border border-transparent text-[10px] transition">
              [02: RETRIEVED CHUNKS]
            </button>
            <button id="graph-mode-present" onclick="setGraphMode('present')" class="px-2.5 py-1 text-neutral-400 hover:text-white border border-transparent text-[10px] transition">
              [03: PRESENT CHUNKS]
            </button>
          </div>

          <!-- Quick Metrics Ticker -->
          <div class="flex items-center gap-3 text-[10px] text-neutral-400">
            <span id="graph-stat-input" class="px-2 py-0.5 bg-void hairline text-amber-300">INPUT: AWAITING QUERY</span>
            <span id="graph-stat-retrieved" class="px-2 py-0.5 bg-void hairline text-emerald-400">RETRIEVED: 0 CHUNKS</span>
            <span id="graph-stat-present" class="px-2 py-0.5 bg-void hairline text-sky-400">PRESENT: 50 CHUNKS</span>
          </div>

        </div>

        <!-- Inline Query Bar for Graph View -->
        <div class="hairline-b bg-void/60 px-6 py-2.5 flex items-center gap-3 font-mono text-xs flex-shrink-0">
          <span class="text-acid font-bold select-none">&gt;</span>
          <input type="text" id="graph-query-input" placeholder="Enter technical query to map retrieval (e.g., GKE Autopilot nodes, Azure RBAC scopes, GCP VPC)..." class="w-full bg-transparent outline-none text-white text-xs placeholder-neutral-500" onkeydown="if(event.key==='Enter') executeGraphQuery()">
          <button onclick="executeGraphQuery()" id="btn-graph-exec" class="px-3 py-1 bg-acid hover:bg-acid-dim text-void font-bold text-[10px] uppercase tracking-wider flex-shrink-0 transition">
            EXEC SCAN ➔
          </button>
        </div>

        <!-- Graph Map Interactive SVG Canvas Container -->
        <div id="graph-canvas-container" class="relative flex-1 bg-void overflow-hidden flex items-center justify-center select-none">
          <svg id="rag-process-svg" class="w-full h-full" viewBox="0 0 960 540" preserveAspectRatio="xMidYMid meet">
            <!-- Dynamic SVG content rendered here -->
          </svg>

          <!-- Floating Canvas Legend -->
          <div class="absolute bottom-4 left-6 pointer-events-none font-mono text-[10px] text-neutral-400 bg-surface-900/90 hairline p-2.5 rounded backdrop-blur space-y-1">
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-amber-400 inline-block shadow-[0_0_8px_rgba(251,191,36,0.6)]"></span>
              <span>Input Chunk (Query Vector &middot; 768-D)</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-emerald-400 inline-block shadow-[0_0_8px_rgba(52,211,153,0.6)]"></span>
              <span>Retrieved Chunks (Cosine Similarities)</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-sky-500 inline-block"></span>
              <span>Present Chunks (GCP & Azure Knowledge Base)</span>
            </div>
          </div>
        </div>

        <!-- Bottom Separate Detail Swimlanes (Togglable / Expandable) -->
        <div class="hairline-t bg-surface-900/70 p-4 overflow-y-auto max-h-64 flex-shrink-0 space-y-3 font-mono text-xs">
          
          <!-- Swimlane Selector Tabs -->
          <div class="flex items-center justify-between hairline-b pb-2">
            <div class="flex items-center gap-2">
              <span class="text-[10px] uppercase text-neutral-500 font-bold">DETAILED BREAKDOWN:</span>
              <button id="tab-btn-input-detail" onclick="switchDetailTab('input')" class="px-2 py-0.5 text-amber-300 bg-white/5 border border-amber-300/40 text-[10px]">
                [INPUT CHUNK (SEPARATE)]
              </button>
              <button id="tab-btn-retrieved-detail" onclick="switchDetailTab('retrieved')" class="px-2 py-0.5 text-neutral-400 hover:text-white text-[10px]">
                [RETRIEVED CHUNKS (SEPARATE)]
              </button>
              <button id="tab-btn-present-detail" onclick="switchDetailTab('present')" class="px-2 py-0.5 text-neutral-400 hover:text-white text-[10px]">
                [ALL PRESENT CHUNKS (SEPARATE)]
              </button>
            </div>
            <span id="detail-counter" class="text-[10px] text-acid">READY</span>
          </div>

          <!-- Section 1: Input Chunk Separate View -->
          <div id="detail-pane-input" class="space-y-3">
            <div class="p-4 bg-void hairline space-y-2">
              <div class="flex items-center justify-between text-[11px]">
                <span class="text-amber-400 font-bold">[INPUT DIRECTIVE & EMBEDDING STATUS]</span>
                <span class="text-neutral-400" id="input-token-badge">TOKEN COUNT: 0</span>
              </div>
              <div id="input-query-display" class="text-white text-sm italic font-serif py-1">"Awaiting query directive..."</div>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 hairline-t text-[10px] text-neutral-400">
                <div>MODEL: <b class="text-white">nomic-embed-text</b></div>
                <div>DIMENSION: <b class="text-white">768-D Float32</b></div>
                <div>METRIC: <b class="text-white">Cosine Distance</b></div>
                <div>STATUS: <b class="text-amber-400" id="input-status-badge">STANDBY</b></div>
              </div>
            </div>
          </div>

          <!-- Section 2: Retrieved Chunks Separate View -->
          <div id="detail-pane-retrieved" class="space-y-2 hidden">
            <div id="retrieved-chunks-grid" class="grid grid-cols-1 md:grid-cols-2 gap-2">
              <div class="p-4 bg-void hairline text-neutral-500 text-center col-span-2">No chunks retrieved yet. Execute a query to inspect cosine matches.</div>
            </div>
          </div>

          <!-- Section 3: All Present Chunks Separate View -->
          <div id="detail-pane-present" class="space-y-2 hidden">
            <div class="flex items-center gap-3 pb-2">
              <input type="text" id="present-search-input" placeholder="Search 50 present chunks by title, topic, or keyword..." oninput="filterPresentChunksList()" class="bg-void hairline px-3 py-1 text-white text-xs w-full max-w-sm outline-none focus:border-acid">
              <div class="flex items-center gap-1 text-[10px]">
                <button onclick="filterPresentByProvider('all')" id="btn-pres-all" class="px-2 py-0.5 text-acid bg-white/5 border border-acid/30">ALL (50)</button>
                <button onclick="filterPresentByProvider('gcp')" id="btn-pres-gcp" class="px-2 py-0.5 text-neutral-400 hover:text-white">GCP</button>
                <button onclick="filterPresentByProvider('azure')" id="btn-pres-azure" class="px-2 py-0.5 text-neutral-400 hover:text-white">AZURE</button>
              </div>
            </div>
            <div id="present-chunks-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 max-h-48 overflow-y-auto">
              <!-- Dynamically populated present chunks -->
            </div>
          </div>

        </div>

      </div>

      <!-- Right Chunk Inspector Drawer -->
      <aside class="w-full md:w-80 lg:w-96 bg-surface-900/80 p-5 flex flex-col flex-shrink-0 overflow-hidden hairline-l">
        <div class="flex items-center justify-between pb-3 hairline-b mb-4 font-mono">
          <div class="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-2 h-2 bg-acid"></span>
            <span>CHUNK INSPECTOR</span>
          </div>
          <span id="inspector-badge" class="text-[10px] text-acid uppercase font-bold">[SELECT NODE]</span>
        </div>

        <div id="inspector-body" class="flex-1 overflow-y-auto font-mono text-xs space-y-4">
          <div class="text-center py-24 text-neutral-500 space-y-2">
            <div class="text-3xl text-neutral-600">//</div>
            <div class="text-white font-bold text-xs uppercase tracking-wider">Node Telemetry Standby</div>
            <p class="text-[10px] text-neutral-400 max-w-[220px] mx-auto leading-relaxed">
              Click or hover on any node in the graph map (Input Chunk, Retrieved Chunk, or Present Knowledge Base Chunk) to inspect its full vector payload.
            </p>
          </div>
        </div>
      </aside>

    </div>

    <!-- ==================== VIEW 3: CORPUS INDEX ==================== -->
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

    // Process Graph Map State
    let currentGraphMode = 'unified'; // 'unified' | 'input' | 'retrieved' | 'present'
    let currentDetailTab = 'input';
    let currentGraphData = null;
    let presentProviderFilter = 'all';
    let isFetchingGraph = false;

    // View Switching
    function switchView(viewName) {
      ['console', 'graph', 'corpus', 'blueprint', 'ingest'].forEach(v => {
        const el = document.getElementById(`view-${v}`);
        if (el) el.classList.add('hidden');
        const btn = document.getElementById(`nav-btn-${v}`);
        if (btn) {
          btn.classList.remove('text-acid', 'bg-white/5', 'border', 'border-acid/40');
          btn.classList.add('text-neutral-400');
        }
      });
      const targetEl = document.getElementById(`view-${viewName}`);
      if (targetEl) targetEl.classList.remove('hidden');
      const activeBtn = document.getElementById(`nav-btn-${viewName}`);
      if (activeBtn) {
        activeBtn.classList.add('text-acid', 'bg-white/5', 'border', 'border-acid/40');
        activeBtn.classList.remove('text-neutral-400');
      }
      if (viewName === 'graph') {
        initGraphView();
      }
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
              syncGraphFromSources(query, data);
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

    // ============================================================
    // PROCESS GRAPH MAP JAVASCRIPT ENGINE
    // ============================================================

    async function initGraphView() {
      if (!currentGraphData && !isFetchingGraph) {
        isFetchingGraph = true;
        try {
          const res = await fetch('/api/graph');
          if (res.ok) {
            currentGraphData = await res.json();
            renderGraphMap(currentGraphData, currentGraphMode);
            renderDetailPanes(currentGraphData);
          }
        } catch (e) {
          console.error('Failed to initialize graph:', e);
        } finally {
          isFetchingGraph = false;
        }
      } else if (currentGraphData) {
        renderGraphMap(currentGraphData, currentGraphMode);
        renderDetailPanes(currentGraphData);
      }
    }

    function setGraphMode(mode) {
      currentGraphMode = mode;
      ['unified', 'input', 'retrieved', 'present'].forEach(m => {
        const btn = document.getElementById('graph-mode-' + m);
        if (!btn) return;
        if (m === mode) {
          btn.className = 'px-2.5 py-1 text-acid bg-white/5 border border-acid/40 text-[10px] font-bold transition';
        } else {
          btn.className = 'px-2.5 py-1 text-neutral-400 hover:text-white border border-transparent text-[10px] transition';
        }
      });

      if (mode === 'input') switchDetailTab('input');
      else if (mode === 'retrieved') switchDetailTab('retrieved');
      else if (mode === 'present') switchDetailTab('present');

      if (currentGraphData) {
        renderGraphMap(currentGraphData, currentGraphMode);
      }
    }

    function switchDetailTab(tab) {
      currentDetailTab = tab;
      ['input', 'retrieved', 'present'].forEach(t => {
        const btn = document.getElementById('tab-btn-' + t + '-detail');
        const pane = document.getElementById('detail-pane-' + t);
        if (t === tab) {
          if (btn) btn.className = 'px-2 py-0.5 text-amber-300 bg-white/5 border border-amber-300/40 text-[10px]';
          if (pane) pane.classList.remove('hidden');
        } else {
          if (btn) btn.className = 'px-2 py-0.5 text-neutral-400 hover:text-white text-[10px]';
          if (pane) pane.classList.add('hidden');
        }
      });
    }

    async function executeGraphQuery() {
      const qInput = document.getElementById('graph-query-input');
      const q = (qInput.value || '').trim();
      if (!q) return;

      const btn = document.getElementById('btn-graph-exec');
      btn.innerText = 'SCANNING...';
      btn.disabled = true;

      try {
        const res = await fetch('/api/graph', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: q, provider: currentScope, top_k: 4 })
        });
        if (res.ok) {
          currentGraphData = await res.json();
          renderGraphMap(currentGraphData, currentGraphMode);
          renderDetailPanes(currentGraphData);
          if (document.getElementById('command-input')) {
            document.getElementById('command-input').value = q;
          }
        }
      } catch (err) {
        console.error('Graph query execution failed:', err);
      } finally {
        btn.innerText = 'EXEC SCAN ➔';
        btn.disabled = false;
      }
    }

    async function syncGraphFromSources(query, sources) {
      if (!currentGraphData) {
        try {
          const res = await fetch('/api/graph');
          if (res.ok) currentGraphData = await res.json();
        } catch (_) {}
      }
      if (currentGraphData) {
        const retrievedIds = new Set((sources || []).map(s => s.id));
        currentGraphData.input_chunk = {
          query: query,
          token_count: Math.max(1, query.split(/\s+/).length),
          embed_model: 'nomic-embed-text',
          embed_dimension: 768,
          status: 'vectorized'
        };
        currentGraphData.retrieved_chunks = sources || [];
        if (currentGraphData.present_chunks) {
          currentGraphData.present_chunks.forEach((c, idx) => {
            c.is_retrieved = retrievedIds.has(c.id);
            const found = (sources || []).find(s => s.id === c.id);
            c.score = found ? found.score : null;
            c.retrieval_rank = found ? (sources.indexOf(found) + 1) : null;
          });
        }
        renderGraphMap(currentGraphData, currentGraphMode);
        renderDetailPanes(currentGraphData);
      }
    }

    function renderGraphMap(data, mode) {
      const svg = document.getElementById('rag-process-svg');
      if (!svg || !data) return;

      const inputChunk = data.input_chunk;
      const retrieved = data.retrieved_chunks || [];
      const present = data.present_chunks || [];
      const totalPresent = data.total_present_count || present.length || 50;

      // Update Tickers
      const inStat = document.getElementById('graph-stat-input');
      const retStat = document.getElementById('graph-stat-retrieved');
      const presStat = document.getElementById('graph-stat-present');
      if (inStat) inStat.innerText = inputChunk ? 'INPUT: ' + inputChunk.token_count + ' TOKENS' : 'INPUT: AWAITING QUERY';
      if (retStat) retStat.innerText = 'RETRIEVED: ' + retrieved.length + ' CHUNKS';
      if (presStat) presStat.innerText = 'PRESENT: ' + totalPresent + ' CHUNKS';

      let out = '';
      out += '<defs>';
      out += '  <filter id="goldGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
      out += '  <filter id="emeraldGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
      out += '  <filter id="blueGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
      out += '  <linearGradient id="vectorLaser" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#fbbf24"/><stop offset="100%" stop-color="#10b981"/></linearGradient>';
      out += '</defs>';

      // Grid Pattern
      out += '<g opacity="0.12">';
      for (let x = 40; x < 960; x += 40) {
        out += '<line x1="' + x + '" y1="0" x2="' + x + '" y2="540" stroke="#fff" stroke-width="0.5"/>';
      }
      for (let y = 40; y < 540; y += 40) {
        out += '<line x1="0" y1="' + y + '" x2="' + y + '" stroke="#fff" stroke-width="0.5"/>';
      }
      out += '</g>';

      // ==========================================
      // VIEW MODE 1: SEPARATE INPUT CHUNK
      // ==========================================
      if (mode === 'input') {
        const qText = inputChunk ? inputChunk.query : 'Awaiting input query...';
        const tokens = inputChunk ? inputChunk.token_count : 0;
        const modelName = inputChunk ? inputChunk.embed_model : 'nomic-embed-text';
        const dims = inputChunk ? inputChunk.embed_dimension : 768;

        out += '<text x="480" y="42" text-anchor="middle" font-family="JetBrains Mono" font-size="12" font-weight="700" fill="#fbbf24" letter-spacing="2">STAGE 01 // INPUT CHUNK ISOLATION & VECTOR SPACE</text>';
        out += '<text x="480" y="62" text-anchor="middle" font-family="Space Grotesk" font-size="11" fill="#94a3b8">The incoming user prompt is tokenized and embedded into a 768-dimensional dense vector representation</text>';

        // Concentric Embedding Radiance
        out += '<circle cx="480" cy="240" r="160" fill="none" stroke="rgba(251,191,36,0.08)" stroke-width="1.5" stroke-dasharray="6,6"/>';
        out += '<circle cx="480" cy="240" r="110" fill="none" stroke="rgba(251,191,36,0.18)" stroke-width="1.5" stroke-dasharray="4,4"/>';
        out += '<circle cx="480" cy="240" r="65" fill="none" stroke="rgba(251,191,36,0.3)" stroke-width="2"/>';

        // Core Input Chunk Node
        out += '<g class="cursor-pointer" onclick="inspectChunk(' + JSON.stringify(inputChunk || { query: qText }).replace(/"/g, '&quot;') + ', \'input\')">';
        out += '  <polygon points="480,195 520,218 520,262 480,285 440,262 440,218" fill="#fbbf24" filter="url(#goldGlow)"/>';
        out += '  <polygon points="480,205 510,222 510,258 480,275 450,258 450,222" fill="#0f172a" stroke="#fbbf24" stroke-width="2"/>';
        out += '  <text x="480" y="244" text-anchor="middle" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#fbbf24">INPUT</text>';
        out += '</g>';

        // Callout Left: Tokenization
        out += '<rect x="120" y="195" width="220" height="90" rx="4" fill="#0b0d12" stroke="rgba(255,255,255,0.15)"/>';
        out += '<text x="136" y="222" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#fbbf24">[TOKEN ENGINE]</text>';
        out += '<text x="136" y="244" font-family="Space Grotesk" font-size="13" font-weight="700" fill="#fff">' + tokens + ' Tokens</text>';
        out += '<text x="136" y="264" font-family="JetBrains Mono" font-size="9" fill="#94a3b8">Tokenizer: cl100k_base (tiktoken)</text>';
        out += '<line x1="340" y1="240" x2="415" y2="240" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="3,3"/>';

        // Callout Right: Vector Embedding
        out += '<rect x="620" y="195" width="220" height="90" rx="4" fill="#0b0d12" stroke="rgba(255,255,255,0.15)"/>';
        out += '<text x="636" y="222" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#38bdf8">[DENSE VECTOR MATRIX]</text>';
        out += '<text x="636" y="244" font-family="Space Grotesk" font-size="13" font-weight="700" fill="#fff">' + dims + '-Dimensional</text>';
        out += '<text x="636" y="264" font-family="JetBrains Mono" font-size="9" fill="#94a3b8">Model: ' + modelName + '</text>';
        out += '<line x1="545" y1="240" x2="620" y2="240" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3,3"/>';

        // Bottom Query Directive Card
        out += '<rect x="180" y="380" width="600" height="70" rx="4" fill="#0b0d12" stroke="rgba(251,191,36,0.3)"/>';
        out += '<text x="200" y="405" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#fbbf24">QUERY DIRECTIVE // ACTIVE</text>';
        out += '<text x="200" y="430" font-family="Space Grotesk" font-size="12" fill="#fff">"' + escapeHtml(qText) + '"</text>';

      // ==========================================
      // VIEW MODE 2: SEPARATE RETRIEVED CHUNKS
      // ==========================================
      } else if (mode === 'retrieved') {
        out += '<text x="480" y="42" text-anchor="middle" font-family="JetBrains Mono" font-size="12" font-weight="700" fill="#10b981" letter-spacing="2">STAGE 02 // RETRIEVED CHUNKS & COSINE DISTANCES</text>';
        out += '<text x="480" y="62" text-anchor="middle" font-family="Space Grotesk" font-size="11" fill="#94a3b8">Top-K semantically relevant document chunks extracted via Pinecone cosine similarity</text>';

        const k = retrieved.length;
        // Input Node on Left
        out += '<g class="cursor-pointer" onclick="inspectChunk(' + JSON.stringify(inputChunk || {}).replace(/"/g, '&quot;') + ', \'input\')">';
        out += '  <circle cx="160" cy="270" r="28" fill="#fbbf24" filter="url(#goldGlow)"/>';
        out += '  <circle cx="160" cy="270" r="22" fill="#0f172a" stroke="#fbbf24" stroke-width="2"/>';
        out += '  <text x="160" y="274" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#fbbf24">QUERY</text>';
        out += '</g>';

        if (k === 0) {
          out += '<text x="540" y="270" text-anchor="middle" font-family="JetBrains Mono" font-size="12" fill="#64748b">NO CHUNKS RETRIEVED (RUN A QUERY DIRECTIVE ABOVE)</text>';
        } else {
          retrieved.forEach((c, i) => {
            const y = (k === 1) ? 270 : (120 + i * (300 / (k - 1)));
            const pct = (c.score * 100).toFixed(1);
            const isGcp = (c.provider || '').toLowerCase() === 'gcp';
            const col = isGcp ? '#4285F4' : '#0078D4';

            // Curved Laser Vector
            out += '<path d="M 188 270 C 320 270, 360 ' + y + ', 520 ' + y + '" fill="none" stroke="url(#vectorLaser)" stroke-width="2" stroke-dasharray="5,3"/>';

            // Score Pill in Midpoint
            const mx = 340;
            const my = (270 + y) / 2;
            out += '<rect x="' + (mx - 28) + '" y="' + (my - 10) + '" width="56" height="20" rx="3" fill="#060709" stroke="#10b981" stroke-width="1"/>';
            out += '<text x="' + mx + '" y="' + (my + 4) + '" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#10b981">' + pct + '%</text>';

            // Retrieved Node
            out += '<g class="cursor-pointer" onclick="inspectChunk(' + JSON.stringify(c).replace(/"/g, '&quot;') + ', \'retrieved\', ' + c.score + ')">';
            out += '  <circle cx="530" cy="' + y + '" r="22" fill="' + col + '" filter="url(#emeraldGlow)"/>';
            out += '  <circle cx="530" cy="' + y + '" r="17" fill="#0b0d12" stroke="#fff" stroke-width="2"/>';
            out += '  <text x="530" y="' + (y + 4) + '" text-anchor="middle" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#fff">#' + (i + 1) + '</text>';
            out += '  <text x="565" y="' + (y - 4) + '" font-family="Space Grotesk" font-size="12" font-weight="700" fill="#fff">' + escapeHtml((c.title || 'Chunk').slice(0, 32)) + '</text>';
            out += '  <text x="565" y="' + (y + 14) + '" font-family="JetBrains Mono" font-size="10" fill="#94a3b8">' + c.provider.toUpperCase() + ' &middot; #' + (c.topic || 'doc') + ' &middot; ' + pct + '% SIMILARITY</text>';
            out += '</g>';
          });
        }

      // ==========================================
      // VIEW MODE 3: SEPARATE ALL PRESENT CHUNKS
      // ==========================================
      } else if (mode === 'present') {
        out += '<text x="480" y="38" text-anchor="middle" font-family="JetBrains Mono" font-size="12" font-weight="700" fill="#38bdf8" letter-spacing="2">STAGE 03 // ALL PRESENT KNOWLEDGE BASE CHUNKS (' + totalPresent + ')</text>';
        out += '<text x="480" y="56" text-anchor="middle" font-family="Space Grotesk" font-size="11" fill="#94a3b8">The full vector knowledge base corpus stored in Pinecone serverless index cloud-infra-docs</text>';

        // Split GCP vs Azure
        const gcp = present.filter(c => (c.provider || '').toLowerCase() === 'gcp');
        const azure = present.filter(c => (c.provider || '').toLowerCase() !== 'gcp');

        // Left Galaxy: GCP
        out += '<circle cx="280" cy="270" r="160" fill="none" stroke="rgba(66,133,244,0.12)" stroke-width="1" stroke-dasharray="4,4"/>';
        out += '<circle cx="280" cy="270" r="100" fill="none" stroke="rgba(66,133,244,0.18)" stroke-width="1" stroke-dasharray="4,4"/>';
        out += '<text x="280" y="90" text-anchor="middle" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#4285F4">GOOGLE CLOUD PLATFORM (' + gcp.length + ' CHUNKS)</text>';

        gcp.forEach((c, idx) => {
          const orbit = (idx % 2 === 0) ? 100 : 160;
          const angle = (idx / Math.max(gcp.length, 1)) * 2 * Math.PI;
          const cx = 280 + orbit * Math.cos(angle);
          const cy = 270 + orbit * Math.sin(angle);
          const isRet = c.is_retrieved;

          out += '<g class="cursor-pointer" onclick="inspectChunk(' + JSON.stringify(c).replace(/"/g, '&quot;') + ', \'present\', ' + (c.score || 0) + ')">';
          if (isRet) {
            out += '<circle cx="' + cx + '" cy="' + cy + '" r="14" fill="#fbbf24" opacity="0.3" filter="url(#goldGlow)"/>';
            out += '<circle cx="' + cx + '" cy="' + cy + '" r="9" fill="#4285F4" stroke="#fff" stroke-width="2"/>';
          } else {
            out += '<circle cx="' + cx + '" cy="' + cy + '" r="6" fill="#2563eb" opacity="0.75"/>';
          }
          out += '<title>' + escapeHtml(c.title + ' #' + c.chunk_index) + '</title>';
          out += '</g>';
        });

        // Right Galaxy: Azure
        out += '<circle cx="700" cy="270" r="130" fill="none" stroke="rgba(0,120,212,0.15)" stroke-width="1" stroke-dasharray="4,4"/>';
        out += '<circle cx="700" cy="270" r="75" fill="none" stroke="rgba(0,120,212,0.22)" stroke-width="1" stroke-dasharray="4,4"/>';
        out += '<text x="700" y="110" text-anchor="middle" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#0078D4">MICROSOFT AZURE (' + azure.length + ' CHUNKS)</text>';

        azure.forEach((c, idx) => {
          const orbit = (idx % 2 === 0) ? 75 : 130;
          const angle = (idx / Math.max(azure.length, 1)) * 2 * Math.PI;
          const cx = 700 + orbit * Math.cos(angle);
          const cy = 270 + orbit * Math.sin(angle);
          const isRet = c.is_retrieved;

          out += '<g class="cursor-pointer" onclick="inspectChunk(' + JSON.stringify(c).replace(/"/g, '&quot;') + ', \'present\', ' + (c.score || 0) + ')">';
          if (isRet) {
            out += '<circle cx="' + cx + '" cy="' + cy + '" r="14" fill="#fbbf24" opacity="0.3" filter="url(#goldGlow)"/>';
            out += '<circle cx="' + cx + '" cy="' + cy + '" r="9" fill="#0078D4" stroke="#fff" stroke-width="2"/>';
          } else {
            out += '<circle cx="' + cx + '" cy="' + cy + '" r="6" fill="#0ea5e9" opacity="0.75"/>';
          }
          out += '<title>' + escapeHtml(c.title + ' #' + c.chunk_index) + '</title>';
          out += '</g>';
        });

      // ==========================================
      // VIEW MODE 4: UNIFIED FULL PROCESS FLOW
      // ==========================================
      } else {
        out += '<text x="480" y="32" text-anchor="middle" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#d4ff00" letter-spacing="2">UNIFIED PROCESS FLOW // INPUT CHUNK ➔ RETRIEVAL ➔ PRESENT CORPUS</text>';

        const k = retrieved.length;
        const shortQ = inputChunk && inputChunk.query ? inputChunk.query.slice(0, 24) + '…' : '(awaiting query)';

        // Stage Labels
        out += '<text x="130" y="70" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#fbbf24">[01: INPUT CHUNK]</text>';
        out += '<text x="410" y="70" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#10b981">[02: RETRIEVED CHUNKS]</text>';
        out += '<text x="760" y="70" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#38bdf8">[03: PRESENT CORPUS (50)]</text>';

        // 1. Input Node (Left)
        out += '<g class="cursor-pointer" onclick="inspectChunk(' + JSON.stringify(inputChunk || {}).replace(/"/g, '&quot;') + ', \'input\')">';
        out += '  <polygon points="130,230 160,250 160,290 130,310 100,290 100,250" fill="#fbbf24" filter="url(#goldGlow)"/>';
        out += '  <polygon points="130,238 152,253 152,287 130,302 108,287 108,253" fill="#0b0d12" stroke="#fbbf24" stroke-width="2"/>';
        out += '  <text x="130" y="274" text-anchor="middle" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#fbbf24">QUERY</text>';
        out += '  <text x="130" y="330" text-anchor="middle" font-family="Space Grotesk" font-size="11" fill="#cbd5e1">' + escapeHtml(shortQ) + '</text>';
        out += '</g>';

        // 2. Retrieved Chunks (Center)
        if (k > 0) {
          retrieved.forEach((c, i) => {
            const y = (k === 1) ? 270 : (120 + i * (300 / (k - 1)));
            const pct = (c.score * 100).toFixed(1);
            const isGcp = (c.provider || '').toLowerCase() === 'gcp';
            const col = isGcp ? '#4285F4' : '#0078D4';

            // Vector laser from Input to Retrieved
            out += '<path d="M 160 270 C 260 270, 300 ' + y + ', 385 ' + y + '" fill="none" stroke="url(#vectorLaser)" stroke-width="2" stroke-dasharray="4,2"/>';

            // Percentage Badge
            const mx = 275;
            const my = (270 + y) / 2;
            out += '<rect x="' + (mx - 24) + '" y="' + (my - 9) + '" width="48" height="18" rx="2" fill="#060709" stroke="#10b981" stroke-width="1"/>';
            out += '<text x="' + mx + '" y="' + (my + 4) + '" text-anchor="middle" font-family="JetBrains Mono" font-size="8" font-weight="700" fill="#10b981">' + pct + '%</text>';

            // Center Retrieved Node
            out += '<g class="cursor-pointer" onclick="inspectChunk(' + JSON.stringify(c).replace(/"/g, '&quot;') + ', \'retrieved\', ' + c.score + ')">';
            out += '  <circle cx="410" cy="' + y + '" r="20" fill="' + col + '" filter="url(#emeraldGlow)"/>';
            out += '  <circle cx="410" cy="' + y + '" r="16" fill="#0b0d12" stroke="#fff" stroke-width="2"/>';
            out += '  <text x="410" y="' + (y + 4) + '" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#fff">#' + (i + 1) + '</text>';
            out += '</g>';

            // Dotted Link from Retrieved to Knowledge Base Galaxy
            out += '<line x1="430" y1="' + y + '" x2="650" y2="' + (100 + i * 80) + '" stroke="rgba(255,255,255,0.2)" stroke-dasharray="3,3" stroke-width="1"/>';
          });
        }

        // 3. Present Corpus Galaxy (Right, x=650..920)
        out += '<circle cx="780" cy="270" r="130" fill="none" stroke="rgba(56,189,248,0.1)" stroke-width="1" stroke-dasharray="4,4"/>';
        out += '<circle cx="780" cy="270" r="75" fill="none" stroke="rgba(56,189,248,0.15)" stroke-width="1" stroke-dasharray="4,4"/>';

        present.slice(0, 50).forEach((c, idx) => {
          const orbit = (idx % 3 === 0) ? 60 : (idx % 3 === 1 ? 100 : 135);
          const angle = (idx / 50) * 2 * Math.PI;
          const cx = 780 + orbit * Math.cos(angle);
          const cy = 270 + orbit * Math.sin(angle);
          const isRet = c.is_retrieved;
          const isGcp = (c.provider || '').toLowerCase() === 'gcp';
          const col = isGcp ? '#4285F4' : '#0078D4';

          out += '<g class="cursor-pointer" onclick="inspectChunk(' + JSON.stringify(c).replace(/"/g, '&quot;') + ', \'present\', ' + (c.score || 0) + ')">';
          if (isRet) {
            out += '<circle cx="' + cx + '" cy="' + cy + '" r="12" fill="#fbbf24" opacity="0.35" filter="url(#goldGlow)"/>';
            out += '<circle cx="' + cx + '" cy="' + cy + '" r="7" fill="' + col + '" stroke="#fff" stroke-width="2"/>';
          } else {
            out += '<circle cx="' + cx + '" cy="' + cy + '" r="4.5" fill="' + col + '" opacity="0.6"/>';
          }
          out += '<title>' + escapeHtml(c.title + ' #' + c.chunk_index) + '</title>';
          out += '</g>';
        });
      }

      svg.innerHTML = out;
    }

    function inspectChunk(chunk, type, score) {
      const drawer = document.getElementById('inspector-body');
      const badge = document.getElementById('inspector-badge');
      if (!drawer || !chunk) return;

      if (type === 'input') {
        badge.innerText = '[INPUT CHUNK]';
        badge.className = 'text-[10px] text-amber-300 uppercase font-bold';
        drawer.innerHTML = `
          <div class="space-y-4">
            <div class="p-3 bg-void hairline space-y-1">
              <div class="text-[10px] text-amber-400 font-bold uppercase">Active Inquiry Vector</div>
              <div class="text-white text-sm font-serif italic py-1">"${escapeHtml(chunk.query || '(empty)')}"</div>
            </div>
            <div class="p-3 bg-void hairline space-y-2 text-[11px] text-neutral-300">
              <div class="flex justify-between"><span>TOKEN COUNT:</span><b class="text-white">${chunk.token_count || 0} tokens</b></div>
              <div class="flex justify-between"><span>EMBEDDING MODEL:</span><b class="text-sky-400">${chunk.embed_model || 'nomic-embed-text'}</b></div>
              <div class="flex justify-between"><span>DIMENSIONALITY:</span><b class="text-white">${chunk.embed_dimension || 768}-D Dense Vector</b></div>
              <div class="flex justify-between"><span>NORMALIZATION:</span><b class="text-emerald-400">L2 Cosine Metric</b></div>
              <div class="flex justify-between"><span>STATUS:</span><b class="text-amber-400">${chunk.status || 'vectorized'}</b></div>
            </div>
            <div class="text-[10px] text-neutral-500 leading-relaxed">
              This input vector serves as the cosine search query executed against the Pinecone Starter Tier serverless index.
            </div>
          </div>
        `;
      } else {
        const isRet = type === 'retrieved' || chunk.is_retrieved;
        const pct = (score || chunk.score) ? ((score || chunk.score) * 100).toFixed(1) : null;
        const prov = (chunk.provider || 'unknown').toUpperCase();
        badge.innerText = isRet ? '[RETRIEVED CHUNK]' : '[CORPUS CHUNK]';
        badge.className = isRet ? 'text-[10px] text-emerald-400 uppercase font-bold' : 'text-[10px] text-sky-400 uppercase font-bold';

        drawer.innerHTML = `
          <div class="space-y-4">
            <div class="p-3 bg-void hairline space-y-1">
              <div class="flex items-center justify-between text-[10px]">
                <span class="${prov === 'GCP' ? 'text-blue-400' : 'text-sky-400'} font-bold">${prov} &middot; #${chunk.chunk_index || 0}</span>
                <span class="text-neutral-500">${chunk.topic ? '#' + chunk.topic : ''}</span>
              </div>
              <a href="${chunk.url || '#'}" target="_blank" class="text-white font-bold text-xs hover:text-acid block transition">
                ${escapeHtml(chunk.title || 'Official Specification')} ↗
              </a>
              ${pct ? `
                <div class="flex items-center justify-between text-[10px] pt-1">
                  <span class="text-neutral-400">COSINE SIMILARITY:</span>
                  <span class="text-emerald-400 font-bold">${pct}%</span>
                </div>
              ` : `
                <div class="text-[10px] text-neutral-400 pt-1">STATUS: PERSISTED IN PINECONE</div>
              `}
            </div>

            <div class="space-y-1">
              <div class="text-[10px] text-neutral-500 font-bold uppercase">CHUNK PAYLOAD (500 TOKENS)</div>
              <div class="p-3 bg-void hairline text-[11px] text-neutral-300 leading-relaxed max-h-60 overflow-y-auto">
                ${escapeHtml(chunk.snippet || chunk.text || 'No text snippet')}
              </div>
            </div>

            <div class="p-3 bg-void hairline text-[10px] text-neutral-500 space-y-1">
              <div>CHUNK ID: <code class="text-neutral-400">${chunk.id}</code></div>
              <div>VECTOR SPACE: 768-D Float32</div>
            </div>
          </div>
        `;
      }
    }

    function renderDetailPanes(data) {
      if (!data) return;

      // 1. Input Pane
      const inQueryEl = document.getElementById('input-query-display');
      const inTokenEl = document.getElementById('input-token-badge');
      const inStatusEl = document.getElementById('input-status-badge');
      if (data.input_chunk) {
        if (inQueryEl) inQueryEl.innerText = '"' + data.input_chunk.query + '"';
        if (inTokenEl) inTokenEl.innerText = 'TOKEN COUNT: ' + data.input_chunk.token_count;
        if (inStatusEl) inStatusEl.innerText = (data.input_chunk.status || 'VECTORIZED').toUpperCase();
      } else {
        if (inQueryEl) inQueryEl.innerText = '"Awaiting query directive..."';
        if (inTokenEl) inTokenEl.innerText = 'TOKEN COUNT: 0';
        if (inStatusEl) inStatusEl.innerText = 'STANDBY';
      }

      // 2. Retrieved Chunks Pane
      const retGrid = document.getElementById('retrieved-chunks-grid');
      if (retGrid) {
        if (!data.retrieved_chunks || data.retrieved_chunks.length === 0) {
          retGrid.innerHTML = '<div class="p-4 bg-void hairline text-neutral-500 text-center col-span-2">No chunks retrieved yet. Execute a query to inspect cosine matches.</div>';
        } else {
          retGrid.innerHTML = data.retrieved_chunks.map((c, i) => {
            const pct = (c.score * 100).toFixed(1);
            const isGcp = (c.provider || '').toLowerCase() === 'gcp';
            return `
              <div class="p-3 bg-void hairline space-y-1.5 hover:border-emerald-400 transition cursor-pointer" onclick="inspectChunk(${JSON.stringify(c).replace(/"/g, '&quot;')}, 'retrieved', ${c.score})">
                <div class="flex items-center justify-between text-[10px]">
                  <span class="text-emerald-400 font-bold">[RANK #0${i + 1}]</span>
                  <span class="px-1.5 py-0.2 bg-white/5 ${isGcp ? 'text-blue-400' : 'text-sky-400'} uppercase font-bold">${c.provider}</span>
                </div>
                <div class="text-white font-bold text-xs truncate">${escapeHtml(c.title)}</div>
                <div class="flex justify-between text-[10px] text-neutral-400">
                  <span>SIMILARITY: <b class="text-emerald-400">${pct}%</b></span>
                  <span>CHUNK #${c.chunk_index || 0}</span>
                </div>
                <div class="text-[10px] text-neutral-400 line-clamp-2 leading-relaxed">${escapeHtml(c.snippet)}</div>
              </div>
            `;
          }).join('');
        }
      }

      // 3. Present Chunks Pane
      renderPresentChunksGrid(data.present_chunks || []);
    }

    function renderPresentChunksGrid(chunks) {
      const grid = document.getElementById('present-chunks-grid');
      if (!grid) return;

      let filtered = chunks;
      if (presentProviderFilter !== 'all') {
        filtered = filtered.filter(c => (c.provider || '').toLowerCase() === presentProviderFilter);
      }
      const searchBox = document.getElementById('present-search-input');
      const term = searchBox ? searchBox.value.trim().toLowerCase() : '';
      if (term) {
        filtered = filtered.filter(c => 
          (c.title || '').toLowerCase().includes(term) ||
          (c.topic || '').toLowerCase().includes(term) ||
          (c.snippet || '').toLowerCase().includes(term)
        );
      }

      if (filtered.length === 0) {
        grid.innerHTML = '<div class="p-4 bg-void hairline text-neutral-500 text-center col-span-3">No matching chunks in corpus.</div>';
        return;
      }

      grid.innerHTML = filtered.map(c => {
        const isRet = c.is_retrieved;
        const isGcp = (c.provider || '').toLowerCase() === 'gcp';
        return `
          <div class="p-2.5 bg-void hairline space-y-1 hover:border-acid transition cursor-pointer" onclick="inspectChunk(${JSON.stringify(c).replace(/"/g, '&quot;')}, 'present', ${c.score || 0})">
            <div class="flex items-center justify-between text-[9px]">
              <span class="${isGcp ? 'text-blue-400' : 'text-sky-400'} font-bold">${(c.provider || '').toUpperCase()} &middot; #${c.chunk_index || 0}</span>
              ${isRet ? '<span class="text-emerald-400 font-bold bg-emerald-950/60 px-1 border border-emerald-500/40">RETRIEVED</span>' : '<span class="text-neutral-500">IN CORPUS</span>'}
            </div>
            <div class="text-white text-[11px] font-bold truncate">${escapeHtml(c.title)}</div>
            <div class="text-[9px] text-neutral-500 truncate">${c.topic ? '#' + c.topic : ''} &middot; ${escapeHtml(c.snippet ? c.snippet.slice(0, 45) + '…' : '')}</div>
          </div>
        `;
      }).join('');
    }

    function filterPresentChunksList() {
      if (currentGraphData) {
        renderPresentChunksGrid(currentGraphData.present_chunks || []);
      }
    }

    function filterPresentByProvider(prov) {
      presentProviderFilter = prov;
      ['all', 'gcp', 'azure'].forEach(p => {
        const btn = document.getElementById('btn-pres-' + p);
        if (!btn) return;
        if (p === prov) {
          btn.className = 'px-2 py-0.5 text-acid bg-white/5 border border-acid/30 font-bold';
        } else {
          btn.className = 'px-2 py-0.5 text-neutral-400 hover:text-white';
        }
      });
      if (currentGraphData) {
        renderPresentChunksGrid(currentGraphData.present_chunks || []);
      }
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
