import os
import sys
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.analyzer import MalGuardAnalyzer

app = FastAPI(
    title="MalGuard AI — Automated Malware Scanner API",
    description="Multi-engine static triage, YARA scanning, PE entropy inspection, and AI threat assessment.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = MalGuardAnalyzer()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MalGuard AI Scanner",
        "yara_engine": "active",
        "version": "1.0.0"
    }

@app.post("/api/scan")
async def scan_file_upload(file: UploadFile = File(...)):
    """Upload a file to perform instant static malware triage and risk scoring."""
    try:
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
            
        report = analyzer.scan_bytes(content, file.filename)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    """Serve the web dashboard interface."""
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "index.html")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>MalGuard AI API is active. UI file not found.</h1>"

if __name__ == "__main__":
    import uvicorn
    print("Starting MalGuard AI Web Server on http://localhost:8000 ...")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
