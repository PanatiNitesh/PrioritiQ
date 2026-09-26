# PrioritiQ: Enterprise Evidence-Grounded AI Sales Decision Engine

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-0F766E?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-Production%20Ready-0284C7?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React%2019-TypeScript-3B82F6?style=for-the-badge&logo=react&logoColor=white" />
  <img src="https://img.shields.io/badge/Vite-5.4-8B5CF6?style=for-the-badge&logo=vite&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-WAL%20Mode-059669?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Tests-63%20Passed%20(100%25)-10B981?style=for-the-badge&logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/Audit-Cryptographic%20SHA--256-D97706?style=for-the-badge&logo=vault&logoColor=white" />
</p>

> **Core Philosophy**: Never entrust mission-critical commercial strategy to an ungrounded LLM that hallucinates sales priorities.  
> **The Solution**: Deterministic Analytics + Semantic Hybrid RAG + 2D Knapsack Capacity Optimization + Blast-Radius Risk Modeling + Primary-Key Fact Checking + Cryptographic Hash Chain Audit Ledger + Human-in-the-Loop Governance.

---

## 🎯 Executive Overview

**PrioritiQ** is an enterprise sales decision intelligence engine designed for VP of Sales, Revenue Operations, and Sales Managers who must answer high-stakes commercial questions with **100% mathematical and factual integrity**:

* **"Which leads should my sales team prioritize today, and why?"** (Deterministic multi-factor composite scoring)
* **"What if my team only has 3 hours?"** (2D Dynamic Programming knapsack solver packing highest ROI accounts without violating time bounds or deal limits)
* **"What is the collateral damage of deferring accounts?"** (Pre-execution blast-radius prediction calculating account attrition, rep skew variance, and quarter-end commit slippage)
* **"Why this lead and why not another (e.g., Vanguard Logistics)?"** (Multi-dimensional counterfactual tradeoff analysis with line-level RAG citations)
* **"What changed since yesterday?"** (Real-time CRM and activity delta detection evaluated against dynamic dataset epochs)
* **"Approve and execute this recommendation"** (Immutable approval pipeline generating personalized outreach drafts and appending to a cryptographic SHA-256 hash chain ledger)

---

## ⚔️ PrioritiQ vs. The Competition

Most sales organizations rely either on legacy **Black-Box CRM Scoring** (arbitrary opacity) or **Generic LLM Wrappers** (hallucination-prone, operationally blind). PrioritiQ provides a transparent, verifiable, and constrained decision intelligence platform:

| Capability | Traditional CRM AI (Salesforce Einstein, HubSpot) | Generic LLM Chatbots & Copilots (ChatGPT, Copilot) | PrioritiQ Enterprise Decision Engine |
| :--- | :--- | :--- | :--- |
| **Grounding & Proof** | ❌ **Black Box**: Arbitrary number (e.g. `82`) with zero provenance or source line citations | ⚠️ **Hallucination Risk**: Invented facts, misquoted numbers, fabricated email context | ✅ **100% Grounded**: Every claim backed by database primary keys and verbatim line-level RAG quotes |
| **Operational Constraints** | ❌ **Blind**: Scores leads in vacuum; ignores sales rep hours, meeting limits, or team bandwidth | ❌ **Incapable**: Cannot solve mathematical knapsack packing problems | ✅ **2D Knapsack DP**: Exact mathematical 0/1 capacity optimization under strict operational time and count limits |
| **Blast-Radius Modeling** | ❌ **Non-existent**: Zero insight into cost of account neglect or rep burn-out | ❌ **Non-existent**: Zero cascading impact calculations | ✅ **Pre-Execution Predictor**: Computes daily churn attrition cost, rep load skew (`±10.8 mins`), and quota commit slippage |
| **Governance & Auditability** | ❌ **Mutable**: Overwritten logs, no cryptographic chain of custody | ❌ **Volatile**: Transient chat histories without enterprise audit trails | ✅ **Tamper-Evident Ledger**: Append-only SHA-256 cryptographic hash chain linking each block to `previous_hash` |
| **Counterfactual Analysis** | ❌ **No comparative rationale** ("Why lead A over lead B?") | ⚠️ **Subjective**: Chatbot rationalizations without grounded metric differentials | ✅ **Deterministic Tradeoffs**: Exact side-by-side differentiators on authority, velocity, deal value, and risk |
| **Action Personalization** | ⚠️ **Canned**: Rigid, robotic merge-tag templates | ⚠️ **Unchecked**: LLMs draft emails with unverified claims or inaccurate pricing | ✅ **Contextual Synthesis**: Auto-generates outreach drafts synthesizing legal redlines, SOC2 clearances, and executive notes |
| **Developer Extensibility** | ❌ **Proprietary Lock-in**: Hardcoded logic requires vendor professional services | ⚠️ **Fragile**: Fragile prompt engineering without schemas or webhooks | ✅ **Full Developer APIs**: Dynamic Scoring Rules API (`/api/decisions/config/rules`) and HMAC-SHA256 Webhook Dispatcher |

---

## 🏛️ System Architecture

PrioritiQ separates **deterministic mathematical calculation** from **unstructured semantic retrieval** before synthesizing them into actionable, verifiable decisions:

```mermaid
flowchart TD
    subgraph DataLayer ["Enterprise Data Ingestion & Storage"]
        DB[(prioritiq.db<br/>SQLite WAL / PostgreSQL)]
        CRM[Structured CRM Records<br/>Leads, Companies, Deals]
        Acts[Activity Telemetry<br/>Touchpoints & Engagements]
        Notes[Unstructured Knowledge Corpus<br/>Call Transcripts, Emails, SLA Redlines]
        DB --> CRM
        DB --> Acts
        Notes --> Chunker[Sliding-Window Chunker<br/>120w window / 25w overlap]
        Chunker --> RAGIdx[Hybrid Semantic Vector Index<br/>BM25 + Dense Embeddings]
    end

    subgraph AgentLayer ["Multi-Agent AI Orchestration Pipeline"]
        Manager([Sales Manager / VP of Sales]) -->|Natural Language Query| IntentAgent[Structured Intent Orchestrator<br/>Compound Query Parsing]
        IntentAgent --> Planner[Query Plan & Constraint Extractor]
        
        Planner -->|Time & Strategy Bounds| AnalyticsAgent[Analytics Agent<br/>Deterministic Scoring & 2D Knapsack]
        Planner -->|Entity & Context Lookup| RetrievalAgent[Retrieval Agent<br/>Line-Level Citation Extractor]
        
        CRM & Acts --> AnalyticsAgent
        RAGIdx --> RetrievalAgent
        
        AnalyticsAgent --> DecisionEngine[PrioritiQ Decision Engine]
        RetrievalAgent --> DecisionEngine
    end

    subgraph EvaluationLayer ["Decision & Governance Guardrails"]
        DecisionEngine --> BlastRadius[Blast-Radius Predictor<br/>Attrition & Rep Skew Modeling]
        DecisionEngine --> VerificationAgent[Verification Agent<br/>PK DB Cross-Check & NLI Entailment]
        DecisionEngine --> ActionGen[Dynamic Contextual Action Generator<br/>Outreach Briefing & Subject Synthesis]
        
        BlastRadius & VerificationAgent & ActionGen --> DAG[Interactive Explainability DAG<br/>SVG Cubic-Bezier Directed Lineage]
    end

    subgraph GovernanceLayer ["Execution, Webhooks & Cryptographic Audit"]
        DAG --> UI[PrioritiQ Nordic Web Console]
        UI -->|Sales Manager Approval| HumanGate{Human-in-the-Loop Gate}
        HumanGate -->|Approve / Edit| Dispatcher[HMAC-SHA256 Webhook Dispatcher<br/>Salesforce, HubSpot, Zapier, Slack]
        HumanGate -->|Tamper-Evident Event| AuditChain[(Cryptographic Hash Chain<br/>SHA-256 Append-Only Ledger)]
        AuditChain --> Verifier[Audit Chain Verifier API<br/>100% Preimage Verification]
    end

    classDef primary fill:#0F766E,stroke:#0B5650,color:#fff;
    classDef secondary fill:#FBFBF9,stroke:#E5E5DF,color:#0F172A;
    classDef accent fill:#D97706,stroke:#B45309,color:#fff;
    class IntentAgent,DecisionEngine,VerificationAgent primary;
    class DataLayer,EvaluationLayer secondary;
    class BlastRadius,HumanGate,AuditChain accent;
```

---

## 🚀 What We Have Done: The PrioritiQ Solution

PrioritiQ was built from the ground up to eliminate the critical failure points of current enterprise decision tools:

### 1. Deterministic Multi-Factor Lead Scoring Engine
Instead of arbitrary neural-net predictions, PrioritiQ calculates deterministic composite scores across verified dimensions:
* **Deal Normalization**: Calibrated log-scale normalization across pipeline values.
* **Stage Probability Weights**: Dynamic multipliers according to sales pipeline milestones (`Closing = 1.0`, `Negotiation = 0.88`, `Proposal = 0.72`, `Demo = 0.55`, `Discovery = 0.35`).
* **Behavioral Intent & Touchpoint Velocity**: Real-time engagement frequency from inbound telemetry.
* **Enterprise ICP Alignment**: Firmographic fit scored against target employee tiers, annual revenue, and technology stack compatibility.
* **Dynamic Recency Decay**: Time decay modeled dynamically from the latest activity timestamp in the database, preventing stale calendar decay.

### 2. Two-Dimensional Bounded Knapsack DP Solver
Standard CRM tools order leads linearly by score, ignoring the fact that sales reps have strict shift boundaries. When a manager asks *"What if my team only has 3 hours?"*, PrioritiQ formulates a **2D Bounded Dynamic Programming Knapsack Solver**:

```text
Maximize:   Σ Final_Score_i   for all selected leads i ∈ S
Subject To: Σ Effort_Mins_i ≤ Available_Time_Mins
            |S| ≤ Requested_Limit
```

* **Capacity Constraint**: Allocates deals so that cumulative rep effort never exceeds the available time budget.
* **Cardinality Limit**: Guarantees output conforms to requested page size bounds.
* **Direct Objective Alignment**: Directly maximizes strategic score without distorting deal size, ensuring user strategies like `Velocity` or `Balanced` remain strictly honored.

### 3. Pre-Execution Blast-Radius Predictor
Every resource prioritization decision creates trade-offs. PrioritiQ models downstream operational consequences before recommendations are executed:

* **Account Attrition Cost**: Calculates the pipeline exposure of excluded accounts, especially high-churn customers left unserviced:
  ```text
  Daily Attrition Risk = Σ (Deal_Size_i × Churn_Probability_i)  for all i ∈ Excluded_Accounts
  ```
* **Sales Rep Capacity Skew & Bottlenecks**: Analyzes rep workload balance, computes the standard deviation of allocated effort (`±10.8 mins`), and flags operational bottlenecks (e.g. assigning one rep 190 minutes while another receives 0 minutes).
* **Quota & Commitment Slippage**: Flags late-stage deals (Negotiation, Proposal) deferred outside the immediate schedule to protect quarterly forecasts.
* **Live Governance Warnings**: Surfaces collateral damage warnings directly on the approval console.

### 4. Zero-Hallucination Verification Agent
PrioritiQ implements verifiable proof mechanisms across every recommendation:

* **Primary-Key Database Integrity**: Directly queries the `prioritiq.db` database using primary keys (`LEAD-101`, `COMP-201`). Validates that `deal_size`, `stage`, and `assigned_rep` have not been mutated or corrupted.
* **Citation Quote Provenance**: Cross-references every retrieved citation against the underlying source documents (emails, meeting transcripts, contract redlines) to confirm quote authenticity.
* **Semantic Entailment Verification**: Evaluates lexical entailment between recommendation claims and cited evidence.
* **Calibrated Confidence**: Computes dynamic grounding scores (e.g., `94.2%`) rather than displaying static marketing strings.

### 5. Append-Only Cryptographic Hash Chain Audit Ledger
Enterprise compliance requires immutable accountability:

* **SHA-256 Preimage Chaining**: Each audit entry incorporates the hash of the preceding block into its calculation:
  ```text
  Audit_Hash_k = SHA-256( Previous_Hash_(k-1) || Event_ID_k || Decision_ID_k || Timestamp_k || Action_k || Payload_k )
  ```
* **Thread-Safe ACID Transactions**: Writes are protected by database transactions and concurrency locks to prevent race conditions during concurrent manager approvals.
* **Cryptographic Verification Endpoint**: Provides `GET /api/decisions/audit/verify` which verifies the entire ledger from the Genesis block to detect historical tampering.

### 6. Semantic Hybrid RAG Layer
Unstructured enterprise knowledge is indexed and retrieved with line-level attribution:

* **Sliding-Window Chunker**: Segments complex agreements, call notes, and transcripts into 120-word windows with 25-word overlaps.
* **Hybrid Retrieval**: Combines semantic embeddings with exact token containment for domain-specific terminology (e.g. Section 9.2 indemnification, SOC2 Type II clearance, CapEx fiscal deadlines).
* **Verbatim Provenance**: Citations specify the exact source file, author, timestamp, and verbatim quote.

### 7. Interactive Explainability DAG (Directed Acyclic Graph)
The frontend console provides complete visual transparency into decision logic:

* **Curved SVG Connectors**: Renders cubic bezier splines with directional arrowheads linking `Policy & Goals` $\to$ `Selected Accounts` $\to$ `Grounded Evidence` $\to$ `Dispatched Actions`.
* **Interactive Hover Lineage**: Hovering over or clicking any account card highlights its entire causal lineage while dimming unrelated graph elements.
* **Deep Inspection**: Clicking any node opens a detail drawer displaying source files, confidence levels, and connected relational edges.

### 8. Dynamic Contextual Action Generator & Webhooks
* **Personalized Outreach Briefs**: Synthesizes lead metadata, stage signals, and RAG citations to automatically compose targeted outreach titles and emails.
* **HMAC-SHA256 Webhook Dispatcher**: Asynchronously dispatches cryptographically signed payloads to external webhooks (Salesforce, HubSpot, Zapier, Slack) upon manager approval.
* **Dynamic Scoring Rules API**: Exposes `/api/decisions/config/rules` allowing RevOps teams to tune stage weights, strategy weightings, and churn penalties at runtime without code redeployments.

---

## 🗄️ Relational Database Schema

PrioritiQ provides production-ready PostgreSQL DDL (`backend/database/schema.sql`) and operates with an indexed SQLite WAL-mode engine (`data/prioritiq.db`):

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    COMPANIES    │       │      USERS      │       │    PRODUCTS     │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ name            │       │ name            │       │ name            │
│ employees       │       │ email           │       │ tier            │
│ annual_revenue  │       │ role            │       │ base_price      │
│ icp_fit_score   │       │ team            │       │ description     │
└────────┬────────┘       └────────┬────────┘       └────────┬────────┘
         │                         │                         │
         └────────────┬────────────┘                         │
                      ↓                                      │
            ┌───────────────────┐                            │
            │       LEADS       │                            │
            ├───────────────────┤                            │
            │ id (PK)           │                            │
            │ company_id (FK)   │                            │
            │ name, email       │                            │
            │ deal_value        │                            │
            │ intent_score      │                            │
            │ est_effort_mins   │                            │
            │ assigned_rep (FK) │                            │
            │ churn_risk        │                            │
            │ status / stage    │                            │
            └─────────┬─────────┘                            │
                      │                                      │
       ┌──────────────┴──────────────┐                       │
       ↓                             ↓                       ↓
┌──────────────┐             ┌───────────────┐     ┌───────────────────┐
│  ACTIVITIES  │             │   DECISIONS   │     │   OPPORTUNITIES   │
├──────────────┤             ├───────────────┤     ├───────────────────┤
│ id (PK)      │             │ id (PK)       │     │ id (PK)           │
│ lead_id (FK) │             │ question      │     │ lead_id (FK)      │
│ user_id (FK) │             │ decision_data │     │ product_id (FK)   │
│ type         │             │ blast_radius  │     │ amount, stage     │
│ timestamp    │             │ score, status │     │ probability       │
└──────────────┘             └───────┬───────┘     └───────────────────┘
                                     │
                      ┌──────────────┴──────────────┐
                      ↓                             ↓
            ┌───────────────────┐         ┌───────────────────┐
            │ DECISION_EVIDENCE │         │      ACTIONS      │
            ├───────────────────┤         ├───────────────────┤
            │ id (PK)           │         │ id (PK)           │
            │ decision_id (FK)  │         │ decision_id (FK)  │
            │ lead_id (FK)      │         │ lead_id (FK)      │
            │ field, value      │         │ action_type       │
            │ fact_checked      │         │ payload, audit_h  │
            └───────────────────┘         └───────────────────┘
```

Infrastructure tables:
* **`audit_ledger`**: Stores immutable events with `previous_hash` and `audit_hash` forming a verifiable SHA-256 hash chain.
* **`scoring_rules`**: Stores active dynamic scoring policy configurations.
* **`webhooks`**: Stores registered outbound endpoints with HMAC secrets and subscribed event types.

---

## ⚡ Quickstart & Installation

### Prerequisites
* **Python**: 3.10+ (tested on Python 3.13)
* **Node.js**: v18+ with `npm`

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/PanatiNitesh/PrioritiQ.git
cd PrioritiQ

# Python virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install backend dependencies
pip install fastapi uvicorn pandas scikit-learn pydantic pytest
```

### 2. Initialize Database & Seed Ground-Truth Data
```bash
python -m backend.database.seed
```

### 3. Run Automated Test Suite (63 Tests)
```bash
python -m pytest tests -v
```
All 63 unit, integration, and benchmark tests pass in ~1 second.

### 4. Launch Backend API Server
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive Swagger API documentation is available at `http://127.0.0.1:8000/docs`.

### 5. Launch Frontend Application
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` to access the PrioritiQ console.

---

## 📡 REST API Reference

### Decisions API
* **`POST /api/decisions/query`**: Process natural language query with optional time budget or strategy overrides.
  ```json
  {
    "query": "If I have 2 hours, prioritize deal value, but why not Vanguard?",
    "time_budget_hours": 2.0,
    "priority_weight": "deal_value",
    "target_lead_id": "LEAD-107"
  }
  ```
* **`GET /api/decisions/{decision_id}`**: Retrieves immutable persisted decision dossier (returns strict HTTP 404 if not found).
* **`POST /api/decisions/approve`**: Human-in-the-loop governance endpoint. Updates status to `APPROVED`, creates queued tasks, and appends to audit ledger.
* **`GET /api/decisions/history`**: Returns historical audit chain records.
* **`GET /api/decisions/audit/verify`**: Cryptographically traverses and verifies the entire SHA-256 hash chain from genesis block.

### Developer Configuration & Webhook APIs
* **`GET /api/decisions/config/rules`**: Returns active stage weights, strategy weightings, and churn penalty multipliers.
* **`POST /api/decisions/config/rules`**: Dynamically updates scoring rules at runtime without code deployment.
* **`GET /api/decisions/config/webhooks`**: Lists registered outbound webhook integrations.
* **`POST /api/decisions/config/webhooks`**: Registers external webhook with automatic HMAC-SHA256 signature verification.
  ```json
  {
    "url": "https://hooks.zapier.com/hooks/catch/prioritiq",
    "event_types": ["decision.approved", "task.dispatched"],
    "secret": "whsec_enterprise_secret_key"
  }
  ```

---

## 🎨 UI & Design Philosophy

PrioritiQ features a custom **Nordic Verdigris & Warm Sand** design system engineered for executive focus:

* **Background**: Warm Sand porcelain (`#F7F7F5`) with crisp sub-panels (`#FBFBF9`).
* **Primary Accent**: Deep Nordic Verdigris (`#0F766E` / `#005F56`) delivering high contrast without corporate blue fatigue.
* **Typography**: Clean, modern Plus Jakarta Sans with monospace telemetry counters (`ui-monospace`, `JetBrains Mono`).
* **Borders & Elevation**: Subtle 1px borders (`#E5E5DF`) with soft micro-shadows, completely avoiding harsh dark-mode clashes.

---

## 🧪 Verification & Benchmark Results

PrioritiQ ships with a comprehensive test suite in [tests/](file:///d:/hackproject/New%20folder/PrioritiQ/tests):

1. **`test_knapsack.py`**:
   * Adherence to time budget across varying hour blocks.
   * Adherence to cardinality limit bounds.
   * Objective value alignment with strategic weights.
2. **`test_verification_agent.py`**:
   * Authentic primary-key match verification.
   * Rejection of corrupted deal sizes ($>\$9,000,000$).
   * Rejection of non-existent leads.
3. **`test_blast_radius.py`**:
   * Excluded pipeline calculation and high-churn neglect alerts.
   * Sales rep capacity skew and workload standard deviation detection.
4. **`test_audit_chain.py`**:
   * SHA-256 cryptographic chain continuity and `previous_hash` linking.
   * Verification of ledger integrity.
5. **`test_rag_eval.py`**:
   * Retrieval accuracy over knowledge corpus: **Recall@4 $\ge 0.75$**, **MRR $\ge 0.70$**.
6. **`test_benchmark_50_queries.py`**:
   * 50 golden queries spanning general prioritization, time limits, strategy weights, counterfactuals, and approvals.

---

## 📄 License & Intellectual Property

This project is licensed under the MIT License - see the [LICENSE](file:///d:/hackproject/New%20folder/PrioritiQ/LICENSE) file for details. Built for enterprise commercial decision intelligence.
