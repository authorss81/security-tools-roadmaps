import zipfile
import re
import io
from typing import Dict, Any, List

DANGEROUS_PERMISSIONS = {
    "android.permission.SEND_SMS": {"severity": "HIGH", "category": "Financial / Fraud", "desc": "Send SMS messages (Toll fraud)"},
    "android.permission.READ_SMS": {"severity": "HIGH", "category": "Privacy / 2FA Theft", "desc": "Read SMS / OTP verification codes"},
    "android.permission.RECEIVE_SMS": {"severity": "HIGH", "category": "Interception", "desc": "Intercept incoming SMS / OTP codes"},
    "android.permission.RECORD_AUDIO": {"severity": "HIGH", "category": "Spyware", "desc": "Record background audio via microphone"},
    "android.permission.CAMERA": {"severity": "MEDIUM", "category": "Spyware", "desc": "Access device camera"},
    "android.permission.ACCESS_FINE_LOCATION": {"severity": "MEDIUM", "category": "Tracking", "desc": "Precise GPS location tracking"},
    "android.permission.SYSTEM_ALERT_WINDOW": {"severity": "HIGH", "category": "Overlay Attack", "desc": "Draw overlays over banking apps / lock screen"},
    "android.permission.REQUEST_INSTALL_PACKAGES": {"severity": "HIGH", "category": "Dropper", "desc": "Silently install secondary APKs"},
    "android.permission.RECEIVE_BOOT_COMPLETED": {"severity": "MEDIUM", "category": "Persistence", "desc": "Auto-start payload when device reboots"},
    "android.permission.READ_CONTACTS": {"severity": "MEDIUM", "category": "Exfiltration", "desc": "Harvest user contact address book"},
    "android.permission.BIND_ACCESSIBILITY_SERVICE": {"severity": "CRITICAL", "category": "Accessibility Hijacking", "desc": "Full remote control of Android UI"}
}

def analyze_apk(file_bytes: bytes) -> Dict[str, Any]:
    """Inspect Android APK packages (permissions, DEX bytecode indicators, native .so files)."""
    results = {
        "is_apk": False,
        "package_name": "Unknown",
        "suspicious_permissions": [],
        "suspicious_dex_strings": [],
        "native_libraries": [],
        "heuristics_score": 0
    }
    
    if not file_bytes.startswith(b"PK\x03\x04"):
        return results
        
    try:
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
            namelist = z.namelist()
            if "AndroidManifest.xml" not in namelist and "classes.dex" not in namelist:
                return results
                
            results["is_apk"] = True
            
            # 1. Inspect AndroidManifest.xml for permissions
            if "AndroidManifest.xml" in namelist:
                manifest_bytes = z.read("AndroidManifest.xml")
                manifest_str = manifest_bytes.decode("latin-1", errors="ignore")
                
                for perm, meta in DANGEROUS_PERMISSIONS.items():
                    # Android permissions appear in binary XML or raw format
                    clean_name = perm.split(".")[-1]
                    if perm in manifest_str or clean_name in manifest_str:
                        results["suspicious_permissions"].append({
                            "permission": perm,
                            "severity": meta["severity"],
                            "category": meta["category"],
                            "description": meta["desc"]
                        })
                        if meta["severity"] == "CRITICAL":
                            results["heuristics_score"] += 35
                        elif meta["severity"] == "HIGH":
                            results["heuristics_score"] += 20
                        else:
                            results["heuristics_score"] += 10

            # 2. Inspect classes.dex for malicious C2 or dropper keywords
            dex_files = [f for f in namelist if f.endswith(".dex")]
            for dex_name in dex_files[:3]:
                dex_data = z.read(dex_name)
                dex_lower = dex_data.lower()
                
                indicators = [
                    (b"http://", "Plaintext HTTP C2 traffic / unencrypted communication", 15),
                    (b"/system/bin/su", "Root exploit check / privilege escalation", 25),
                    (b"accessibilityservice", "Accessibility service hijacking", 30),
                    (b"smsreceiver", "SMS broadcast receiver / OTP stealing", 25),
                    (b"dexclassloader", "Dynamic DEX code loading (payload dropper)", 30),
                    (b"dalvik.system.pathclassloader", "Dynamic code loading", 20)
                ]
                
                for term, desc, score in indicators:
                    if term in dex_lower:
                        results["suspicious_dex_strings"].append({
                            "keyword": term.decode(),
                            "description": desc,
                            "score_impact": score
                        })
                        results["heuristics_score"] += score

            # 3. Check for native .so libraries
            results["native_libraries"] = [f for f in namelist if f.startswith("lib/") and f.endswith(".so")]

    except Exception:
        pass
        
    return results
