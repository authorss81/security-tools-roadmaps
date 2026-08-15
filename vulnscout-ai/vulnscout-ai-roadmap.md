# VulnScout AI — AI-Powered Web Vulnerability Scanner

**Version:** 1.0.0  
**License:** MIT  
**Budget:** $0 (fully free to build and run)  
**Target Audience:** Solo security researchers, bug bounty hunters, DevSecOps teams, small development shops  
**Repository Concept:** `github.com/vulnscout/vulnscout-ai`

---

## Executive Summary

VulnScout AI is a production-ready, AI-driven web vulnerability scanner that combines traditional DAST tooling (OWASP ZAP, Nuclei, sqlmap, ffuf) with a multi-LLM AI orchestration layer to automatically discover, validate, and report web vulnerabilities — with near-zero false positives and minimal manual effort.

**The core insight:** Existing free scanners (ZAP, Nikto, Wapiti) produce high false-positive rates (30-47% in benchmarks). Commercial tools solve this with proof-based scanning but cost thousands. VulnScout solves it by stacking free LLM APIs (Groq, Gemini, Mistral, OpenRouter, Cerebras) behind an intelligent router, using them to generate context-aware payloads, analyze HTTP responses semantically, and validate each finding before reporting.

**Key metrics (target):**
- **Detection coverage:** OWASP Top 10 + common CVEs + logic flaws
- **False positive rate:** <5% (vs 30-47% for ZAP, 60%+ for HexStrike)
- **Scan time:** 5-15 min for medium targets (vs 30-60 min for ZAP full scan)
- **Cost per scan:** $0 (free LLM tiers + local tooling)
- **Output:** CLI + Web UI + CI/CD integration + SARIF/JSON/HTML reports

---

## Tech Stack (Free Only)

### Core Language & Runtime
| Component | Choice | Why |
|-----------|--------|-----|
| Language | **Python 3.11+** | Rich security tooling ecosystem (sqlmap, nuclei integrations), easy async, LLM SDKs |
| Async runtime | **asyncio + httpx** | Concurrent crawling/fuzzing, non-blocking LLM calls |
| CLI framework | **click + rich** | Production-grade CLI with beautiful terminal output |
| Web UI | **FastAPI + HTMX + Alpine.js** | Server-rendered reactive UI, zero JS build step |
| Database | **SQLite (via SQLAlchemy + alembic)** | Zero-dependency, portable, good enough for single-user |
| Task queue | **arq** (Redis-based) or **dramatiq** | Background scan execution |
| Container | **Docker + Docker Compose** | Single-command deploy, reproducible builds |

### Web Crawling & Reconnaissance
| Tool | Purpose | License |
|------|---------|---------|
| **playwright** (Microsoft) | Headless browser crawling (SPA-aware) | Apache 2.0 |
| **httpx** (ProjectDiscovery) | Fast HTTP probing, tech fingerprinting | MIT |
| **katana** (ProjectDiscovery) | Passive/active URL discovery | MIT |
| **gau** (ProjectDiscovery) | Wayback machine URL gathering | MIT |
| **ffuf** | Directory/file fuzzing | MIT |
| **subfinder** (ProjectDiscovery) | Subdomain enumeration | MIT |

### Vulnerability Detection Engines
| Tool | Purpose | License |
|------|---------|---------|
| **Nuclei** (ProjectDiscovery) | Template-based CVE/misconfig scanning | MIT |
| **sqlmap** | Automated SQL injection detection & exploitation | GPL v2 |
| **OWASP ZAP CLI** (`zap-cli`) | Active/passive scanning via API | Apache 2.0 |
| **Dalfox** | Parameter-based XSS scanner | MIT |
| **Custom Python modules** | IDOR, CSRF, Open Redirect, LFI/RFI, SSRF, Command Injection | MIT |

### AI / LLM Stack
| Provider / Tool | Free Tier | Purpose |
|-----------------|-----------|---------|
| **Groq** | 1,000 req/day, 30 RPM, 320 tok/s | Primary LLM: fast inference for payload gen & response analysis |
| **Gemini (AI Studio)** | 1,500 req/day, 1M context | Secondary LLM: long-context analysis, report generation |
| **Mistral AI** | ~1B tokens/month | Tertiary LLM: high-volume batch processing |
| **OpenRouter** | 20+ free models, 50 req/day | Fallback router: model diversity & failover |
| **Cerebras** | 1M tokens/day, 2,600 tok/s | Ultra-fast fallback for simple classifications |
| **FreeLLMAPI** | Aggregates all above into one endpoint | Optional: unified router with auto-failover |
| **Ollama** + **Qwen2.5-Coder:7B** | Unlimited (local) | Offline mode, private scanning, no data leaves machine |
| **Nullsec-S1** (LoRA adapter) | Free (local, 7B base) | Security-specific JSON verdicts, safety layer enforcement |

### AI Coding Assistants (for *building* VulnScout)
| Tool | Purpose | Free Tier |
|------|---------|-----------|
| **OpenCode** | Terminal-native coding agent | MIT license, BYOK |
| **Aider** | Git-native pair programming | Apache 2.0 |
| **Gemini CLI** | Google's agentic coding assistant | 1,000 req/day free |
| **Codex CLI** | OpenAI's coding agent | Included with ChatGPT Plus ($20/mo) or BYOK |

### CI/CD & Distribution
| Tool | Purpose |
|------|---------|
| **GitHub Actions** | CI pipeline, automated testing, Docker build |
| **PyPI** | Python package distribution (`pip install vulnscout`) |
| **Docker Hub / GHCR** | Container distribution |
| **pre-commit** | Git hook integration |

---

## Free AI Tools & Integration Strategy

### The Router Architecture

Instead of relying on a single LLM provider (which hits rate limits and goes down), VulnScout implements a **multi-provider router** with automatic failover:

```
                    ┌─────────────┐
                    │  VulnScout  │
                    │  AI Router  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  Groq    │ │  Gemini  │ │ Mistral  │
        │(primary) │ │(secondary)│ │(batch)   │
        └──────────┘ └──────────┘ └──────────┘
              │            │            │
        ┌─────┴─────┐ ┌───┴───┐  ┌────┴────┐
        │Llama 3.3  │ │Gemini │  │Mistral  │
        │70B (fast) │ │2.5Flash│  │Small 4  │
        └───────────┘ └───────┘  └─────────┘
```

**Router logic (`vulnscout/ai/router.py`):**
```python
# Simplified routing strategy
PROVIDER_CHAIN = [
    ("groq", "llama-3.3-70b-versatile", 1000, 30),    # 1000 req/day, 30 RPM
    ("gemini", "gemini-2.5-flash", 1500, 15),          # 1500 req/day, 15 RPM
    ("mistral", "mistral-small-latest", 86000, 60),    # ~86K req/day, 1 req/s
    ("cerebras", "llama-3.3-70b", 1000000, 30),        # 1M tok/day, 30 RPM
    ("openrouter", "meta-llama/llama-3.3-70b-instruct:free", 50, 20),
]
```

### AI Usage Patterns by Scan Phase

| Phase | AI Task | Provider | Est. Tokens/Scan | Why This Provider |
|-------|---------|----------|------------------|-------------------|
| **Pre-Scan Planning** | Analyze target tech stack, select relevant templates | Groq (Llama 3.3 70B) | ~2K | Fastest inference, low latency |
| **Payload Generation** | Generate context-aware SQLi/XSS/SSRF payloads | Gemini 2.5 Flash | ~4K | 1M context, strong code generation |
| **Response Analysis** | Semantic analysis of HTTP responses for subtle vulns | Groq (Llama 3.3 70B) | ~1K/response | Speed-critical, many parallel calls |
| **FP Validation** | Validate each finding with multi-perspective analysis | Gemini 2.5 Flash | ~3K/finding | Long context, nuanced reasoning |
| **Report Generation** | Executive summary, fix guidance, CVSS scoring | Mistral Small 4 | ~8K | High volume, batch processing |
| **Offline Mode** | All of the above | Ollama + Qwen2.5-Coder:7B | Unlimited | Privacy, no API dependency |

### Rate Limit Management

Each provider gets a dedicated rate-limiter with token-bucket algorithm:

```python
# vulnscout/ai/rate_limiter.py
class ProviderRateLimiter:
    """Token-bucket rate limiter per provider with daily quota awareness."""
    
    def __init__(self, provider: str, rpm: int, rpd: int):
        self.provider = provider
        self.tokens_per_min = rpm
        self.tokens_per_day = rpd
        self.bucket = TokenBucket(rpm, 60)  # refill per second
        self.daily_counter = 0
        self.daily_reset = time.time() + 86400
    
    async def acquire(self) -> bool:
        """Wait for capacity, return False if daily quota exhausted."""
        if self.daily_counter >= self.tokens_per_day:
            return False
        await self.bucket.acquire()
        self.daily_counter += 1
        return True
```

### Offline Mode (Ollama)

For fully air-gapped / private scanning:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the security-tuned model
ollama pull qwen2.5-coder:7b

# Or use Nullsec-S1 for structured security verdicts
# (Requires QLoRA adapter + base model)
git clone https://github.com/trynullsec/nullsec-s1.git
cd nullsec-s1
pip install -r requirements.txt
python scripts/serve.py --model qwen2.5-coder:7b --adapter outputs/nullsec-s1-qlora
```

---

## Architecture

### High-Level Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        VulnScout AI Pipeline                         │
└─────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐
│   Crawler   │───▶│   Fuzzer     │───▶│  AI Analyzer │───▶│ Reporter │
│  (Recon)    │    │  (Detection) │    │ (Validation) │    │ (Output) │
└─────────────┘    └──────────────┘    └──────────────┘    └──────────┘
     │                   │                   │                   │
     ▼                   ▼                   ▼                   ▼
┌─────────┐      ┌─────────────┐      ┌───────────┐      ┌──────────┐
│ URL     │      │ Payloads    │      │ LLM-based │      │ HTML/    │
│ Discovery│      │ & Probes   │      │ FP Filter │      │ JSON/    │
│ + Tech  │      │ + Nuclei   │      │ + CVSS    │      │ SARIF    │
│ Finger- │      │ + sqlmap   │      │ Scoring   │      │ + CLI    │
│ printing│      │ + Custom   │      │ + Fix     │      │ Output   │
└─────────┘      └─────────────┘      │ Guidance  │      └──────────┘
                                      └───────────┘
```

### Directory Structure

```
vulnscout/
├── pyproject.toml              # Build config (PEP 621)
├── setup.cfg                   # Package metadata
├── Dockerfile                  # Production image
├── docker-compose.yml          # Full stack (app + optional redis)
├── Makefile                    # Dev workflow shortcuts
├── README.md                   # Project documentation
├── docs/
│   ├── installation.md         # Installation guide
│   ├── usage.md                # CLI & Web UI usage
│   ├── api.md                  # REST API reference
│   ├── ci-cd.md                # CI/CD integration guide
│   ├── architecture.md         # Detailed architecture
│   └── contributing.md         # How to contribute
├── tests/
│   ├── conftest.py             # Shared test fixtures
│   ├── test_crawler.py
│   ├── test_fuzzer.py
│   ├── test_ai_analyzer.py
│   ├── test_reporter.py
│   ├── test_integration.py     # Full pipeline tests
│   └── fixtures/               # Test targets (OWASP Juice Shop subset)
├── vulnscout/
│   ├── __init__.py
│   ├── main.py                 # Entry point: CLI + server
│   ├── config.py               # Configuration (YAML + env vars)
│   ├── exceptions.py           # Custom exceptions
│   │
│   ├── crawler/
│   │   ├── __init__.py
│   │   ├── engine.py           # Orchestrates all crawlers
│   │   ├── playwright_crawler.py  # SPA-aware browser crawling
│   │   ├── httpx_crawler.py    # Fast HTTP crawling
│   │   ├── katana_wrapper.py   # ProjectDiscovery katana integration
│   │   ├── gau_wrapper.py      # Wayback machine integration
│   │   ├── tech_detector.py    # Wappalyzer-style tech fingerprinting
│   │   └── scope.py            # URL scope filtering
│   │
│   ├── fuzzer/
│   │   ├── __init__.py
│   │   ├── engine.py           # Orchestrates all fuzzers
│   │   ├── nuclei_runner.py    # Nuclei template execution
│   │   ├── sqlmap_runner.py    # sqlmap automation
│   │   ├── dalfox_runner.py    # Dalfox XSS scanner
│   │   ├── custom_checks/
│   │   │   ├── sqli.py         # Custom SQLi detection
│   │   │   ├── xss.py          # Custom XSS detection
│   │   │   ├── lfi_rfi.py      # LFI/RFI detection
│   │   │   ├── ssrf.py         # SSRF detection
│   │   │   ├── cmd_injection.py # Command injection detection
│   │   │   ├── idor.py         # IDOR detection (sequential/pattern)
│   │   │   ├── csrf.py         # CSRF detection
│   │   │   ├── open_redirect.py # Open redirect detection
│   │   │   └── misconfig.py    # Common misconfigurations
│   │   └── payloads/
│   │       ├── sqli.json       # SQLi payload dictionary
│   │       ├── xss.json        # XSS payload dictionary
│   │       ├── lfi.json        # LFI path traversal payloads
│   │       ├── ssrf.json       # SSRF callback payloads
│   │       ├── cmd_inject.json # Command injection payloads
│   │       └── templates/      # Jinja2 payload templates (AI-generated)
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── router.py           # Multi-provider LLM router
│   │   ├── rate_limiter.py     # Per-provider token bucket rate limiter
│   │   ├── provider.py         # LLM provider wrappers (Groq, Gemini, etc.)
│   │   ├── payload_generator.py   # AI generates context-aware payloads
│   │   ├── response_analyzer.py   # AI analyzes HTTP responses
│   │   ├── fp_validator.py     # AI false positive validation engine
│   │   ├── cvss_scorer.py      # AI-assisted CVSS 3.1 scoring
│   │   ├── report_generator.py # AI executive summaries & fix guidance
│   │   ├── prompts/
│   │   │   ├── tech_analysis.j2    # Tech stack analysis prompt
│   │   │   ├── payload_gen_sqli.j2 # SQLi payload generation prompt
│   │   │   ├── payload_gen_xss.j2  # XSS payload generation prompt
│   │   │   ├── response_analysis.j2 # Response analysis prompt
│   │   │   ├── fp_validation.j2    # False positive validation prompt
│   │   │   ├── cvss_scoring.j2     # CVSS scoring prompt
│   │   │   └── report_summary.j2   # Executive summary prompt
│   │   └── models/
│   │       ├── isolation_forest.pkl # Anomaly detection model (Phase 3)
│   │       └── scaler.pkl          # Feature scaler
│   │
│   ├── validator/
│   │   ├── __init__.py
│   │   ├── engine.py           # Multi-stage validation pipeline
│   │   ├── heuristic.py        # Rule-based pre-filtering (15+ heuristics)
│   │   ├── ai_validator.py     # LLM-based deep validation
│   │   └── proof_builder.py    # Builds reproducible PoC (curl commands, screenshots)
│   │
│   ├── reporter/
│   │   ├── __init__.py
│   │   ├── engine.py           # Report orchestration
│   │   ├── json_output.py      # JSON report (machine-readable)
│   │   ├── html_output.py      # HTML report (interactive dashboard)
│   │   ├── sarif_output.py     # SARIF output (GitHub Code Scanning)
│   │   ├── cli_output.py       # Rich terminal output
│   │   └── templates/
│   │       ├── report.html.j2  # HTML report template
│   │       └── executive.html.j2 # Executive summary template
│   │
│   ├── server/
│   │   ├── __init__.py
│   │   ├── app.py              # FastAPI application
│   │   ├── routes/
│   │   │   ├── scans.py        # Scan management endpoints
│   │   │   ├── findings.py     # Findings CRUD endpoints
│   │   │   ├── config.py       # Configuration endpoints
│   │   │   └── web.py          # Web UI endpoints (HTMX)
│   │   ├── models/
│   │   │   ├── scan.py         # SQLAlchemy scan model
│   │   │   ├── finding.py      # SQLAlchemy finding model
│   │   │   └── endpoint.py     # SQLAlchemy endpoint model
│   │   └── static/
│   │       ├── css/
│   │       │   └── app.css     # Tailwind-compiled styles
│   │       └── js/
│   │           └── app.js      # HTMX + Alpine.js behaviors
│   │
│   └── utils/
│       ├── __init__.py
│       ├── http.py             # HTTP utilities
│       ├── validators.py       # Input validation
│       ├── timestamp.py        # Time utilities
│       └── logging.py          # Structured logging
│
└── templates/                   # Nuclei custom templates
    ├── vulnscout-sqli.yaml
    ├── vulnscout-xss.yaml
    ├── vulnscout-lfi.yaml
    └── vulnscout-ssrf.yaml
```

---

## Phase 1: Core Scanner MVP

**Goal:** A working CLI scanner that crawls targets and runs template-based + basic injection detection.

### 1.1 Project Scaffold (Week 1)

```bash
# Initialize project
mkdir vulnscout && cd vulnscout
python -m venv .venv && source .venv/bin/activate
pip install poetry  # or use pip + pyproject.toml

# Initialize with AI assistance
opencode   # Use OpenCode to scaffold the initial project structure
```

**`pyproject.toml`** core dependencies:
```toml
[project]
name = "vulnscout"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "click>=8.1",
    "rich>=13.0",
    "httpx>=0.27",
    "playwright>=1.40",
    "beautifulsoup4>=4.12",
    "lxml>=5.0",
    "sqlalchemy>=2.0",
    "alembic>=1.13",
    "pydantic>=2.5",
    "pyyaml>=6.0",
    "jinja2>=3.1",
    "wappalyzer-core>=0.4",
    "tldextract>=5.0",
]

[project.optional-dependencies]
ai = [
    "openai>=1.0",         # OpenAI-compatible (Groq, etc.)
    "google-genai>=1.0",   # Gemini
    "httpx>=0.27",
]
server = [
    "fastapi>=0.109",
    "uvicorn[standard]>=0.27",
    "python-multipart>=0.0.6",
    "jinja2>=3.1",
    "aiosqlite>=0.19",
]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-cov>=5.0",
    "ruff>=0.3",
    "mypy>=1.8",
    "pre-commit>=3.6",
]
```

### 1.2 Crawler Engine (Week 1-2)

**`vulnscout/crawler/engine.py`:**
```python
"""Orchestrates all crawler sources for comprehensive URL discovery."""

class CrawlerEngine:
    """Runs multiple crawlers in parallel, deduplicates URLs, fingerprints tech."""
    
    def __init__(self, target: str, scope: Scope, config: CrawlerConfig):
        self.target = target
        self.scope = scope
        self.config = config
        
        # Crawler strategies (each runs in parallel)
        self.crawlers = [
            PlaywrightCrawler(target, scope),  # SPA-aware, JS rendering
            HttpxCrawler(target, scope),       # Fast HTTP, static pages
            KatanaWrapper(target, scope),      # Passive JS URL extraction
            GauWrapper(target),                # Wayback machine historical URLs
        ]
    
    async def run(self) -> CrawlResult:
        """Execute all crawlers concurrently with asyncio.gather."""
        urls = set()
        forms = []
        tech_stack = {}
        
        # Phase 1: Tech fingerprinting (fast, synchronous)
        tech_stack = await TechDetector(self.target).detect()
        log.info(f"Tech stack: {tech_stack}")
        
        # Phase 2: Parallel crawling
        tasks = [crawler.crawl() for crawler in self.crawlers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, CrawlResult):
                urls.update(result.urls)
                forms.extend(result.forms)
        
        # Phase 3: Filter by scope
        urls = self.scope.filter(urls)
        
        # Phase 4: De-duplicate and normalize
        urls = self._deduplicate(urls)
        
        return CrawlResult(
            urls=sorted(urls),
            forms=forms,
            tech_stack=tech_stack,
            stats=CrawlStats(
                total_urls=len(urls),
                total_forms=len(forms),
                technologies=tech_stack,
            )
        )
```

**`vulnscout/crawler/playwright_crawler.py`:**
```python
"""SPA-aware crawler using Playwright with stealth mode."""

class PlaywrightCrawler:
    """Headless Chromium crawler that executes JavaScript and captures API calls."""
    
    async def crawl(self) -> CrawlResult:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=self._random_ua(),
                extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
            )
            page = await context.new_page()
            
            # Intercept all XHR/fetch calls to discover API endpoints
            api_calls = []
            await page.route("**/*", self._capture_api_call(api_calls))
            
            # Navigate and wait for JS to render
            await page.goto(self.target, wait_until="networkidle")
            
            # Extract all links, forms, and JS files
            urls = await page.evaluate("""
                () => {
                    const links = [...document.querySelectorAll('a[href]')]
                        .map(a => a.href);
                    const forms = [...document.querySelectorAll('form')]
                        .map(f => ({
                            action: f.action,
                            method: f.method,
                            inputs: [...f.querySelectorAll('input')]
                                .map(i => ({ name: i.name, type: i.type }))
                        }));
                    return { links, forms };
                }
            """)
            
            await browser.close()
            
            return CrawlResult(
                urls=list(set(urls + [call.url for call in api_calls])),
                forms=urls.get("forms", []),
            )
```

### 1.3 Fuzzer Engine (Week 2-3)

**`vulnscout/fuzzer/engine.py`:**
```python
"""Orchestrates all vulnerability detection modules."""

class FuzzerEngine:
    """Runs template-based (Nuclei) and custom check-based fuzzing in parallel."""
    
    # Maps vulnerability classes to their detection modules
    CHECKS = {
        "sqli": SQLiChecker,
        "xss": XSSChecker,
        "lfi": LFIChecker,
        "ssrf": SSRFChecker,
        "cmd_injection": CommandInjectionChecker,
        "idor": IDORChecker,
        "csrf": CSRFChecker,
        "open_redirect": OpenRedirectChecker,
        "misconfig": MisconfigChecker,
    }
    
    async def run(self, targets: CrawlResult) -> list[RawFinding]:
        raw_findings = []
        tasks = []
        
        # 1. Run Nuclei templates in parallel
        tasks.append(self._run_nuclei(targets.urls))
        
        # 2. Run sqlmap on parameters with DB tech
        if targets.tech_stack.get("database"):
            tasks.append(self._run_sqlmap(targets.urls))
        
        # 3. Run custom checks on each endpoint
        for url in targets.urls:
            for check_name, Checker in self.CHECKS.items():
                checker = Checker(url, targets.tech_stack)
                tasks.append(checker.run())
        
        # Execute all in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                raw_findings.extend(result)
        
        return raw_findings
```

**`vulnscout/fuzzer/nuclei_runner.py`:**
```python
"""Nuclei template execution wrapper."""

class NucleiRunner:
    TEMPLATE_CATEGORIES = {
        "sql-injection": "cves/sqli/*.yaml",
        "xss": "cves/xss/*.yaml",
        "lfi": "cves/lfi/*.yaml",
        "ssrf": "cves/ssrf/*.yaml",
        "misconfig": "misconfiguration/*.yaml",
        "exposed-panels": "exposed-panels/*.yaml",
        "tech-detect": "technologies/*.yaml",
    }
    
    async def run(self, urls: list[str], tech: dict) -> list[RawFinding]:
        findings = []
        
        # Select templates based on detected tech stack
        template_flags = self._select_templates(tech)
        
        # Run nuclei as subprocess with JSON output
        proc = await asyncio.create_subprocess_exec(
            "nuclei", "-u", self.target,
            "-t", template_dir,
            "-json", "-o", output_file,
            "-stats", "-silent",
        )
        await proc.wait()
        
        # Parse results
        findings = self._parse_nuclei_output(output_file)
        return findings
```

### 1.4 Configuration & CLI (Week 1-3)

**`vulnscout/config.py`:**
```python
from pydantic import BaseModel, Field
from typing import Optional, Literal

class VulnScoutConfig(BaseModel):
    """Unified configuration loaded from YAML + env vars + CLI flags."""
    
    target: str
    scope: ScopeConfig = Field(default_factory=ScopeConfig)
    crawling: CrawlingConfig = Field(default_factory=CrawlingConfig)
    fuzzing: FuzzingConfig = Field(default_factory=FuzzingConfig)
    ai: AIConfig = Field(default_factory=AIConfig)
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)
    
    class ScopeConfig(BaseModel):
        include_subdomains: bool = False
        exclude_paths: list[str] = []
        max_depth: int = 3
    
    class CrawlingConfig(BaseModel):
        max_pages: int = 200
        use_playwright: bool = True
        use_wayback: bool = True
        timeout: int = 30
    
    class FuzzingConfig(BaseModel):
        use_nuclei: bool = True
        use_sqlmap: bool = True
        custom_checks: list[str] = ["sqli", "xss", "lfi", "ssrf", 
                                     "cmd_injection", "idor", "csrf", 
                                     "open_redirect", "misconfig"]
        concurrency: int = 10
    
    class AIConfig(BaseModel):
        enabled: bool = True
        provider: Literal["groq", "gemini", "mistral", "cerebras", 
                          "openrouter", "ollama"] = "groq"
        model: str = "llama-3.3-70b-versatile"
        api_key: Optional[str] = None
        temperature: float = 0.3
        max_retries: int = 3
        offline_mode: bool = False
        ollama_model: str = "qwen2.5-coder:7b"
    
    class ReportingConfig(BaseModel):
        formats: list[str] = ["cli", "json", "html"]
        output_dir: str = "./vulnscout-reports"
        include_evidence: bool = True
```

**`vulnscout/main.py` (CLI entry point):**
```python
import click
from rich.console import Console
from rich.table import Table

@click.group()
@click.version_option()
def cli():
    """VulnScout AI - AI-Powered Web Vulnerability Scanner."""
    pass

@cli.command()
@click.argument("url")
@click.option("--config", "-c", help="Config file path")
@click.option("--output", "-o", default="./vulnscout-reports")
@click.option("--ai/--no-ai", default=True, help="Enable/disable AI analysis")
@click.option("--deep/--quick", default=False, help="Deep scan (slower, more thorough)")
@click.option("--auth-header", "-H", help="Authentication header (e.g., 'Bearer xxx')")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def scan(url, config, output, ai, deep, auth_header, json_output):
    """Scan a web application for vulnerabilities."""
    console = Console()
    
    with console.status("[bold green]Scanning...") as status:
        # 1. Load config
        cfg = load_config(config, url, ai, deep, auth_header)
        
        # 2. Crawl
        status.update("[bold green]Phase 1/4: Crawling target...")
        crawler = CrawlerEngine(url, cfg)
        crawl_result = asyncio.run(crawler.run())
        
        # 3. Fuzz
        status.update("[bold green]Phase 2/4: Fuzzing endpoints...")
        fuzzer = FuzzerEngine(cfg)
        raw_findings = asyncio.run(fuzzer.run(crawl_result))
        
        # 4. Analyze (AI - Phase 2)
        if ai and cfg.ai.enabled:
            status.update("[bold green]Phase 3/4: AI analysis...")
            analyzer = AIAnalyzer(cfg)
            findings = asyncio.run(analyzer.analyze(raw_findings, crawl_result))
        else:
            findings = raw_findings
        
        # 5. Report
        status.update("[bold green]Phase 4/4: Generating report...")
        report = ReportGenerator(cfg)
        report_path = asyncio.run(report.generate(findings))
    
    # Summary table
    summary_table = Table(title="Scan Summary")
    summary_table.add_column("Severity", style="cyan")
    summary_table.add_column("Count", style="magenta")
    for severity in ["Critical", "High", "Medium", "Low", "Info"]:
        count = len([f for f in findings if f.severity == severity])
        summary_table.add_row(severity, str(count))
    console.print(summary_table)
    console.print(f"\n[green]Report saved to: {report_path}[/green]")
```

### 1.5 Testing Against OWASP Juice Shop

```bash
# Setup test target
docker run -d -p 3000:3000 bkimminich/juice-shop

# Run VulnScout basic scan
vulnscout scan http://localhost:3000 --quick

# Expected: 5-15 findings (security headers, some XSS, SQLi on search)
# False positives: 40-60% (Phase 2 AI will reduce this)
```

**Test suite (`tests/test_integration.py`):**
```python
@pytest.mark.asyncio
async def test_juice_shop_scan():
    """Integration test against OWASP Juice Shop."""
    scanner = VulnScout(target="http://localhost:3000", quick=True)
    result = await scanner.run()
    
    assert len(result.findings) > 0
    assert any(f.vuln_type == "sql_injection" for f in result.findings)
    assert any(f.vuln_type == "xss" for f in result.findings)
```

---

## Phase 2: AI-Powered Detection

**Goal:** Replace static payload dictionaries with dynamically generated, context-aware payloads. Use LLMs to analyze HTTP responses for subtle vulnerabilities that regex-based matchers miss.

### 2.1 AI Router Implementation (Week 4)

**`vulnscout/ai/router.py`:**
```python
"""Multi-provider LLM router with automatic failover and rate limiting."""

@dataclass
class LLMProvider:
    name: str
    base_url: str
    default_model: str
    api_key_env: str
    rpm: int      # requests per minute
    rpd: int      # requests per day
    priority: int  # lower = preferred

class AIRouter:
    """Routes LLM requests to best available provider."""
    
    PROVIDERS = [
        LLMProvider("groq", "https://api.groq.com/openai/v1", 
                    "llama-3.3-70b-versatile", "GROQ_API_KEY", 30, 1000, 1),
        LLMProvider("gemini", "https://generativelanguage.googleapis.com/v1beta",
                    "gemini-2.5-flash", "GEMINI_API_KEY", 15, 1500, 2),
        LLMProvider("mistral", "https://api.mistral.ai/v1",
                    "mistral-small-latest", "MISTRAL_API_KEY", 60, 86000, 3),
        LLMProvider("cerebras", "https://api.cerebras.ai/v1",
                    "llama-3.3-70b", "CEREBRAS_API_KEY", 30, 1000000, 4),
        LLMProvider("openrouter", "https://openrouter.ai/api/v1",
                    "meta-llama/llama-3.3-70b-instruct:free", 
                    "OPENROUTER_API_KEY", 20, 50, 5),
    ]
    
    def __init__(self):
        self.limiters = {
            p.name: TokenBucketRateLimiter(p.rpm, p.rpd)
            for p in self.PROVIDERS
        }
        self.failover_counts = defaultdict(int)
    
    async def complete(self, messages: list[dict], 
                       temperature: float = 0.3) -> str:
        """Send completion to best available provider with auto-failover."""
        
        # Sort by priority, then by failover count (least-failed first)
        sorted_providers = sorted(
            self.PROVIDERS,
            key=lambda p: (self.failover_counts[p.name], p.priority)
        )
        
        for provider in sorted_providers:
            # Check rate limits
            limiter = self.limiters[provider.name]
            if not await limiter.can_accept():
                continue
            
            # Get API key
            api_key = os.getenv(provider.api_key_env)
            if not api_key:
                continue
            
            try:
                client = OpenAI(
                    base_url=provider.base_url,
                    api_key=api_key,
                )
                response = await client.chat.completions.create(
                    model=provider.default_model,
                    messages=messages,
                    temperature=temperature,
                    timeout=30,
                )
                self.failover_counts[provider.name] = 0
                return response.choices[0].message.content
            
            except Exception as e:
                log.warning(f"{provider.name} failed: {e}")
                self.failover_counts[provider.name] += 1
                continue  # Try next provider
        
        raise NoProviderAvailable("All LLM providers exhausted")
```

### 2.2 AI Payload Generator (Week 4-5)

**`vulnscout/ai/payload_generator.py`:**
```python
"""Generates context-aware attack payloads using LLM."""

class PayloadGenerator:
    """AI generates targeted payloads based on detected tech stack."""
    
    async def generate_sqli_payloads(self, endpoint: Endpoint, 
                                      tech_stack: dict) -> list[str]:
        """Generate SQLi payloads tailored to the detected database."""
        
        db_type = tech_stack.get("database", "mysql")
        input_type = endpoint.param_type  # numeric, string, JSON, etc.
        
        prompt = self._render_template("payload_gen_sqli.j2", {
            "db_type": db_type,
            "input_type": input_type,
            "param_name": endpoint.param_name,
            "endpoint_path": endpoint.path,
            "method": endpoint.method,
        })
        
        response = await self.router.complete([
            {"role": "system", "content": "You are a security researcher generating SQL injection payloads. Return ONLY a JSON array of strings, no other text."},
            {"role": "user", "content": prompt},
        ])
        
        payloads = json.loads(response)
        
        # Combine AI-generated payloads with static dictionary
        static_payloads = self._load_static_payloads("sqli", db_type)
        all_payloads = list(set(payloads + static_payloads))
        
        return all_payloads[:20]  # Limit to 20 most relevant
```

**`vulnscout/ai/prompts/payload_gen_sqli.j2`:**
```
You are testing a web application for SQL injection vulnerabilities.

Target details:
- URL path: {{ endpoint_path }}
- HTTP method: {{ method }}
- Parameter name: {{ param_name }}
- Parameter type: {{ input_type }}
- Detected database: {{ db_type }}

Generate 5-10 SQL injection payloads specifically targeting {{ db_type }} 
that would bypass common WAF filters (Cloudflare, ModSecurity, AWS WAF).

For each payload, consider:
1. The parameter type (string needs quotes, numeric doesn't)
2. Database-specific syntax (MySQL CONCAT vs PostgreSQL ||)
3. WAF bypass techniques (comments, encoding, case variation)

Return ONLY a JSON array of strings like: ["payload1", "payload2", ...]
```

### 2.3 AI Response Analyzer (Week 5-6)

**`vulnscout/ai/response_analyzer.py`:**
```python
"""Uses LLM to semantically analyze HTTP responses for subtle vulnerabilities."""

class ResponseAnalyzer:
    """LLM-based HTTP response analysis beyond regex matching."""
    
    ANALYSIS_TYPES = {
        "sqli": self._analyze_sqli_response,
        "xss": self._analyze_xss_response,
        "lfi": self._analyze_lfi_response,
        "ssrf": self._analyze_ssrf_response,
        "cmd_injection": self._analyze_cmd_injection,
    }
    
    async def analyze(self, request: Request, response: Response, 
                      vuln_type: str) -> AnalysisResult:
        """Analyze HTTP response for signs of successful exploitation."""
        
        analyzer = self.ANALYSIS_TYPES.get(vuln_type)
        if not analyzer:
            return AnalysisResult(confidence=0.0, evidence="")
        
        return await analyzer(request, response)
    
    async def _analyze_sqli_response(self, req, resp) -> AnalysisResult:
        """Check for SQL error messages, data leaks, time-based indicators."""
        
        prompt = f"""
        Analyze this HTTP response for signs of SQL injection:
        
        Request: {req.method} {req.url}
        Payload: {req.body[:500]}
        
        Response Status: {resp.status_code}
        Response Headers: {dict(resp.headers)}
        Response Body (first 2000 chars): {resp.text[:2000]}
        
        Does this response indicate successful SQL injection?
        Look for:
        - SQL error messages (e.g., "MySQL syntax error", "unclosed quotation")
        - Database version/name disclosure
        - Different response length vs baseline
        - Time delay evidence (if time-based)
        - Conditional content changes (if boolean-based)
        
        Return JSON:
        {{
            "is_exploitable": boolean,
            "confidence": 0.0-1.0,
            "evidence": "specific evidence found",
            "injection_type": "error/boolean/time/union/none",
            "db_fingerprint": "detected database or null"
        }}
        """
        
        result = await self.router.complete([
            {"role": "system", "content": "You are a SQL injection analysis expert."},
            {"role": "user", "content": prompt},
        ])
        
        return AnalysisResult(**json.loads(result))
```

### 2.4 LLM-Guided Attack Chaining (Week 6)

The AI doesn't just test individual parameters — it chains findings:

```python
class AttackChainer:
    """AI identifies and executes multi-step attack chains."""
    
    CHAIN_RULES = [
        # SQLi → data exfiltration → auth bypass
        ChainRule("sqli", "data_leak", "auth_bypass",
                  lambda f: f.get("admin_creds")),
        # XSS → session theft → account takeover
        ChainRule("xss", "session_leak", "account_takeover",
                  lambda f: f.get("cookie")),
        # SSRF → internal port scan → RCE
        ChainRule("ssrf", "internal_reach", "rce",
                  lambda f: f.get("internal_service")),
        # LFI → log poisoning → RCE
        ChainRule("lfi", "log_access", "rce",
                  lambda f: f.get("log_path")),
    ]
    
    async def chain(self, findings: list[Finding]) -> list[ChainFinding]:
        """Ask LLM to identify exploitable chains across findings."""
        
        prompt = f"""
        Given these confirmed vulnerabilities on {self.target}:
        {json.dumps([f.to_dict() for f in findings], indent=2)}
        
        Identify any attack chains where combining 2+ findings 
        could escalate impact (e.g., LFI + log poisoning = RCE).
        
        Return JSON array of chains with exploitation steps.
        """
        
        chains = await self.router.complete([{"role": "user", "content": prompt}])
        return self._parse_chains(chains)
```

---

## Phase 3: False Positive Reduction Engine

**Goal:** Reduce false positive rate from ~40% (Phase 1 levels) to <5% using a multi-stage AI validation pipeline. This is VulnScout's core differentiator.

### 3.1 Three-Stage Validation Pipeline (Week 7-8)

```
Raw Finding ──▶ Stage 1: Heuristic Pre-Filter ──▶ Stage 2: AI Deep Validation ──▶ Stage 3: Proof Builder ──▶ Confirmed Finding
                     (15 rule-based filters)         (LLM analyzes full context)      (curl/cmd reproduction)     (with evidence)
```

**`vulnscout/validator/engine.py`:**
```python
"""Multi-stage validation pipeline for false positive reduction."""

class ValidationEngine:
    """Validates each finding through three stages before reporting."""
    
    STAGE_CONFIGS = {
        "heuristic": {"enabled": True, "filters": 15},
        "ai": {"enabled": True, "provider": "gemini", "model": "gemini-2.5-flash"},
        "proof": {"enabled": True, "timeout": 30},
    }
    
    async def validate(self, raw_finding: RawFinding, 
                       context: ScanContext) -> Finding:
        """Run all validation stages, return enriched finding."""
        
        # Stage 1: Fast heuristic pre-filter
        if not await HeuristicFilter(raw_finding).passes():
            return Finding(
                status="false_positive",
                reason="Failed heuristic pre-filter",
                confidence=0.0,
            )
        
        # Stage 2: AI deep validation
        ai_result = await AIValidator(raw_finding, context).validate()
        if not ai_result.is_vulnerable:
            return Finding(
                status="false_positive",
                reason=ai_result.reason,
                confidence=ai_result.confidence,
                ai_analysis=ai_result.analysis,
            )
        
        # Stage 3: Build proof of concept
        proof = await ProofBuilder(raw_finding).build()
        
        return Finding(
            status="confirmed",
            confidence=ai_result.confidence,
            severity=self._calculate_severity(raw_finding, ai_result),
            cvss_vector=ai_result.cvss_vector,
            curl_command=proof.curl_command,
            screenshot=proof.screenshot,
            evidence=proof.evidence,
            remediation=ai_result.remediation,
            ai_analysis=ai_result.analysis,
        )
```

### 3.2 Heuristic Pre-Filter (Stage 1) (Week 7)

**`vulnscout/validator/heuristic.py`:**
```python
"""Rule-based pre-filtering before expensive LLM calls."""

class HeuristicFilter:
    """15+ deterministic checks to quickly discard obvious false positives."""
    
    RULES = [
        # Soft 404s: Different content but same status code
        ("soft_404", lambda f: self._check_soft_404(f)),
        
        # CDN/WAF generic error pages (not real errors)
        ("cdn_error", lambda f: self._check_cdn_generic(f)),
        
        # Reflected values in error messages (not SQL errors)
        ("reflection_not_sqli", lambda f: self._check_reflection_vs_sqli(f)),
        
        # Same-org SRI (Subresource Integrity is intentional)
        ("same_org_sri", lambda f: self._check_same_org_sri(f)),
        
        # CORS on error responses (4xx/5xx CORS headers are noise)
        ("cors_on_error", lambda f: self._check_cors_on_error(f)),
        
        # Third-party cookies (not a vulnerability)
        ("third_party_cookie", lambda f: self._check_3p_cookie(f)),
        
        # Framework-aware CSP (React/Vue patterns are not misconfigs)
        ("framework_csp", lambda f: self._check_framework_csp(f)),
        
        # Timestamp disclosure (10-digit numbers that aren't timestamps)
        ("false_timestamp", lambda f: self._check_false_timestamp(f)),
        
        # XSS in non-rendered contexts (JSON, XML without HTML)
        ("xss_non_html_context", lambda f: self._check_non_html_context(f)),
        
        # Host header injection on non-virtual-host targets
        ("host_header_no_vhost", lambda f: self._check_vhost_scope(f)),
        
        # Blind injection without differential testing
        ("blind_no_differential", lambda f: self._check_differential(f)),
        
        # Default error pages (not exploitable)
        ("default_error_page", lambda f: self._check_default_error_page(f)),
        
        # Version disclosure in non-exploitable paths
        ("version_info_only", lambda f: self._check_version_disclosure(f)),
        
        # Info-level findings with no impact path
        ("info_no_impact", lambda f: self._check_info_impact(f)),
        
        # Duplicate findings (same vuln on same param)
        ("duplicate", lambda f: self._check_duplicate(f)),
    ]
    
    async def passes(self) -> bool:
        """Run all rules, return False if any marks as FP."""
        for rule_name, rule_fn in self.RULES:
            result = rule_fn(self.finding)
            if result.is_false_positive:
                log.debug(f"Heuristic '{rule_name}' flagged FP: {result.reason}")
                return False
        return True
```

### 3.3 AI Deep Validation (Stage 2) (Week 8-9)

**`vulnscout/validator/ai_validator.py`:**
```python
"""LLM-based deep validation with full context awareness."""

class AIValidator:
    """Uses LLM to analyze finding with full attack context."""
    
    async def validate(self) -> AIValidationResult:
        """Send finding + full request/response to LLM for analysis."""
        
        prompt = self._build_prompt()
        
        # Use Gemini for deep validation (1M context allows full req/resp history)
        response = await self.router.complete(
            [{"role": "user", "content": prompt}],
            provider="gemini",  # Force Gemini for long-context validation
            model="gemini-2.5-flash",
        )
        
        return AIValidationResult(**json.loads(response))
    
    def _build_prompt(self) -> str:
        return f"""
        You are a senior application security engineer validating a vulnerability finding.
        
        ## Finding Details
        Type: {self.finding.vuln_type}
        URL: {self.finding.url}
        Parameter: {self.finding.param}
        Payload: {self.finding.payload}
        
        ## Attack Context
        Original Request:
        {self.context.request_summary}
        
        Baseline Response (without payload):
        {self.context.baseline_response[:3000]}
        
        Attack Response (with payload):
        {self.context.attack_response[:3000]}
        
        ## Tech Stack
        {json.dumps(self.context.tech_stack, indent=2)}
        
        ## Task
        Is this a genuine vulnerability or a false positive?
        
        Consider:
        - Is the payload reflected in a rendering context (not in raw HTML/JSON)?
        - Does the response difference indicate actual exploitation or just error handling?
        - Could a WAF/CDN be generating a misleading response?
        - Is the attack vector actually reachable/postable from a real browser?
        - Does a real attacker have a practical exploit path?
        
        Return JSON:
        {{
            "is_vulnerable": true/false,
            "confidence": 0.0-1.0,
            "reason": "detailed explanation",
            "severity": "critical/high/medium/low/info",
            "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
            "cvss_score": 9.1,
            "attack_scenario": "step-by-step exploitation scenario",
            "remediation": "specific fix with code example"
        }}
        """
```

### 3.4 Proof Builder (Stage 3) (Week 9)

**`vulnscout/validator/proof_builder.py`:**
```python
"""Builds reproducible proof-of-concept for each finding."""

class ProofBuilder:
    """Generates curl commands, screenshots, and reproduction steps."""
    
    async def build(self) -> Proof:
        """Create reproduction evidence for the finding."""
        
        # 1. Generate curl command
        curl = self._build_curl_command()
        
        # 2. For XSS: take Playwright screenshot showing alert()
        screenshot = None
        if self.finding.vuln_type == "xss":
            screenshot = await self._capture_xss_screenshot()
        
        # 3. For SQLi: extract database fingerprint if possible
        db_evidence = None
        if self.finding.vuln_type == "sql_injection":
            db_evidence = await self._extract_db_fingerprint()
        
        return Proof(
            curl_command=curl,
            screenshot=screenshot,
            db_evidence=db_evidence,
            reproduction_steps=self._generate_steps(),
        )
    
    def _build_curl_command(self) -> str:
        """Generate a one-liner curl command that reproduces the finding."""
        cmd = f"curl '{self.finding.url}'"
        if self.finding.method == "POST":
            cmd += f" -X POST"
            cmd += f" -d '{self.finding.body}'"
        if self.finding.headers:
            for k, v in self.finding.headers.items():
                cmd += f" -H '{k}: {v}'"
        cmd += " -v 2>&1 | grep -i 'sql\\|error\\|warning'"
        return cmd
    
    async def _capture_xss_screenshot(self) -> str:
        """Use Playwright to prove XSS executes in a real browser."""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            # Set up dialog handler to capture alert()
            dialog_text = []
            page.on("dialog", lambda d: dialog_text.append(d.message))
            
            await page.goto(self.finding.url)
            await page.wait_for_timeout(3000)
            
            if dialog_text:
                screenshot_path = f"evidence/{self.finding.id}_xss.png"
                await page.screenshot(path=screenshot_path)
                await browser.close()
                return screenshot_path
            
            await browser.close()
            return None
```

---

## Phase 4: Production Ready

**Goal:** Package as installable CLI tool + optional web UI + CI/CD integration.

### 4.1 CLI Polish & Packaging (Week 10)

**Installation methods:**

```bash
# Method 1: pip install (primary)
pip install vulnscout

# Method 2: Docker
docker run -v $PWD/reports:/reports vulnscout/vulnscout scan https://example.com

# Method 3: GitHub Releases (standalone binary via PyInstaller)
```

**Final CLI interface:**

```bash
vulnscout scan https://example.com                    # Quick scan
vulnscout scan https://example.com --deep               # Deep scan (30+ min)
vulnscout scan https://example.com --auth-header "Bearer xxx"  # Authed scan
vulnscout scan https://example.com --output ./reports   # Custom output dir
vulnscout scan https://example.com --json               # JSON output

vulnscout server --port 8080                           # Launch web UI
vulnscout gate https://example.com --threshold high     # CI/CD gate (exit code)
vulnscout list-scans                                    # List previous scans
vulnscout show-scan <id>                                # Show scan details
vulnscout config init                                   # Generate config file
vulnscout config validate                               # Validate config
vulnscout update-templates                              # Update Nuclei templates
```

**`vulnscout/main.py` — gate command:**
```python
@cli.command()
@click.argument("url")
@click.option("--threshold", type=click.Choice(["critical", "high", "medium"]), 
              default="high")
@click.option("--max-findings", type=int, default=0)
def gate(url, threshold, max_findings):
    """CI/CD security gate. Exits with code 1 if threshold exceeded."""
    result = asyncio.run(run_scan(url, quick=True))
    
    severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
    threshold_value = severity_order[threshold]
    
    violations = [
        f for f in result.findings
        if f.status == "confirmed" and severity_order.get(f.severity, 0) >= threshold_value
    ]
    
    if max_findings > 0 and len(violations) > max_findings:
        console.print(f"[red]FAIL: {len(violations)} violations found (threshold: {max_findings})[/red]")
        raise SystemExit(1)
    
    if violations:
        console.print(f"[red]FAIL: {len(violations)} {threshold}+ severity findings[/red]")
        raise SystemExit(1)
    
    console.print("[green]PASS: No violations above threshold[/green]")
```

### 4.2 Web UI (Week 10-11)

**`vulnscout/server/app.py`:**
```python
"""FastAPI-based web UI with HTMX for reactive updates."""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="VulnScout AI")

# Web UI routes (HTMX server-rendered)
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    scans = await ScanRepository.list_recent(limit=10)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "scans": scans,
        "stats": await get_dashboard_stats(),
    })

@app.post("/scans/new", response_class=HTMLResponse)
async def start_scan(url: str = Form(...), deep: bool = Form(False)):
    scan = await ScanRepository.create(url=url, deep=deep)
    asyncio.create_task(run_scan_background(scan.id, url, deep))
    return templates.TemplateResponse("scan_progress.html", {"scan": scan})

# HTMX partials for real-time updates
@app.get("/scans/{scan_id}/progress", response_class=HTMLResponse)
async def scan_progress(scan_id: int):
    scan = await ScanRepository.get(scan_id)
    return templates.TemplateResponse("_progress.html", {"scan": scan})

@app.get("/scans/{scan_id}/findings", response_class=HTMLResponse)
async def scan_findings(scan_id: int):
    findings = await FindingRepository.get_by_scan(scan_id)
    return templates.TemplateResponse("_findings_table.html", {
        "findings": findings,
    })

# REST API for CI/CD integration
@app.post("/api/v1/scans")
async def api_start_scan(request: ScanRequest):
    scan = await ScanRepository.create(**request.dict())
    asyncio.create_task(run_scan_background(scan.id, request.url))
    return scan

@app.get("/api/v1/scans/{scan_id}")
async def api_get_scan(scan_id: int):
    return await ScanRepository.get(scan_id)

@app.get("/api/v1/scans/{scan_id}/findings")
async def api_get_findings(scan_id: int, status: str = None):
    return await FindingRepository.get_by_scan(scan_id, status=status)
```

### 4.3 CI/CD Integration (Week 11)

**GitHub Action** (`.github/actions/vulnscout-scan/action.yml`):
```yaml
name: VulnScout Scan
description: Run VulnScout AI security scan
inputs:
  target:
    required: true
    description: Target URL
  threshold:
    default: high
    description: Fail threshold (critical/high/medium)
  auth-header:
    default: ""
    description: Authorization header
outputs:
  findings-count:
    description: Number of confirmed findings
  report-path:
    description: Path to generated report
runs:
  using: composite
  steps:
    - name: Install VulnScout
      run: pip install vulnscout
      shell: bash
    
    - name: Run scan
      run: |
        vulnscout scan "${{ inputs.target }}" \
          --json \
          --output ./vulnscout-reports \
          ${{ inputs.auth-header && format('--auth-header "{0}"', inputs.auth-header) }}
      shell: bash
    
    - name: Security gate
      run: |
        vulnscout gate "${{ inputs.target }}" \
          --threshold ${{ inputs.threshold }}
      shell: bash
      continue-on-error: true
    
    - name: Upload SARIF
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: ./vulnscout-reports/results.sarif
    
    - name: Upload report
      uses: actions/upload-artifact@v4
      with:
        name: vulnscout-report
        path: ./vulnscout-reports/
```

**CI/CD workflow** (`.github/workflows/security-scan.yml`):
```yaml
name: Security Scan
on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly full scan

jobs:
  vulnscout:
    runs-on: ubuntu-latest
    services:
      app:
        image: myapp:latest
        ports:
          - 3000:3000
    
    steps:
      - uses: actions/checkout@v4
      
      - name: VulnScout Scan
        uses: ./.github/actions/vulnscout-scan
        with:
          target: http://localhost:3000
          threshold: high
      
      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(
              fs.readFileSync('./vulnscout-reports/summary.json')
            );
            
            let comment = '## VulnScout AI Scan Results\n\n';
            for (const [sev, count] of Object.entries(report.severity_counts)) {
              const emoji = {critical:'🔴', high:'🟠', medium:'🟡', low:'🟢', info:'ℹ️'};
              comment += `${emoji[sev] || ''} **${sev}**: ${count}\n`;
            }
            
            if (report.findings.length > 0) {
              comment += '\n### Top Findings\n';
              report.findings.slice(0, 5).forEach(f => {
                comment += `- **${f.severity}** ${f.vuln_type} at ${f.url}\n`;
              });
            }
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

### 4.4 Pre-commit Hook (Week 11)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/vulnscout/vulnscout
    rev: v1.0.0
    hooks:
      - id: vulnscout-scan
        name: VulnScout quick scan
        entry: vulnscout gate --threshold high
        language: python
        pass_filenames: false
        # Run against your local dev server
        args: ["http://localhost:3000"]
```

---

## Development Workflow Using Free AI

### How to Build Each Component with AI Help

This section provides ready-to-use prompts for building every part of VulnScout using free AI coding tools (OpenCode, Aider, Codex CLI, Gemini CLI).

### Phase 1: Core Scanner

**1. Scaffold project with OpenCode:**

```bash
# OpenCode session: scaffold the project
opencode << 'EOF'
Create a Python CLI project structure for a web vulnerability scanner called VulnScout.
- Use `pyproject.toml` with `click` for CLI, `rich` for output, `httpx` for HTTP
- Create the directory structure in vulnscout/
- Include a basic `vulnscout/main.py` with a `scan` CLI command that accepts a URL
- Create `vulnscout/config.py` with Pydantic settings
- Include `vulnscout/__init__.py` with version
- Add a basic test in `tests/test_cli.py`
EOF
```

**2. Crawler with Aider:**

```bash
# Aider session: build crawler
aider --model gemini/gemini-2.5-flash << 'EOF'
Add a Playwright-based web crawler module to the VulnScout project.

Create `vulnscout/crawler/playwright_crawler.py` that:
1. Launches headless Chromium via Playwright
2. Navigates to the target URL and waits for networkidle
3. Extracts all links, forms, input fields, and API calls (intercept XHR/fetch)
4. Recursively crawls discovered same-origin links up to max_depth
5. Deduplicates URLs and respects scope (same domain)
6. Returns a CrawlResult dataclass with urls, forms, and api_endpoints
7. Uses stealth mode (random user-agent, viewport)

Also create `vulnscout/crawler/engine.py` that orchestrates multiple crawlers.
EOF
```

**3. Fuzzer with Codex CLI:**

```bash
# Codex CLI session: build XSS checker
codex << 'EOF'
Create a reflected XSS detection module for the VulnScout scanner.

Create `vulnscout/fuzzer/custom_checks/xss.py`:
- Class `XSSChecker` that takes a URL and tech stack
- Tests both reflected and stored XSS
- Payloads should be context-aware (html context, attribute context, JS context)
- Checks response for unescaped reflection of payload
- Uses httpx for async HTTP requests
- Uses Playwright to verify XSS with browser rendering (alert() proof)
- Returns list of RawFinding dataclass instances
- Apply 5+ pre-filter heuristics before declaring a finding

Create corresponding test at `tests/test_xss_checker.py`
EOF
```

**4. SQLi Checker with Gemini CLI:**

```bash
# Gemini CLI session: build SQLi checker
gemini -p "Create a SQL injection detection module for a Python web scanner..."

# Or use the OpenCode plan mode for complex tasks
opencode plan << 'EOF'
Plan the SQL injection detection module for VulnScout.

Requirements:
1. Custom SQLi checker with error-based, boolean-based, time-based, and UNION detection
2. sqlmap integration as an escalation path (when custom checks find something)
3. Support for MySQL, PostgreSQL, MSSQL, Oracle, SQLite
4. WAF detection to adjust payloads accordingly
5. Response analysis for database fingerprinting

Output the plan as a structured document, then implement it.
EOF
```

### Phase 2: AI Integration

**5. AI Router with OpenCode:**

```bash
opencode << 'PLAN'
Create a multi-provider LLM router for VulnScout.

The router (`vulnscout/ai/router.py`) should:
1. Support Groq, Gemini, Mistral, Cerebras, and OpenRouter as providers
2. Each provider has OpenAI-compatible API
3. Implement token-bucket rate limiting per provider (RPM + RPD)
4. Auto-failover: if one provider 429s or 5xxs, try the next
5. Track failover counts and prefer least-failed providers
6. Support both streaming and non-streaming completions
7. Include proper error handling and logging
8. Read API keys from environment variables

Also create `vulnscout/ai/rate_limiter.py` with the TokenBucketRateLimiter class.
PLAN
```

**6. Payload Generator with Aider + Groq:**

```bash
export GROQ_API_KEY="gsk_..."
aider --model groq/llama-3.3-70b-versatile << 'EOF'
Add an AI-powered payload generator to the VulnScout scanner.

Create `vulnscout/ai/payload_generator.py` that:
1. Takes an endpoint (URL, method, params, param types) and detected tech stack
2. Uses the AIRouter to generate contextual SQL injection payloads
3. Creates prompt templates in `vulnscout/ai/prompts/payload_gen_sqli.j2`
4. Combines AI-generated payloads with static payload dictionary
5. Handles rate limiting gracefully (falls back to static payloads)

The prompt template should ask the LLM to generate:
- Database-specific payloads (MySQL CONCAT vs PG ||)
- WAF bypass techniques (comments, unicode, case variation)
- Parameter-context-aware (numeric vs string) payloads
EOF
```

**7. Response Analyzer with Gemini CLI:**

```bash
# Use Gemini CLI for the response analyzer (Gemini excels at nuanced text analysis)
cat > /tmp/response_analyzer_prompt.md << 'EOF'
Build an AI-powered HTTP response analyzer for a web vulnerability scanner.

The analyzer uses an LLM to semantically examine HTTP responses for signs of successful exploitation. Create the file `vulnscout/ai/response_analyzer.py`.

The analyzer must:
1. Accept a request (method, URL, headers, body), response (status, headers, body), and vuln_type
2. Route to the appropriate analysis method based on vuln_type
3. Each analysis method sends a structured prompt to the LLM via AIRouter
4. Parse the LLM JSON response into an AnalysisResult dataclass

Analysis methods needed:
- SQLi: Check for SQL errors, data leaks, time delays, conditional content
- XSS: Check for reflected payload in rendering context, JS execution evidence
- LFI: Check for file content inclusion, path disclosure
- SSRF: Check for external callbacks, internal IP leakage
- Command Injection: Check for command output in response

Create the prompt template at `vulnscout/ai/prompts/response_analysis.j2`
EOF

gemini -p "$(cat /tmp/response_analyzer_prompt.md)"
```

### Phase 3: False Positive Reduction

**8. Validation Pipeline with Codex CLI:**

```bash
codex << 'EOF'
Build the false positive reduction engine for VulnScout.

Create these files:

1. `vulnscout/validator/engine.py` - Validation pipeline orchestrator
   - Three-stage pipeline: heuristic → AI → proof builder
   - Each stage can independently reject a finding as FP
   - Enriches confirmed findings with evidence and CVSS scores

2. `vulnscout/validator/heuristic.py` - 15+ rule-based pre-filters
   - Soft 404 detection (compare with baseline)
   - CDN/WAF generic error page detection
   - False timestamp detection (decimal coordinates vs unix epoch)
   - Reflection-in-non-rendering-context detection
   - CORS-on-error-response detection
   - Framework-aware CSP analysis
   - Third-party cookie detection
   - Duplicate finding detection
   - Blind-injection-without-differential testing check

3. `vulnscout/validator/ai_validator.py` - LLM-based deep validation
   - Full request/response context to the LLM
   - Asks: "Is this genuinely exploitable?"
   - Returns JSON with is_vulnerable, confidence, severity, CVSS, remediation

4. `vulnscout/validator/proof_builder.py` - Reproducible proof generation
   - Build curl commands that reproduce the finding
   - For XSS: use Playwright to screenshot alert() execution
   - For SQLi: extract database fingerprint
   - Generate human-readable reproduction steps
EOF
```

**9. Anomaly Detection Model (optional enhancement):**

```python
# train_anomaly_detector.py
# Use Isolation Forest for unsupervised FP detection
# This is a local ML model — no API calls needed

from sklearn.ensemble import IsolationForest
import joblib
import json

# Training data: features from past confirmed findings and FPs
features = []
labels = []

for finding in historical_findings:
    features.append([
        finding.response_status,
        len(finding.response_body),
        finding.response_time_ms,
        finding.is_identical_to_baseline,  # 0 or 1
        finding.has_error_keywords,        # 0 or 1
        finding.payload_length,
        finding.num_params_tested,
        finding.reflection_ratio,          # 0.0 to 1.0
        finding.response_entropy,          # Shannon entropy of body
    ])
    labels.append(0 if finding.was_false_positive else 1)

model = IsolationForest(
    contamination=0.15,  # Expected FP rate
    random_state=42
)
model.fit(features)

joblib.dump(model, "vulnscout/ai/models/isolation_forest.pkl")
joblib.dump(scaler, "vulnscout/ai/models/scaler.pkl")
```

### Phase 4: Production

**10. Web UI with FastAPI + HTMX:**

```bash
opencode << 'EOF'
Build a FastAPI web server with HTMX for the VulnScout dashboard.

Create `vulnscout/server/app.py`:
- FastAPI app with Jinja2 templates
- Routes: GET / (dashboard), POST /scans/new, GET /scans/{id}, GET /findings/{id}
- HTMX partials for streaming scan progress and findings table
- REST API under /api/v1/ for CI/CD integration

Create templates in `vulnscout/server/templates/`:
- dashboard.html: overview with scan history, quick scan form, stats
- scan_detail.html: real-time progress, findings list, severity breakdown
- finding_detail.html: curl reproduction, evidence, remediation, CVSS score
- _progress.html: HTMX partial showing live scan status
- _findings_table.html: HTMX partial for sortable findings table

Use SQLAlchemy with SQLite for persistence.
Models: Scan (id, url, status, created_at, completed_at, summary JSON)
         Finding (id, scan_id, vuln_type, severity, url, evidence JSON)

Use Tailwind CSS via CDN for styling. Dark theme by default.
EOF
```

### Prompt Library for AI Coding Assistants

| Task | Best AI Tool | Key Prompt Element |
|------|-------------|-------------------|
| Scaffold project structure | OpenCode | "Create a Python project with click CLI, rich output, pytest tests" |
| Build Playwright crawler | Aider + Gemini | "SPA-aware crawler that intercepts XHR/fetch calls" |
| Write Nuclei runner | Codex CLI | "Parse JSONL output from nuclei subprocess" |
| Implement AI router | OpenCode | "Multi-provider LLM router with auto-failover and rate limiting" |
| Design prompt templates | Aider + Groq | "Generate security-specific Jinja2 prompt templates" |
| Build heuristic filters | Gemini CLI | "15+ rule-based checks to detect false positives" |
| Create HTML report | OpenCode | "Interactive HTML report with severity donut charts" |
| Dockerfile + compose | Codex CLI | "Multi-stage Docker build for Python CLI + FastAPI server" |

---

## Resource Links

### Free AI Tools (2026)
| Tool | URL | Free Tier |
|------|-----|-----------|
| **Groq** | https://console.groq.com/keys | 1,000 req/day, 30 RPM |
| **Gemini AI Studio** | https://aistudio.google.com/apikey | 1,500 req/day, 1M context |
| **Mistral** | https://console.mistral.ai/api-keys | 1B tokens/month |
| **Cerebras** | https://cloud.cerebras.ai/ | 1M tokens/day |
| **OpenRouter** | https://openrouter.ai/keys | 20+ free models, 50 req/day |
| **FreeLLMAPI** | https://freellmapi.co | Aggregates all above |
| **Ollama** | https://ollama.com | Unlimited local inference |

### Free AI Coding Assistants
| Tool | URL | Notes |
|------|-----|-------|
| **OpenCode** | https://opencode.ai | Best for bulk code generation |
| **Aider** | https://github.com/Aider-AI/aider | Best for Git-native patches |
| **Codex CLI** | https://github.com/openai/codex | Best for CI scripting |
| **Gemini CLI** | https://cloud.google.com/gemini-cli | Best with Gemini models |
| **Cline** | https://github.com/cline/cline | Best for VS Code integration |

### Security-Specific AI Models
| Model | URL | Description |
|-------|-----|-------------|
| **Nullsec-S1** | https://github.com/trynullsec/nullsec-s1 | Security-tuned QLoRA adapter (Qwen2.5-Coder-7B) |
| **Cisco Antares** | https://huggingface.co/fdtn-ai/antares | Vuln localization SLMs (350M, 1B) |
| **RakshakAI** | https://github.com/Muneerali199/RakshakAI | Security-tuned 7B model, 80K CWE training |

### Open Source Vulnerability Scanners
| Tool | URL | License |
|------|-----|---------|
| **OWASP ZAP** | https://www.zaproxy.org | Apache 2.0 |
| **Nuclei** | https://github.com/projectdiscovery/nuclei | MIT |
| **sqlmap** | https://sqlmap.org | GPL v2 |
| **ffuf** | https://github.com/ffuf/ffuf | MIT |
| **httpx** | https://github.com/projectdiscovery/httpx | MIT |
| **katana** | https://github.com/projectdiscovery/katana | MIT |
| **Dalfox** | https://github.com/hahwul/dalfox | MIT |
| **Nikto** | https://github.com/sullo/nikto | GPL v2 |
| **Wapiti** | https://github.com/wapiti-scanner/wapiti | GPL v2 |

### Reference Projects (Study These)
| Project | URL | Key Takeaway |
|---------|-----|-------------|
| **ptai** | https://github.com/0xSteph/pentest-ai | AI-agent design, MCP-driven scanning |
| **SIPHON** | https://github.com/Christbowel/siphon | Local LLM reasoning engine, dual-track architecture |
| **SecBot** | https://github.com/odnamta/secbot | Claude AI + Playwright integration, CVSS scoring |
| **AOBTD** | https://github.com/oz9un/AOBTD | MITM proxy + specialist LLM agents |
| **NumaSec** | https://github.com/umairbari/numasec | MCP server design, autonomous pentest agent |
| **KramScan** | https://github.com/shaikhakramshakil/kramscan | Multi-provider AI analysis, modular plugin system |
| **VulnShieldAI** | https://github.com/sriramparanthaman24it/VulnShieldAI | GROQ-guided crawler prioritizing vulnerable pages |
| **Magnus** | https://github.com/carolinacherry/magnus | 5-phase scan, XSS proof hierarchy |
| **MEDUSA** | https://github.com/Pantheon-Security/medusa | 40K+ AI security patterns, heuristic FP filter |
| **Probus** | https://github.com/etairl/Probus | 3-agent SAST pipeline with OpenRouter |
| **open·kritt** | https://github.com/Kritt-ai/open-kritt | Orchestrated AI agent workflows for security |

### Testing Targets
| Target | URL | Description |
|--------|-----|-------------|
| **OWASP Juice Shop** | https://github.com/juice-shop/juice-shop | Modern SPA with 100+ challenges |
| **DVWA** | https://github.com/digininja/DVWA | Classic LAMP vulnerable app |
| **WebGoat** | https://github.com/WebGoat/WebGoat | OWASP's Java-based training app |
| **vulnado** | https://github.com/ScaleSec/vulnado | Serverless vulnerable app |

---

## Timeline & Effort Estimate

| Phase | Weeks | Hours (Solo) | Cost | Key Deliverables | AI Tool to Use |
|-------|-------|-------------|------|------------------|---------------|
| **Phase 1: Core MVP** | 1-3 | 40-60 | $0 | CLI with scan, config, crawler, basic fuzzer | OpenCode, Aider |
| 1.1 Project scaffold | Week 1 | 5 | $0 | pyproject.toml, CLI skeleton, config | OpenCode |
| 1.2 Crawler engine | Week 1-2 | 15 | $0 | Playwright + httpx crawling, tech detection | Aider + Gemini |
| 1.3 Fuzzer engine | Week 2-3 | 20 | $0 | Nuclei runner, custom check modules | Codex CLI |
| 1.4 Tests | Week 3 | 5-10 | $0 | Integration tests vs Juice Shop | Gemini CLI |
| **Phase 2: AI Detection** | 4-6 | 40-50 | $0 | AI router, payload gen, response analysis | OpenCode, Aider |
| 2.1 AI router | Week 4 | 10 | $0 | Multi-provider routing, rate limiting | OpenCode |
| 2.2 Payload generator | Week 4-5 | 10 | $0 | AI context-aware payloads | Aider + Groq |
| 2.3 Response analyzer | Week 5-6 | 15 | $0 | LLM response analysis per vuln type | Gemini CLI |
| 2.4 Attack chaining | Week 6 | 5-10 | $0 | Cross-finding chain detection | OpenCode |
| **Phase 3: FP Reduction** | 7-9 | 30-40 | $0 | <5% FP rate, evidence, PoC | Codex CLI |
| 3.1 Heuristic pre-filter | Week 7 | 10 | $0 | 15+ rule-based filters | Gemini CLI |
| 3.2 AI deep validation | Week 8 | 15 | $0 | Full-context LLM validation | Aider + Gemini |
| 3.3 Proof builder | Week 9 | 5-10 | $0 | curl commands, screenshots, steps | OpenCode |
| 3.4 Anomaly detection | Week 9 | 5 | $0 | Isolation Forest model (optional) | Local Python |
| **Phase 4: Production** | 10-12 | 40-50 | $0 | CLI polish, Web UI, CI/CD, docs | OpenCode, Codex |
| 4.1 CLI polish | Week 10 | 10 | $0 | PyPI package, Docker, `vulnscout gate` | OpenCode |
| 4.2 Web UI | Week 10-11 | 15 | $0 | FastAPI + HTMX dashboard | OpenCode |
| 4.3 CI/CD integration | Week 11 | 10 | $0 | GitHub Action, pre-commit hook | Codex CLI |
| 4.4 Documentation | Week 12 | 5-10 | $0 | README, docs, examples | Gemini CLI |
| **Total** | **12 weeks** | **150-190** | **$0** | **Production-ready scanner** | **All free tools** |

### Cost Breakdown (Full Development on Free Tiers)

| Item | Cost | Notes |
|------|------|-------|
| LLM API calls (development) | $0 | Groq (1K/day) + Gemini (1.5K/day) + Mistral (1B/mo) is far more than enough for development. Using OpenCode/Aider with these free tiers costs $0/month. |
| Compute (local dev) | $0 | Standard laptop/desktop. Playwright needs ~2GB RAM. |
| Compute (Docker build) | $0 | GitHub Actions has free 2,000 min/month. |
| Security model serving | $0 | Ollama + Qwen2.5-Coder:7B runs on consumer GPU (8GB VRAM) or CPU (slow). |
| Domain / hosting | $0 | CLI tool, no hosted service needed. Web UI is self-hosted. |
| **Total** | **$0** | 100% free to build and use. |

### Mitigating LLM Free Tier Limitations

| Risk | Mitigation |
|------|-----------|
| Groq rate limit (30 RPM) | Router auto-failover to Gemini. Queue requests with asyncio. |
| Gemini data training opt-in | Use Mistral (EU, GDPR) or Ollama (local) for sensitive targets. |
| OpenRouter 50 req/day limit | Use as last resort fallback only. Add $10 for 1,000/day if needed. |
| Mistral 2 RPM limit | Batch processing: send 10 findings in one prompt instead of 1 at a time. |
| No internet (air-gapped) | Ollama + Qwen2.5-Coder:7B handles everything locally. |
| Provider goes offline | Router architecture means zero downtime — next provider takes over. |

---

## Quick Start (Begin Here)

```bash
# 1. Install system dependencies
pip install playwright && playwright install chromium
pip install sqlmap nuclei dalfox httpx

# 2. Get free API keys (pick any 2)
export GROQ_API_KEY="gsk_..."     # https://console.groq.com/keys
export GEMINI_API_KEY="AIza..."   # https://aistudio.google.com/apikey
export MISTRAL_API_KEY="xxx"      # https://console.mistral.ai/api-keys

# 3. Install VulnScout
git clone https://github.com/vulnscout/vulnscout.git
cd vulnscout
pip install -e ".[ai,server,dev]"

# 4. Run your first scan
vulnscout scan https://example.com

# 5. Launch web UI (optional)
vulnscout server --port 8080
```

**Total effort to MVP:** 3 weeks / ~60 hours for a solo developer using free AI tools.

**Total effort to production:** 12 weeks / ~190 hours for a complete, polished tool with <5% false positive rate, web UI, and CI/CD integration.