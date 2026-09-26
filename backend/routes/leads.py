from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
import os
import pandas as pd
from ..analytics.lead_scoring import compute_deterministic_scores, load_data
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

@router.get("/{lead_id}", response_model=Dict[str, Any])
async def get_lead_detail(lead_id: str):
    merged_df, activities_df = load_data()
    lead_row = merged_df[merged_df['lead_id'] == lead_id]
    if lead_row.empty:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    lead_data = lead_row.iloc[0].to_dict()
    lead_data['delta_info'] = get_lead_delta_since_yesterday(lead_id)
    
    # Activities
    lead_acts = activities_df[activities_df['lead_id'] == lead_id].to_dict(orient="records")
    lead_data['activities'] = lead_acts
    
    # Grounded Citations
    citations = get_evidence_for_lead(lead_id)
    lead_data['grounded_citations'] = [c.dict() for c in citations]
    
    return lead_data
