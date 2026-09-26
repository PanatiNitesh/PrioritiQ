import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..database.db import get_connection, _db_lock

GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

def get_latest_audit_hash() -> str:
    """
    Returns the audit_hash of the most recent block in the hash chain.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT audit_hash FROM audit_ledger ORDER BY rowid DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    if row and row[0]:
        return row[0]
    return GENESIS_HASH

def log_decision_event(
    decision_id: str,
    query: str,
    action: str,  # CREATED, APPROVED, EDITED, REJECTED
    user_role: str,
    payload: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Thread-safe, append-only cryptographic hash chain logger.
    Each block hashes the previous block's hash, preventing historical tampering.
    """
    with _db_lock:
        conn = get_connection()
        cur = conn.cursor()

        # Get previous hash
        cur.execute("SELECT audit_hash, rowid FROM audit_ledger ORDER BY rowid DESC LIMIT 1")
        last_row = cur.fetchone()
        previous_hash = last_row["audit_hash"] if last_row and last_row["audit_hash"] else GENESIS_HASH
        event_num = (last_row["rowid"] + 1) if last_row else 1
        event_id = f"EVT-{event_num:04d}"

        timestamp = datetime.now().isoformat()
        payload_serialized = json.dumps(payload, sort_keys=True)

        # Cryptographic link: previous_hash MUST be in the preimage
        preimage = f"{previous_hash}|{event_id}|{decision_id}|{timestamp}|{action}|{user_role}|{payload_serialized}"
        audit_hash = hashlib.sha256(preimage.encode("utf-8")).hexdigest()

        cur.execute("""
        INSERT INTO audit_ledger 
        (event_id, decision_id, query, action, user_role, timestamp, payload, previous_hash, audit_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event_id,
            decision_id,
            query,
            action,
            user_role,
            timestamp,
            payload_serialized,
            previous_hash,
            audit_hash
        ))
        conn.commit()
        conn.close()

        entry = {
            "event_id": event_id,
            "decision_id": decision_id,
            "query": query,
            "timestamp": timestamp,
            "action": action,
            "user_role": user_role,
            "previous_hash": previous_hash,
            "audit_hash": audit_hash,
            "details": payload
        }
        return entry

def get_all_audit_logs() -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM audit_ledger ORDER BY rowid DESC")
    rows = cur.fetchall()
    conn.close()

    logs = []
    for r in rows:
        item = dict(r)
        try:
            item["details"] = json.loads(item["payload"])
        except Exception:
            item["details"] = {}
        logs.append(item)
    return logs

def get_decision_audit(decision_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM audit_ledger WHERE decision_id = ? ORDER BY rowid ASC", (decision_id,))
    rows = cur.fetchall()
    conn.close()

    logs = []
    for r in rows:
        item = dict(r)
        try:
            item["details"] = json.loads(item["payload"])
        except Exception:
            item["details"] = {}
        logs.append(item)
    return logs

def verify_audit_chain_integrity() -> Dict[str, Any]:
    """
    Cryptographically verifies the entire historical audit ledger from genesis.
    Returns status, broken link if any, and verified block count.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM audit_ledger ORDER BY rowid ASC")
    rows = cur.fetchall()
    conn.close()

    expected_prev = GENESIS_HASH
    for idx, r in enumerate(rows):
        stored_prev = r["previous_hash"]
        stored_hash = r["audit_hash"]

        if stored_prev != expected_prev:
            return {
                "valid": False,
                "error": f"Chain broken at event {r['event_id']}. Expected prev_hash {expected_prev}, found {stored_prev}",
                "verified_blocks": idx
            }

        # Recalculate
        preimage = f"{stored_prev}|{r['event_id']}|{r['decision_id']}|{r['timestamp']}|{r['action']}|{r['user_role']}|{r['payload']}"
        recalculated_hash = hashlib.sha256(preimage.encode("utf-8")).hexdigest()

        if recalculated_hash != stored_hash:
            return {
                "valid": False,
                "error": f"Tampering detected at event {r['event_id']}. Stored {stored_hash} != Recalculated {recalculated_hash}",
                "verified_blocks": idx
            }

        expected_prev = stored_hash

    return {
        "valid": True,
        "verified_blocks": len(rows),
        "latest_block_hash": expected_prev,
        "message": f"All {len(rows)} audit events cryptographically verified."
    }
