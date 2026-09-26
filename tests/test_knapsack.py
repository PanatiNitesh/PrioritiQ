import pytest
from backend.analytics.ranking import optimize_lead_prioritization

def test_knapsack_budget_strict_adherence():
    """Verify that allocated effort never exceeds max_mins = hours * 60."""
    for hours in [1.0, 1.5, 2.0, 3.0]:
        max_mins = int(hours * 60)
        selected, sim_state, excluded = optimize_lead_prioritization(time_budget_hours=hours, limit=10)
        total_mins = sum(l.get("est_effort_mins", 30) for l in selected)
        assert total_mins <= max_mins, f"Total mins {total_mins} exceeded budget {max_mins}"

def test_knapsack_respects_cardinality_limit():
    """Verify that 2D knapsack strictly respects the limit bounds (Weakness 15)."""
    for limit in [1, 2, 3, 5]:
        selected, sim_state, excluded = optimize_lead_prioritization(time_budget_hours=5.0, limit=limit)
        assert len(selected) <= limit, f"Selected count {len(selected)} exceeded limit {limit}"

def test_knapsack_unconstrained_fallback():
    """When budget is None, returns standard sorted ranking bounded by limit."""
    selected, sim_state, excluded = optimize_lead_prioritization(time_budget_hours=None, limit=4)
    assert len(selected) == 4
    assert sim_state["constrained"] is False
