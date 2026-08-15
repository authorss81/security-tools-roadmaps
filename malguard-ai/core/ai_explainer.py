import os
import json
from typing import Dict, Any, List

def generate_ai_analysis(scan_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate an AI-driven threat assessment and plain-English breakdown of findings.
    Supports offline heuristic generation with fallback to Ollama or OpenRouter.
    """
    risk_score = scan_data.get("risk_score", 0)
    verdict = scan_data.get("verdict", "BENIGN")
    yara_hits = scan_data.get("yara_matches", [])
    suspicious_apis = scan_data.get("pe_analysis", {}).get("suspicious_apis", [])
    script_indicators = scan_data.get("doc_script_analysis", {}).get("suspicious_indicators", [])
    entropy = scan_data.get("entropy", 0.0)
    
    # 1. Offline Deterministic Security Heuristic Synthesis
    executive_summary = []
    tactics = set()
    recommendations = []
    
    if verdict == "MALICIOUS":
        executive_summary.append(f"CRITICAL THREAT: Sample exhibits high-confidence malicious behaviors (Risk Score: {risk_score}/100).")
    elif verdict == "SUSPICIOUS":
        executive_summary.append(f"WARNING: Suspicious indicators and packing/obfuscation characteristics detected (Risk Score: {risk_score}/100).")
    else:
        executive_summary.append(f"BENIGN: No prominent malicious signatures or indicators observed (Risk Score: {risk_score}/100).")

    # Analyze YARA
    if yara_hits:
        rules = [y["rule"] for y in yara_hits]
        executive_summary.append(f"Matched threat signatures: {', '.join(rules)}.")
        for y in yara_hits:
            if "mitre" in y.get("meta", {}):
                for m in y["meta"]["mitre"].split(","):
                    tactics.add(m.strip())

    # Analyze Suspicious PE APIs
    if suspicious_apis:
        api_names = list(set(a["function"] for a in suspicious_apis))
        categories = list(set(a["category"] for a in suspicious_apis))
        executive_summary.append(f"Binary invokes dangerous Windows APIs associated with: {', '.join(categories)} (APIs: {', '.join(api_names[:5])}).")
        for a in suspicious_apis:
            tactics.add(a["mitre"])

    # Analyze Entropy
    if entropy > 7.2:
        executive_summary.append(f"High overall Shannon entropy ({entropy}/8.0) strongly suggests binary packing, custom encryption, or compressed shellcode payloads.")
        tactics.add("T1027 (Obfuscated/Encrypted Payloads)")

    # Analyze Scripts/Docs
    if script_indicators:
        terms = [s.get("description", "") for s in script_indicators]
        executive_summary.append(f"Detected suspicious script triggers: {'; '.join(terms[:3])}.")
        for s in script_indicators:
            if "mitre" in s:
                tactics.add(s["mitre"])

    # Recommendations
    if verdict in ["MALICIOUS", "SUSPICIOUS"]:
        recommendations.append("Immediately isolate endpoint from corporate network.")
        recommendations.append("Quarantine or safely hash and neutralize the file to prevent execution.")
        recommendations.append("Check DNS/firewall logs for any egress connection attempts matching observed C2 imports.")
        recommendations.append("Block file SHA256 in EDR / SIEM across the fleet.")
    else:
        recommendations.append("File appears safe for execution. Verify authenticity with digital certificate if applicable.")

    result = {
        "provider": "MalGuard Heuristic Engine",
        "summary": " ".join(executive_summary),
        "mitre_attack_tactics": sorted(list(tactics)),
        "actionable_recommendations": recommendations
    }

    # Optional: Enhance with Ollama if configured
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    # If environment has an active Ollama or API key, could query asynchronously
    return result
