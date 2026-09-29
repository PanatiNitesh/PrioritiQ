import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from .lead_scoring import compute_deterministic_scores

def optimize_lead_prioritization(
    time_budget_hours: Optional[float] = None,
    priority_weight: str = "balanced",
    limit: int = 10,
    stage_filter: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], Dict[str, Any], List[Dict[str, Any]]]:
    """
    Solves multi-dimensional bounded knapsack problem:
    1. Maximizes strategic final_score directly without distorted double-weighting (Weakness 15).
    2. Strictly respects cardinality limit: count <= limit (Weakness 15).
    3. Respects capacity constraint: total_time <= max_mins.
    Returns: (selected_leads, simulation_state, excluded_leads).
    """
    df = compute_deterministic_scores(priority_weight=priority_weight)
    
    if stage_filter:
        df = df[df['stage'].str.lower() == stage_filter.lower()]
        
    leads_list = df.to_dict(orient="records")
    
    if time_budget_hours is not None and time_budget_hours <= 0:
        return [], {
            "constrained": True,
            "time_budget_mins": 0,
            "allocated_mins": 0,
            "slack_mins": 0,
            "total_deal_value": 0.0,
            "priority_weight": priority_weight,
            "leads_evaluated": len(leads_list),
            "leads_selected": 0,
            "excluded_count": len(leads_list),
            "cardinality_limit": limit,
            "constraint_explanation": "Zero or non-positive time budget specified (0 mins). Zero accounts scheduled."
        }, leads_list

    if time_budget_hours is None:
        # Standard unconstrained ranking bounded by limit
        selected = leads_list[:limit]
        excluded = leads_list[limit:]
        total_time = sum(lead.get('est_effort_mins', 30) for lead in selected)
        total_val = sum(lead.get('deal_size', 0) for lead in selected)
        
        sim_state = {
            "constrained": False,
            "time_budget_mins": None,
            "allocated_mins": total_time,
            "total_deal_value": total_val,
            "priority_weight": priority_weight,
            "leads_evaluated": len(leads_list),
            "leads_selected": len(selected),
            "excluded_count": len(excluded),
            "constraint_explanation": f"Unconstrained ranking with {priority_weight} strategy. Top {len(selected)} leads prioritized."
        }
        return selected, sim_state, excluded

    # 2D Bounded Knapsack DP: Capacity (time) AND Cardinality (limit)
    max_mins = max(0, int(time_budget_hours * 60))
    max_items = min(limit, len(leads_list))
    
    # Items: (lead, effort_mins, strategic_value)
    # strategic_value is directly final_score without double deal-size distortion
    items = []
    for lead in leads_list:
        weight = int(lead.get('est_effort_mins', 30))
        value = float(lead.get('final_score', 0))
        items.append((lead, weight, value))

    n = len(items)
    # dp[i][w][k] = max value using subset of first i items with weight <= w and count <= k
    # Optimized memory: 2D dp table dp[w][k]
    dp = [[0.0 for _ in range(max_items + 1)] for _ in range(max_mins + 1)]
    # Keep track of chosen items for exact reconstruction
    parent = {}

    for i in range(n):
        lead, w, val = items[i]
        for c in range(max_mins, w - 1, -1):
            for k in range(max_items, 0, -1):
                if dp[c - w][k - 1] + val > dp[c][k]:
                    dp[c][k] = dp[c - w][k - 1] + val
                    parent[(i, c, k)] = True

    # Find optimal (c, k)
    best_val = -1.0
    best_c, best_k = max_mins, max_items
    for c in range(max_mins + 1):
        for k in range(max_items + 1):
            if dp[c][k] > best_val:
                best_val = dp[c][k]
                best_c, best_k = c, k

    # Backtrack chosen items
    c, k = best_c, best_k
    chosen_indices = set()
    for i in range(n - 1, -1, -1):
        if (i, c, k) in parent:
            chosen_indices.add(i)
            c -= items[i][1]
            k -= 1

    chosen_leads = [items[i][0] for i in range(n) if i in chosen_indices]
    excluded_leads = [items[i][0] for i in range(n) if i not in chosen_indices]

    # Sort chosen by score descending
    chosen_leads.sort(key=lambda x: x.get('final_score', 0), reverse=True)
    
    total_allocated_mins = sum(lead.get('est_effort_mins', 30) for lead in chosen_leads)
    total_deal_val = sum(lead.get('deal_size', 0) for lead in chosen_leads)
    
    sim_state = {
        "constrained": True,
        "time_budget_mins": max_mins,
        "allocated_mins": total_allocated_mins,
        "slack_mins": max_mins - total_allocated_mins,
        "total_deal_value": total_deal_val,
        "priority_weight": priority_weight,
        "leads_evaluated": len(leads_list),
        "leads_selected": len(chosen_leads),
        "excluded_count": len(excluded_leads),
        "cardinality_limit": limit,
        "constraint_explanation": (
            f"Strict {time_budget_hours}h ({max_mins} mins) team capacity with max limit of {limit} accounts. "
            f"Optimized schedule selects {len(chosen_leads)} accounts utilizing "
            f"{total_allocated_mins}/{max_mins} mins (${total_deal_val:,.0f} pipeline value)."
        )
    }
    
    return chosen_leads, sim_state, excluded_leads
