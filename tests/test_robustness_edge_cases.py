import pytest
from backend.analytics.ranking import optimize_lead_prioritization
from backend.agents.intent_agent import parse_user_intent
from backend.decision.engine import process_decision_query
from backend.analytics.lead_scoring import compute_deterministic_scores
from backend.analytics.blast_radius import BlastRadiusPredictor

def test_knapsack_zero_time_budget():
    selected, sim, excluded = optimize_lead_prioritization(time_budget_hours=0.0)
    assert len(selected) == 0
    assert sim["allocated_mins"] == 0
    assert sim["leads_selected"] == 0
    assert len(excluded) > 0

def test_knapsack_negative_time_budget():
    selected, sim, excluded = optimize_lead_prioritization(time_budget_hours=-2.5)
    assert len(selected) == 0
    assert sim["allocated_mins"] == 0
    assert len(excluded) > 0

def test_knapsack_extremely_large_time_budget():
    # 100 hours is plenty for all leads
    selected, sim, excluded = optimize_lead_prioritization(time_budget_hours=100.0, limit=10)
    # Respects cardinality limit of 10
    assert len(selected) <= 10
    assert sim["allocated_mins"] <= 100 * 60

def test_intent_agent_handles_empty_and_whitespace_query():
    empty_result = parse_user_intent("")
    assert empty_result["intent_type"] == "PRIORITIZE_LEADS"
    assert empty_result["priority_weight"] == "balanced"

    none_result = parse_user_intent(None)
    assert none_result["intent_type"] == "PRIORITIZE_LEADS"

    spaces_result = parse_user_intent("     \n\t   ")
    assert spaces_result["intent_type"] == "PRIORITIZE_LEADS"

def test_intent_agent_handles_special_characters_and_emojis():
    emoji_result = parse_user_intent("🚀 Prioritize our largest $$$ deals in 2.5 hrs! 🔥")
    assert emoji_result["priority_weight"] == "deal_value"
    assert emoji_result["time_budget_hours"] == 2.5

def test_deterministic_scoring_consistency():
    # Scoring must be 100% deterministic (calling twice returns identical scores)
    df1 = compute_deterministic_scores(priority_weight="deal_value")
    df2 = compute_deterministic_scores(priority_weight="deal_value")
    assert list(df1["final_score"]) == list(df2["final_score"])
    assert list(df1["lead_id"]) == list(df2["lead_id"])

def test_blast_radius_empty_recommendation_handling():
    predictor = BlastRadiusPredictor()
    all_leads = compute_deterministic_scores().to_dict(orient="records")
    # If no leads are recommended (0 time budget)
    res = predictor.predict(all_leads=all_leads, recommended_leads=[], time_budget_hours=0.0)
    assert res["excluded_accounts_count"] == len(all_leads)
    assert res["risk_level"] in ["CRITICAL", "ELEVATED", "LOW"]

def test_full_decision_query_with_edge_budget():
    res = process_decision_query(
        query_text="Quick test with 1.0 hour sprint",
        override_time_budget=1.0
    )
    assert res.simulation_state["allocated_mins"] <= 60
    assert len(res.recommendations) > 0
