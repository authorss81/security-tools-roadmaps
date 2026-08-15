# NetPulse AI — Roadmap

## AI-Powered Open-Source Network Security Monitoring & Intrusion Detection

**Version:** 1.0  
**Date:** July 2026  
**Budget:** $0 (100% free & open-source tooling)  
**License:** MIT  

---

## Executive Summary

NetPulse AI is a **free, production-ready, AI-powered network intrusion detection system (NIDS)** that fills the critical gap left by traditional signature-based tools (Snort, Suricata, Zeek). Those tools only flag known attack patterns from rule databases — they cannot detect zero-day exploits, novel malware, or subtle behavioral anomalies without human-written signatures.

**The NetPulse AI advantage:**

| Capability | Snort/Suricata | Zeek | NetPulse AI |
|---|---|---|---|
| Signature detection | ✅ | ❌ (no IDS) | ✅ (via Suricata integration) |
| Unsupervised ML anomaly detection | ❌ | ❌ | ✅ Isolation Forest + PyOD ensemble |
| LLM-powered log analysis | ❌ | ❌ | ✅ Qwen3 / DeepSeek-R1 local |
| Real-time Web dashboard | ❌ | ❌ | ✅ FastAPI + WebSocket + Chart.js |
| Zero-day detection | ❌ | ❌ | ✅ Behavioral anomaly scoring |
| Free AI tooling | ❌ | ❌ | ✅ All models self-hosted (Ollama) |
| Alert triage with AI reasoning | ❌ | ❌ | ✅ LLM summarizes incidents |

NetPulse AI uses **unsupervised ML (Isolation Forest, PyOD ensemble)** to learn normal traffic patterns and flag deviations, plus a **local LLM (Qwen3-8B via Ollama)** to analyze logs and produce human-readable incident summaries — all at zero cost.

---

## Tech Stack (All Free)

### Core Runtime
| Component | Choice | Why |
|---|---|---|
| Language | **Python 3.12+** | ML ecosystem, pcap libraries, FastAPI |
| Packet capture | **Scapy** + **libpcap** (Npcap on Windows) | Free, full packet manipulation |
| High-speed capture | **PF_RING** (Linux) or **AF_PACKET** | Zero-copy for 10Gbps+ |
| Async runtime | **asyncio** + **uvloop** | High-concurrency packet processing |

### ML & AI
| Component | Choice | Why |
|---|---|---|
| Anomaly detection | **scikit-learn Isolation Forest** | Blazing fast, unsupervised, no labels needed |
| Ensemble outlier detection | **PyOD** (ECOD, LOF, HBOS) | 60+ algorithms, 46M+ downloads |
| Deep learning AD | **PyOD SUOD** (GPU-accelerated) | 100x speedup on compatible HW |
| Local LLM inference | **Ollama** | Runs Qwen3, DeepSeek-R1, Phi-4 locally |
| LLM for log analysis | **Qwen3-8B** (via Ollama) | Best quality/size ratio, Apache 2.0 |
| Feature extraction | **NumPy** + **pandas** + **scikit-learn** | Industry standard |

### Web Dashboard
| Component | Choice | Why |
|---|---|---|
| Backend framework | **FastAPI** | Async-native, WebSocket support |
| Real-time transport | **WebSocket** (via FastAPI) | Bidirectional, low-latency |
| Frontend | **Vanilla JS** + **Chart.js** | Zero build step, no npm bloat |
| CSS framework | **Water.css** (dark mode) | Lightweight, minimal |
| Optional dashboard | **Streamlit** (plugin mode) | Rapid prototyping |

### Storage & Alerting
| Component | Choice | Why |
|---|---|---|
| Time-series storage | **SQLite** (dev) / **DuckDB** (prod) | Zero-dependency, fast analytics |
| Alert queue | **Redis** (optional) or in-memory | Pub/sub for real-time alerts |
| Notification | **SMTP** + **Discord webhook** + **Slack webhook** | Free tiers available |
| Monitoring | **Prometheus** + **Grafana** (optional add-on) | Industry standard |

### AI Coding Tools (Build Assistance)
| Tool | Role |
|---|---|
| **OpenCode** (CLI agent) | Code generation, refactoring, debugging |
| **Ollama** + **Qwen3-Coder** | Local AI coding assistant (free, private) |
| **Aider** | Git-tracked AI pair programming |
| **Continue** (VS Code) | IDE-integrated AI completions |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   NetPulse AI System                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │  Packet       │    │  Feature     │    │  ML Inference │   │
│  │  Capture      │───▶│  Extraction  │───▶│  Engine       │   │
│  │  (Scapy/     │    │  (NumPy/     │    │  (Isolation   │   │
│  │   libpcap)    │    │   pandas)    │    │   Forest +    │   │
│  │               │    │              │    │   PyOD)       │   │
│  └──────────────┘    └──────────────┘    └──────┬───────┘   │
│                                                  │          │
│                                                  ▼          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │  LLM Log     │    │  Alert       │    │  Anomaly     │   │
│  │  Analyst     │◀───│  Engine      │◀───│  Scorer      │   │
│  │  (Ollama +   │    │  (Rules +    │    │              │   │
│  │   Qwen3)     │    │   Threshold) │    │              │   │
│  └──────────────┘    └──────┬───────┘    └──────────────┘   │
│                             │                                │
│                             ▼                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Web Dashboard (FastAPI + WS)             │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │   │
│  │  │ Traffic │ │Anomaly  │ │ Alert   │ │ LLM     │   │   │
│  │  │ Stats   │ │Heatmap  │ │ Timeline│ │Summary  │   │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Notification Channels                     │   │
│  │  [Discord] [Slack] [Email] [Syslog] [Webhook]        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Packet Capture** → Live traffic from interface (or PCAP replay)
2. **Flow Aggregation** → 5-tuple flows, windowed stats (1s/10s/60s bins)
3. **Feature Engineering** → 40+ features: packet rate, byte rate, flow duration, protocol dist., port entropy, TCP flag ratios, inter-arrival times, packet size variance
4. **ML Scoring** → Isolation Forest anomaly score + PyOD ensemble outlier probability
5. **Threshold Decision** → Weighted score > threshold → alert
6. **LLM Enrichment** → Alert batch sent to Qwen3 for natural-language analysis
7. **Dashboard Push** → WebSocket broadcast to all connected dashboards
8. **Notification** → Discord/Slack/Email dispatch

---

## Phase 1: Packet Capture & Analysis Core

**Goal:** Working packet sniffer that computes real-time traffic statistics.

### Deliverables
- `netpulse/sniffer.py` — Async packet capture via Scapy
- `netpulse/flow.py` — 5-tuple flow tracking with sliding windows
- `netpulse/features.py` — Statistical feature extraction (40+ features)
- `netpulse/stats.py` — Bandwidth, packet rate, protocol distribution
- `netpulse/config.yaml` — Interface selection, capture filters

### Key Implementation Details

```
# Feature vector produced every 10s per flow:
features = {
    "packets_per_sec": float,
    "bytes_per_sec": float,
    "flow_duration_ms": float,
    "mean_pkt_size": float,
    "std_pkt_size": float,
    "port_entropy": float,          # High entropy → scanning
    "syn_ratio": float,              # SYN flood indicator
    "fin_ratio": float,
    "rst_ratio": float,
    "tcp_flag_entropy": float,
    "inter_arrival_mean": float,
    "inter_arrival_std": float,
    "protocol_entropy": float,
    "src_ip_entropy": float,        # Distributed attack detection
    "dst_ip_entropy": float,
    "payload_bytes_mean": float,
    "payload_bytes_std": float,
    "window_scale": float,           # TCP WS from SYN
    "ttl_mean": float,
    "ttl_std": float,
}
```

### Commands

```bash
# Install dependencies
pip install scapy numpy pandas scikit-learn pyod fastapi uvicorn websockets
pip install "pyod[suod]"  # GPU-accelerated streaming

# Windows: install Npcap from https://npcap.com (WinPcap-compatible mode)
# Linux: libpcap-dev, optionally PF_RING

# Test packet capture
python -c "from scapy.all import sniff; sniff(count=10, prn=lambda p: p.summary())"

# Run feature extractor
python netpulse/sniffer.py --interface eth0 --flow-window 10
```

### Milestones
1. ✅ Packet capture from live interface works
2. ✅ Flow aggregation with 1s/10s/60s windows
3. ✅ 40+ statistical features computed in real-time
4. ✅ CSV/JSON log output for verification
5. Offline PCAP replay mode for development

**Effort:** 2-3 weeks (with AI coding assistance, ~40 hours)

---

## Phase 2: ML Anomaly Detection

**Goal:** Train unsupervised models on normal traffic, detect anomalies in real-time.

### Training Pipeline

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Baseline     │    │  Feature     │    │  Model       │
│  Capture      │───▶│  Matrix      │───▶│  Training    │
│  (normal-only)│    │  (X_train)   │    │  (IF + PyOD) │
└──────────────┘    └──────────────┘    └──────┬───────┘
                                                │
                                                ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Live        │    │  Anomaly     │    │  Model       │
│  Scoring     │◀───│  Threshold   │◀───│  Export      │
│  (netpulse)  │    │  (p99 score) │    │  (pickle/    │
│               │    │              │    │   ONNX)      │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Deliverables
- `netpulse/train.py` — Offline training script with UNSW-NB15 + custom capture
- `netpulse/models/` — Saved model artifacts (pickle or ONNX)
- `netpulse/inference.py` — Real-time scoring engine
- `netpulse/threshold.py` — Adaptive threshold calibration
- `netpulse/llm_analyzer.py` — Qwen3 integration for log analysis

### Model Ensemble Strategy

```python
# netpulse/inference.py (conceptual)
from sklearn.ensemble import IsolationForest
from pyod.models.ecod import ECOD
from pyod.models.lof import LOF
from pyod.models.hbos import HBOS
import numpy as np

class AnomalyEnsemble:
    def __init__(self):
        self.models = {
            "iforest": IsolationForest(contamination=0.05, n_estimators=200),
            "ecod": ECOD(contamination=0.05),       # Fast, no params
            "lof": LOF(contamination=0.05, n_neighbors=20),
            "hbos": HBOS(contamination=0.05),       # Histogram-based, fast
        }
        self.weights = {"iforest": 0.4, "ecod": 0.3, "lof": 0.15, "hbos": 0.15}
        self.contamination = 0.05

    def train(self, X):
        for name, model in self.models.items():
            model.fit(X)

    def score(self, X):
        scores = np.zeros((X.shape[0], len(self.models)))
        for i, (name, model) in enumerate(self.models.items()):
            scores[:, i] = model.decision_function(X)
        # Weighted ensemble score
        return np.dot(scores, list(self.weights.values()))

    def predict(self, X, threshold=None):
        scores = self.score(X)
        if threshold is None:
            threshold = np.percentile(scores, (1 - self.contamination) * 100)
        return scores > threshold, scores
```

### LLM Integration

```python
# netpulse/llm_analyzer.py (conceptual)
import ollama  # pip install ollama

PROMPT_TEMPLATE = """You are a network security analyst. Analyze this alert batch:

{alerts_json}

For each alert, provide:
1. Severity (LOW/MEDIUM/HIGH/CRITICAL)
2. Likely attack type (port scan, DDoS, data exfiltration, C2, etc.)
3. Recommended immediate action
4. Confidence score (0-1)

Respond in JSON format only."""

def analyze_alerts(alerts: list[dict]) -> dict:
    response = ollama.chat(
        model="qwen3:8b",  # or "deepseek-r1:7b", "phi-4:14b"
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(alerts_json=json.dumps(alerts, indent=2))}],
        format="json",
    )
    return json.loads(response["message"]["content"])
```

### Free Training Datasets

| Dataset | Size | Attack Types | Use |
|---|---|---|---|
| **UNSW-NB15** | 2.5M records, 49 features | 9 attack classes | Primary training |
| **CIC-IDS2017** | 2.8M records, 80+ features | 14 attack classes | Validation |
| **CTU-13** | 13 PCAPs (botnet traffic) | Botnet C2 behavior | Botnet-specific |
| **TON_IoT** | IoT/IIoT traffic | 9 attack types | IoT anomaly |
| **Custom capture** | As needed | Your network baseline | Deployment tuning |

### Training Commands

```bash
# Download UNSW-NB15
wget https://cloudstor.aarnet.edu.au/plus/s/2DhnLGDdEECo4ys/download --output-document=unsw-nb15.zip

# Train model on normal traffic
python netpulse/train.py --data data/your_normal_traffic.csv --output models/ensemble.pkl

# Calibrate threshold (p99 on normal data)
python netpulse/threshold.py --model models/ensemble.pkl --data data/normal.csv

# Start inference engine
python netpulse/inference.py --model models/ensemble.pkl --interface eth0
```

### Milestones
1. Isolation Forest trained on UNSW-NB15, F1 > 0.90
2. PyOD ensemble added, F1 > 0.94
3. Real-time scoring < 5ms per flow batch
4. LLM analysis produces actionable summaries
5. Adaptive threshold (no manual tuning needed)

**Effort:** 3-4 weeks (ML training + tuning, ~60 hours)

---

## Phase 3: Real-Time Dashboard

**Goal:** Browser-based dashboard with live traffic visualization, anomaly alerts, and LLM analysis.

### Architecture

```
┌────────────────────────────────────────────────────┐
│                  FastAPI Server                      │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │
│  │ REST API   │  │ WebSocket  │  │ SSE Endpoint │  │
│  │ /api/*     │  │ /ws/alerts │  │ /stream/stats│  │
│  └────────────┘  └────────────┘  └──────────────┘  │
│  ┌──────────────────────────────────────────────┐   │
│  │  Static Files: /dashboard/* (HTML/JS/CSS)     │   │
│  └──────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│  Browser        │  │  Browser        │
│  Dashboard #1   │  │  Dashboard #2   │
│  (Chart.js +    │  │  (Chart.js +    │
│   WebSocket)    │  │   WebSocket)    │
└─────────────────┘  └─────────────────┘
```

### Dashboard Panels

```
┌─────────────────────────────────────────────────────────┐
│  NetPulse AI Dashboard                    [● Live]      │
├────────────────────┬────────────────────────────────────┤
│                    │                                    │
│  Traffic Overview  │  Anomaly Score Timeline           │
│  ┌───────────────┐ │  ┌────────────────────────────┐   │
│  │ 1.2 Gbps      │ │  │  ▁▃▅▇▆▄▂▁▃▅▇█▇▆▄▂▁       │   │
│  │ 15k pkt/s     │ │  │  Threshold: ████▁▁▁▁▁▁     │   │
│  │ 42% TCP       │ │  └────────────────────────────┘   │
│  │ 35% UDP       │ │                                    │
│  └───────────────┘ │                                    │
├────────────────────┼────────────────────────────────────┤
│  Protocol Pie      │  Top Talkers                       │
│  ┌───────────────┐ │  ┌────────────────────────────┐   │
│  │   TCP  █████  │ │  │  10.0.0.1 → 8.8.8.8  2GB  │   │
│  │   UDP  ████   │ │  │  10.0.0.2 → 1.1.1.1  1GB  │   │
│  │   ICMP █      │ │  │  10.0.0.3 → 192.168...    │   │
│  └───────────────┘ │  └────────────────────────────┘   │
├────────────────────┴────────────────────────────────────┤
│  Alerts (Live Feed)                                     │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 🔴 CRITICAL 14:23:02  Port scan from 10.0.0.100   │ │
│  │    → 500 ports in 2s (LLM: Horizontal port scan)   │ │
│  │ 🟡 MEDIUM   14:22:15  DNS query anomaly            │ │
│  │    → 1500 queries to unknown domain (LLM: DGA)     │ │
│  └────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│  LLM Analysis Panel                                     │
│  ┌────────────────────────────────────────────────────┐ │
│  │ NetPulse AI Analysis @ 14:23:05                    │ │
│  │                                                    │ │
│  │ Detected anomalous traffic pattern from 10.0.0.100 │ │
│  │ to 10.0.0.1:3306. 500 connection attempts in 2s   │ │
│  │ to sequential ports (3306-3406).                   │ │
│  │                                                    │ │
│  │ Assessment: Horizontal MySQL port scan (HIGH conf) │ │
│  │ Recommended: Block source IP, investigate MySQL    │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Implementation

```python
# dashboard/server.py (conceptual)
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import asyncio
import json

app = FastAPI()
app.mount("/dashboard", StaticFiles(directory="dashboard"), name="dashboard")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def broadcast(self, message: dict):
        dead = []
        for conn in self.active_connections:
            try:
                await conn.send_json(message)
            except Exception:
                dead.append(conn)
        for conn in dead:
            self.disconnect(conn)

manager = ConnectionManager()

@app.websocket("/ws/alerts")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()  # Keep-alive
    except WebSocketDisconnect:
        manager.disconnect(ws)

async def broadcast_loop():
    """Pushes alerts/stats from inference engine to all dashboards."""
    while True:
        alert = await inference_queue.get()  # From inference engine
        await manager.broadcast(alert)
        await asyncio.sleep(0.1)
```

```html
<!-- dashboard/index.html — simplified structure -->
<!DOCTYPE html>
<html data-theme="dark">
<head>
  <title>NetPulse AI</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>/* Water.css dark theme overrides */</style>
</head>
<body>
  <h1>NetPulse AI</h1>
  <div class="grid">
    <div class="card"><h2>Throughput</h2><canvas id="throughputChart"></canvas></div>
    <div class="card"><h2>Anomaly Score</h2><canvas id="anomalyChart"></canvas></div>
    <div class="card" id="alertFeed"><h2>Alerts</h2></div>
    <div class="card" id="llmPanel"><h2>AI Analysis</h2></div>
  </div>
  <script>
    const ws = new WebSocket(`ws://${location.host}/ws/alerts`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      updateCharts(data);
      appendAlert(data);
    };
  </script>
</body>
</html>
```

### Milestones
1. FastAPI serves dashboard with live metrics
2. WebSocket pushes anomaly alerts in real-time (<100ms delay)
3. Chart.js visualizations for throughput, protocol mix, anomaly timeline
4. LLM analysis panel shows AI-generated incident summaries
5. Auto-reconnect, dark theme, responsive layout

**Effort:** 2-3 weeks (frontend + backend, ~40 hours)

---

## Phase 4: Production Hardening

**Goal:** Enterprise-ready: rules engine, persistent storage, notifications, packaging.

### Components

#### 4.1 Rules Engine (`netpulse/rules/`)
- YAML-defined correlation rules (e.g., ">100 SYN to same host in 5s = SYN flood")
- MITRE ATT&CK mapping for each rule
- Overrides ML for known attack patterns (reduces false positives)

```yaml
# rules/port_scan.yaml
name: horizontal_port_scan
description: Detect horizontal port scanning across multiple destinations
mitre_id: T1046
condition: flow.dst_ports_unique > 50 AND flow.duration_seconds < 5
severity: HIGH
action: alert
override_ml: false  # Let ML still decide
```

#### 4.2 Storage Backend (`netpulse/store/`)
- **SQLite** for single-node deployments (zero config)
- **DuckDB** for analytics queries over historical data
- Schema: `flows`, `alerts`, `anomaly_scores`, `llm_analyses`

```sql
CREATE TABLE flows (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    src_ip TEXT,
    dst_ip TEXT,
    src_port INT,
    dst_port INT,
    protocol TEXT,
    packets INT,
    bytes INT,
    duration_ms REAL
);

CREATE TABLE alerts (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    severity TEXT,
    alert_type TEXT,
    source_ip TEXT,
    destination_ip TEXT,
    anomaly_score REAL,
    llm_summary TEXT,
    mitre_id TEXT,
    acknowledged INTEGER DEFAULT 0
);
```

#### 4.3 Notification Channels (`netpulse/notify/`)
- **Discord webhook** — Free, unlimited notifications
- **Slack webhook** — Free tier
- **SMTP email** — Gmail free tier (500/day)
- **Syslog** — Standard SIEM integration
- **Webhook** — Custom HTTP endpoint

```python
# netpulse/notify/discord.py (conceptual)
import aiohttp

DISCORD_EMBED = {
    "title": "🚨 NetPulse AI Alert",
    "color": 0xFF0000,  # Red
    "fields": [
        {"name": "Severity", "value": "{severity}", "inline": True},
        {"name": "Type", "value": "{alert_type}", "inline": True},
        {"name": "Source", "value": "{source_ip}", "inline": True},
        {"name": "Destination", "value": "{dst_ip}", "inline": True},
        {"name": "Anomaly Score", "value": "{score:.3f}", "inline": True},
        {"name": "AI Analysis", "value": "{llm_summary}"},
    ],
    "timestamp": "{timestamp}",
}
```

#### 4.4 Packaging & Deployment
- **PyPI package** (`pip install netpulse-ai`)
- **Docker image** (single container, all-in-one)
- **Docker Compose** (for Redis + PostgreSQL optional)
- **Systemd service** for Linux daemon
- **Windows service** via NSSM

```dockerfile
# Dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y libpcap-dev
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "dashboard.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: "3.8"
services:
  netpulse:
    build: .
    network_mode: "host"  # Needed for packet capture
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - INTERFACE=eth0
      - DISCORD_WEBHOOK_URL=${DISCORD_WEBHOOK_URL}
    restart: unless-stopped
```

#### 4.5 Documentation
- `README.md` — Quick start (5-minute setup)
- `docs/installation.md` — Windows, Linux, macOS
- `docs/configuration.md` — All config options
- `docs/ml_training.md` — How to train on your network
- `docs/rules.md` — Rule writing guide
- `docs/api.md` — REST API reference
- `docs/architecture.md` — Full architecture diagram

### Milestones
1. Rules engine processes 100k+ flows/sec
2. Storage persists 30+ days of data
3. Discord + Slack + Email notifications functional
4. Docker image published to Docker Hub
5. Full documentation written

**Effort:** 3-4 weeks (hardening + docs, ~60 hours)

---

## Phase 5: AI-Assisted Development Guide

### Using Free AI Coding Tools to Build NetPulse AI

#### Setup

```bash
# 1. Install Ollama for local AI coding
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:8b          # Best coding+reasoning local model
ollama pull qwen3-coder:7b    # Specialized coding variant

# 2. Install OpenCode (terminal AI agent)
curl -fsSL https://opencode.ai/install.sh | sh

# 3. Configure OpenCode for local models
mkdir -p ~/.config/opencode
cat > ~/.config/opencode/opencode.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "name": "Local Ollama",
      "options": { "baseURL": "http://localhost:11434/v1" },
      "models": {
        "qwen3:8b": { "name": "Qwen3 8B" },
        "qwen3-coder:7b": { "name": "Qwen3 Coder 7B" }
      }
    }
  },
  "customCommands": [
    { "name": "test", "command": "pytest tests/ -v", "description": "Run tests" },
    { "name": "lint", "command": "ruff check netpulse/", "description": "Lint code" },
    { "name": "typecheck", "command": "mypy netpulse/", "description": "Type check" }
  ]
}
EOF

# 4. Alternatively install Aider (git-native AI pair programmer)
pip install aider-chat
```

#### AI-Assisted Workflow

```
┌─────────────────────────────────────────────────────┐
│               Development Loop                        │
├─────────────────────────────────────────────────────┤
│                                                       │
│  1. Describe feature in natural language              │
│     → "Create a TCP flow tracker with 10s windows"   │
│                                                       │
│  2. OpenCode generates code with tests                │
│     → `opencode "Implement flow aggregation..."`     │
│                                                       │
│  3. Run tests, lint, typecheck                        │
│     → `opencode test` → auto-fix failures            │
│                                                       │
│  4. Review and commit                                 │
│     → `git diff` → `git commit -m "feat: flow agg"`  │
│                                                       │
│  5. Repeat                                            │
│                                                       │
└─────────────────────────────────────────────────────┘
```

#### Prompt Templates for AI Coding

**Feature implementation:**
```
Implement a NetworkFlow class in netpulse/flow.py that:
- Tracks 5-tuple (src_ip, dst_ip, src_port, dst_port, protocol)
- Maintains sliding windows of 1s, 10s, 60s
- Computes: packet_count, byte_count, mean/std of pkt_size,
  inter-arrival times, TCP flag ratios
- Is thread-safe (use asyncio.Lock)
- Yields flow snapshots via async generator

Include type hints and a test in tests/test_flow.py.
```

**ML model training:**
```
Write netpulse/train.py that:
- Loads UNSW-NB15 CSV from data/unsw-nb15/
- Trains an ensemble: IsolationForest + PyOD ECOD + PyOD HBOS
- Saves model to models/ensemble.pkl with joblib
- Prints precision, recall, F1 on test split
- Uses Optuna for hyperparameter tuning (5 trials)

Include argument parser with --data, --output, --contamination flags.
```

**Dashboard feature:**
```
Add a real-time anomaly chart to dashboard/index.html:
- Uses Chart.js line chart
- WebSocket receives {timestamp, score, threshold}
- Shows last 60 seconds of data
- Red highlight when score > threshold
- Auto-scrolls, auto-scales Y axis

Style matches existing dark theme.
```

---

## Resource Links

### Free AI/ML Models
| Model | Params | License | Use Case |
|---|---|---|---|
| [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 8B | Apache 2.0 | Log analysis, coding |
| [Qwen3-Coder-7B](https://huggingface.co/Qwen/Qwen3-Coder-7B) | 7B | Apache 2.0 | AI-assisted coding |
| [DeepSeek-R1-7B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B) | 7B | MIT | Security reasoning |
| [Phi-4-14B](https://huggingface.co/microsoft/phi-4) | 14B | MIT | Local deployment |
| [Gemma 4-26B](https://huggingface.co/google/gemma-4-26b-it) | 26B (4B active) | Apache 2.0 | Best quality local |

### Free Datasets
| Dataset | Link | Size |
|---|---|---|
| UNSW-NB15 | https://research.unsw.edu.au/projects/unsw-nb15-dataset | 2.5M records |
| CIC-IDS2017 | https://www.unb.ca/cic/datasets/ids-2017.html | 2.8M records |
| CTU-13 | https://www.stratosphereips.org/datasets-ctu13 | 13 PCAPs |
| TON_IoT | https://research.unsw.edu.au/projects/toniot-dataset | IoT/IIoT |
| CSE-CIC-IDS2018 | https://www.unb.ca/cic/datasets/ids-2018.html | 6.2M records |

### Free ML Libraries
| Library | Link | Description |
|---|---|---|
| PyOD | https://github.com/yzhao062/pyod | 60+ anomaly detection algorithms |
| scikit-learn | https://scikit-learn.org | Isolation Forest, standard ML |
| Ollama | https://ollama.com | Local LLM runner |
| Optuna | https://optuna.org | Hyperparameter optimization |
| ONNX Runtime | https://onnxruntime.ai | Cross-platform inference |

### Free Dashboard Tools
| Tool | Link | Description |
|---|---|---|
| Chart.js | https://www.chartjs.org | Lightweight JS charts |
| FastAPI | https://fastapi.tiangolo.com | Async Python web framework |
| Streamlit | https://streamlit.io | Quick Python dashboards |
| DuckDB | https://duckdb.org | Embedded analytical database |

### Free NIDS References
| Tool | Link | Description |
|---|---|---|
| Suricata | https://suricata.io | Multi-threaded IDS/IPS |
| Zeek | https://zeek.org | Network analysis framework |
| Snort | https://www.snort.org | Signature-based IDS |

---

## Timeline & Effort Summary

| Phase | Duration | Hours | Cost | Key Outcome |
|---|---|---|---|---|
| **Phase 1:** Packet Capture & Analysis | 2-3 weeks | ~40 | $0 | Real-time flow features |
| **Phase 2:** ML Anomaly Detection | 3-4 weeks | ~60 | $0 | F1 > 0.94 ensemble model |
| **Phase 3:** Real-Time Dashboard | 2-3 weeks | ~40 | $0 | Live Web UI |
| **Phase 4:** Production Hardening | 3-4 weeks | ~60 | $0 | Docker + docs |
| **Buffer & integration** | 2 weeks | ~30 | $0 | Edge case fixes |
| **Total** | **12-16 weeks** | **~230 hours** | **$0** | **Production-ready NIDS** |

### Parallel Tracks

```
Week:  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
      ┌─────────────────────────────────────────────────┐
P1    │███████████████                                   │
P2    │         ███████████████████████                  │
P3    │                    ████████████████████           │
P4    │                               ████████████████████│
Doc   │███      ███      ███      ███      ███      ███  │
Test  │  ███  ███  ███  ███  ███  ███  ███  ███  ███    │
      └─────────────────────────────────────────────────┘
```

### Zero-Cost Commitment

| Item | Cost |
|---|---|
| Python, Scapy, scikit-learn, PyOD | Free (MIT/BSD) |
| Ollama + Qwen3 (local LLM) | Free (Apache 2.0) |
| FastAPI, Chart.js | Free (MIT) |
| OpenCode, Aider (AI coding) | Free (MIT/Apache 2.0) |
| Discord/Slack notifications | Free tier |
| Docker | Free |
| GitHub hosting | Free |
| **Total** | **$0** |

---

## Getting Started (5-Minute Quick Start)

```bash
# 1. Clone
git clone https://github.com/yourname/netpulse-ai.git
cd netpulse-ai

# 2. Install
pip install -r requirements.txt

# 3. Download a pre-trained model
wget https://github.com/yourname/netpulse-ai/releases/download/v1.0/ensemble.pkl -O models/ensemble.pkl

# 4. Run (online mode)
python netpulse/run.py --interface eth0

# 5. Open dashboard
open http://localhost:8000/dashboard

# OR: offline mode (replay a PCAP)
python netpulse/run.py --pcap samples/botnet.pcap
```

---

## Conclusion

NetPulse AI delivers **enterprise-grade AI-powered NIDS at zero cost** by combining:

- **Unsupervised ML** (Isolation Forest + PyOD ensemble) for zero-day anomaly detection
- **Local LLM** (Qwen3 via Ollama) for intelligent alert analysis with no API fees
- **Real-time WebSocket dashboard** for instant visibility
- **Open-source everything** — no vendor lock-in, no subscriptions

Built entirely with free tools available in 2026 — including OpenCode for AI-assisted development and Ollama for local model inference — NetPulse AI is the most cost-effective path to AI-driven network security monitoring.
