import struct
import datetime
from typing import Dict, Any, List
from .hasher import calculate_entropy

# Suspicious Windows API imports mapped to MITRE ATT&CK
SUSPICIOUS_APIS = {
    # Process Injection (T1055)
    "VirtualAlloc": {"category": "Process Injection", "mitre": "T1055", "severity": "HIGH", "desc": "Allocates virtual memory regions"},
    "VirtualAllocEx": {"category": "Process Injection", "mitre": "T1055", "severity": "CRITICAL", "desc": "Allocates memory in remote processes"},
    "WriteProcessMemory": {"category": "Process Injection", "mitre": "T1055", "severity": "CRITICAL", "desc": "Writes payload into target process memory"},
    "CreateRemoteThread": {"category": "Process Injection", "mitre": "T1055", "severity": "CRITICAL", "desc": "Executes thread in remote process"},
    "SetThreadContext": {"category": "Process Injection", "mitre": "T1055", "severity": "HIGH", "desc": "Modifies CPU registers of a thread"},
    "QueueUserAPC": {"category": "Process Injection", "mitre": "T1055", "severity": "HIGH", "desc": "Asynchronous procedure call injection"},
    "NtMapViewOfSection": {"category": "Process Injection", "mitre": "T1055", "severity": "HIGH", "desc": "Process hollowing section mapping"},
    
    # Defense Evasion / Anti-Analysis (T1497)
    "IsDebuggerPresent": {"category": "Anti-Debugging", "mitre": "T1497", "severity": "MEDIUM", "desc": "Checks if PEB BeingDebugged flag is set"},
    "CheckRemoteDebuggerPresent": {"category": "Anti-Debugging", "mitre": "T1497", "severity": "MEDIUM", "desc": "Checks if attached to debugger"},
    "OutputDebugStringA": {"category": "Anti-Debugging", "mitre": "T1497", "severity": "LOW", "desc": "Emits string to debugger"},
    "OutputDebugStringW": {"category": "Anti-Debugging", "mitre": "T1497", "severity": "LOW", "desc": "Emits string to debugger"},
    "NtQueryInformationProcess": {"category": "Anti-Debugging", "mitre": "T1497", "severity": "HIGH", "desc": "Queries debug port and environment"},
    
    # Persistence (T1547.001)
    "RegSetValueExA": {"category": "Persistence", "mitre": "T1547.001", "severity": "MEDIUM", "desc": "Modifies registry keys (e.g. Run keys)"},
    "RegSetValueExW": {"category": "Persistence", "mitre": "T1547.001", "severity": "MEDIUM", "desc": "Modifies registry keys (e.g. Run keys)"},
    "CreateServiceA": {"category": "Persistence", "mitre": "T1543.003", "severity": "HIGH", "desc": "Installs a new Windows service"},
    "CreateServiceW": {"category": "Persistence", "mitre": "T1543.003", "severity": "HIGH", "desc": "Installs a new Windows service"},
    
    # Spyware / Collection (T1056 / T1113)
    "GetAsyncKeyState": {"category": "Keylogging", "mitre": "T1056.001", "severity": "HIGH", "desc": "Monitors keystroke state"},
    "GetKeyState": {"category": "Keylogging", "mitre": "T1056.001", "severity": "MEDIUM", "desc": "Retrieves status of virtual key"},
    "SetWindowsHookExA": {"category": "Keylogging / Hooking", "mitre": "T1056.001", "severity": "HIGH", "desc": "Installs global keyboard/mouse hooks"},
    "BitBlt": {"category": "Screen Capture", "mitre": "T1113", "severity": "MEDIUM", "desc": "Performs bitmap screen captures"},
    
    # Ingress / C2 Download (T1105)
    "URLDownloadToFileA": {"category": "Downloader", "mitre": "T1105", "severity": "HIGH", "desc": "Downloads remote payload directly to disk"},
    "URLDownloadToFileW": {"category": "Downloader", "mitre": "T1105", "severity": "HIGH", "desc": "Downloads remote payload directly to disk"},
    "InternetOpenA": {"category": "Network C2", "mitre": "T1071", "severity": "LOW", "desc": "Initializes WinINet HTTP connection"},
    "WinHttpOpen": {"category": "Network C2", "mitre": "T1071", "severity": "LOW", "desc": "Initializes WinHTTP session"},
    
    # Ransomware / Encryption (T1486)
    "CryptEncrypt": {"category": "Ransomware / Crypto", "mitre": "T1486", "severity": "HIGH", "desc": "Encrypts data buffer with CryptoAPI"},
    "BCryptEncrypt": {"category": "Ransomware / Crypto", "mitre": "T1486", "severity": "HIGH", "desc": "CNG encryption routine"}
}

def analyze_pe(file_bytes: bytes) -> Dict[str, Any]:
    """Analyze Windows PE binary using pefile if available, or fallback parser."""
    if not file_bytes.startswith(b"MZ"):
        return {"is_pe": False}

    try:
        import pefile
        return _analyze_with_pefile(file_bytes)
    except ImportError:
        return _analyze_with_fallback(file_bytes)

def _analyze_with_pefile(file_bytes: bytes) -> Dict[str, Any]:
    import pefile
    try:
        pe = pefile.PE(data=file_bytes)
    except Exception as e:
        return {"is_pe": True, "error": f"Failed to parse PE: {str(e)}"}

    sections_info = []
    suspicious_sections = []
    
    for sec in pe.sections:
        name = sec.Name.decode(errors="ignore").strip("\x00")
        sec_data = sec.get_data()
        entropy = calculate_entropy(sec_data)
        is_high_entropy = entropy > 7.0
        
        # Check if section is both Writable and Executable (W^X violation)
        characteristics = sec.Characteristics
        is_wx = bool((characteristics & 0x80000000) and (characteristics & 0x20000000))
        
        info = {
            "name": name,
            "virtual_address": hex(sec.VirtualAddress),
            "virtual_size": sec.Misc_VirtualSize,
            "raw_size": sec.SizeOfRawData,
            "entropy": entropy,
            "is_packed_likely": is_high_entropy,
            "is_writable_and_executable": is_wx
        }
        sections_info.append(info)
        
        if is_high_entropy or is_wx or name.lower() in [".upx0", ".upx1", ".aspack", ".themida"]:
            suspicious_sections.append(info)

    # Extract imports
    imports = []
    detected_suspicious_apis = []
    imphash = ""
    try:
        imphash = pe.get_imphash()
    except Exception:
        imphash = ""

    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            dll_name = entry.dll.decode(errors="ignore") if entry.dll else "UNKNOWN"
            dll_funcs = []
            for imp in entry.imports:
                func_name = imp.name.decode(errors="ignore") if imp.name else (f"Ord({imp.ordinal})" if imp.ordinal else "")
                if func_name:
                    dll_funcs.append(func_name)
                    if func_name in SUSPICIOUS_APIS:
                        api_meta = SUSPICIOUS_APIS[func_name]
                        detected_suspicious_apis.append({
                            "dll": dll_name,
                            "function": func_name,
                            "category": api_meta["category"],
                            "mitre": api_meta["mitre"],
                            "severity": api_meta["severity"],
                            "description": api_meta["desc"]
                        })
            imports.append({"dll": dll_name, "count": len(dll_funcs)})

    # Compile timestamp
    timestamp = pe.FILE_HEADER.TimeDateStamp
    try:
        compilation_time = datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        compilation_time = "Invalid/Forged"

    # Machine Architecture
    machine_type = "x86 (32-bit)" if pe.FILE_HEADER.Machine == 0x14c else ("x64 (64-bit)" if pe.FILE_HEADER.Machine == 0x8664 else hex(pe.FILE_HEADER.Machine))

    # TLS Callbacks (Anti-Analysis / Early Execution)
    has_tls = hasattr(pe, "DIRECTORY_ENTRY_TLS") and pe.DIRECTORY_ENTRY_TLS is not None

    return {
        "is_pe": True,
        "machine": machine_type,
        "compilation_time": compilation_time,
        "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
        "imphash": imphash,
        "has_tls_callbacks": has_tls,
        "sections_count": len(sections_info),
        "sections": sections_info,
        "suspicious_sections": suspicious_sections,
        "imported_dlls_count": len(imports),
        "suspicious_apis": detected_suspicious_apis
    }

def _analyze_with_fallback(file_bytes: bytes) -> Dict[str, Any]:
    """Lightweight built-in PE header parser without external dependencies."""
    if len(file_bytes) < 64:
        return {"is_pe": False}
        
    pe_offset = struct.unpack_from("<I", file_bytes, 0x3c)[0]
    if pe_offset + 24 > len(file_bytes):
        return {"is_pe": False}
        
    pe_sig = file_bytes[pe_offset : pe_offset + 4]
    if pe_sig != b"PE\x00\x00":
        return {"is_pe": False}
        
    machine = struct.unpack_from("<H", file_bytes, pe_offset + 4)[0]
    machine_str = "x86 (32-bit)" if machine == 0x14c else ("x64 (64-bit)" if machine == 0x8664 else hex(machine))
    num_sections = struct.unpack_from("<H", file_bytes, pe_offset + 6)[0]
    time_date_stamp = struct.unpack_from("<I", file_bytes, pe_offset + 8)[0]
    
    try:
        compilation_time = datetime.datetime.utcfromtimestamp(time_date_stamp).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        compilation_time = "Unknown"

    # Search for known suspicious API strings directly in raw binary
    detected_suspicious_apis = []
    for api, meta in SUSPICIOUS_APIS.items():
        if api.encode() in file_bytes:
            detected_suspicious_apis.append({
                "dll": "Detected in Strings",
                "function": api,
                "category": meta["category"],
                "mitre": meta["mitre"],
                "severity": meta["severity"],
                "description": meta["desc"]
            })

    return {
        "is_pe": True,
        "machine": machine_str,
        "compilation_time": compilation_time,
        "entry_point": "N/A (Install pefile for deep structure)",
        "imphash": "N/A",
        "has_tls_callbacks": False,
        "sections_count": num_sections,
        "sections": [],
        "suspicious_sections": [],
        "imported_dlls_count": 0,
        "suspicious_apis": detected_suspicious_apis
    }
