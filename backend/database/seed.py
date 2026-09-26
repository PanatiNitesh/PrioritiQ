import os
import json
import pandas as pd
from .db import get_connection, init_database

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

def seed_database(force: bool = False):
    init_database()
    conn = get_connection()
    cur = conn.cursor()

    if not force:
        cur.execute("SELECT COUNT(*) FROM leads;")
        count = cur.fetchone()[0]
        if count > 0:
            conn.close()
            return

    # Clear existing if force
    if force:
        cur.execute("DELETE FROM activities;")
        cur.execute("DELETE FROM leads;")
        cur.execute("DELETE FROM companies;")
        cur.execute("DELETE FROM users;")

    # 1. Seed Users
    users = [
        ("USER-001", "Marcus Chen", "mchen@prioritiq.ai", "Sales Manager", "Enterprise Sales"),
        ("USER-002", "Alex Rivera", "arivera@prioritiq.ai", "Account Executive", "Mid-Market / Enterprise"),
        ("USER-003", "Elena Rostova", "erostova@prioritiq.ai", "Senior AE", "Healthcare & Tech"),
        ("USER-004", "Devon Miller", "dmiller@prioritiq.ai", "Strategic AE", "Energy & Manufacturing")
    ]
    cur.executemany("INSERT OR REPLACE INTO users (id, name, email, role, team) VALUES (?, ?, ?, ?, ?)", users)

    # 2. Seed Companies
    comp_csv = os.path.join(DATA_DIR, "companies.csv")
    if os.path.exists(comp_csv):
        comp_df = pd.read_csv(comp_csv)
        for _, r in comp_df.iterrows():
            cur.execute("""
            INSERT OR REPLACE INTO companies (id, name, domain, industry, employees, annual_revenue, tech_stack, region, icp_fit_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r['company_id'], r['name'], r['domain'], r['industry'],
                int(r['employees']), float(r['annual_revenue']), r['tech_stack'],
                r['region'], int(r['icp_fit'])
            ))

    # 3. Seed Leads
    leads_csv = os.path.join(DATA_DIR, "leads.csv")
    if os.path.exists(leads_csv):
        leads_df = pd.read_csv(leads_csv)
        for _, r in leads_df.iterrows():
            cur.execute("""
            INSERT OR REPLACE INTO leads 
            (id, company_id, name, email, phone, title, status, source, industry, deal_value, intent_score, est_effort_mins, assigned_rep_name, churn_risk, last_activity_date, delta_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r['lead_id'], r['company_id'], r['name'], r['email'],
                r['phone'], r['title'], r['stage'], 'Inbound Evaluation',
                'Enterprise Tech', float(r['deal_size']), float(r['intent_score']),
                int(r['est_effort_mins']), r.get('assigned_rep', 'Alex Rivera'),
                r['churn_risk'], r.get('last_activity_date', '2026-09-26'),
                r.get('delta_status', 'ACTIVE')
            ))

    # 4. Seed Activities
    act_csv = os.path.join(DATA_DIR, "activities.csv")
    if os.path.exists(act_csv):
        act_df = pd.read_csv(act_csv)
        for _, r in act_df.iterrows():
            cur.execute("""
            INSERT OR REPLACE INTO activities (id, lead_id, type, description, duration_mins, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                r['activity_id'], r['lead_id'], r['type'], r['outcome'],
                int(r['duration']), r['timestamp'], json.dumps({"notes_ref": r.get('notes_ref', ''), "rep": r.get('rep', '')})
            ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_database(force=True)
    print("Database seeded with fresh ground-truth records.")
