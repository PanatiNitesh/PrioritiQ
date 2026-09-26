import pytest
from backend.agents.verification_agent import VerificationAgent
from backend.models.schemas import GroundedCitation
from backend.database.db import get_lead_by_id

def test_verification_agent_pk_integrity():
    agent = VerificationAgent()
    # Authentic lead in DB
    lead = get_lead_by_id("LEAD-101")
    assert lead is not None, "LEAD-101 should exist in seeded database"

    citations = [
        GroundedCitation(
            source_file="NOTE-LEAD-101-04.txt",
            source_type="Inbound Email",
            author_or_actor="Sarah Jenkins",
            timestamp="2026-09-26 08:42",
            quote="We have full executive authorization to execute the $145,000 annual agreement today, provided we make one quick edit to Section 9.2 (standard mutual indemnification wording)."
        )
    ]

    result = agent.verify_recommendation(
        lead_dict=lead,
        citations=citations,
        constraint_mins_limit=60
    )

    assert result["is_verified"] is True
    assert result["checks_passed"] >= 3
    assert result["grounding_score_pct"] >= 75.0
    assert result["hallucination_risk"] in ["LOW_CALIBRATED", "MODERATE"]

def test_verification_agent_rejects_corrupted_deal_size():
    agent = VerificationAgent()
    corrupted_lead = {
        "lead_id": "LEAD-101",
        "deal_size": 9999999.0,  # Falsified deal size
        "assigned_rep": "Alex Rivera",
        "stage": "Proposal",
        "est_effort_mins": 30
    }

    citations = [
        GroundedCitation(
            source_file="apexfin_notes.txt",
            source_type="sales_note",
            author_or_actor="Sarah Jenkins",
            timestamp="2026-09-26 08:42",
            quote="Indemnification revision needed"
        )
    ]

    result = agent.verify_recommendation(
        lead_dict=corrupted_lead,
        citations=citations
    )

    # Primary key check must fail
    pk_check = next((c for c in result["checks"] if c["check"] == "PRIMARY_KEY_DATABASE_INTEGRITY"), None)
    assert pk_check is not None
    assert pk_check["passed"] is False, "Corrupted deal size must fail database integrity check"
    assert result["is_verified"] is False

def test_verification_agent_rejects_nonexistent_lead():
    agent = VerificationAgent()
    fake_lead = {
        "lead_id": "LEAD-999_FAKE",
        "deal_size": 50000.0,
        "assigned_rep": "Ghost Agent",
        "stage": "Proposal"
    }

    result = agent.verify_recommendation(
        lead_dict=fake_lead,
        citations=[]
    )

    assert result["is_verified"] is False
    assert result["hallucination_risk"] == "HIGH_UNGROUNDED"
