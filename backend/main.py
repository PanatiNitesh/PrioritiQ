import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routes.decisions import router as decisions_router
from .routes.leads import router as leads_router
from .routes.sources import router as sources_router
from .database.db import get_connection
from .decision.audit import verify_audit_chain_integrity

app = FastAPI(
    title="PrioritiQ Decision Engine API",
    description="Enterprise Evidence-Grounded AI Sales Decision Engine Backend",
    version="2.0.0"
)

# Enable CORS for frontend workspace
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(decisions_router)
app.include_router(leads_router)
app.include_router(sources_router)

DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(DIST_DIR):
    assets_dir = os.path.join(DIST_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.api_route("/", methods=["GET", "HEAD"])
def read_root(request: Request):
    accept = request.headers.get("accept", "")
    index_file = os.path.join(DIST_DIR, "index.html")
    if "text/html" in accept and os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "engine": "PrioritiQ",
        "description": "Enterprise Evidence-Grounded AI Sales Decision Engine",
        "version": "2.0.0",
        "status": "ONLINE",
        "architecture": "Deterministic Multi-Factor Analytics + Hybrid Semantic RAG + 2D Knapsack DP + Cryptographic SHA-256 Ledger + Human Governance"
    }

@app.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    """
    Comprehensive system health diagnostics:
    - Verifies SQLite WAL database connectivity and table row counts
    - Cryptographically validates audit ledger chain of custody
    - Verifies knowledge corpus documents
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM leads")
        leads_count = cur.fetchone()[0] or 0
        cur.execute("SELECT COUNT(*) FROM companies")
        companies_count = cur.fetchone()[0] or 0
        cur.execute("SELECT COUNT(*) FROM activities")
        activities_count = cur.fetchone()[0] or 0
        cur.execute("SELECT COUNT(*) FROM decisions")
        decisions_count = cur.fetchone()[0] or 0
        cur.execute("SELECT COUNT(*) FROM audit_ledger")
        audit_blocks_count = cur.fetchone()[0] or 0
        conn.close()

        # Audit chain verification check
        audit_status = verify_audit_chain_integrity()

        notes_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "notes"))
        notes_count = len(os.listdir(notes_dir)) if os.path.exists(notes_dir) else 0

        return {
            "status": "healthy",
            "version": "2.0.0",
            "database": {
                "engine": "SQLite WAL Mode",
                "connected": True,
                "leads": leads_count,
                "companies": companies_count,
                "activities": activities_count,
                "decisions": decisions_count,
                "audit_blocks": audit_blocks_count
            },
            "audit_chain": {
                "valid": audit_status.get("valid", True),
                "verified_blocks": audit_status.get("verified_blocks", 0),
                "latest_hash": audit_status.get("latest_block_hash", "")[:16] + "..." if audit_status.get("latest_block_hash") else ""
            },
            "rag_knowledge_base": {
                "status": "INDEXED",
                "document_count": notes_count
            }
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }

if os.path.exists(DIST_DIR):
    @app.api_route("/{full_path:path}", methods=["GET", "HEAD"])
    async def serve_spa(full_path: str):
        # Allow API routes to be handled or return 404
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API route not found")
        file_path = os.path.join(DIST_DIR, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        index_file = os.path.join(DIST_DIR, "index.html")
        if os.path.isfile(index_file):
            return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="Resource not found")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=False)

