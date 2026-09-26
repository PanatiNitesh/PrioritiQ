import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import threading

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "prioritiq.db"))
_db_lock = threading.Lock()

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for high concurrency read/write
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_database():
    with _db_lock:
        conn = get_connection()
        cur = conn.cursor()

        # 1. users
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'Sales Manager',
            team TEXT DEFAULT 'Enterprise Sales',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. companies
        cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            domain TEXT,
            industry TEXT,
            employees INTEGER,
            annual_revenue REAL,
            tech_stack TEXT,
            region TEXT,
            icp_fit_score INTEGER
        );
        """)

        # 3. products
        cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            tier TEXT NOT NULL,
            base_annual_price REAL,
            description TEXT
        );
        """)

        # 4. leads
        cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id TEXT PRIMARY KEY,
            company_id TEXT REFERENCES companies(id),
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            title TEXT,
            status TEXT NOT NULL,
            source TEXT DEFAULT 'Inbound',
            industry TEXT,
            deal_value REAL NOT NULL DEFAULT 0.0,
            intent_score REAL DEFAULT 50.0,
            est_effort_mins INTEGER DEFAULT 30,
            assigned_rep_id TEXT REFERENCES users(id),
            assigned_rep_name TEXT DEFAULT 'Alex Rivera',
            churn_risk TEXT DEFAULT 'Low',
            last_activity_date TEXT,
            delta_status TEXT DEFAULT 'ACTIVE',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 5. activities
        cur.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id TEXT PRIMARY KEY,
            lead_id TEXT REFERENCES leads(id),
            user_id TEXT REFERENCES users(id),
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            duration_mins INTEGER DEFAULT 0,
            timestamp TEXT NOT NULL,
            metadata TEXT DEFAULT '{}'
        );
        """)

        # 6. opportunities
        cur.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id TEXT PRIMARY KEY,
            lead_id TEXT REFERENCES leads(id),
            product_id TEXT REFERENCES products(id),
            stage TEXT NOT NULL,
            amount REAL NOT NULL,
            expected_close_date DATE,
            probability REAL DEFAULT 0.5,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 7. decisions (Permanent Persistence)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id TEXT PRIMARY KEY,
            user_id TEXT DEFAULT 'USER-001',
            question TEXT NOT NULL,
            objective TEXT NOT NULL,
            decision_payload TEXT NOT NULL,
            score REAL NOT NULL,
            status TEXT DEFAULT 'PENDING',
            simulation_state TEXT DEFAULT '{}',
            blast_radius TEXT DEFAULT '{}',
            verification_report TEXT DEFAULT '{}',
            approval_details TEXT DEFAULT '{}',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            approved_at TEXT
        );
        """)

        # 8. decision_evidence
        cur.execute("""
        CREATE TABLE IF NOT EXISTS decision_evidence (
            id TEXT PRIMARY KEY,
            decision_id TEXT REFERENCES decisions(id) ON DELETE CASCADE,
            lead_id TEXT REFERENCES leads(id) ON DELETE CASCADE,
            source_type TEXT NOT NULL,
            source_record_id TEXT NOT NULL,
            field TEXT NOT NULL,
            value TEXT NOT NULL,
            weight REAL DEFAULT 1.0,
            fact_checked INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 9. actions
        cur.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id TEXT PRIMARY KEY,
            decision_id TEXT REFERENCES decisions(id) ON DELETE CASCADE,
            lead_id TEXT REFERENCES leads(id) ON DELETE CASCADE,
            action_type TEXT NOT NULL,
            title TEXT NOT NULL,
            assigned_to TEXT,
            status TEXT DEFAULT 'QUEUED',
            payload TEXT NOT NULL,
            audit_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 10. audit_ledger (Append-only Cryptographic Hash Chain)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_ledger (
            event_id TEXT PRIMARY KEY,
            decision_id TEXT NOT NULL,
            query TEXT NOT NULL,
            action TEXT NOT NULL,
            user_role TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            payload TEXT NOT NULL,
            previous_hash TEXT NOT NULL,
            audit_hash TEXT NOT NULL
        );
        """)

        # 11. scoring_rules (Developer Customization API)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS scoring_rules (
            id TEXT PRIMARY KEY,
            rules_json TEXT NOT NULL,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 12. webhooks (Developer Webhook Dispatcher)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS webhooks (
            id TEXT PRIMARY KEY,
            url TEXT NOT NULL,
            event_types TEXT NOT NULL,
            secret TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_company ON leads(company_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_activities_lead ON activities(lead_id, timestamp);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_decisions_created ON decisions(created_at DESC);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_audit_chain ON audit_ledger(timestamp ASC);")

        conn.commit()
        conn.close()

# Auto initialize
init_database()

# ==============================================================================
# DATA ACCESS REPOSITORY METHODS
# ==============================================================================

def get_all_leads_with_companies() -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT 
        l.id as lead_id,
        l.name as lead_name,
        l.email,
        l.phone,
        l.title,
        l.status as stage,
        l.source,
        l.industry,
        l.deal_value as deal_size,
        l.intent_score,
        l.est_effort_mins,
        l.assigned_rep_name as assigned_rep,
        l.churn_risk,
        l.last_activity_date,
        l.delta_status,
        c.id as company_id,
        c.name as company_name,
        c.domain,
        c.employees,
        c.annual_revenue,
        c.tech_stack,
        c.region,
        c.icp_fit_score as icp_fit
    FROM leads l
    LEFT JOIN companies c ON l.company_id = c.id
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def get_lead_by_id(lead_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT 
        l.id as lead_id,
        l.name as lead_name,
        l.email,
        l.phone,
        l.title,
        l.status as stage,
        l.source,
        l.industry,
        l.deal_value as deal_size,
        l.intent_score,
        l.est_effort_mins,
        l.assigned_rep_name as assigned_rep,
        l.churn_risk,
        l.last_activity_date,
        l.delta_status,
        c.id as company_id,
        c.name as company_name,
        c.domain,
        c.employees,
        c.annual_revenue,
        c.tech_stack,
        c.region,
        c.icp_fit_score as icp_fit
    FROM leads l
    LEFT JOIN companies c ON l.company_id = c.id
    WHERE l.id = ?
    """, (lead_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_activities_for_lead(lead_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM activities WHERE lead_id = ? ORDER BY timestamp DESC", (lead_id,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def get_max_dataset_timestamp() -> datetime:
    """
    Dynamically extracts the maximum activity timestamp from the ingested dataset.
    Prevents artificial calendar date decay (Weakness 10).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(timestamp) FROM activities")
    row = cur.fetchone()
    conn.close()
    if row and row[0]:
        try:
            # Parse '2026-09-26 10:10' or ISO format
            clean_ts = row[0].replace('T', ' ').split('.')[0]
            if len(clean_ts) == 16:
                return datetime.strptime(clean_ts, "%Y-%m-%d %H:%M")
            return datetime.strptime(clean_ts[:19], "%Y-%m-%d %H:%M:%S")
        except Exception:
            pass
    return datetime.now()

def persist_decision(decision_id: str, query: str, decision_payload: Dict[str, Any], score: float, sim_state: Dict[str, Any], blast_radius: Dict[str, Any], verification_report: Dict[str, Any]) -> None:
    with _db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO decisions 
        (id, question, objective, decision_payload, score, status, simulation_state, blast_radius, verification_report, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            decision_id,
            query,
            sim_state.get('constraint_explanation', 'Prioritize Sales Leads'),
            json.dumps(decision_payload),
            score,
            'PENDING',
            json.dumps(sim_state),
            json.dumps(blast_radius),
            json.dumps(verification_report),
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

def load_persisted_decision(decision_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM decisions WHERE id = ?", (decision_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d['decision_payload'] = json.loads(d['decision_payload'])
    d['simulation_state'] = json.loads(d['simulation_state'])
    d['blast_radius'] = json.loads(d['blast_radius'])
    d['verification_report'] = json.loads(d['verification_report'])
    return d

def update_decision_approval(decision_id: str, action: str, approved_leads: List[str], manager_notes: Optional[str]) -> bool:
    with _db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        UPDATE decisions 
        SET status = ?, approved_at = ?, approval_details = ?
        WHERE id = ?
        """, (
            action,
            datetime.now().isoformat(),
            json.dumps({"action": action, "approved_leads": approved_leads, "manager_notes": manager_notes}),
            decision_id
        ))
        updated = cur.rowcount > 0
        conn.commit()
        conn.close()
        return updated
