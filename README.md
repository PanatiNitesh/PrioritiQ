# PrioritiQ: Enterprise Evidence-Grounded AI Sales Decision Engine

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-0F766E?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-Production%20Ready-0284C7?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React%2018-TypeScript-3B82F6?style=for-the-badge&logo=react&logoColor=white" />
  <img src="https://img.shields.io/badge/Vite-5.4-8B5CF6?style=for-the-badge&logo=vite&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-WAL%20Mode-059669?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Tests-88%20Passed%20(100%25)-10B981?style=for-the-badge&logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/Audit-Cryptographic%20SHA--256-D97706?style=for-the-badge&logo=vault&logoColor=white" />
  <img src="https://img.shields.io/badge/Monte%20Carlo-1000%20Trials-8B5CF6?style=for-the-badge&logo=affinity&logoColor=white" />
  <a href="https://prioritiq-ai.onrender.com" target="_blank"><img src="https://img.shields.io/badge/Live%20Demo-prioritiq--ai.onrender.com-46E3B7?style=for-the-badge&logo=render&logoColor=white" /></a>
</p>

> **Core Philosophy**: Never entrust mission-critical commercial strategy to an ungrounded LLM that hallucinates sales priorities.  
> **The Solution**: Deterministic Analytics + Semantic Hybrid RAG + 2D Knapsack Capacity Optimization + Blast-Radius Risk Modeling + Monte Carlo Stochastic Simulation + Primary-Key Fact Checking + Cryptographic Hash Chain Audit Ledger + Human-in-the-Loop Governance.

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

| Capability | Traditional CRM AI (Salesforce, HubSpot) | Generic LLM Chatbots & Copilots | PrioritiQ Enterprise Decision Engine |
| :--- | :--- | :--- | :--- |
| **Grounding & Proof** | ❌ **Black Box**: Arbitrary numbers with zero provenance or source line citations | ⚠️ **Hallucination Risk**: Invented facts, misquoted numbers, fabricated email context | ✅ **100% Grounded**: Every claim backed by database primary keys and verbatim line-level RAG quotes |
| **Operational Constraints** | ❌ **Blind**: Scores leads in vacuum; ignores sales rep hours or team bandwidth | ❌ **Incapable**: Cannot solve mathematical knapsack packing problems | ✅ **2D Knapsack DP**: Exact mathematical 0/1 capacity optimization under strict operational time and count limits |
| **Blast-Radius Modeling** | ❌ **Non-existent**: Zero insight into cost of account neglect or rep burn-out | ❌ **Non-existent**: Zero cascading impact calculations | ✅ **Pre-Execution Predictor**: Computes daily churn attrition cost, rep load skew, and quota commit slippage |
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
        DB[(SQLite WAL DB)]
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

## 🚀 Core Engine Capabilities

### 1. Deterministic Multi-Factor Lead Scoring Engine
Instead of arbitrary neural-net predictions, PrioritiQ calculates deterministic composite scores across verified dimensions:
* **Deal Normalization**: Calibrated log-scale normalization across pipeline values.
* **Stage Probability Weights**: Dynamic multipliers according to sales pipeline milestones (`Closing = 1.0`, `Negotiation = 0.88`, `Proposal = 0.72`, `Demo = 0.55`, `Discovery = 0.35`).
* **Behavioral Intent & Touchpoint Velocity**: Real-time engagement frequency from inbound telemetry.
* **Enterprise ICP Alignment**: Firmographic fit scored against target employee tiers, annual revenue, and technology stack compatibility.
* **Dynamic Recency Decay**: Time decay modeled dynamically from the latest activity timestamp in the database (`get_max_dataset_timestamp()`), preventing stale calendar decay.

### 2. Two-Dimensional Bounded Knapsack DP Solver
Standard CRM tools order leads linearly by score, ignoring the fact that sales reps have strict shift boundaries. When a manager asks *"What if my team only has 3 hours?"*, PrioritiQ formulates a **2D Bounded Dynamic Programming Knapsack Solver**:

```text
Maximize:   SUM(Final_Score_i)  for all i in Selected
Subject To: SUM(Effort_Mins_i) <= Available_Time_Mins
            Count(Selected)    <= Requested_Limit
```

* **Capacity Constraint**: Allocates deals so that cumulative rep effort never exceeds the available time budget.
* **Cardinality Limit**: Guarantees output conforms to requested page size bounds.
* **Direct Objective Alignment**: Directly maximizes strategic score without distorting deal size, ensuring user strategies like `Velocity` or `Balanced` remain strictly honored.
* **Defensive Edge Handling**: Gracefully handles 0 or negative budgets, providing exact operational feedback.

### 3. Pre-Execution Blast-Radius Predictor
Every resource prioritization decision creates trade-offs. PrioritiQ models downstream operational consequences before recommendations are executed:

* **Account Attrition Cost**: Calculates the pipeline exposure of excluded accounts, especially high-churn customers left unserviced:
  ```text
  Daily Attrition Risk = SUM over excluded accounts of (Deal_Size_i * Churn_Probability_i)
  ```
* **Sales Rep Capacity Skew & Bottlenecks**: Analyzes rep workload balance, computes the standard deviation of allocated effort (`±10.8 mins`), and flags operational bottlenecks.
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
  Audit_Hash[k] = SHA-256(Previous_Hash[k-1] || Event_ID[k] || Decision_ID[k] || Timestamp[k] || Action[k] || Payload[k])
  ```
* **Thread-Safe ACID Transactions**: Writes are protected by database transactions and concurrency locks (`_db_lock`) to prevent race conditions during concurrent manager approvals.
* **Cryptographic Verification Endpoint**: Provides `GET /api/decisions/audit/verify` which verifies the entire ledger from the Genesis block to detect historical tampering.
* **Adversarial Tamper Detection Tested**: Automated test suites assert that any modification of historical payloads or previous hashes immediately breaks the chain and flags the exact corrupted event ID.

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

### 9. Stochastic Monte Carlo Pipeline Risk & Revenue Simulation (1,000 Iterations)
Deterministic scores provide an optimal schedule, but sales leaders also need to understand revenue variance and tail risk:
* **1,000-Trial Stochastic Engine**: Dynamically simulates 1,000 macroeconomic realization passes combining win probabilities, stage slippage, and volatility factors.
* **P10, P50, P90 Value-at-Risk**: Projects conservative (P10: 90% confidence), median expected (P50), and upside potential (P90) pipeline revenues.
* **Benchmark Alpha vs Legacy CRM**: Quantifies the mathematical lift delivered by PrioritiQ's knapsack-packed schedule over chronological legacy CRM outreach.
* **Interactive Probability Density Histogram**: Visualizes the simulated revenue bell curve with color-coded quartile markers and risk metrics.

### 10. RevOps Live Policy & Scoring Rule Studio
Gives Revenue Operations complete visual and programmatic control over prioritization formulas:
* **Interactive Stage Multipliers**: Adjust weights for Closing, Negotiation, Proposal, Demo, and Discovery stages in real time.
* **Strategy Weighting Balancer**: Tune the relative importance of Deal Size, Behavioral Intent, ICP Fit, and Velocity across presets (`balanced`, `deal_value`, `velocity`, `win_rate`).
* **Dynamic Recency Decay Half-Life**: Fine-tune decay half-lives (1.0 to 14.0 days) against real inbound telemetry.
* **Real-Time Rank Shift Impact Engine**: Calculates prospective score deltas and rank changes across the live pipeline before committing changes to disk.

### 11. Executive Outreach Studio & Webhook Simulator
Bridges strategic prioritization directly to high-converting executive engagement:
* **4 Role-Specific Strategic Angles**: Automatically synthesizes personalized emails tailored for:
  1. *C-Level Strategic Urgency* (ROI, competitive pressure, timeline risk)
  2. *InfoSec & Compliance Clearance* (SOC2 Type II, HIPAA, zero-trust architecture)
  3. *Legal & Redline Acceleration* (Mutual indemnification, SLA turnarounds)
  4. *Procurement & Budget Lock* (End-of-quarter discounting, CapEx allocations)
* **Cryptographic HMAC-SHA256 Webhook Verification**: Simulates production webhook dispatch with signature verification (`sha256=<hex>`), proving payload authenticity for Zapier, Salesforce, and custom CRM endpoints.

---

## 🧪 Automated Test Suite (88 Tests • 100% Pass Rate)

PrioritiQ ships with an industry-grade automated test suite in [`tests/`](./tests):

```bash
python -m pytest tests -v
# Output: 88 passed in ~4.6s (100% pass rate)
```

| Test Module | Tests | Focus Area |
| :--- | :---: | :--- |
| **`test_benchmark_50_queries.py`** | 50 | Synthetic benchmark across 50 distinct managerial queries: capacity hours, deal value vs velocity strategies, counterfactuals, deltas, and approvals. |
| **`test_api_endpoints.py`** | 15 | Comprehensive REST API integration tests covering `/query`, `/{id}`, `/approve`, `/audit/verify`, `/simulate` (Monte Carlo), `/config/rules` (GET/PUT/POST), `/config/rules/preview`, `/config/webhooks`, `/leads`, `/sources`, `/health`, and strict HTTP 404 validation. |
| **`test_robustness_edge_cases.py`** | 8 | Boundary condition checks: 0 hours, negative budgets, 100h budgets, empty queries, special characters/emojis, scoring determinism, and blast-radius empty lists. |
| **`test_verification_agent.py`** | 3 | Primary-key database integrity, rejection of corrupted deal sizes ($>\$9,000,000$), and rejection of non-existent leads. |
| **`test_blast_radius.py`** | 2 | Account attrition risk calculation, neglected pipeline modeling, and sales rep capacity skew detection. |
| **`test_audit_chain.py`** | 1 | SHA-256 cryptographic continuity and `previous_hash` linking. |
| **`test_audit_tamper_detection.py`** | 2 | Adversarial tamper detection verifying that modifying historical payloads or corrupted hashes is immediately flagged. |
| **`test_intent_orchestrator.py`** | 3 | Compound query parsing, entity resolution, and confidence scoring. |
| **`test_knapsack.py`** | 3 | Strict capacity adherence, cardinality limit enforcement, and unconstrained fallback. |
| **`test_rag_eval.py`** | 1 | Semantic retrieval accuracy: Recall@4 >= 0.75, MRR >= 0.70. |

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API Engine metadata, architecture summary, and online status |
| `GET` | `/health` | Live system health diagnostics (DB stats, cryptographic ledger status, RAG docs) |
| `POST` | `/api/decisions/query` | Process natural language query with optional time budget or strategy overrides |
| `GET` | `/api/decisions/{decision_id}` | Retrieves immutable persisted decision dossier (strict HTTP 404 on missing ID) |
| `POST` | `/api/decisions/approve` | Human-in-the-loop governance: generates CRM tasks, emails, and appends to SHA-256 ledger |
| `GET` | `/api/decisions/history` | Returns historical audit chain records |
| `GET` | `/api/decisions/audit/verify` | Cryptographically traverses and verifies the entire SHA-256 hash chain from genesis block |
| `POST` | `/api/decisions/simulate` | Executes 1,000-trial Monte Carlo stochastic risk simulation (P10/P50/P90 distributions) |
| `GET` | `/api/decisions/config/rules` | Returns active scoring rules, stage weights, and churn penalty configuration |
| `PUT` / `POST` | `/api/decisions/config/rules` | Dynamically updates scoring rules at runtime without redeployment |
| `POST` | `/api/decisions/config/rules/preview` | Computes prospective lead score deltas and rank shifts in real time |
| `GET` | `/api/decisions/config/webhooks` | Lists registered outbound webhook integrations |
| `POST` | `/api/decisions/config/webhooks` | Registers external webhook endpoint with HMAC-SHA256 signature verification |
| `GET` | `/api/leads` | Lists all indexed CRM leads with dynamic delta info |
| `GET` | `/api/leads/{lead_id}` | Returns lead details, activity history, and line-level RAG citations |
| `GET` | `/api/sources/summary` | Returns status and row counts of all integrated structured and unstructured sources |
| `GET` | `/api/sources/notes` | Returns knowledge corpus documents |

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

---

## 🎨 UI & Design Philosophy

PrioritiQ features a custom **Nordic Verdigris & Warm Sand** design system engineered for executive clarity:

* **Background**: Warm Sand porcelain (`#F7F7F5`) with crisp sub-panels (`#FBFBF9`).
* **Primary Accent**: Deep Nordic Verdigris (`#0F766E` / `#005F56`) delivering high contrast without corporate blue fatigue.
* **Typography**: Clean, modern Plus Jakarta Sans with monospace telemetry counters (`JetBrains Mono`, `ui-monospace`).
* **Live System Diagnostics**: Real-time status pill in the navigation bar showing database connection, cryptographic ledger verification, and RAG document status.
* **1-Click Executive Export**: Instantly export decision dossiers as JSON or copy executive markdown briefs to clipboard.

---

## ⚡ Setup & Installation Instructions

### 📦 Clone Repository
```bash
git clone https://github.com/PanatiNitesh/PrioritiQ.git
cd PrioritiQ
```

---

### Option A: One-Click Startup (Fastest)

#### On Windows:
```cmd
# Run entire stack (seeds database, starts backend & frontend):
start_server.bat

# Run automated 88-test suite:
run_tests.bat
```

#### On Linux / macOS:
```bash
chmod +x start_server.sh run_tests.sh

# Run entire stack:
./start_server.sh

# Run automated 88-test suite:
./run_tests.sh
```

---

### Option B: Docker & Docker Compose

Run the entire application in isolated containers with zero manual configuration:
```bash
docker compose up --build
```
* **Frontend Web Console**: `http://localhost:5173`
* **Backend API & Swagger Docs**: `http://localhost:8000/docs`
* **Health Diagnostics**: `http://localhost:8000/health`

---

### Option C: Manual Step-by-Step Setup

#### Prerequisites
* **Python**: 3.10+ (tested on Python 3.11, 3.12, 3.13)
* **Node.js**: v18+ with `npm`

#### 1. Setup Backend Environment
```bash
python -m venv venv

# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

#### 2. Initialize Database & Seed Ground-Truth Data
```bash
python -m backend.database.seed
```

#### 3. Run Automated Tests (88 Tests)
```bash
python -m pytest tests -v
```

#### 4. Launch Backend API Server
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive Swagger documentation is available at `http://127.0.0.1:8000/docs`.

#### 5. Launch Frontend Console
In a separate terminal window:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` to access the PrioritiQ console.

---

### Option D: Cloud Deployment on Render (100% Unified Service)

PrioritiQ is configured for seamless full-stack deployment on **[Render](https://render.com)** as a single unified web service serving both the FastAPI decision engine and the compiled React 18 SPA console.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

#### Method 1: Automatic Blueprint Deployment (Recommended)
1. Push code to GitHub:
   ```bash
   git push origin main
   ```
2. In [Render Dashboard](https://dashboard.render.com), click **New +** $\to$ **Blueprint**.
3. Select your `PrioritiQ` repository.
4. Render automatically reads [`render.yaml`](./render.yaml) and executes [`build.sh`](./build.sh). Click **Apply**.

#### Method 2: Manual Web Service Setup
1. In Render Dashboard, click **New +** $\to$ **Web Service**.
2. Connect your GitHub repository.
3. Configure settings:
   * **Build Command**: `bash build.sh`
   * **Start Command**: `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   * **Plan**: `Free`
   * **Environment Variables**:
     * `PYTHON_VERSION` = `3.11.9`
     * `NODE_VERSION` = `20.12.0`
     * `VITE_API_BASE` = `/api`
4. Click **Create Web Service**.

#### Verification Checklist After Deployment:
* **Interactive Web Console**: [`https://prioritiq-ai.onrender.com/`](https://prioritiq-ai.onrender.com/)
* **Swagger API Documentation**: [`https://prioritiq-ai.onrender.com/docs`](https://prioritiq-ai.onrender.com/docs)
* **System Health Diagnostics**: [`https://prioritiq-ai.onrender.com/health`](https://prioritiq-ai.onrender.com/health)
* **Audit Ledger Verification**: [`https://prioritiq-ai.onrender.com/api/decisions/audit/verify`](https://prioritiq-ai.onrender.com/api/decisions/audit/verify)

---

## 🤖 Disclosure of AI Tools Used

In adherence to hackathon integrity and transparency standards, the following AI tools and technologies were utilized during the design, architecture, and engineering of **PrioritiQ**:

* **AI Agentic Coding & IDE Frameworks:**
  * **Antigravity Agentic IDE:** Leveraged for multi-agent architecture scaffolding, iterative debugging, test generation (88/88 test cases), and full-stack integration between FastAPI and React 18.
* **Large Language Models & Semantic Retrieval:**
  * **Google Gemini & Anthropic Claude (via Agentic IDEs):** Used for architectural planning, contextual executive outreach prompt templates, and schema optimization.
  * **HuggingFace `sentence-transformers` (MiniLM-L6-v2) & Lexical BM25:** Implemented directly within the application engine for local semantic search and line-level hybrid citation retrieval.
* **Deterministic Guardrails & Human Authorship:**
  * All core mathematical algorithms (**2D Bounded Knapsack Dynamic Programming solver**, **Monte Carlo 1,000-trial stochastic risk engine**, **Primary-Key verification logic**, and **SHA-256 cryptographic hash-chain ledger**) are 100% deterministically engineered and verified with automated unit and regression suites to prevent LLM hallucinations.

---

## 📄 License & Intellectual Property

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details. Built for enterprise commercial decision intelligence by [PanatiNitesh](https://github.com/PanatiNitesh).