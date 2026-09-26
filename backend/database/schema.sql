-- ==============================================================================
-- PrioritiQ: Enterprise Evidence-Grounded AI Sales Decision Engine Schema
-- PostgreSQL DDL with Indexes, Foreign Keys, and Constraints
-- ==============================================================================

-- 1. USERS
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'Sales Manager', -- Sales Manager, Account Executive, SDR, Admin
    team VARCHAR(100) DEFAULT 'Enterprise Sales',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. COMPANIES (Firmographic Accounts)
CREATE TABLE IF NOT EXISTS companies (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    industry VARCHAR(100),
    employees INTEGER DEFAULT 0,
    annual_revenue NUMERIC(15, 2) DEFAULT 0.00,
    tech_stack TEXT,
    region VARCHAR(100),
    icp_fit_score INTEGER CHECK (icp_fit_score BETWEEN 0 AND 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. PRODUCTS
CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tier VARCHAR(50) NOT NULL, -- Starter, Professional, Enterprise Zero-Trust
    base_annual_price NUMERIC(12, 2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. LEADS (Requested Schema)
CREATE TABLE IF NOT EXISTS leads (
    id VARCHAR(64) PRIMARY KEY,
    company_id VARCHAR(64) REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    title VARCHAR(150),
    status VARCHAR(50) NOT NULL, -- Discovery, Demo, Proposal, Negotiation, Closing, Deferred
    source VARCHAR(100) DEFAULT 'Inbound', -- Inbound, Outbound, Referral, Event
    industry VARCHAR(100),
    deal_value NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    intent_score NUMERIC(5, 2) DEFAULT 50.0,
    est_effort_mins INTEGER DEFAULT 30,
    assigned_rep_id VARCHAR(64) REFERENCES users(id) ON DELETE SET NULL,
    churn_risk VARCHAR(20) DEFAULT 'Low', -- Low, Medium, High
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. ACTIVITIES (Requested Schema)
CREATE TABLE IF NOT EXISTS activities (
    id VARCHAR(64) PRIMARY KEY,
    lead_id VARCHAR(64) REFERENCES leads(id) ON DELETE CASCADE,
    user_id VARCHAR(64) REFERENCES users(id) ON DELETE SET NULL,
    type VARCHAR(50) NOT NULL, -- Email Inbound, Call, Demo, Redline Received, PO Sent
    description TEXT NOT NULL,
    duration_mins INTEGER DEFAULT 0,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb, -- e.g. sentiment score, email subject, notes_ref
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. OPPORTUNITIES (Deals in progress)
CREATE TABLE IF NOT EXISTS opportunities (
    id VARCHAR(64) PRIMARY KEY,
    lead_id VARCHAR(64) REFERENCES leads(id) ON DELETE CASCADE,
    product_id VARCHAR(64) REFERENCES products(id) ON DELETE SET NULL,
    stage VARCHAR(50) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    expected_close_date DATE,
    probability NUMERIC(4, 3) DEFAULT 0.50,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. DECISIONS (Requested Schema)
CREATE TABLE IF NOT EXISTS decisions (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) REFERENCES users(id) ON DELETE SET NULL,
    question TEXT NOT NULL, -- e.g. "Which leads should my sales team prioritize today?"
    objective VARCHAR(255) NOT NULL, -- "Maximize expected ARR under 3 hour time constraint"
    decision JSONB NOT NULL, -- Recommended ranked list of leads with weights
    score NUMERIC(5, 2) NOT NULL DEFAULT 0.0, -- Composite engine score
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- PENDING, APPROVED, EDITED, REJECTED
    simulation_state JSONB DEFAULT '{}'::jsonb, -- Time bounds, knapsack allocation, slack
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP WITH TIME ZONE
);

-- 8. DECISION_EVIDENCE (Requested Schema)
CREATE TABLE IF NOT EXISTS decision_evidence (
    id VARCHAR(64) PRIMARY KEY,
    decision_id VARCHAR(64) REFERENCES decisions(id) ON DELETE CASCADE,
    lead_id VARCHAR(64) REFERENCES leads(id) ON DELETE CASCADE,
    source_type VARCHAR(50) NOT NULL, -- crm_structured, rag_email, rag_call_transcript, rag_contract
    source_record_id VARCHAR(255) NOT NULL, -- NOTE-LEAD-101-04.txt or ACT-301
    field VARCHAR(100) NOT NULL, -- deal_size, cfo_budget_approval, soc2_clearance
    value TEXT NOT NULL, -- Grounded verbatim quote or quantitative number
    weight NUMERIC(4, 3) DEFAULT 1.000, -- Multi-agent factor weighting
    fact_checked BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. ACTIONS (Dispatched CRM Tasks, Generated Rep Emails)
CREATE TABLE IF NOT EXISTS actions (
    id VARCHAR(64) PRIMARY KEY,
    decision_id VARCHAR(64) REFERENCES decisions(id) ON DELETE CASCADE,
    lead_id VARCHAR(64) REFERENCES leads(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL, -- DISPATCH_EMAIL, CREATE_CRM_TASK, SCHEDULE_CALL
    title VARCHAR(255) NOT NULL,
    assigned_to VARCHAR(64) REFERENCES users(id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'QUEUED', -- QUEUED, DISPATCHED, COMPLETED
    payload JSONB NOT NULL, -- email subject, body, CRM deadline
    audit_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- INDEXES FOR LOW-LATENCY DETERMINISTIC ANALYTICS
-- ==============================================================================
CREATE INDEX IF NOT EXISTS idx_leads_company_id ON leads(company_id);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_deal_value ON leads(deal_value DESC);
CREATE INDEX IF NOT EXISTS idx_activities_lead_timestamp ON activities(lead_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_decisions_created_at ON decisions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_decision_evidence_decision_id ON decision_evidence(decision_id);
CREATE INDEX IF NOT EXISTS idx_actions_decision_id ON actions(decision_id);
