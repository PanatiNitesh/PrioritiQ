import pytest
from backend.agents.intent_agent import parse_user_intent

def test_intent_compound_query_resolution():
    """Verify that compound query extracts time constraint, deal weight, and counterfactual target."""
    query = "If I have 2 hours, prioritize deal value, but why not Vanguard?"
    intent = parse_user_intent(query)

    assert intent["time_budget_hours"] == 2.0
    assert intent["priority_weight"] == "deal_value"
    assert intent["target_lead_ref"] is not None
    assert "vanguard" in str(intent["target_lead_ref"]).lower() or intent["target_lead_ref"] == "LEAD-107"
    assert intent["confidence"] >= 0.85
    assert intent["query_plan"]["require_constraint_optimization"] is True
    assert intent["query_plan"]["require_counterfactual_comparison"] is True

def test_intent_velocity_query():
    query = "Focus on leads closing this week with fast turnaround"
    intent = parse_user_intent(query)
    assert intent["priority_weight"] == "velocity"

def test_intent_approval():
    query = "Approve this recommendation and dispatch to sales reps"
    intent = parse_user_intent(query)
    assert "APPROVE" in intent["compound_intents"]
