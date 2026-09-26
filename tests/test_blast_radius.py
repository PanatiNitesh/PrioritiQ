import pytest
from backend.analytics.blast_radius import BlastRadiusPredictor

def test_blast_radius_predicts_account_attrition():
    predictor = BlastRadiusPredictor()
    all_leads = [
        {"lead_id": "L1", "deal_size": 100000, "churn_risk": "Low", "assigned_rep": "Alex Rivera", "stage": "Proposal", "est_effort_mins": 30},
        {"lead_id": "L2", "deal_size": 150000, "churn_risk": "High", "assigned_rep": "Devon Miller", "stage": "Negotiation", "est_effort_mins": 45},
        {"lead_id": "L3", "deal_size": 80000, "churn_risk": "High", "assigned_rep": "Alex Rivera", "stage": "Proposal", "est_effort_mins": 30},
        {"lead_id": "L4", "deal_size": 60000, "churn_risk": "Medium", "assigned_rep": "Devon Miller", "stage": "Discovery", "est_effort_mins": 30}
    ]

    # Only L1 recommended, L2 and L3 omitted
    recommended = [all_leads[0]]
    result = predictor.predict(all_leads=all_leads, recommended_leads=recommended, time_budget_hours=1.0)

    assert result["excluded_accounts_count"] == 3
    assert result["at_risk_excluded_value"] == 230000  # L2 ($150k) + L3 ($80k)
    assert result["collateral_damage_score"] > 30
    assert any("Attrition Risk" in w for w in result["warnings"])

def test_blast_radius_detects_rep_capacity_skew():
    predictor = BlastRadiusPredictor()
    all_leads = [
        {"lead_id": "L1", "deal_size": 100000, "churn_risk": "Low", "assigned_rep": "Alex Rivera", "est_effort_mins": 90},
        {"lead_id": "L2", "deal_size": 120000, "churn_risk": "Low", "assigned_rep": "Alex Rivera", "est_effort_mins": 100},
        {"lead_id": "L3", "deal_size": 70000, "churn_risk": "Low", "assigned_rep": "Devon Miller", "est_effort_mins": 30}
    ]

    # Assigning 190 mins to Alex Rivera, 0 to Devon Miller
    recommended = [all_leads[0], all_leads[1]]
    result = predictor.predict(all_leads=all_leads, recommended_leads=recommended, time_budget_hours=3.5)

    assert result["rep_skew_std_dev_mins"] > 40
    alex_stats = next(r for r in result["rep_utilizations"] if r["rep_name"] == "Alex Rivera")
    assert alex_stats["bottleneck_risk"] is True
    assert any("Bottleneck" in w for w in result["warnings"])
