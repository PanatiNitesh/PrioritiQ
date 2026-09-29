import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database.db import get_connection

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["engine"] == "PrioritiQ"
    assert data["status"] == "ONLINE"
    assert "version" in data

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert data["database"]["connected"] is True
    assert data["database"]["leads"] > 0
    assert "audit_chain" in data
    assert data["audit_chain"]["valid"] is True
    assert "rag_knowledge_base" in data

def test_query_decision_engine_standard():
    payload = {
        "query": "Which leads should we prioritize today?",
        "priority_weight": "balanced"
    }
    response = client.post("/api/decisions/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "decision_id" in data
    assert data["decision_id"].startswith("DEC-")
    assert len(data["recommendations"]) > 0
    assert data["approval_status"] == "PENDING"
    assert "blast_radius" in data
    assert "evidence_graph" in data
    assert "verification_report" in data
    assert data["verification_report"]["pipeline_grounded"] is True

def test_query_decision_engine_time_budget():
    payload = {
        "query": "What if my team only has 2 hours?",
        "time_budget_hours": 2.0,
        "priority_weight": "velocity"
    }
    response = client.post("/api/decisions/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    sim = data["simulation_state"]
    assert sim["constrained"] is True
    assert sim["allocated_mins"] <= 120
    assert len(data["recommendations"]) > 0

def test_query_decision_engine_counterfactual():
    payload = {
        "query": "Prioritize leads but why not Vanguard?",
        "target_lead_id": "LEAD-107"
    }
    response = client.post("/api/decisions/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["counterfactual_analysis"] is not None
    cf = data["counterfactual_analysis"]
    assert "focus_lead" in cf
    assert "alternative_lead" in cf
    assert "tradeoff_summary" in cf
    assert len(cf["key_differentiators"]) >= 2

def test_get_decision_by_id_success_and_404():
    # 1. Create a decision
    res = client.post("/api/decisions/query", json={"query": "Test persistence retrieval"})
    assert res.status_code == 200
    dec_id = res.json()["decision_id"]

    # 2. Retrieve existing decision
    get_res = client.get(f"/api/decisions/{dec_id}")
    assert get_res.status_code == 200
    retrieved = get_res.json()
    assert retrieved["decision_id"] == dec_id

    # 3. Retrieve non-existent decision -> must return strict 404
    missing_res = client.get("/api/decisions/DEC-NONEXISTENT-9999")
    assert missing_res.status_code == 404
    assert "not found" in missing_res.json()["detail"].lower()

def test_approve_decision_workflow():
    # Create decision
    create_res = client.post("/api/decisions/query", json={"query": "Approval test flow"})
    assert create_res.status_code == 200
    dec = create_res.json()
    dec_id = dec["decision_id"]
    lead_ids = [r["lead_id"] for r in dec["recommendations"][:2]]

    # Approve decision
    approve_payload = {
        "decision_id": dec_id,
        "action": "APPROVE",
        "approved_lead_ids": lead_ids,
        "manager_notes": "Approved for Q3 execution by VP of Sales."
    }
    appr_res = client.post("/api/decisions/approve", json=approve_payload)
    assert appr_res.status_code == 200
    appr_data = appr_res.json()
    assert appr_data["status"] == "APPROVE"
    assert len(appr_data["audit_hash"]) == 64
    assert len(appr_data["created_tasks"]) == len(lead_ids)
    assert len(appr_data["dispatched_emails"]) == len(lead_ids)

    # Check that GET decision now reflects approval
    updated_dec = client.get(f"/api/decisions/{dec_id}").json()
    assert updated_dec["approval_status"] == "APPROVE"

def test_audit_ledger_history_and_verify():
    hist_res = client.get("/api/decisions/history")
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert isinstance(history, list)
    assert len(history) > 0

    verify_res = client.get("/api/decisions/audit/verify")
    assert verify_res.status_code == 200
    verify_data = verify_res.json()
    assert verify_data["valid"] is True
    assert verify_data["verified_blocks"] > 0

def test_scoring_rules_configuration_api():
    # Fetch active rules
    rules_res = client.get("/api/decisions/config/rules")
    assert rules_res.status_code == 200
    rules = rules_res.json()
    assert "strategy_weights" in rules
    assert "stage_weights" in rules

    # Update rules dynamically
    rules["strategy_weights"]["deal_value"]["deal_size"] = 0.65
    update_res = client.post("/api/decisions/config/rules", json=rules)
    assert update_res.status_code == 200
    updated_rules = update_res.json()["rules"]
    assert updated_rules["strategy_weights"]["deal_value"]["deal_size"] == 0.65

def test_webhooks_api():
    # Register test webhook
    wh_payload = {
        "url": "https://httpbin.org/post",
        "event_types": ["decision.approved"],
        "secret": "test_enterprise_secret_123"
    }
    reg_res = client.post("/api/decisions/config/webhooks", json=wh_payload)
    assert reg_res.status_code == 200
    wh_data = reg_res.json()
    assert wh_data["url"] == wh_payload["url"]
    assert wh_data["is_active"] is True

    # List webhooks
    list_res = client.get("/api/decisions/config/webhooks")
    assert list_res.status_code == 200
    all_wh = list_res.json()
    assert any(w["url"] == wh_payload["url"] for w in all_wh)

def test_leads_endpoints():
    leads_res = client.get("/api/leads")
    assert leads_res.status_code == 200
    leads = leads_res.json()
    assert len(leads) > 0
    first_lead = leads[0]
    assert "lead_id" in first_lead
    assert "delta_info" in first_lead

    # Lead detail
    lead_id = first_lead["lead_id"]
    detail_res = client.get(f"/api/leads/{lead_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["lead_id"] == lead_id
    assert "activities" in detail
    assert "grounded_citations" in detail

    # 404 for missing lead
    missing_lead = client.get("/api/leads/LEAD-INVALID-999")
    assert missing_lead.status_code == 404

def test_sources_endpoints():
    summary_res = client.get("/api/sources/summary")
    assert summary_res.status_code == 200
    summary = summary_res.json()
    assert summary["status"] == "OPERATIONAL_CONNECTED"
    assert len(summary["sources"]) >= 3

    notes_res = client.get("/api/sources/notes")
    assert notes_res.status_code == 200
    notes = notes_res.json()
    assert isinstance(notes, list)
    assert len(notes) > 0

def test_monte_carlo_simulate_endpoint():
    sim_payload = {
        "trials": 500,
        "market_volatility": 0.15,
        "priority_weight": "deal_value"
    }
    res = client.post("/api/decisions/simulate", json=sim_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["simulation_trials"] == 500
    assert "expected_revenue_optimized" in data
    assert "expected_revenue_baseline" in data
    assert "prioritiq_schedule" in data
    assert "legacy_crm_baseline" in data
    assert len(data["distribution_buckets"]) > 0

def test_rules_preview_endpoint():
    preview_payload = {
        "stage_weights": {
            "Closing": 1.0,
            "Negotiation": 0.90,
            "Proposal": 0.70,
            "Demo": 0.50,
            "Discovery": 0.30
        },
        "strategy_weights": {
            "balanced": {
                "deal_size": 0.50,
                "intent_score": 0.20,
                "icp_fit": 0.15,
                "stage_weight": 0.15
            }
        },
        "churn_penalties": {
            "High": 0.25,
            "Medium": 0.10,
            "Low": 0.0
        },
        "recency_decay_half_life_days": 4.0
    }
    res = client.post("/api/decisions/config/rules/preview", json=preview_payload)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    first = data[0]
    assert "lead_id" in first
    assert "old_score" in first
    assert "new_score" in first
    assert "score_delta" in first
    assert "rank_shift" in first

def test_get_and_update_rules():
    # 1. Get current rules
    get_res = client.get("/api/decisions/config/rules")
    assert get_res.status_code == 200
    current_rules = get_res.json()
    assert "stage_weights" in current_rules
    assert "strategy_weights" in current_rules

    # 2. Update rules
    update_res = client.put("/api/decisions/config/rules", json=current_rules)
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["status"] == "SUCCESS"
    assert "rules" in updated
