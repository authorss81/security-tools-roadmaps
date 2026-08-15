import os
import json
import shutil
from datetime import datetime
from typing import Dict, Any

DEFAULT_QUARANTINE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "quarantine_vault")
XOR_KEY = 0x5A  # Simple byte scrambling to neutralize execution

def quarantine_file(file_path: str, scan_result: Dict[str, Any], vault_dir: str = DEFAULT_QUARANTINE_DIR) -> Dict[str, Any]:
    """Safely encrypt and move a malicious file into the quarantine vault."""
    if not os.path.exists(file_path):
        return {"success": False, "error": f"File not found: {file_path}"}
        
    os.makedirs(vault_dir, exist_ok=True)
    
    file_name = os.path.basename(file_path)
    sha256 = scan_result.get("hashes", {}).get("sha256", "unknown_hash")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    
    vault_file_name = f"{timestamp}_{sha256[:12]}_{file_name}.quarantine"
    vault_file_path = os.path.join(vault_dir, vault_file_name)
    meta_file_path = os.path.join(vault_dir, f"{vault_file_name}.json")
    
    try:
        with open(file_path, "rb") as f:
            raw_bytes = f.read()
            
        # Neutralize with XOR
        neutralized_bytes = bytes([b ^ XOR_KEY for b in raw_bytes])
        
        with open(vault_file_path, "wb") as f:
            f.write(neutralized_bytes)
            
        metadata = {
            "original_path": os.path.abspath(file_path),
            "original_filename": file_name,
            "quarantined_at": datetime.utcnow().isoformat() + "Z",
            "sha256": sha256,
            "risk_score": scan_result.get("risk_score", 0),
            "verdict": scan_result.get("verdict", "UNKNOWN"),
            "vault_file": vault_file_name
        }
        
        with open(meta_file_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
            
        # Remove original malicious file
        os.remove(file_path)
        
        return {
            "success": True,
            "vault_file_path": vault_file_path,
            "metadata_file_path": meta_file_path,
            "message": f"Successfully quarantined and neutralized: {file_name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def restore_file(vault_file_path: str, destination_path: str) -> Dict[str, Any]:
    """Restore a neutralized quarantined file back to its original raw state."""
    if not os.path.exists(vault_file_path):
        return {"success": False, "error": "Quarantine vault file not found."}
        
    try:
        with open(vault_file_path, "rb") as f:
            neutralized = f.read()
            
        original_bytes = bytes([b ^ XOR_KEY for b in neutralized])
        
        dest_dir = os.path.dirname(destination_path)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
            
        with open(destination_path, "wb") as f:
            f.write(original_bytes)
            
        return {"success": True, "restored_path": destination_path}
    except Exception as e:
        return {"success": False, "error": str(e)}
