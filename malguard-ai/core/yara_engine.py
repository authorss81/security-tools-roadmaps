import os
import re
from typing import Dict, Any, List

RULES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rules", "malware_rules.yar")

class YaraEngine:
    """YARA Scanner with automatic fallback to high-speed native pattern matching."""
    
    def __init__(self, rule_file: str = RULES_PATH):
        self.rule_file = rule_file
        self.yara_available = False
        self.compiled_rules = None
        
        try:
            import yara
            if os.path.exists(self.rule_file):
                self.compiled_rules = yara.compile(filepath=self.rule_file)
                self.yara_available = True
        except Exception:
            self.yara_available = False

    def scan(self, data: bytes) -> List[Dict[str, Any]]:
        """Scan byte array with YARA if available, or native signature fallback."""
        if self.yara_available and self.compiled_rules:
            return self._scan_yara(data)
        else:
            return self._scan_native_fallback(data)

    def _scan_yara(self, data: bytes) -> List[Dict[str, Any]]:
        matches = self.compiled_rules.match(data=data)
        results = []
        for m in matches:
            results.append({
                "rule": m.rule,
                "tags": m.tags,
                "meta": m.meta,
                "matched_strings": [str(s) for s in m.strings[:5]],
                "engine": "yara-c"
            })
        return results

    def _scan_native_fallback(self, data: bytes) -> List[Dict[str, Any]]:
        """Native pure-python signature detection matching malware_rules.yar."""
        matches = []
        data_lower = data.lower()

        # EICAR
        if b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*" in data:
            matches.append({
                "rule": "EICAR_Test_File",
                "meta": {"description": "Standard EICAR Antivirus Test File", "severity": "INFO", "threat_level": 0},
                "matched_strings": ["EICAR test string match"],
                "engine": "malguard-native"
            })

        # Ransomware
        ransom_hits = []
        ransom_patterns = [
            b"vssadmin delete shadows", b"vssadmin.exe delete shadows",
            b"bcdedit /set {default} recoveryenabled no", b"bcdedit /set {default} bootstatuspolicy ignoreallfailures",
            b"wbadmin delete catalog", b"your files have been encrypted",
            b"all your files are encrypted", b"decrypt_instruction", b"how_to_recover_files"
        ]
        for p in ransom_patterns:
            if p in data_lower:
                ransom_hits.append(p.decode(errors="ignore"))
        if len(ransom_hits) >= 2:
            matches.append({
                "rule": "Generic_Ransomware_Indicators",
                "meta": {"description": "Common Ransomware Commands and Behaviors", "severity": "CRITICAL", "threat_level": 90, "mitre": "T1486, T1490"},
                "matched_strings": ransom_hits,
                "engine": "malguard-native"
            })

        # WebShell
        webshell_patterns = [
            b"eval(base64_decode(", b"eval($_post[", b"assert($_post[",
            b"system($_get[", b"passthru($_request[", b"c99shell", b"r57shell", b"b374k", b"wso web shell"
        ]
        ws_hits = [p.decode(errors="ignore") for p in webshell_patterns if p in data_lower]
        if ws_hits:
            matches.append({
                "rule": "Generic_WebShell",
                "meta": {"description": "Common PHP/JSP/ASP WebShell Indicators", "severity": "HIGH", "threat_level": 85, "mitre": "T1505.003"},
                "matched_strings": ws_hits,
                "engine": "malguard-native"
            })

        # Mimikatz
        mimikatz_patterns = [
            b"sekurlsa::logonpasswords", b"lsadump::sam", b"privilege::debug",
            b"kerberos::golden", b"wdigest.dll", b"gentilkiwi"
        ]
        mimi_hits = [p.decode(errors="ignore") for p in mimikatz_patterns if p in data_lower]
        if mimi_hits:
            matches.append({
                "rule": "Credential_Theft_Mimikatz_Artifacts",
                "meta": {"description": "Mimikatz and LSASS Memory Dumping Artifacts", "severity": "CRITICAL", "threat_level": 95, "mitre": "T1003.001"},
                "matched_strings": mimi_hits,
                "engine": "malguard-native"
            })

        # Malicious PowerShell
        ps_patterns = [
            b"iex (new-object net.webclient).downloadstring", b"invoke-expression",
            b"-executionpolicy bypass -noprofile -windowstyle hidden",
            b"[system.convert]::frombase64string(", b"net.sockets.tcpclient",
            b"powershell.exe -enc", b"powershell.exe -e "
        ]
        ps_hits = [p.decode(errors="ignore") for p in ps_patterns if p in data_lower]
        if len(ps_hits) >= 2 or (b"downloadstring" in data_lower and b"iex" in data_lower):
            matches.append({
                "rule": "Malicious_PowerShell_Download_Exec",
                "meta": {"description": "PowerShell In-Memory Download Cradle and Obfuscation", "severity": "HIGH", "threat_level": 80, "mitre": "T1059.001"},
                "matched_strings": ps_hits,
                "engine": "malguard-native"
            })

        # Reverse Shell
        rev_patterns = [
            b"/bin/sh -i >& /dev/tcp/", b"/bin/bash -i >& /dev/tcp/",
            b"mkfifo /tmp/f", b"nc -e /bin/sh", b"nc -e /bin/bash",
            b"import socket,subprocess,os;s=socket.socket", b"nc.exe -e cmd.exe"
        ]
        rev_hits = [p.decode(errors="ignore") for p in rev_patterns if p in data_lower]
        if rev_hits:
            matches.append({
                "rule": "Reverse_Shell_Payload",
                "meta": {"description": "Common Reverse Shell Scripts and One-Liners", "severity": "HIGH", "threat_level": 85, "mitre": "T1059"},
                "matched_strings": rev_hits,
                "engine": "malguard-native"
            })

        # Office Macro execution
        macro_hits = []
        for m in [b"autoopen", b"workbook_open", b"document_open"]:
            if m in data_lower:
                macro_hits.append(m.decode(errors="ignore"))
        for s in [b"wscript.shell", b"shellexecute", b"urldownloadtofile"]:
            if s in data_lower:
                macro_hits.append(s.decode(errors="ignore"))
        if len(macro_hits) >= 2:
            matches.append({
                "rule": "Suspicious_Macro_OLE_Execution",
                "meta": {"description": "Malicious Office VBA Macro Execution Primitives", "severity": "HIGH", "threat_level": 75, "mitre": "T1204.002"},
                "matched_strings": macro_hits,
                "engine": "malguard-native"
            })

        return matches
