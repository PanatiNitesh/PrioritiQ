from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
import os
import pandas as pd
from ..analytics.lead_scoring import compute_deterministic_scores
from ..analytics.metrics import get_lead_delta_since_yesterday
from ..rag.retrieval import get_evidence_for_lead

router = APIRouter(prefix="/api/leads", tags=["leads"])

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

@router.get("", response_model=List[Dict[str, Any]])
async def list_leads(stage: Optional[str] = None, rep: Optional[str] = None):
    scores_df = compute_deterministic_scores(priority_weight="balanced")
    
    if stage:
        scores_df = scores_df[scores_df['stage'].str.lower() == stage.lower()]
    if rep:
        scores_df = scores_df[scores_df['assigned_rep'].str.lower() == rep.lower()]
        
    leads = scores_df.to_dict(orient="records")
    for l in leads:
        l['delta_info'] = get_lead_delta_since_yesterday(l['lead_id'])
    return leads

from ..database.db import get_lead_by_id, get_activities_for_lead

@router.get("/{lead_id}", response_model=Dict[str, Any])
async def get_lead_detail(lead_id: str):
    lead_data = get_lead_by_id(lead_id)
    if not lead_data:
        raise HTTPException(status_code=404, detail=f"Lead with ID '{lead_id}' not found.")
        
    lead_data['delta_info'] = get_lead_delta_since_yesterday(lead_id)
    
    # Activities
    lead_acts = get_activities_for_lead(lead_id)
    lead_data['activities'] = lead_acts
    
    # Grounded Citations
    citations = get_evidence_for_lead(lead_id)
    lead_data['grounded_citations'] = [c.model_dump() for c in citations]
    
    return lead_data
