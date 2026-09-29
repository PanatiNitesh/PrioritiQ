import pytest
import sqlite3
from backend.decision.audit import (
    log_decision_event,
    verify_audit_chain_integrity
)
from backend.database.db import get_connection, _db_lock

def test_tamper_detection_on_mutated_payload():
    # 1. Log a valid test event
    event = log_decision_event(
        decision_id="DEC-TAMPER-TEST",
        query="Tamper detection test query",
        action="CREATED",
        user_role="Compliance Officer",
        payload={"sensitive_field": "Original Authentic Value"}
    )
    event_id = event["event_id"]

    # 2. Assert chain is valid before tampering
    before = verify_audit_chain_integrity()
    assert before["valid"] is True

    # 3. Adversary tampers with the row in SQLite directly
    with _db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE audit_ledger SET payload = ? WHERE event_id = ?", (
            '{"sensitive_field": "Forged Tampered Value"}',
            event_id
        ))
        conn.commit()
        conn.close()

    # 4. Verification must detect the tampering and fail
    tamper_result = verify_audit_chain_integrity()
    assert tamper_result["valid"] is False
    assert "Tampering detected" in tamper_result["error"]
    assert event_id in tamper_result["error"]

    # 5. Restore original authentic payload so subsequent tests succeed
    with _db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE audit_ledger SET payload = ? WHERE event_id = ?", (
            '{"sensitive_field": "Original Authentic Value"}',
            event_id
        ))
        conn.commit()
        conn.close()

    # 6. Verify restored chain is valid again
    restored = verify_audit_chain_integrity()
    assert restored["valid"] is True

def test_tamper_detection_on_corrupted_previous_hash():
    # 1. Get the last event
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT event_id, previous_hash FROM audit_ledger ORDER BY rowid DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if not row:
        pytest.skip("No audit events in ledger to test hash corruption")

    event_id = row["event_id"]
    original_prev_hash = row["previous_hash"]
    corrupted_prev_hash = "deadbeef" * 8

    # 2. Corrupt previous_hash
    with _db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE audit_ledger SET previous_hash = ? WHERE event_id = ?", (
            corrupted_prev_hash,
            event_id
        ))
        conn.commit()
        conn.close()

    # 3. Verification must fail
    check = verify_audit_chain_integrity()
    assert check["valid"] is False
    assert "Chain broken" in check["error"] or "Tampering detected" in check["error"]

    # 4. Restore original previous_hash
    with _db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE audit_ledger SET previous_hash = ? WHERE event_id = ?", (
            original_prev_hash,
            event_id
        ))
        conn.commit()
        conn.close()

    # 5. Final check
    final_check = verify_audit_chain_integrity()
    assert final_check["valid"] is True
