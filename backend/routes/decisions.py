from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional
from ..models.schemas import (
    DecisionQueryRequest,
    DecisionResponse,
    ApprovalActionRequest,
    ApprovalActionResponse
)
from ..decision.engine import process_decision_query
from ..decision.audit import get_all_audit_logs, log_decision_event, verify_audit_chain_integrity
from ..decision.webhooks import WebhookDispatcher
from ..database.db import (
    load_persisted_decision,
    update_decision_approval,
    get_connection,
    _db_lock
)
from ..analytics.rules import ScoringRulesConfig, load_scoring_rules, save_scoring_rules

router = APIRouter(prefix="/api/decisions", tags=["decisions"])

# In-memory L1 cache (backed by SQLite L2 persistent store)
active_decisions: Dict[str, DecisionResponse] = {}

@router.post("/query", response_model=DecisionResponse)
async def query_decision_engine(request: DecisionQueryRequest):
    try:
        response = process_decision_query(
            query_text=request.query,
            override_time_budget=request.time_budget_hours,
            override_priority_weight=request.priority_weight,
            target_lead_id=request.target_lead_id
        )
        active_decisions[response.decision_id] = response
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[Dict[str, Any]])
async def get_decisions_history():
    return get_all_audit_logs()

@router.get("/audit/verify", response_model=Dict[str, Any])
async def verify_audit_ledger():
    """
    Cryptographic verification endpoint for the tamper-evident hash chain.
    """
    return verify_audit_chain_integrity()

@router.get("/{decision_id}", response_model=DecisionResponse)
async def get_decision_by_id(decision_id: str):
    # 1. Check L1 in-memory cache
    if decision_id in active_decisions:
        return active_decisions[decision_id]

    # 2. Check L2 SQLite persistent store
    persisted = load_persisted_decision(decision_id)
    if persisted:
        try:
            payload = persisted.get("decision_payload", {})
            restored = DecisionResponse(**payload)
            # Restore approval status if updated
            restored.approval_status = persisted.get("status", "PENDING")
            active_decisions[decision_id] = restored
            return restored
        except Exception:
            pass

    # 3. Weakness 3 Fix: NEVER silently re-run a default query. Return strict HTTP 404!
    raise HTTPException(
        status_code=404,
        detail=f"Decision with ID '{decision_id}' not found in active or persistent audit storage."
    )

@router.post("/approve", response_model=ApprovalActionResponse)
async def approve_decision(req: ApprovalActionRequest):
    # Attempt to load from cache or DB
    decision = active_decisions.get(req.decision_id)
    if not decision:
        persisted = load_persisted_decision(req.decision_id)
        if persisted:
            decision = DecisionResponse(**persisted.get("decision_payload", {}))
            active_decisions[req.decision_id] = decision

    approved_leads = req.approved_lead_ids or []
    created_tasks = []
    dispatched_emails = []

    if decision:
        decision.approval_status = req.action
        decision.approval_details = {
            "action": req.action,
            "manager_notes": req.manager_notes,
            "approved_lead_ids": approved_leads
        }

        # Build tasks and email actions for approved leads
        for rec in decision.recommendations:
            if not approved_leads or rec.lead_id in approved_leads:
                created_tasks.append({
                    "task_id": f"TASK-{rec.lead_id}",
                    "lead_id": rec.lead_id,
                    "title": rec.suggested_action.get("title", f"Action for {rec.lead_name}"),
                    "rep": rec.assigned_rep,
                    "status": "QUEUED_CRM",
                    "due": "Today 17:00"
                })
                dispatched_emails.append({
                    "email_id": f"EML-{rec.lead_id}",
                    "to": rec.suggested_action.get("email_draft", {}).get("to"),
                    "subject": rec.suggested_action.get("email_draft", {}).get("subject"),
                    "status": "DRAFT_READY"
                })

    # Update database persistence
    update_decision_approval(
        decision_id=req.decision_id,
        action=req.action,
        approved_leads=approved_leads,
        manager_notes=req.manager_notes
    )

    # Append to cryptographic hash chain audit ledger
    audit_entry = log_decision_event(
        decision_id=req.decision_id,
        query=decision.query if decision else "Prioritize leads",
        action=req.action,
        user_role="Sales Manager",
        payload={
            "action": req.action,
            "approved_lead_ids": approved_leads,
            "manager_notes": req.manager_notes,
            "tasks_count": len(created_tasks),
            "emails_count": len(dispatched_emails)
        }
    )

    # Dispatch outbound webhooks asynchronously (Weakness 13)
    WebhookDispatcher.dispatch_event_async("decision.approved", {
        "decision_id": req.decision_id,
        "action": req.action,
        "approved_lead_ids": approved_leads,
        "tasks": created_tasks,
        "audit_hash": audit_entry.get("audit_hash")
    })

    return ApprovalActionResponse(
        decision_id=req.decision_id,
        status=req.action,
        audit_hash=audit_entry.get("audit_hash", ""),
        timestamp=audit_entry.get("timestamp", ""),
        created_tasks=created_tasks,
        dispatched_emails=dispatched_emails,
        audit_entry=audit_entry
    )

# ==============================================================================
# DEVELOPER CONFIGURATION APIs (Weakness 13 & 14)
# ==============================================================================

@router.get("/config/rules", response_model=Dict[str, Any])
async def get_scoring_rules_config():
    """
    Returns the active enterprise scoring policy and weight configuration.
    """
    rules = load_scoring_rules()
    return rules.model_dump()

@router.post("/config/rules", response_model=Dict[str, Any])
@router.put("/config/rules", response_model=Dict[str, Any])
async def update_scoring_rules_config(updated_rules: Dict[str, Any]):
    """
    Dynamically tunes scoring weights, churn penalties, and stage multipliers.
    """
    try:
        validated = ScoringRulesConfig(**updated_rules)
        save_scoring_rules(validated)
        return {"status": "SUCCESS", "message": "Scoring rules updated successfully.", "rules": validated.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/config/webhooks", response_model=List[Dict[str, Any]])
async def list_active_webhooks():
    return WebhookDispatcher.list_webhooks()

@router.post("/config/webhooks", response_model=Dict[str, Any])
async def register_webhook_endpoint(data: Dict[str, Any]):
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    event_types = data.get("event_types", ["decision.approved", "decision.created"])
    secret = data.get("secret")
    return WebhookDispatcher.register_webhook(url=url, event_types=event_types, secret=secret)

# ==============================================================================
# ADVANCED ANALYTICS: MONTE CARLO & REVOPS PREVIEW ENDPOINTS
# ==============================================================================

@router.post("/simulate", response_model=Dict[str, Any])
async def run_custom_monte_carlo(req: Dict[str, Any]):
    """
    On-demand stochastic Monte Carlo simulation with customizable volatility & trials.
    """
    from ..analytics.simulation import MonteCarloPipelineSimulator
    from ..database.db import get_all_leads_with_companies
    from ..analytics.lead_scoring import compute_deterministic_scores

    trials = int(req.get("trials", 1000))
    volatility = float(req.get("market_volatility", 0.12))
    efficiency = float(req.get("execution_efficiency", 1.0))
    time_budget = req.get("time_budget_hours")

    all_leads = get_all_leads_with_companies()
    scores_df = compute_deterministic_scores(priority_weight=req.get("priority_weight", "balanced"))
    recommended = scores_df.to_dict(orient="records")[:req.get("limit", 5)]

    simulator = MonteCarloPipelineSimulator(random_seed=req.get("seed", 42))
    result = simulator.simulate(
        all_leads=all_leads,
        recommended_leads=recommended,
        trials=trials,
        market_volatility=volatility,
        execution_efficiency=efficiency
    )
    return result

@router.post("/config/rules/preview", response_model=List[Dict[str, Any]])
async def preview_scoring_rules_impact(prospective_rules: Dict[str, Any]):
    """
    Simulates real-time pipeline ranking differentials when adjusting scoring weights.
    Returns before-and-after lead scores and rank shifts.
    """
    import numpy as np
    import pandas as pd
    from ..analytics.lead_scoring import load_data
    from ..database.db import get_max_dataset_timestamp

    df = load_data()
    if df.empty:
        return []

    # Current baseline scores
    from ..analytics.lead_scoring import compute_deterministic_scores
    current_df = compute_deterministic_scores(priority_weight="balanced")
    current_scores = {r["lead_id"]: r["final_score"] for r in current_df.to_dict(orient="records")}
    current_ranks = {r["lead_id"]: idx + 1 for idx, r in enumerate(current_df.to_dict(orient="records"))}

    # Calculate prospective scores
    stage_weights = prospective_rules.get("stage_weights", {})
    strategy_weights = prospective_rules.get("strategy_weights", {}).get("balanced", {})
    churn_penalties = prospective_rules.get("churn_penalties", {})
    half_life_days = prospective_rules.get("recency_decay_half_life_days", 4.0)

    now_ref = get_max_dataset_timestamp()
    df['last_act_dt'] = pd.to_datetime(df['last_activity_date'], errors='coerce').fillna(now_ref)
    df['days_since_act'] = (now_ref - df['last_act_dt']).dt.total_seconds() / 86400.0
    df['days_since_act'] = df['days_since_act'].clip(lower=0.0)
    df['recency_multiplier'] = np.exp(-df['days_since_act'] / half_life_days)
    df['stage_score'] = df['stage'].map(stage_weights).fillna(0.35)

    df['norm_deal'] = np.log1p(df['deal_size']) / np.log1p(1500000.0)
    df['norm_intent'] = df['intent_score'] / 100.0
    df['norm_icp'] = df['icp_fit'] / 100.0

    w_deal = strategy_weights.get("deal_size", 0.40)
    w_intent = strategy_weights.get("intent_score", 0.25)
    w_icp = strategy_weights.get("icp_fit", 0.20)
    w_stage = strategy_weights.get("stage_weight", 0.15)

    df['raw_score'] = (
        (df['norm_deal'] * w_deal) +
        (df['norm_intent'] * w_intent) +
        (df['norm_icp'] * w_icp) +
        (df['stage_score'] * w_stage)
    ) * df['recency_multiplier']

    df['churn_penalty'] = df['churn_risk'].map(churn_penalties).fillna(0.0)
    df['new_final_score'] = np.clip((df['raw_score'] - df['churn_penalty']) * 100.0, 0.0, 100.0).round(1)

    df = df.sort_values(by="new_final_score", ascending=False)
    diff_records = []
    for new_rank, (_, row) in enumerate(df.iterrows(), start=1):
        lid = row["lead_id"]
        old_score = current_scores.get(lid, 0.0)
        old_rank = current_ranks.get(lid, 99)
        new_score = row["new_final_score"]
        diff_records.append({
            "lead_id": lid,
            "lead_name": row.get("lead_name") or row.get("name"),
            "company_name": row.get("company_name") or row.get("name_y") or row.get("company_id"),
            "stage": row.get("stage"),
            "deal_size": float(row.get("deal_size", 0)),
            "old_score": round(old_score, 1),
            "new_score": round(new_score, 1),
            "score_delta": round(new_score - old_score, 1),
            "old_rank": old_rank,
            "new_rank": new_rank,
            "rank_shift": old_rank - new_rank  # positive means improved rank
        })
    return diff_records
