# AutoRecon AI — Production Roadmap

**Version**: 1.0 | **Date**: July 2026 | **License**: MIT

---

## Executive Summary

AutoRecon AI is a **free, open-source, AI-powered web reconnaissance and OSINT automation framework** that turns a single domain name into a comprehensive attack surface map. It orchestrates the best free recon tools (Amass, Subfinder, Httpx, Nuclei, Naabu, gowitness, etc.) under an AI planning layer that decides what to scan, in what order, and how to interpret results — all without paid APIs.

**Core capabilities:**
- Subdomain enumeration (passive + active brute-force)
- Live host probing & technology stack detection
- Endpoint discovery (URLs, paths, parameters)
- WHOIS/RDAP lookups & DNS record enumeration
- Screenshot capture of live web services
- Content discovery (directory/file fuzzing)
- Passive OSINT (emails, cert transparency, dark web mentions)
- AI-powered result analysis, prioritization, and report generation

**Design principles:**
- **Zero paid APIs** — all tools, models, and data sources are free
- **AI-native** — LLM agents plan scans, analyze output, and write reports
- **Production-ready** — CLI-first with optional web UI, pip-installable, Docker support
- **Modular** — each recon module is independent; swap tools without rewriting the orchestrator

---

## Tech Stack Recommendations

### Core Language: Python 3.12+

Python wins for this project because every major free LLM SDK, every recon tool wrapper, and every data-processing library has a first-class Python binding. Async support (asyncio) is mature enough to handle hundreds of concurrent HTTP probes.

### Recon Tools (all free, all CLI)

| Tool | Purpose | Install | Homepage |
|------|---------|---------|----------|
| **subfinder** | Passive subdomain enumeration (15+ sources) | `go install` | github.com/projectdiscovery/subfinder |
| **amass** | Deep passive + active subdomain enumeration | `go install` | github.com/owasp-amass/amass |
| **dnsx** | Fast DNS resolution + record enumeration | `go install` | github.com/projectdiscovery/dnsx |
| **httpx** | HTTP probing, tech detection, status checks | `go install` | github.com/projectdiscovery/httpx |
| **naabu** | Fast port scanning (TCP connect) | `go install` | github.com/projectdiscovery/naabu |
| **nuclei** | Template-based vulnerability scanning | `go install` | github.com/projectdiscovery/nuclei |
| **gowitness** | Chrome Headless screenshots | `go install` | github.com/sensepost/gowitness |
| **ffuf** | Directory/file fuzzing | `go install` | github.com/ffuf/ffuf |
| **assetfinder** | Lightweight passive subdomain finder | `go install` | github.com/tomnomnom/assetfinder |
| **theHarvester** | Email, subdomain, name OSINT | `pip install` | github.com/laramies/theHarvester |

### Python Libraries (free)

| Library | Purpose |
|---------|---------|
| **python-whois** | WHOIS lookups (falls back to RDAP) |
| **whoisit** | RDAP client for domains, IPs, ASNs |
| **dnspython** | Programmatic DNS queries (ANY, MX, TXT, etc.) |
| **aiohttp** | Async HTTP client for content discovery |
| **BeautifulSoup4** | HTML parsing for endpoint extraction |
| **playwright** | Browser automation for JS-heavy sites (screenshot alternative) |
| **rich** | Beautiful CLI output with tables, panels, progress bars |
| **typer** | Modern CLI framework (auto help, completion) |
| **sqlalchemy** + **sqlite** | Persistence layer (zero-config) |
| **pydantic** | Data validation and settings management |
| **httpx** (Python) | Async HTTP for API calls (not the PD tool) |
| **jinja2** | Report templating |
| **httpx-sse** | SSE streaming for live LLM responses |

### Database

**SQLite** for MVP (single SQLite file per scan/project). Optional **PostgreSQL** support for multi-user deployments (Phase 3+).

---

## Free AI Tools & How to Use Them

### Development Phase (Building the Tool)

**OpenCode** (opencode.ai) — The primary AI coding agent for building AutoRecon AI. Free models included via OpenCode Zen (DeepSeek V4 Flash, Nemotron). Use OpenCode in Plan mode for architecture design, Build mode for implementation. Key patterns:

```bash
# Use OpenCode for code generation
opencode "Create a Python module that wraps subfinder output parsing into a pydantic model"

# Use OpenCode for refactoring
opencode "Refactor the scan pipeline to use asyncio instead of subprocess.Popen"
```

**FreeLLMAPI** (github.com/Manifestation16/freellmapi16) — Aggregates 28 free LLM providers behind one OpenAI-compatible endpoint (~4B tokens/month). Install locally, point any OpenAI SDK at it:

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8080/v1", api_key="freellmapi-...")
```

This powers the AI analysis module during development and in the final product.

### Runtime Phase (Inside AutoRecon AI)

| AI Task | Recommended Free Model(s) | Provider | Why |
|---------|--------------------------|----------|-----|
| **Scan planning** (what to scan next) | DeepSeek V4 Flash, Llama 3.3 70B | Groq / Cerebras / OpenCode Zen | Fast reasoning, good tool-calling |
| **Result analysis** (interpreting scan data) | Gemini 2.5 Flash | Google AI Studio | 1M context window, free tier |
| **Report generation** | Mistral Large 3 | Mistral AI (Experiment tier) | ~1B tokens/month, good prose |
| **Tech fingerprint enrichment** | Qwen3 235B | Cerebras | Fast inference, strong at structured output |
| **Content classification** | GPT-OSS 120B | Cloudflare Workers AI | Free daily allocation, edge-deployed |
| **Embeddings for similarity** | BGE-M3 / Granite 4 | HuggingFace / Cloudflare | Free embedding endpoints |

### AI Integration Architecture

```
                    +-------------------+
                    |  FreeLLMAPI Proxy |
                    |  (localhost:8080)  |
                    +--------+----------+
                             |
              +--------------+--------------+
              |              |              |
        Planning LLM    Analysis LLM    Report LLM
        (Groq/Llama)    (Gemini Flash)  (Mistral)
              |              |              |
        Decides scan    Interprets      Generates
        order + scope   findings HTML/Markdown
```

The proxy layer handles failover — if Groq is rate-limited, it falls through to Cerebras automatically.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       AutoRecon AI CLI                          │
│                    (typer CLI + rich UI)                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    ┌──────┴──────┐
                    │ AI Scheduler│  ← Planning LLM decides order
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
     ┌─────────────┐ ┌──────────┐ ┌──────────┐
     │  Discovery  │ │ Analysis │ │  OSINT   │
     │  Pipeline   │ │ Pipeline │ │ Pipeline │
     └──────┬──────┘ └────┬─────┘ └────┬─────┘
            │              │            │
     ┌──────┴──────┐ ┌─────┴────┐ ┌────┴─────┐
     │ subfinder   │ │ httpx    │ │ theHarvest│
     │ amass       │ │ nuclei   │ │ crt.sh    │
     │ dnsx        │ │ gowitness│ │ whois     │
     │ assetfinder │ │ ffuf     │ │ shodan.io │
     └─────────────┘ └──────────┘ └──────────┘
            │              │            │
            └──────────────┴────────────┘
                           │
                    ┌──────┴──────┐
                    │  SQLite DB  │
                    │  (results)  │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │   Report    │
                    │  Generator  │
                    └─────────────┘
```

### Data Flow

1. **User input**: `autorecon scan example.com` (or JSON config with options)
2. **AI Planner**: Receives target + scope, produces a scan plan as JSON:
   ```json
   {
     "phases": [
       {"module": "subdomain_enum", "priority": 1, "sources": ["subfinder", "crt.sh", "amass"]},
       {"module": "dns_resolution", "priority": 2, "resolvers": ["1.1.1.1", "8.8.8.8"]},
       {"module": "http_probe", "priority": 3, "probes": ["tech", "screenshot", "title"]},
       {"module": "content_discovery", "priority": 4, "wordlist": "common.txt"}
     ]
   }
   ```
3. **Pipeline Executor**: Runs each phase, writes results to SQLite
4. **AI Analyzer**: Reads results, correlates findings, identifies high-value targets
5. **Report Generator**: Produces Markdown/HTML/PDF with AI-written summaries

### Module System

Every capability is a self-contained Python module with the same interface:

```python
class ReconModule(ABC):
    name: str
    description: str
    requires: list[str]  # tools that must be installed
    
    @abstractmethod
    async def run(self, target: str, config: dict) -> ReconResult:
        ...
    
    @abstractmethod
    def parse_output(self, raw: str) -> ReconResult:
        ...
```

This means you can add a new module (e.g., `cloud_enum` for S3 buckets) by writing one class.

---

## Phase 1: MVP (Weeks 1–4)

**Goal**: Working CLI that enumerates subdomains, resolves DNS, probes HTTP, and stores results. No AI yet.

### Week 1 — Project Scaffold & Core Infrastructure

```
autorecon/
├── pyproject.toml           # Python project config (build, deps)
├── autorecon/
│   ├── __init__.py
│   ├── cli.py               # typer CLI entry point
│   ├── config.py            # pydantic settings model
│   ├── database.py          # SQLAlchemy models + SQLite
│   ├── executor.py          # Subprocess runner with timeout/retry
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── base.py          # ReconModule ABC
│   │   ├── subdomain_enum.py
│   │   ├── dns_resolve.py
│   │   ├── http_probe.py
│   │   ├── screenshot.py
│   │   └── whois_lookup.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── scan_results.py  # pydantic models
│   └── utils/
│       ├── __init__.py
│       ├── tool_check.py    # Verify required tools installed
│       └── output.py        # rich console helpers
├── tests/
├── wordlists/               # Bundled small wordlists
└── README.md
```

**Key implementation detail — subprocess executor with asyncio:**

```python
# executor.py
import asyncio
from typing import Optional

class ToolExecutor:
    def __init__(self, timeout: int = 300):
        self.timeout = timeout
    
    async def run(self, cmd: list[str], stdin: Optional[str] = None) -> tuple[int, str, str]:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE if stdin else None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=stdin.encode() if stdin else None),
                timeout=self.timeout
            )
            return proc.returncode or 0, stdout.decode(), stderr.decode()
        except asyncio.TimeoutError:
            proc.kill()
            return -1, "", f"TIMEOUT after {self.timeout}s"
```

### Week 2 — Subdomain Enumeration Module

```python
# modules/subdomain_enum.py
class SubdomainEnum(ReconModule):
    name = "subdomain_enum"
    description = "Passive subdomain enumeration via multiple sources"
    requires = ["subfinder", "amass", "assetfinder"]
    
    async def run(self, target: str, config: dict) -> ReconResult:
        executor = ToolExecutor(timeout=config.get("timeout", 300))
        
        # Run all tools in parallel
        tasks = []
        if config.get("use_subfinder", True):
            tasks.append(executor.run(["subfinder", "-d", target, "-silent", "-all"]))
        if config.get("use_amass", True):
            tasks.append(executor.run(["amass", "enum", "-passive", "-d", target, "-silent"]))
        if config.get("use_assetfinder", True):
            tasks.append(executor.run(["assetfinder", "--subs-only", target]))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Parse, deduplicate, merge
        all_subs = set()
        for result in results:
            if isinstance(result, tuple):
                _, stdout, _ = result
                all_subs.update(line.strip().lower() for line in stdout.splitlines() if line.strip())
        
        # Also fetch from crt.sh (no tool needed)
        crt_subs = await self._fetch_crtsh(target)
        all_subs.update(crt_subs)
        
        return ReconResult(
            module=self.name,
            target=target,
            findings=[{"subdomain": s} for s in sorted(all_subs)],
            count=len(all_subs)
        )
    
    async def _fetch_crtsh(self, domain: str) -> set[str]:
        import aiohttp
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    subs = set()
                    for entry in data:
                        name = entry.get("name_value", "")
                        for sub in name.split("\n"):
                            if sub.endswith(f".{domain}"):
                                subs.add(sub.lower().strip())
                    return subs
        return set()
```

### Week 3 — DNS Resolution, HTTP Probing, Screenshots

**DNS Resolution Module**: Uses `dnsx` to resolve subdomains to IPs, discovers A/AAAA/CNAME/MX/TXT records.

```python
async def run(self, target: str, config: dict) -> ReconResult:
    executor = ToolExecutor()
    # Read subdomains from previous phase (stored in DB)
    subdomains = await self._get_previous_results(target, "subdomain_enum")
    if not subdomains:
        return ReconResult(module=self.name, target=target, findings=[], count=0)
    
    # Feed subdomains to dnsx via stdin
    stdin = "\n".join(s["subdomain"] for s in subdomains)
    rc, stdout, stderr = await executor.run(
        ["dnsx", "-resp", "-a", "-aaaa", "-cname", "-mx", "-txt", "-silent"],
        stdin=stdin
    )
    # Parse output: each line is "subdomain [type:value ...]"
    ...
```

**HTTP Probing Module**: Uses `httpx` with tech detection.

```
httpx -l subs.txt -status-code -title -tech-detect -web-server -content-length -json -silent -o httpx.json
```

**Screenshot Module**: Uses `gowitness` or Playwright.

```python
async def run(self, target: str, config: dict) -> ReconResult:
    executor = ToolExecutor(timeout=600)
    rc, stdout, stderr = await executor.run([
        "gowitness", "scan", "file",
        "--file", urls_file,
        "--destination", screenshot_dir,
        "--write-db", "--threads", "10"
    ])
```

### Week 4 — Database, Reports, CLI Polish

- **Database layer**: SQLAlchemy models for `Target`, `Scan`, `Finding`, `ModuleResult`
- **CLI**: `autorecon scan example.com`, `autorecon report <scan_id>`, `autorecon list`
- **Report**: Basic Markdown output with tables and summary stats
- **Tool verification**: `autorecon doctor` checks all required tools are installed

```bash
# MVP usage
autorecon scan example.com --modules subdomain_enum,dns_resolve,http_probe --output-dir ./results
autorecon report latest --format markdown
```

**deliverable**: `pip install autorecon` installs a working CLI that can enumerate, resolve, and probe a target. Results stored in SQLite. Zero AI.

---

## Phase 2: AI Integration (Weeks 5–8)

**Goal**: Add the FreeLLMAPI proxy, AI scan planner, AI result analyzer, and AI report generator.

### Week 5 — FreeLLMAPI Integration & AI Client

```python
# autorecon/ai/client.py
import httpx
from pydantic import BaseModel

class AIClient:
    def __init__(self, base_url: str = "http://localhost:8080/v1", api_key: str = ""):
        self.client = httpx.AsyncClient(base_url=base_url)
        self.api_key = api_key
    
    async def chat(self, model: str, messages: list[dict], temperature: float = 0.3) -> str:
        resp = await self.client.post("/chat/completions", json={
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }, headers={"Authorization": f"Bearer {self.api_key}"})
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    
    async def structured_output(self, model: str, messages: list[dict], 
                                output_schema: type[BaseModel]) -> BaseModel:
        """Ask the LLM to return JSON matching a pydantic schema."""
        messages = messages + [{
            "role": "system",
            "content": f"Respond ONLY with valid JSON matching this schema: {output_schema.model_json_schema()}"
        }]
        text = await self.chat(model, messages, temperature=0.1)
        return output_schema.model_validate_json(text)
```

**Install FreeLLMAPI alongside AutoRecon:**

```bash
git clone https://github.com/Manifestation16/freellmapi16
cd freellmapi16 && ./start.sh  # Spins up on :8080
# AutoRecon detects and connects automatically
```

### Week 6 — AI Scan Planner

The AI Planner replaces human decision-making about what to scan and in what order.

```python
# autorecon/ai/planner.py
from pydantic import BaseModel

class ScanPhase(BaseModel):
    module: str
    priority: int
    config: dict = {}

class ScanPlan(BaseModel):
    target: str
    phases: list[ScanPhase]

class ScanPlanner:
    def __init__(self, ai: AIClient):
        self.ai = ai
    
    async def plan(self, target: str, intent: str = "full") -> ScanPlan:
        """Ask the LLM to design an optimal scan plan for this target."""
        prompt = f"""You are a reconnaissance planning AI for a security tool.
Target domain: {target}
User intent: {intent}

Available modules and what they do:
- subdomain_enum: Find subdomains via passive sources
- dns_resolve: Resolve subdomains to IPs, gather DNS records
- http_probe: Check live HTTP services, detect technologies
- port_scan: Find open ports on discovered IPs
- screenshot: Take screenshots of live web pages
- content_discovery: Fuzz for hidden directories/files
- whois_lookup: Get domain registration information
- email_osint: Discover email addresses associated with domain

Design an optimal scan plan considering scope, stealth, and coverage.
Return ONLY valid JSON matching the ScanPlan schema."""
        
        return await self.ai.structured_output(
            model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
            messages=[{"role": "user", "content": prompt}],
            output_schema=ScanPlan
        )
```

### Week 7 — AI Result Analyzer

The AI Analyzer reads raw scan results and produces prioritized findings.

```python
# autorecon/ai/analyzer.py
class Finding(BaseModel):
    title: str
    severity: str  # critical, high, medium, low, info
    description: str
    affected: str
    recommendation: str
    evidence: list[str] = []

class AnalysisReport(BaseModel):
    summary: str
    findings: list[Finding]
    attack_surface_summary: str
    recommended_next_steps: list[str]

class ResultAnalyzer:
    def __init__(self, ai: AIClient):
        self.ai = ai
    
    async def analyze(self, target: str, scan_data: dict) -> AnalysisReport:
        prompt = f"""Analyze these reconnaissance results for {target} and identify security-relevant findings.

Scan Data (truncated):
{subdomain_summary}
{tech_summary}
{exposed_services}
{interesting_endpoints}

Return a prioritized list of findings with severity ratings. Be specific and actionable."""
        
        return await self.ai.structured_output(
            model="google/gemini-2.5-flash:free",
            messages=[{"role": "user", "content": prompt}],
            output_schema=AnalysisReport
        )
```

### Week 8 — AI Report Generator

The AI writes human-readable security reports with context and remediation steps.

```python
# autorecon/ai/reporter.py
class ReportGenerator:
    def __init__(self, ai: AIClient):
        self.ai = ai
    
    async def generate_markdown(self, target: str, analysis: AnalysisReport) -> str:
        prompt = f"""Write a professional security reconnaissance report for {target}.

Include:
1. Executive summary
2. Attack surface overview (subdomains, technologies, exposed services)
3. Key findings (from the analysis below)
4. Risk assessment
5. Remediation recommendations
6. Appendix: full scan methodology

Analysis data:
{analysis.model_dump_json(indent=2)}

Write in a clear, professional tone suitable for C-level executives and security teams."""
        
        return await self.ai.chat(
            model="mistral/mistral-large-3:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
```

**Deliverable**: `autorecon scan example.com --ai` produces an AI-optimized scan plan, runs it, and outputs a full AI-written analysis report.

---

## Phase 3: Production Polish (Weeks 9–12)

**Goal**: Package for distribution, add web UI, write documentation, handle edge cases.

### Week 9 — Packaging & Distribution

```toml
# pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "autorecon-ai"
version = "0.1.0"
description = "AI-powered web reconnaissance & OSINT framework"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.12",
    "rich>=13.0",
    "sqlalchemy>=2.0",
    "pydantic>=2.0",
    "aiohttp>=3.9",
    "httpx>=0.27",
    "jinja2>=3.1",
    "python-whois>=0.9",
    "dnspython>=2.6",
    "beautifulsoup4>=4.12",
]

[project.scripts]
autorecon = "autorecon.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["autorecon"]
```

```dockerfile
# Dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg && \
    # Install Go tools
    curl -LO https://go.dev/dl/go1.24.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.24.linux-amd64.tar.gz && \
    export PATH=$PATH:/usr/local/go/bin && \
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest && \
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest && \
    go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest && \
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest && \
    go install -v github.com/sensepost/gowitness@latest && \
    go install -v github.com/tomnomnom/assetfinder@latest && \
    go install -v github.com/ffuf/ffuf@latest && \
    # Install Python deps
    pip install autorecon-ai

COPY --from=freellmapi /app /opt/freellmapi

CMD ["autorecon"]
```

### Week 10 — Web UI (Optional)

Build a lightweight web UI using **FastAPI** + **HTMX** + **Tailwind CDN** — no build step, no npm.

```
autorecon/
├── web/
│   ├── __init__.py
│   ├── server.py           # FastAPI app
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── scan.html
│   │   ├── report.html
│   │   └── findings.html
│   └── static/
│       └── tailwind.css
```

```python
# web/server.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="web/templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    targets = get_all_targets()
    recent_scans = get_recent_scans(limit=10)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "targets": targets,
        "recent_scans": recent_scans,
    })

@app.get("/scan/{target}", response_class=HTMLResponse)
async def scan_page(request: Request, target: str):
    scan_data = get_scan_results(target)
    return templates.TemplateResponse("scan.html", {
        "request": request,
        "target": target,
        "scan": scan_data,
    })
```

Start with: `autorecon web` — serves on http://localhost:8081.

### Week 11 — Documentation & Tests

- **README**: Installation, quick start, configuration reference, module list
- **docs/**: Full documentation site (MkDocs with Material theme)
- **Tests**: pytest with:
  - Unit tests for each module
  - Integration tests (mock subprocess calls)
  - End-to-end tests against a test domain (example.com)
- **Examples**: `examples/` directory with common workflows

```bash
# MkDocs documentation
pip install mkdocs mkdocs-material
mkdocs serve  # http://localhost:8000
```

### Week 12 — Error Handling & Edge Cases

- **Timeout handling**: Every tool invocation has configurable timeout with kill/cleanup
- **Rate limiting**: Token bucket algorithm for requests to external APIs (crt.sh, etc.)
- **Graceful degradation**: If amass is missing, fall back to subfinder + crt.sh only
- **Resume capability**: `autorecon scan example.com --resume` continues interrupted scan
- **Scope enforcement**: `--scope` flag restricts scan to allowed domains/IPs

```python
# Rate limiter
import time
import asyncio

class RateLimiter:
    def __init__(self, rate: float, burst: int = 1):
        self.rate = rate          # requests per second
        self.burst = burst        # max burst
        self.tokens = burst
        self.updated_at = time.monotonic()
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.updated_at
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            self.updated_at = now
            if self.tokens < 1:
                wait = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait)
                self.tokens = 0
            else:
                self.tokens -= 1
```

---

## Phase 4: Advanced Features (Weeks 13–16)

**Goal**: Local ML models, continuous monitoring, passive OSINT sources, community plugins.

### Week 13 — Local ML Models (Optional, No Internet Required)

For air-gapped or offline use, bundle small ONNX models:

```python
# autorecon/ml/classifier.py
import onnxruntime as ort
import numpy as np

class ContentClassifier:
    """Classifies HTTP response content (login page, admin panel, etc.)"""
    
    def __init__(self, model_path: str = "models/content_classifier.onnx"):
        self.session = ort.InferenceSession(model_path)
        self.labels = ["login", "admin", "api", "static", "cms", "error", "other"]
    
    def predict(self, html_text: str, headers: dict) -> str:
        # Simple heuristic since we can't fit a real model here
        text_lower = html_text.lower()
        if "wp-admin" in text_lower or "wp-login" in text_lower:
            return "cms:wordpress"
        if "admin" in text_lower and "password" in text_lower:
            return "admin_login"
        if "api" in headers.get("content-type", ""):
            return "api_endpoint"
        return "other"
```

**Train a custom classifier**: Use free HuggingFace datasets (e.g., "commoncrawl" subset) + HuggingFace free inference to label training data, then export to ONNX.

### Week 14 — Continuous Monitoring

```bash
# Add to crontab or systemd timer
autorecon watch example.com --interval 24h --notify slack

# Detects new subdomains, changed tech stacks, new open ports
# Sends notification with AI-written diff summary
```

```python
# autorecon/monitor.py
class Monitor:
    async def check_changes(self, target: str):
        previous = await self.db.get_latest_scan(target)
        current = await self.scanner.run_full(target)
        
        diff = self.compute_diff(previous, current)
        if diff.has_changes:
            summary = await self.ai.summarize_changes(diff)
            await self.notifier.send(summary)
```

### Week 15 — Passive OSINT Sources

- **Shodan InternetDB** (free, no key): `https://internetdb.shodan.io/{ip}` — open ports, tags, CVEs
- **Censys** (free tier): Certificate search, host enumeration
- **SecurityTrails** (free tier): Historical DNS data
- **URLScan.io** (free, no key): `https://urlscan.io/api/v1/search/?q=domain:{target}`
- **AlienVault OTX** (free key): Passive DNS, URL list

```python
# modules/osint_passive.py
class PassiveOSINT(ReconModule):
    async def run(self, target: str, config: dict) -> ReconResult:
        findings = []
        
        # Shodan InternetDB
        async with aiohttp.ClientSession() as session:
            for ip in resolved_ips:
                async with session.get(f"https://internetdb.shodan.io/{ip}") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        findings.append({"source": "shodan", "ip": ip, "data": data})
        
        # URLScan.io
        async with session.get(f"https://urlscan.io/api/v1/search/?q=domain:{target}") as resp:
            if resp.status == 200:
                data = await resp.json()
                for result in data.get("results", []):
                    findings.append({"source": "urlscan", "url": result.get("page", {}).get("url")})
        
        return ReconResult(module=self.name, target=target, findings=findings)
```

### Week 16 — Plugin System & Community

```python
# autorecon/plugins/loader.py
import importlib
import pkgutil

class PluginManager:
    def __init__(self):
        self.modules = {}
    
    def discover_plugins(self):
        # Scan autorecon/modules/ and $HOME/.autorecon/plugins/
        for finder, name, ispkg in pkgutil.iter_modules():
            if name.startswith("autorecon_module_"):
                module = importlib.import_module(name)
                self.register(module.setup())
    
    def register(self, module: ReconModule):
        self.modules[module.name] = module
```

**Community contributions**: A simple `# autorecon-module` tag on GitHub repos makes modules auto-discoverable via `autorecon plugin install <github-url>`.

---

## Development Guide (Using Free AI Tools)

### Setting Up the Dev Environment

```bash
# 1. Install Python 3.12+
# 2. Install Go (for recon tools)
winget install GoLang.Go  # Windows
brew install go           # macOS

# 3. Install recon tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/sensepost/gowitness@latest
go install -v github.com/tomnomnom/assetfinder@latest
go install -v github.com/ffuf/ffuf@latest

# 4. Install FreeLLMAPI for AI
git clone https://github.com/Manifestation16/freellmapi16
cd freellmapi16
pip install -r requirements.txt
python server.py  # Starts on :8080

# 5. Install OpenCode for development assistance
npm install -g opencode-ai
# Or use the desktop app from opencode.ai/download
```

### Using OpenCode to Build AutoRecon

```bash
# Plan the architecture first
opencode -p "Plan the module system for AutoRecon AI. Each module should be a class with async run() and parse_output() methods. The planner should use an LLM to decide scan order."

# Generate boilerplate
opencode "Create the cli.py entry point with typer commands: scan, report, list, doctor, web"

# Implement specific modules
opencode "Implement the http_probe module that wraps httpx to detect technologies, status codes, and titles. Parse JSON output from httpx."

# Write tests
opencode "Write pytest test cases for the subdomain enumeration module. Mock subprocess calls to avoid running actual tools."
```

### Using FreeLLMAPI for AI Features

```python
# Throughout development, test AI features against the local FreeLLMAPI proxy:
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="freellmapi-local-key"
)

# Test scan planning
response = client.chat.completions.create(
    model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
    messages=[{"role": "user", "content": "Plan a recon scan for example.com"}]
)
print(response.choices[0].message.content)

# Test result analysis
response = client.chat.completions.create(
    model="google/gemini-2.5-flash:free",
    messages=[{"role": "user", "content": "Analyze these findings: ..."}]
)
```

### Testing Without Actual Targets

Use a local testbed. Spin up with Docker and point AutoRecon at it:

```bash
# DVWA or WebGoat for target practice
docker run -d -p 8080:80 vulnerables/web-dvwa
# AutoRecon will discover and analyze it
autorecon scan localhost:8080
```

### CI/CD (Free Tier)

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          pip install hatch
          hatch env create
      - name: Lint
        run: hatch run lint
      - name: Type check
        run: hatch run typecheck
      - name: Test
        run: hatch run test
```

---

## Resource Links

### Free AI Models & APIs (Verified July 2026)

| Resource | URL | Free Tier |
|----------|-----|-----------|
| FreeLLMAPI | github.com/Manifestation16/freellmapi16 | Aggregates 28 providers, 4B tokens/month |
| OpenCode Zen | opencode.ai/zen | 7 free models, no credit card |
| Groq | console.groq.com | Llama 3.3 70B, 30 RPM, 1000 RPD |
| Cerebras | cerebras.ai | Qwen3 235B, 30 RPM, ~1M tokens/day |
| Mistral (Experiment) | console.mistral.ai | ~1B tokens/month, phone verify |
| Google AI Studio | aistudio.google.com | Gemini 2.5 Flash, 1M context, no card |
| Cloudflare Workers AI | workers.ai | 20+ models, daily allocation |
| HuggingFace Inference | huggingface.co/inference-api | 100K+ models, rate-limited |
| OpenRouter | openrouter.ai | 20+ free models, single API key |
| AINative Studio | ainative.studio | 84 models, 10M tokens/month |
| Pollinations | pollinations.ai | GPT-OSS 20B, anonymous |

### Recon Tools

| Tool | URL | Stars |
|------|-----|-------|
| Amass | github.com/owasp-amass/amass | 14.8K |
| Subfinder | github.com/projectdiscovery/subfinder | 14K |
| Httpx | github.com/projectdiscovery/httpx | 8K |
| Nuclei | github.com/projectdiscovery/nuclei | 22K |
| Naabu | github.com/projectdiscovery/naabu | 5K |
| gowitness | github.com/sensepost/gowitness | 4K |
| ffuf | github.com/ffuf/ffuf | 13K |
| assetfinder | github.com/tomnomnom/assetfinder | 3K |
| theHarvester | github.com/laramies/theHarvester | 12K |
| dnsx | github.com/projectdiscovery/dnsx | 2K |

### Reference Frameworks

| Project | URL | Notes |
|---------|-----|-------|
| reNgine | github.com/yogeshojha/rengine | Full-featured recon framework, Django + Docker |
| Sn1per | github.com/1N3/Sn1per | Automated pentest scanner |
| BBOT | github.com/blacklanternsecurity/bbot | OSINT automation |
| Atlas-ASM | github.com/DerekHaber/Atlas-ASM | Free ASM tool, Python CLI |

### Free Data Sources

| Source | URL | Type |
|--------|-----|------|
| crt.sh | crt.sh | Certificate transparency logs |
| Shodan InternetDB | internetdb.shodan.io | Open ports, tags, CVEs (no key) |
| URLScan.io | urlscan.io | Screenshots, DOM, requests |
| AlienVault OTX | otx.alienvault.com | Passive DNS, pulses |
| SecurityTrails | securitytrails.com | Historical DNS (free tier) |
| who-dat | who-dat.as93.net | Free WHOIS/RDAP API |
| DNS Robot | dnsrobot.net | 53 free DNS/network tools |
| HackerTarget | hackertarget.com | Free DNS/lookup API (10/day) |

### Free Wordlists

| List | URL |
|------|-----|
| SecLists | github.com/danielmiessler/SecLists |
| Assetnote Wordlists | wordlists.assetnote.io |
| Commonspeak2 | github.com/assetnote/commonspeak2 |

---

## Time & Effort Estimate

| Phase | Weeks | Hours | Key Deliverable |
|-------|-------|-------|-----------------|
| **Phase 1: MVP** | 4 | 120 | Working CLI, 5 modules, SQLite storage |
| **Phase 2: AI Integration** | 4 | 100 | AI planner, analyzer, report generator |
| **Phase 3: Production Polish** | 4 | 80 | pip package, Docker, web UI, docs |
| **Phase 4: Advanced Features** | 4 | 80 | Monitoring, OSINT, plugin system |
| **Total** | **16** | **380** | **Full-featured AI recon framework** |

### Solo Developer (20 hrs/week): ~19 weeks
### Part-time Team (2 people, 15 hrs/week each): ~13 weeks
### Full-time (40 hrs/week): ~10 weeks

### Cost Breakdown (All Free)

| Item | Cost |
|------|------|
| AI model inference | $0 (free tiers via FreeLLMAPI) |
| Cloud VPS for testing | $0 (local dev, GitHub Codespaces free tier) |
| Domain for testing | $0 (example.com, or free subdomain) |
| CI/CD | $0 (GitHub Actions free tier) |
| Package hosting | $0 (PyPI, free) |
| Documentation hosting | $0 (GitHub Pages) |
| **Total** | **$0** |

---

## Appendix: Quickstart Commands

```bash
# Install AutoRecon AI
pip install autorecon-ai

# Setup FreeLLMAPI for AI features (optional)
git clone https://github.com/Manifestation16/freellmapi16
cd freellmapi16 && pip install -r requirements.txt && python server.py &

# Verify environment
autorecon doctor

# Basic scan (no AI)
autorecon scan example.com

# AI-powered scan (requires FreeLLMAPI running)
autorecon scan example.com --ai

# Generate report
autorecon report latest --format html

# Start web UI
autorecon web

# Continuous monitoring
autorecon watch example.com --interval 24h

# List all targets and last scan
autorecon list
```

---

*This roadmap is a living document. As free AI models improve and new recon tools emerge, AutoRecon AI should evolve with them. The modular architecture makes it easy to swap in better components without rewriting the framework.*