import hashlib
import math
import mimetypes
from typing import Dict, Any, List

def calculate_hashes(file_bytes: bytes) -> Dict[str, str]:
    """Calculate standard cryptographic hashes for a byte array."""
    md5 = hashlib.md5(file_bytes).hexdigest()
    sha1 = hashlib.sha1(file_bytes).hexdigest()
    sha256 = hashlib.sha256(file_bytes).hexdigest()
    return {
        "md5": md5,
        "sha1": sha1,
        "sha256": sha256
    }

def calculate_entropy(data: bytes) -> float:
    """
    Calculate Shannon entropy of byte data (0.0 to 8.0).
    Values > 7.0 typically indicate encryption, obfuscation, or compression (e.g. packed malware).
    """
    if not data:
        return 0.0
    
    entropy = 0.0
    length = len(data)
    byte_counts = [0] * 256
    
    for byte in data:
        byte_counts[byte] += 1
        
    for count in byte_counts:
        if count > 0:
            p = float(count) / length
            entropy -= p * math.log2(p)
            
    return round(entropy, 4)

def calculate_sliding_window_entropy(data: bytes, window_size: int = 1024, step: int = 512) -> List[Dict[str, Any]]:
    """Generate sliding window entropy points to detect packed/encrypted payload blocks."""
    points = []
    data_len = len(data)
    
    if data_len < window_size:
        return [{"offset": 0, "entropy": calculate_entropy(data)}]
        
    for offset in range(0, data_len - window_size + 1, step):
        chunk = data[offset : offset + window_size]
        ent = calculate_entropy(chunk)
        points.append({
            "offset": offset,
            "entropy": ent
        })
    return points

def get_byte_distribution(data: bytes) -> Dict[str, int]:
    """Calculate frequencies of null bytes, printable ASCII, and high non-ASCII bytes."""
    if not data:
        return {"null_bytes": 0, "printable_ascii": 0, "non_ascii": 0}
        
    nulls = 0
    printable = 0
    non_ascii = 0
    
    for b in data:
        if b == 0:
            nulls += 1
        elif 32 <= b <= 126 or b in (9, 10, 13):
            printable += 1
        else:
            non_ascii += 1
            
    total = len(data)
    return {
        "null_percent": round((nulls / total) * 100, 2),
        "printable_ascii_percent": round((printable / total) * 100, 2),
        "non_ascii_percent": round((non_ascii / total) * 100, 2)
    }

def detect_file_type(data: bytes, file_path: str = "") -> str:
    """Detect file magic format based on signature headers and extension."""
    if data.startswith(b"MZ"):
        return "Windows Executable (PE/DLL)"
    elif data.startswith(b"\x7fELF"):
        return "Linux Executable (ELF)"
    elif data.startswith(b"%PDF"):
        return "Adobe PDF Document"
    elif data.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
        return "Microsoft Office Legacy (OLE2/DOC/XLS)"
    elif data.startswith(b"PK\x03\x04"):
        if file_path.endswith((".docx", ".xlsx", ".pptx")):
            return "Microsoft Office Modern (OpenXML)"
        elif file_path.endswith(".apk"):
            return "Android Application Package (APK)"
        elif file_path.endswith(".jar"):
            return "Java Archive (JAR)"
        return "ZIP Archive"
    elif data.startswith(b"Rar!\x1a\x07"):
        return "RAR Archive"
    elif data.startswith(b"\x1f\x8b"):
        return "GZIP Compressed Archive"
    elif data.startswith(b"7z\xbc\xaf\x27\x1c"):
        return "7-Zip Archive"
    elif b"powershell" in data.lower() or b"$env:" in data.lower() or file_path.endswith(".ps1"):
        return "PowerShell Script"
    elif b"wscript" in data.lower() or b"cscript" in data.lower() or file_path.endswith(".vbs"):
        return "VBScript"
    elif b"#!/bin/bash" in data or b"#!/bin/sh" in data or file_path.endswith(".sh"):
        return "Shell Script"
    elif data.startswith(b"<!DOCTYPE html") or data.startswith(b"<html") or b"<script" in data:
        return "HTML / Web Page"
    
    guessed, _ = mimetypes.guess_type(file_path)
    return guessed if guessed else "Generic Binary / Unknown"
