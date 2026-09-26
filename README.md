# DecisionGraph: Evidence-Grounded AI Sales Decision Engine

> **Core Principle**: Do not build an LLM that pretends to be a business analyst.  
> Build: **Deterministic analytics + RAG + AI orchestration + evidence + human approval.**

DecisionGraph is an evidence-grounded decision engine purpose-built for Sales Managers answering high-stakes commercial questions:
- *“Which leads should my sales team prioritize today, and why?”*
- *“What if my team only has 3 hours?”* (Solves bounded knapsack capacity allocation)
- *“What if I prioritize deal value?”* (Strategic multi-factor weighting)
- *“Why not another lead (e.g., Vanguard Logistics)?”* (Counterfactual tradeoff analysis)
- *“What changed since yesterday?”* (Day-over-day grounded delta tracking)
- *“Approve this recommendation”* (Human governance with SHA-256 cryptographic audit logs)

---

## 🏛️ System Architecture

```
                  ┌──────────────────────┐
                  │   BUSINESS DATA      │
                  │                      │
                  │ CRM / CSV / Excel    │
                  │ Sales / Customers    │
                  │ Activities / Deals   │
                  └──────────┬───────────┘
                             ↓
                  ┌──────────────────────┐
                  │  DATA INGESTION      │
                  │                      │
                  │ Parse / Validate     │
                  │ Clean / Normalize    │
                  │ Deduplicate          │
                  └──────────┬───────────┘
                             ↓
                  ┌──────────────────────┐
                  │ BUSINESS DATA MODEL  │
                  │                      │
                  │ Leads                │
                  │ Companies            │
                  │ Activities           │
                  │ Deals                │
                  │ Customers            │
                  └──────────┬───────────┘
                             ↓
              ┌──────────────┴──────────────┐
              ↓                             ↓
      ┌───────────────┐             ┌───────────────┐
      │ STRUCTURED    │             │ UNSTRUCTURED  │
      │ ANALYTICS     │             │ KNOWLEDGE     │
      │               │             │               │
      │ SQL           │             │ RAG           │
      │ Aggregations  │             │ Notes         │
      │ Statistics    │             │ Emails        │
      │ Scoring       │             │ Documents     │
      └───────┬───────┘             └───────┬───────┘
              │                             │
              └──────────────┬──────────────┘
                             ↓
                  ┌──────────────────────┐
                  │   AI ORCHESTRATOR    │
                  │                      │
                  │ Intent → Plan        │
                  │ Retrieve → Analyze   │
                  │ Verify → Recommend   │
                  └──────────┬───────────┘
                             ↓
                  ┌──────────────────────┐
                  │   DECISION ENGINE    │
                  │                      │
                  │ Lead scoring         │
                  │ Ranking              │
                  │ Constraints          │
                  │ Business rules       │
                  └──────────┬───────────┘
                             ↓
                  ┌──────────────────────┐
                  │   EVIDENCE GRAPH     │
                  │                      │
                  │ Recommendation       │
                  │      ↓               │
                  │ Evidence             │
                  │      ↓               │
                  │ Source records       │
                  └──────────┬───────────┘
                             ↓
                  ┌──────────────────────┐
                  │ HUMAN APPROVAL       │
                  │                      │
                  │ APPROVE / EDIT /     │
                  │ REJECT               │
                  └──────────┬───────────┘
                             ↓
                  ┌──────────────────────┐
                  │ ACTION               │
                  │                      │
                  │ Create task          │
                  │ Update CRM           │
                  │ Generate email       │
                  └──────────┬───────────┘
                             ↓
                  ┌──────────────────────┐
                  │ AUDIT / DECISION LOG │
                  └──────────────────────┘
```

---

## 🤖 Multi-Agent Orchestration Pipeline

```
                    USER
                      ↓
               Intent Agent
                      ↓
                Query Planner
                 ↙        ↘
          Analytics       RAG
             Agent        Agent
                 ↘        ↙
                Evidence
                    ↓
             Decision Engine
                    ↓
              Verification
                    ↓
             Recommendation
                    ↓
             Human Approval
                    ↓
                 Action
```

1. **Intent Agent (`backend/agents/intent_agent.py`)**: Classifies query types, parses time bounds (e.g., 3 hours), strategic weights (`deal_value`, `velocity`), and counterfactual entity targets.
2. **Query Planner**: Decomposes intent into structured SQL/Pandas analytics tasks and unstructured RAG search requirements.
3. **Analytics Agent (`backend/agents/analytics_agent.py`)**: Executes deterministic composite scoring, recency decay functions, stage probability weighting, and bounded knapsack capacity solving.
4. **Retrieval Agent (`backend/agents/retrieval_agent.py`)**: Searches unstructured call transcripts, customer emails, and rep notes using hybrid vector search (TF-IDF + keyword entity boosting) and extracts verbatim quotes with line-level provenance.
5. **Decision Engine (`backend/decision/engine.py`)**: Synthesizes structured data and qualitative context into ranked recommendations with grounded *"Why this lead?"* reasoning.
6. **Verification Agent (`backend/agents/verification_agent.py`)**: Evaluates claims against source CSV files and markdown notes to guarantee 0% hallucination rate before surfacing recommendations.
7. **Human Approval & Governance (`backend/decision/audit.py`)**: Requires sales manager sign-off (`APPROVE`, `EDIT`, or `REJECT`) before automatically generating outbound email drafts and logging SHA-256 audit entries.

---

## 📂 Project Structure

```
decisiongraph/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DecisionGraph/        # Interactive Evidence Graph DAG visualizer
│   │   │   ├── EvidencePanel/        # Grounded citations & verification checklist
│   │   │   ├── RecommendationCard/   # Ranked lead card with delta indicators & email previews
│   │   │   ├── ApprovalPanel/        # Manager governance, reject/approve & audit hashes
│   │   │   └── DataSources/          # Ingestion inspector & raw notes viewer
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx         # AI Decision Workspace home
│   │   │   ├── Decisions.tsx         # Audit ledger table & export
│   │   │   ├── Leads.tsx             # CRM pipeline intelligence & filter table
│   │   │   └── DecisionDetail.tsx    # Dossier view for any decision ID
│   │   ├── services/                 # API client for FastAPI endpoints
│   │   └── index.css                 # Dark mode glassmorphism design system
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── agents/
│   │   ├── intent_agent.py           # Intent parsing & query decomposition
│   │   ├── analytics_agent.py        # Deterministic aggregations & queries
│   │   ├── retrieval_agent.py        # RAG over notes, transcripts, emails
│   │   ├── decision_agent.py         # Multi-agent coordination
│   │   └── verification_agent.py     # Ground-truth fact checker
│   ├── analytics/
│   │   ├── lead_scoring.py           # Multi-factor deterministic scoring
│   │   ├── ranking.py                # Knapsack capacity optimization (e.g., 3 hours)
│   │   └── metrics.py                # Pipeline metrics & day-over-day deltas
│   ├── rag/
│   │   ├── ingestion.py              # Frontmatter parser & document loader
│   │   ├── embeddings.py             # Hybrid vector & TF-IDF index
│   │   └── retrieval.py              # Quotation extractor & citation builder
│   ├── decision/
│   │   ├── engine.py                 # Core Decision Engine
│   │   ├── evidence.py               # DAG Graph builder (Nodes & Edges)
│   │   └── audit.py                  # Cryptographic SHA-256 audit log
│   ├── models/                       # Pydantic request/response schemas
│   ├── routes/                       # FastAPI router endpoints
│   ├── main.py                       # FastAPI application entrypoint
│   └── generate_data.py              # Enterprise CRM & notes generator
│
├── data/
│   ├── leads.csv                     # CRM leads with deal sizes, stages, reps
│   ├── companies.csv                 # Firmographics, revenue, tech stack, ICP fit
│   ├── activities.csv                # Engagement history & call logs
│   ├── decision_audit_log.json       # Immutable decision log
│   └── notes/                        # 12+ real-world sales transcripts & emails
│
└── README.md
```

---

## 🚀 Running DecisionGraph

### 1. Start the Backend API (FastAPI)
```bash
python -m uvicorn decisiongraph.backend.main:app --host 127.0.0.1 --port 8000 --reload
```
API docs available at: `http://127.0.0.1:8000/docs`

### 2. Start the Frontend Workspace (Vite + React)
```bash
cd decisiongraph/frontend
npm run dev
```
Open `http://localhost:5173` in your browser.
