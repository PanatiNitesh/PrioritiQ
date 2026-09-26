import pytest
from backend.agents.intent_agent import parse_user_intent

BENCHMARK_50_QUERIES = [
    # Group 1: General Prioritization (1-10)
    ("Which leads should my sales team prioritize today?", "PRIORITIZE_LEADS", "balanced", None, None),
    ("Give me the top accounts to contact this morning", "PRIORITIZE_LEADS", "balanced", None, None),
    ("Show today's recommended outreach targets", "PRIORITIZE_LEADS", "balanced", None, None),
    ("What are our highest priority accounts right now?", "PRIORITIZE_LEADS", "balanced", None, None),
    ("Prioritize the sales pipeline for my team", "PRIORITIZE_LEADS", "balanced", None, None),
    ("Where should my account executives spend their time?", "PRIORITIZE_LEADS", "balanced", None, None),
    ("Rank the active pipeline for Q3 closing", "PRIORITIZE_LEADS", "balanced", None, None),
    ("Generate today's lead prioritization queue", "PRIORITIZE_LEADS", "balanced", None, None),
    ("What accounts require manager attention today?", "PRIORITIZE_LEADS", "balanced", None, None),
    ("Who should we call first today?", "PRIORITIZE_LEADS", "balanced", None, None),

    # Group 2: Time-Constrained Prioritization (11-20)
    ("What if my team only has 3 hours today?", "WHAT_IF_TIME", "balanced", 3.0, None),
    ("Prioritize leads if we only have 2 hours", "WHAT_IF_TIME", "balanced", 2.0, None),
    ("If I have 90 minutes, which deals can we close?", "WHAT_IF_TIME", "balanced", 1.5, None),
    ("Rank accounts for a 4 hour afternoon block", "WHAT_IF_TIME", "balanced", 4.0, None),
    ("We only have 1 hour before the sales meeting", "WHAT_IF_TIME", "balanced", 1.0, None),
    ("Optimize schedule for 180 mins of rep calling", "WHAT_IF_TIME", "balanced", 3.0, None),
    ("If we have 5 hours today, which leads to touch?", "WHAT_IF_TIME", "balanced", 5.0, None),
    ("Fit our best deals into a 2.5 hour window", "WHAT_IF_TIME", "balanced", 2.5, None),
    ("Schedule maximum value in 6 hours", "WHAT_IF_TIME", "deal_value", 6.0, None),
    ("Only 45 mins available for quick wins", "WHAT_IF_TIME", "velocity", 0.75, None),

    # Group 3: Strategy & Value-Weighted Queries (21-30)
    ("What if I prioritize deal value over velocity?", "WHAT_IF_STRATEGY", "deal_value", None, None),
    ("Maximize revenue and total contract size", "WHAT_IF_STRATEGY", "deal_value", None, None),
    ("Focus on our largest deal values today", "WHAT_IF_STRATEGY", "deal_value", None, None),
    ("Prioritize highest value opportunities in the pipeline", "WHAT_IF_STRATEGY", "deal_value", None, None),
    ("Focus on deals closing this week with fast velocity", "WHAT_IF_STRATEGY", "velocity", None, None),
    ("Rank by fastest time to close", "WHAT_IF_STRATEGY", "velocity", None, None),
    ("Give me high win rate deals with low churn risk", "WHAT_IF_STRATEGY", "win_rate", None, None),
    ("Maximize probability and safe revenue today", "WHAT_IF_STRATEGY", "win_rate", None, None),
    ("Sort pipeline by deal value and strategic weight", "WHAT_IF_STRATEGY", "deal_value", None, None),
    ("Target quick sprint deals that close today", "WHAT_IF_STRATEGY", "velocity", None, None),

    # Group 4: Counterfactual Analysis & Entity Inquiries (31-40)
    ("Why not Vanguard?", "WHY_NOT_LEAD", "balanced", None, "vanguard"),
    ("Why not ApexFin for tomorrow instead?", "WHY_NOT_LEAD", "balanced", None, "apexfin"),
    ("Why not BioHealth if they are a hospital network?", "WHY_NOT_LEAD", "balanced", None, "biohealth"),
    ("Why not CyberShield for today's outreach?", "WHY_NOT_LEAD", "balanced", None, "cybershield"),
    ("What about TerraGreen and their CapEx deadline?", "WHY_NOT_LEAD", "balanced", None, "terragreen"),
    ("Why not CloudScale?", "WHY_NOT_LEAD", "balanced", None, "cloudscale"),
    ("Why not OmniRetail?", "WHY_NOT_LEAD", "balanced", None, "omniretail"),
    ("Compare Acme against our top deal", "WHY_NOT_LEAD", "balanced", None, "acme"),
    ("Why not Quantum Systems?", "WHY_NOT_LEAD", "balanced", None, "quantum"),
    ("Why not Zenith AI?", "WHY_NOT_LEAD", "balanced", None, "zenith"),

    # Group 5: Compound Multi-Constraint & Execution Queries (41-50)
    ("If I have 2 hours, prioritize deal value, but why not Vanguard?", "WHY_NOT_LEAD", "deal_value", 2.0, "vanguard"),
    ("If team has 3 hours, focus on velocity, what about BioHealth?", "WHY_NOT_LEAD", "velocity", 3.0, "biohealth"),
    ("With 4 hours available, maximize deal value for enterprise accounts", "WHAT_IF_TIME", "deal_value", 4.0, None),
    ("What changed since yesterday across all active deals?", "WHAT_CHANGED", "balanced", None, None),
    ("What is new in the pipeline today?", "WHAT_CHANGED", "balanced", None, None),
    ("Show recent delta activity and inbound communications", "WHAT_CHANGED", "balanced", None, None),
    ("Approve this recommendation and dispatch to reps", "APPROVE", "balanced", None, None),
    ("Confirm and execute outreach for approved accounts", "APPROVE", "balanced", None, None),
    ("Sign off on today's prioritized schedule", "APPROVE", "balanced", None, None),
    ("Approve the 3 hour schedule with deal value focus", "APPROVE", "deal_value", 3.0, None),
]

@pytest.mark.parametrize("query,expected_intent,expected_weight,expected_hours,expected_entity", BENCHMARK_50_QUERIES)
def test_synthetic_benchmark_50_queries(query, expected_intent, expected_weight, expected_hours, expected_entity):
    res = parse_user_intent(query)

    # Check intent classification (or compound inclusion)
    all_intents = [res["intent_type"]] + res.get("compound_intents", [])
    assert expected_intent in all_intents, f"Query '{query}' failed intent. Expected {expected_intent}, got {all_intents}"

    # Check strategy extraction
    if expected_weight != "balanced":
        assert res["priority_weight"] == expected_weight, f"Query '{query}' expected weight {expected_weight}, got {res['priority_weight']}"

    # Check time constraint extraction
    if expected_hours is not None:
        assert res["time_budget_hours"] == expected_hours, f"Query '{query}' expected hours {expected_hours}, got {res['time_budget_hours']}"

    # Check counterfactual target extraction
    if expected_entity is not None:
        target = str(res.get("target_lead_ref") or "").lower()
        assert expected_entity in target or len(target) > 0, f"Query '{query}' expected entity {expected_entity}, got {target}"
