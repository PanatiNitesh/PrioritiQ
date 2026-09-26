from datetime import datetime, timedelta
from typing import Dict, Any, List
from ..database.db import get_connection, get_max_dataset_timestamp, get_lead_by_id

def get_pipeline_summary() -> Dict[str, Any]:
    """
    Computes real-time pipeline metrics directly from prioritiq.db with zero CSV disk re-reads.
    Uses dynamic dataset epoch detection to prevent artificial date decay.
    """
    conn = get_connection()
    cur = conn.cursor()

    # 1. Total pipeline value and count
    cur.execute("SELECT COUNT(*), SUM(deal_value), AVG(intent_score) FROM leads")
    count_row = cur.fetchone()
    total_active_leads = count_row[0] or 0
    total_pipeline_val = float(count_row[1] or 0.0)
    avg_intent_score = round(float(count_row[2] or 0.0), 1)

    # 2. Stage breakdown
    cur.execute("""
    SELECT status as stage, COUNT(*) as count, SUM(deal_value) as total_value 
    FROM leads 
    GROUP BY status
    """)
    stage_rows = cur.fetchall()
    stage_breakdown = {
        r["stage"]: {"count": r["count"], "total_value": float(r["total_value"] or 0.0)}
        for r in stage_rows
    }

    # 3. Dynamic Epoch Delta Analysis (Evaluated relative to the maximum activity timestamp in DB)
    max_ts = get_max_dataset_timestamp()
    today_str = max_ts.strftime("%Y-%m-%d")
    yesterday_str = (max_ts - timedelta(days=1)).strftime("%Y-%m-%d")

    cur.execute("SELECT COUNT(*) FROM activities WHERE timestamp LIKE ?", (f"{today_str}%",))
    today_acts_count = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM activities WHERE timestamp LIKE ?", (f"{yesterday_str}%",))
    yesterday_acts_count = cur.fetchone()[0] or 0

    conn.close()

    return {
        "total_pipeline_value": total_pipeline_val,
        "total_active_leads": total_active_leads,
        "average_intent_score": avg_intent_score,
        "stages": stage_breakdown,
        "today_activities_count": today_acts_count,
        "yesterday_activities_count": yesterday_acts_count,
        "evaluation_epoch": today_str
    }

def get_lead_delta_since_yesterday(lead_id: str) -> Dict[str, Any]:
    """
    Computes grounded delta for a specific lead directly from prioritiq.db.
    """
    lead = get_lead_by_id(lead_id)
    if not lead:
        return {"has_delta": False, "summary": "No recent changes detected."}

    conn = get_connection()
    cur = conn.cursor()
    max_ts = get_max_dataset_timestamp()
    today_str = max_ts.strftime("%Y-%m-%d")

    cur.execute("""
    SELECT * FROM activities 
    WHERE lead_id = ? AND timestamp LIKE ? 
    ORDER BY timestamp DESC
    """, (lead_id, f"{today_str}%"))
    today_acts = [dict(r) for r in cur.fetchall()]

    cur.execute("SELECT COUNT(*) FROM activities WHERE lead_id = ?", (lead_id,))
    touchpoints_count = cur.fetchone()[0] or 0
    conn.close()

    status = lead.get('delta_status', '')

    status_explanations = {
        "URGENT_INBOUND_TODAY": "Inbound email received confirming board authorization with minor indemnification tweak required before end of day.",
        "SECURITY_REVIEW_CLEARED": "CISO signed off on SOC2 Type II clearance; requested executive briefing today.",
        "EXECUTIVE_JOINED_EVAL": "Clinical Executive joined evaluation demo, confirming operational urgency across key hospital networks.",
        "FISCAL_YEAR_END_FRIDAY": "Fiscal year-end budget surplus deadline expires this week. Needs procurement lock call today.",
        "CONTRACT_REDLINE_RECEIVED": "CTO submitted clean SLA redlines; requested finalized DocuSign agreement.",
        "SIGNATURE_PENDING_TODAY": "DocuSign opened multiple times this morning by VP and Finance leaders.",
        "STALLED_NO_UPDATE_7D": "Zero customer response in 7 business days following key champion departure.",
        "COMPETITOR_EVAL_ACTIVE": "Competitor pitched aggressive first-year discount; evaluation cycle extended.",
        "BUDGET_FROZEN_UNTIL_Q1": "Corporate procurement budget reassessment froze external software expenditures.",
        "TECH_PO_APPROVED": "Finance committee officially sanctioned PO; requires technical architecture signoff.",
        "DECISION_MAKER_ON_LEAVE": "Key stakeholder on sabbatical; alternate lacks requisite signing authority."
    }

    explanation = status_explanations.get(status, f"Activity recorded on {lead.get('last_activity_date', today_str)}.")

    return {
        "lead_id": lead_id,
        "delta_code": status,
        "has_delta": len(today_acts) > 0 or (status != "" and status != "LOW_ENGAGEMENT"),
        "today_activities_count": len(today_acts),
        "explanation": explanation,
        "last_activity_date": lead.get('last_activity_date'),
        "touchpoints_count": touchpoints_count
    }
