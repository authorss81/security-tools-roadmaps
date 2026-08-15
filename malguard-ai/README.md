# MalGuard AI 🛡️

> **Free & Open-Source Automated Multi-Engine Malware Scanner & Static Triage Platform**

---

## Features

- **Multi-Engine Static Scanning:** Instant PE/ELF inspection, cryptographic hashing (MD5, SHA1, SHA256), and Shannon entropy calculation.
- **Rule & Signature Matching:** Integrated YARA engine with pre-loaded signatures for ransomware, webshells, credential dumpers (Mimikatz), reverse shells, and malicious scripts.
- **PE Header & Import Analysis:** Detects dangerous Windows API calls (Process Injection, Anti-Debugging, Persistence, Keylogging, C2 Ingress) and maps them to **MITRE ATT&CK**.
- **Document & Script De-obfuscation:** Detects suspicious Office VBA macros, dangerous PDF tags (`/Launch`, `/JavaScript`, `/OpenAction`), and auto-decodes obfuscated Base64 payloads.
- **AI Threat Intelligence:** Synthesizes raw indicators into plain-English threat breakdowns, MITRE ATT&CK matrices, and actionable incident response steps.
- **Neutralizing Quarantine Vault:** Encrypts and neutralizes malicious files into isolated storage to prevent accidental execution.
- **Multiple Interfaces:** Rich interactive CLI, Async FastAPI backend, and drag-and-drop Web Dashboard.

---

## Quick Start

### 1. Installation

```bash
# Optional: install enhanced parsing libraries (CLI works out of the box with standard library too)
pip install -r requirements.txt
```

### 2. Command Line Interface (CLI)

```bash
# Scan a single file
python cli.py samples/suspicious_powershell.ps1

# Scan an entire directory
python cli.py samples/

# Output raw JSON report
python cli.py samples/suspicious_powershell.ps1 --json

# Automatically quarantine if malicious
python cli.py samples/suspicious_powershell.ps1 --quarantine
```

### 3. Web Dashboard & REST API

```bash
# Start the FastAPI web service & dashboard
python api.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser for the drag-and-drop malware analysis dashboard.

---

## Roadmap

For the complete architectural blueprint, FOSS integration matrix, and future dynamic sandbox specifications, check **[`malguard-ai-roadmap.md`](./malguard-ai-roadmap.md)**.
