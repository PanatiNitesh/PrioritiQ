import pytest
from backend.decision.audit import (
    log_decision_event,
    verify_audit_chain_integrity,
    get_all_audit_logs
)

def test_cryptographic_audit_chain_verification():
    # Log two distinct events
    e1 = log_decision_event(
        decision_id="DEC-TEST01",
        query="Prioritize leads",
        action="CREATED",
        user_role="Sales Manager",
        payload={"deal_ids": ["LEAD-101"]}
    )
    e2 = log_decision_event(
        decision_id="DEC-TEST01",
        action="APPROVED",
        query="Prioritize leads",
        user_role="Sales Manager",
        payload={"approved": True}
    )

    # Cryptographic link check: e2.previous_hash must match e1.audit_hash
    assert e2["previous_hash"] == e1["audit_hash"]

    # Verify entire chain
    verification = verify_audit_chain_integrity()
    assert verification["valid"] is True
    assert verification["verified_blocks"] >= 2
