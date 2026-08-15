import re
import base64
from typing import Dict, Any, List

def analyze_document_or_script(file_bytes: bytes, file_name: str = "") -> Dict[str, Any]:
    """Analyze script files, PDFs, or office documents for obfuscation and malicious payloads."""
    results = {
        "is_script_or_doc": False,
        "type": "Unknown",
        "suspicious_indicators": [],
        "decoded_payloads": [],
        "heuristics_score": 0
    }
    
    # Check if PDF
    if file_bytes.startswith(b"%PDF"):
        results["is_script_or_doc"] = True
        results["type"] = "PDF Document"
        _scan_pdf(file_bytes, results)
        return results

    # Check if Office legacy or OpenXML
    if file_bytes.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1") or file_name.endswith((".doc", ".xls", ".docm", ".xlsm")):
        results["is_script_or_doc"] = True
        results["type"] = "Office Document (Macro Potential)"
        _scan_office_indicators(file_bytes, results)
        return results

    # Check text-based scripts
    text_content = ""
    try:
        text_content = file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        pass

    if text_content:
        lower = text_content.lower()
        if any(keyword in lower for keyword in ["powershell", "wscript", "cscript", "cmd.exe", "bash", "curl", "wget", "bitsadmin", "certutil", "eval(", "unescape("]) or file_name.endswith((".ps1", ".vbs", ".bat", ".cmd", ".sh", ".js", ".py", ".php")):
            results["is_script_or_doc"] = True
            results["type"] = "Script / Command Payload"
            _scan_script(text_content, results)
            return results

    return results

def _scan_pdf(data: bytes, results: Dict[str, Any]):
    """Static inspection of PDF tags and actions."""
    pdf_suspicious_tags = [
        (b"/JavaScript", "Embedded JavaScript code inside PDF", 35, "T1059.007"),
        (b"/JS", "Short JavaScript tag", 30, "T1059.007"),
        (b"/Launch", "Automatic application launch action", 45, "T1204.002"),
        (b"/OpenAction", "Executes payload immediately upon PDF open", 30, "T1204.002"),
        (b"/EmbeddedFiles", "Carries embedded secondary file/executable", 25, "T1027"),
        (b"/AcroForm", "Dynamic form with possible script triggers", 10, "T1204"),
        (b"/URI", "External hyperlink trigger", 5, "T1204.001"),
    ]
    
    for tag, desc, score, mitre in pdf_suspicious_tags:
        count = data.count(tag)
        if count > 0:
            results["suspicious_indicators"].append({
                "tag": tag.decode(),
                "occurrences": count,
                "description": desc,
                "mitre": mitre,
                "score_impact": score
            })
            results["heuristics_score"] += score

def _scan_office_indicators(data: bytes, results: Dict[str, Any]):
    """Check OLE2 / Macro indicators in Office documents."""
    data_lower = data.lower()
    macro_indicators = [
        (b"autoopen", "AutoOpen Macro Trigger (Runs on doc open)", 35, "T1204.002"),
        (b"document_open", "Document_Open Event Trigger", 35, "T1204.002"),
        (b"workbook_open", "Workbook_Open Event Trigger", 35, "T1204.002"),
        (b"wscript.shell", "WScript.Shell Object Invocation", 40, "T1059.005"),
        (b"shellexecute", "ShellExecute API invocation", 35, "T1106"),
        (b"urldownloadtofile", "Direct file download from VBA", 45, "T1105"),
        (b"powershell", "PowerShell invocation from Office Macro", 50, "T1059.001"),
        (b"cmd.exe", "Command prompt invocation from Office Macro", 40, "T1059.003"),
    ]
    
    for term, desc, score, mitre in macro_indicators:
        if term in data_lower:
            results["suspicious_indicators"].append({
                "term": term.decode(),
                "description": desc,
                "mitre": mitre,
                "score_impact": score
            })
            results["heuristics_score"] += score

def _scan_script(text: str, results: Dict[str, Any]):
    """Scan script contents for de-obfuscation, base64 payloads, and ingress tools."""
    lower = text.lower()
    
    # Ingress & Execution tools
    tools = [
        (r"certutil(?:\.exe)?\s+(?:-[a-z]+\s+)*-(?:urlcache|split|f)", "Certutil Remote File Ingress / Living-off-the-Land", 45, "T1105"),
        (r"bitsadmin(?:\.exe)?\s+/transfer", "Bitsadmin Background Transfer Ingress", 40, "T1197"),
        (r"curl\s+(?:-[a-z]+\s+)*http[s]?://", "cURL Remote Script Download", 25, "T1105"),
        (r"wget\s+http[s]?://", "Wget Remote Script Download", 25, "T1105"),
        (r"iex\s*\(?new-object\s+net\.webclient", "PowerShell In-Memory Download Cradle", 50, "T1059.001"),
        (r"invoke-webrequest", "PowerShell Web Request", 20, "T1105"),
        (r"-windowstyle\s+hidden", "Hidden Window Style Evasion", 25, "T1564.003"),
        (r"-executionpolicy\s+bypass", "ExecutionPolicy Bypass", 30, "T1562.001"),
        (r"-nop(?:rofile)?", "NoProfile Execution Evasion", 15, "T1562"),
    ]
    
    for pattern, desc, score, mitre in tools:
        if re.search(pattern, lower):
            results["suspicious_indicators"].append({
                "pattern": pattern,
                "description": desc,
                "mitre": mitre,
                "score_impact": score
            })
            results["heuristics_score"] += score

    # Automatic Base64 extraction and decoding
    b64_matches = re.findall(r'(?:[A-Za-z0-9+/]{4}){10,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?', text)
    for b64_str in b64_matches[:5]:
        try:
            decoded = base64.b64decode(b64_str)
            # Try utf-8 or utf-16 (powershell -enc uses utf-16le)
            dec_text = ""
            for enc in ["utf-16le", "utf-8", "latin-1"]:
                try:
                    dec_text = decoded.decode(enc)
                    if any(c.isalnum() for c in dec_text) and len(dec_text) > 8:
                        break
                except Exception:
                    continue
                    
            if dec_text and any(keyword in dec_text.lower() for keyword in ["http", "powershell", "cmd", "iex", "system", "download", "socket"]):
                results["decoded_payloads"].append({
                    "original_b64_snippet": b64_str[:30] + "...",
                    "decoded_snippet": dec_text[:200],
                    "reveals_suspicious_code": True
                })
                results["heuristics_score"] += 35
        except Exception:
            pass
