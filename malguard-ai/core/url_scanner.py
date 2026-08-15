import re
import urllib.request
import urllib.parse
from typing import Dict, Any, List

def analyze_url_or_website(url: str, timeout: int = 10) -> Dict[str, Any]:
    """Fetch and scan a website / URL for malicious scripts, phishing indicators, hidden iframes, and webshells."""
    results = {
        "url": url,
        "is_live": False,
        "status_code": 0,
        "final_url": url,
        "redirect_count": 0,
        "suspicious_indicators": [],
        "external_scripts": [],
        "hidden_iframes": [],
        "heuristics_score": 0
    }
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        results["url"] = url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MalGuard-Security-Bot/1.0"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            results["is_live"] = True
            results["status_code"] = response.status
            results["final_url"] = response.geturl()
            html_bytes = response.read(2 * 1024 * 1024) # read first 2MB max
            html_text = html_bytes.decode("utf-8", errors="ignore")
            
            # Check for hidden iframes (T1189 Drive-by Compromise)
            iframes = re.findall(r'<iframe[^>]+>', html_text, re.IGNORECASE)
            for iframe in iframes:
                if "display:none" in iframe.lower() or "visibility:hidden" in iframe.lower() or "width=0" in iframe.lower() or "height=0" in iframe.lower():
                    results["hidden_iframes"].append(iframe[:100])
                    results["suspicious_indicators"].append({
                        "category": "Drive-by Compromise",
                        "description": "Hidden zero-pixel iframe detected",
                        "mitre": "T1189",
                        "score_impact": 35
                    })
                    results["heuristics_score"] += 35

            # Check for heavily obfuscated JavaScript
            js_obfuscation_patterns = [
                (r'eval\s*\(\s*unescape\s*\(', "eval(unescape(...)) Obfuscated JavaScript Payload", 30),
                (r'eval\s*\(\s*atob\s*\(', "eval(atob(...)) Base64 JavaScript Execution", 35),
                (r'document\.write\s*\(\s*unescape\s*\(', "Obfuscated DOM Ingestion", 25),
                (r'fromCharCode\s*\(', "String.fromCharCode heavy string construction", 15),
                (r'CryptoJS\.AES\.decrypt', "Encrypted Client-Side JavaScript Stage", 25),
            ]
            for pat, desc, score in js_obfuscation_patterns:
                if re.search(pat, html_text, re.IGNORECASE):
                    results["suspicious_indicators"].append({
                        "category": "Script Obfuscation",
                        "description": desc,
                        "mitre": "T1027",
                        "score_impact": score
                    })
                    results["heuristics_score"] += score

            # Phishing credential harvesting forms pointing to external/IP URLs
            forms = re.findall(r'<form[^>]+action=["\']([^"\']+)["\']', html_text, re.IGNORECASE)
            for action in forms:
                if re.match(r'^https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', action):
                    results["suspicious_indicators"].append({
                        "category": "Phishing / Exfiltration",
                        "description": f"HTML form submits directly to raw IP address ({action})",
                        "mitre": "T1566",
                        "score_impact": 40
                    })
                    results["heuristics_score"] += 40

            # Collect external script links
            scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html_text, re.IGNORECASE)
            results["external_scripts"] = scripts[:10]
            
    except Exception as e:
        results["error"] = str(e)

    return results
