from fastapi import APIRouter
import os
import glob
from typing import Dict, Any, List
from ..database.db import get_connection
from ..rag.ingestion import load_all_notes

router = APIRouter(prefix="/api/sources", tags=["sources"])

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

@router.get("/summary", response_model=Dict[str, Any])
async def get_data_sources_summary():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM leads")
    leads_count = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM companies")
    comp_count = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM activities")
    act_count = cur.fetchone()[0] or 0

    cur.execute("SELECT MAX(timestamp) FROM activities")
    latest_ts = cur.fetchone()[0] or "2026-09-26 15:20:00"

    conn.close()

    notes_dir = os.path.join(DATA_DIR, "notes")
    notes_files = glob.glob(os.path.join(notes_dir, "*.txt")) if os.path.exists(notes_dir) else []

    return {
        "status": "OPERATIONAL_CONNECTED",
        "database": "data/prioritiq.db (WAL Mode)",
        "last_synced": latest_ts,
        "sources": [
            {
                "name": "prioritiq.db: leads",
                "type": "CRM Structured Data (Indexed)",
                "records_count": leads_count,
                "status": "ACTIVE_DATABASE"
            },
            {
                "name": "prioritiq.db: companies",
                "type": "Firmographic Enterprise Accounts (Indexed)",
                "records_count": comp_count,
                "status": "ACTIVE_DATABASE"
            },
            {
                "name": "prioritiq.db: activities",
                "type": "Telemetry & Sales Engagements (Indexed)",
                "records_count": act_count,
                "status": "ACTIVE_DATABASE"
            },
            {
                "name": "notes/ & knowledge docs",
                "type": "Unstructured RAG Corpus (Emails, Calls, Redlines)",
                "records_count": len(notes_files),
                "documents": [os.path.basename(f) for f in notes_files],
                "status": "INDEXED_HYBRID"
            }
        ]
    }

@router.get("/notes", response_model=List[Dict[str, Any]])
async def get_all_notes_content():
    return load_all_notes()
