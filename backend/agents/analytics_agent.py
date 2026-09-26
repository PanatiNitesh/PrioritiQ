from typing import Dict, Any, List, Optional
from ..analytics.lead_scoring import compute_deterministic_scores
from ..analytics.ranking import optimize_lead_prioritization
from ..analytics.metrics import get_pipeline_summary, get_lead_delta_since_yesterday

class AnalyticsAgent:
    """
    Executes deterministic business analytics, scoring, knapsack optimization,
    and structured aggregation queries.
    """
    def __init__(self):
        pass

    def run_prioritization(
        self,
        time_budget_hours: Optional[float] = None,
        priority_weight: str = "balanced",
        limit: int = 10
    ) -> Dict[str, Any]:
        ranked_leads, sim_state, excluded = optimize_lead_prioritization(
            time_budget_hours=time_budget_hours,
            priority_weight=priority_weight,
            limit=limit
        )
        
        # Enrich with deltas
        enriched = []
        for lead in ranked_leads:
            lid = lead['lead_id']
            delta = get_lead_delta_since_yesterday(lid)
            lead['delta_info'] = delta
            enriched.append(lead)

        pipeline_stats = get_pipeline_summary()

        return {
            "leads": enriched,
            "simulation": sim_state,
            "pipeline_stats": pipeline_stats
        }

    def get_lead_by_reference(self, ref: str) -> Optional[Dict[str, Any]]:
        scores_df = compute_deterministic_scores(priority_weight="balanced")
        ref_clean = ref.lower().strip()
        
        # Check by ID, Name, or Company Name
        for _, row in scores_df.iterrows():
            d = row.to_dict()
            lead_name = str(d.get('name', '')).lower()
            comp_name = str(d.get('company_name', '')).lower()
            lead_id = str(d.get('lead_id', '')).lower()
            comp_id = str(d.get('company_id', '')).lower()
            
            if (
                ref_clean in lead_id or
                ref_clean in lead_name or
                ref_clean in comp_id or
                ref_clean in comp_name or
                any(part in comp_name for part in ref_clean.split())
            ):
                d['delta_info'] = get_lead_delta_since_yesterday(d['lead_id'])
                return d
        return None
