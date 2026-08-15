import os
import time
from typing import Dict, Any, Union

from .hasher import (
    calculate_hashes,
    calculate_entropy,
    calculate_sliding_window_entropy,
    get_byte_distribution,
    detect_file_type
)
from .pe_scanner import analyze_pe
from .yara_engine import YaraEngine
from .doc_script_scanner import analyze_document_or_script
from .apk_scanner import analyze_apk
from .url_scanner import analyze_url_or_website
from .ai_explainer import generate_ai_analysis

class MalGuardAnalyzer:
    """Master orchestrator combining static, heuristic, signature, and AI malware analysis."""
    
    def __init__(self, custom_rule_path: str = None):
        if custom_rule_path:
            self.yara_engine = YaraEngine(rule_file=custom_rule_path)
        else:
            self.yara_engine = YaraEngine()

    def scan_bytes(self, file_bytes: bytes, file_name: str = "sample.bin") -> Dict[str, Any]:
        """Run full malware triage pipeline on byte buffer."""
        start_time = time.time()
        file_size = len(file_bytes)
        
        # 1. Hashing & Entropy
        hashes = calculate_hashes(file_bytes)
        entropy = calculate_entropy(file_bytes)
        sliding_entropy = calculate_sliding_window_entropy(file_bytes) if file_size < 10 * 1024 * 1024 else []
        byte_dist = get_byte_distribution(file_bytes)
        file_type = detect_file_type(file_bytes, file_name)
        
        # 2. YARA / Signature Rule Matching
        yara_matches = self.yara_engine.scan(file_bytes)
        
        # 3. PE Analysis
        pe_results = analyze_pe(file_bytes)
        
        # 4. Document & Script Inspection
        doc_script_results = analyze_document_or_script(file_bytes, file_name)

        # 5. Android APK Inspection
        apk_results = analyze_apk(file_bytes)
        
        # 6. Composite Risk Score Calculation
        score = 0
        
        # YARA Scoring
        for match in yara_matches:
            threat = match.get("meta", {}).get("threat_level", 40)
            score += threat
            
        # PE Suspicious Imports & High Entropy
        if pe_results.get("is_pe"):
            for api in pe_results.get("suspicious_apis", []):
                sev = api.get("severity", "LOW")
                if sev == "CRITICAL":
                    score += 25
                elif sev == "HIGH":
                    score += 15
                elif sev == "MEDIUM":
                    score += 8
                else:
                    score += 3
                    
            for sec in pe_results.get("suspicious_sections", []):
                if sec.get("is_packed_likely"):
                    score += 20
                if sec.get("is_writable_and_executable"):
                    score += 30

        # Document/Script Scoring
        if doc_script_results.get("is_script_or_doc"):
            score += doc_script_results.get("heuristics_score", 0)

        # APK Scoring
        if apk_results.get("is_apk"):
            score += apk_results.get("heuristics_score", 0)

        # High global entropy if binary
        if entropy > 7.3 and file_size > 4096:
            score += 20
            
        # Cap score between 0 and 100
        risk_score = min(100, max(0, score))
        
        # Determine Verdict
        if risk_score >= 70:
            verdict = "MALICIOUS"
            threat_color = "red"
        elif risk_score >= 40:
            verdict = "SUSPICIOUS"
            threat_color = "yellow"
        elif risk_score > 0:
            verdict = "LOW_RISK"
            threat_color = "blue"
        else:
            verdict = "BENIGN"
            threat_color = "green"
            
        scan_duration_ms = round((time.time() - start_time) * 1000, 2)
        
        # Synthesize Base Report
        report = {
            "file_name": file_name,
            "file_size_bytes": file_size,
            "file_type": file_type,
            "scan_duration_ms": scan_duration_ms,
            "hashes": hashes,
            "entropy": entropy,
            "byte_distribution": byte_dist,
            "sliding_entropy": sliding_entropy[:50],  # sample 50 points
            "risk_score": risk_score,
            "verdict": verdict,
            "threat_color": threat_color,
            "yara_matches": yara_matches,
            "pe_analysis": pe_results,
            "doc_script_analysis": doc_script_results,
            "apk_analysis": apk_results
        }
        
        # 7. AI Explainer & MITRE ATT&CK Mapping
        ai_summary = generate_ai_analysis(report)
        report["ai_analysis"] = ai_summary
        
        return report

    def scan_url(self, target_url: str) -> Dict[str, Any]:
        """Scan a live URL or web page for phishing, malicious iframes, and scripts."""
        return analyze_url_or_website(target_url)

    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Scan a physical file from disk."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(file_path, "rb") as f:
            file_bytes = f.read()
            
        file_name = os.path.basename(file_path)
        return self.scan_bytes(file_bytes, file_name)
