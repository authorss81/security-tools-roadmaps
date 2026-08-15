import os
import sys
import json
import argparse
from typing import List

# Ensure parent directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.analyzer import MalGuardAnalyzer
from core.quarantine import quarantine_file

def print_banner():
    banner = r"""
  __  __       _  _____                     _      _    ___ 
 |  \/  |     | |/ ____|                   | |    / \  |_ _|
 | \  / | __ _| | |  __ _   _  __ _ _ __ __| |   / _ \  | | 
 | |\/| |/ _` | | | |_ | | | |/ _` | '__/ _` |  / ___ \ | | 
 | |  | | (_| | | |__| | |_| | (_| | | | (_| | / /   \ \| | 
 |_|  |_|\__,_|_|\_____|\__,_|\__,_|_|  \__,_|/_/     \_\___|
  Automated Multi-Engine Malware Scanner & Static Triage
    """
    print(banner)

def render_rich_report(report: dict):
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.text import Text
        
        console = Console()
        verdict = report["verdict"]
        score = report["risk_score"]
        color = "red" if verdict == "MALICIOUS" else ("yellow" if verdict == "SUSPICIOUS" else "green")
        
        # Header Panel
        header_text = Text()
        header_text.append(f"Target File: {report['file_name']}\n", style="bold white")
        header_text.append(f"Verdict: {verdict} (Risk Score: {score}/100)\n", style=f"bold {color}")
        header_text.append(f"Type: {report['file_type']} | Size: {report['file_size_bytes']:,} bytes | Scan Time: {report['scan_duration_ms']}ms", style="dim")
        console.print(Panel(header_text, title="[bold]Scan Overview[/bold]", border_style=color))
        
        # Hashes Table
        hash_table = Table(title="Cryptographic Identifiers & Entropy", show_header=True, header_style="bold cyan")
        hash_table.add_column("Property", style="bold")
        hash_table.add_column("Value")
        hash_table.add_row("MD5", report["hashes"]["md5"])
        hash_table.add_row("SHA1", report["hashes"]["sha1"])
        hash_table.add_row("SHA256", report["hashes"]["sha256"])
        hash_table.add_row("Shannon Entropy", f"{report['entropy']} / 8.0 (Higher > 7.0 indicates packing/encryption)")
        console.print(hash_table)
        
        # YARA Hits
        if report.get("yara_matches"):
            yara_table = Table(title="[bold red]YARA Rule Detections[/bold red]", show_header=True, header_style="bold red")
            yara_table.add_column("Rule Name")
            yara_table.add_column("Severity")
            yara_table.add_column("Description")
            yara_table.add_column("MITRE ATT&CK")
            for m in report["yara_matches"]:
                yara_table.add_row(
                    m["rule"],
                    m.get("meta", {}).get("severity", "INFO"),
                    m.get("meta", {}).get("description", "Pattern matched"),
                    m.get("meta", {}).get("mitre", "N/A")
                )
            console.print(yara_table)
            
        # PE Analysis
        pe = report.get("pe_analysis", {})
        if pe.get("is_pe") and pe.get("suspicious_apis"):
            api_table = Table(title="[bold yellow]Suspicious Windows API Imports[/bold yellow]", show_header=True, header_style="bold yellow")
            api_table.add_column("API Function")
            api_table.add_column("Category")
            api_table.add_column("MITRE ID")
            api_table.add_column("Description")
            for a in pe["suspicious_apis"]:
                api_table.add_row(a["function"], a["category"], a["mitre"], a["description"])
            console.print(api_table)

        # AI Threat Intelligence
        ai = report.get("ai_analysis", {})
        if ai:
            ai_text = Text()
            ai_text.append(f"{ai['summary']}\n\n", style="white")
            if ai.get("mitre_attack_tactics"):
                ai_text.append(f"Mapped MITRE Tactics: {', '.join(ai['mitre_attack_tactics'])}\n\n", style="bold cyan")
            ai_text.append("Actionable Steps:\n", style="bold yellow")
            for r in ai.get("actionable_recommendations", []):
                ai_text.append(f" • {r}\n", style="dim")
            console.print(Panel(ai_text, title="[bold magenta]AI Threat Analysis & Mitigation[/bold magenta]", border_style="magenta"))
            
    except ImportError:
        # Fallback Plain Text Rendering
        print(f"\n=======================================================")
        print(f" Target File: {report['file_name']}")
        print(f" Verdict:     {report['verdict']} (Score: {report['risk_score']}/100)")
        print(f" File Type:   {report['file_type']}")
        print(f" File Size:   {report['file_size_bytes']} bytes")
        print(f" SHA256:      {report['hashes']['sha256']}")
        print(f" Entropy:     {report['entropy']} / 8.0")
        print(f"-------------------------------------------------------")
        if report.get("yara_matches"):
            print(" [!] YARA Rule Matches:")
            for y in report["yara_matches"]:
                print(f"     - {y['rule']} ({y.get('meta', {}).get('description', '')})")
        if report.get("pe_analysis", {}).get("suspicious_apis"):
            print(" [!] Suspicious PE APIs:")
            for a in report["pe_analysis"]["suspicious_apis"]:
                print(f"     - {a['function']} [{a['category']}] -> {a['mitre']}")
        print(f"-------------------------------------------------------")
        print(f" AI Summary:  {report.get('ai_analysis', {}).get('summary', 'N/A')}")
        print(f"=======================================================\n")

def scan_target(target_path: str, quarantine: bool = False, json_output: bool = False):
    analyzer = MalGuardAnalyzer()
    
    if os.path.isfile(target_path):
        report = analyzer.scan_file(target_path)
        if json_output:
            print(json.dumps(report, indent=2))
        else:
            render_rich_report(report)
            
        if quarantine and report["verdict"] in ["MALICIOUS", "SUSPICIOUS"]:
            q_res = quarantine_file(target_path, report)
            if not json_output:
                print(f"[!] Quarantine Result: {q_res.get('message', q_res.get('error'))}")
    elif os.path.isdir(target_path):
        results = []
        for root, _, files in os.walk(target_path):
            for file in files:
                p = os.path.join(root, file)
                try:
                    rep = analyzer.scan_file(p)
                    results.append(rep)
                    if not json_output:
                        render_rich_report(rep)
                    if quarantine and rep["verdict"] == "MALICIOUS":
                        quarantine_file(p, rep)
                except Exception as e:
                    if not json_output:
                        print(f"[-] Error scanning {file}: {e}")
        if json_output:
            print(json.dumps(results, indent=2))
    else:
        print(f"[-] Error: Path does not exist: {target_path}")

def scan_url_target(url: str, json_output: bool = False):
    analyzer = MalGuardAnalyzer()
    res = analyzer.scan_url(url)
    if json_output:
        print(json.dumps(res, indent=2))
    else:
        print(f"\n=======================================================")
        print(f" Target URL:    {res['url']}")
        print(f" Status Code:   {res.get('status_code', 'N/A')}")
        print(f" Final URL:     {res.get('final_url', 'N/A')}")
        print(f" Risk Score:    {res.get('heuristics_score', 0)}")
        print(f"-------------------------------------------------------")
        if res.get("suspicious_indicators"):
            print(" [!] Suspicious Website Indicators:")
            for ind in res["suspicious_indicators"]:
                print(f"     - [{ind['category']}] {ind['description']} ({ind.get('mitre', '')})")
        if res.get("hidden_iframes"):
            print(f" [!] Hidden Iframes: {len(res['hidden_iframes'])}")
        print(f"=======================================================\n")

def main():
    parser = argparse.ArgumentParser(description="MalGuard AI — Automated Malware Scanner & Static Triage")
    parser.add_argument("target", nargs="?", default="", help="Path to file or directory to scan")
    parser.add_argument("--url", help="URL / website to scan for phishing & malicious scripts")
    parser.add_argument("--json", action="store_true", help="Output results in raw JSON")
    parser.add_argument("--quarantine", action="store_true", help="Automatically neutralize and quarantine malicious files")
    parser.add_argument("--no-banner", action="store_true", help="Suppress startup banner")
    
    args = parser.parse_args()
    
    if not args.no_banner and not args.json:
        print_banner()
        
    if args.url:
        scan_url_target(args.url, json_output=args.json)
    elif args.target:
        scan_target(args.target, quarantine=args.quarantine, json_output=args.json)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
