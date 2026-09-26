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
    return rules.dict()

@router.post("/config/rules", response_model=Dict[str, Any])
async def update_scoring_rules_config(updated_rules: Dict[str, Any]):
    """
    Dynamically tunes scoring weights, churn penalties, and stage multipliers.
    """
    try:
        validated = ScoringRulesConfig(**updated_rules)
        save_scoring_rules(validated)
        return {"status": "SUCCESS", "message": "Scoring rules updated successfully.", "rules": validated.dict()}
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
