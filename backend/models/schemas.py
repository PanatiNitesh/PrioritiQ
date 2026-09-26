from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class DecisionQueryRequest(BaseModel):
    query: str
    time_budget_hours: Optional[float] = None
    priority_weight: Optional[str] = "balanced"  # balanced, deal_value, velocity, win_rate
    target_lead_id: Optional[str] = None  # for "Why not Lead X?" follow-ups
    compare_lead_ids: Optional[List[str]] = None
    limit: Optional[int] = 10

class EvidenceNode(BaseModel):
    id: str
    type: str  # decision, lead, metric, rag_evidence, constraint, action
    label: str
    data: Dict[str, Any] = Field(default_factory=dict)
    grounded_source: Optional[str] = None
    confidence: float = 1.0

class EvidenceEdge(BaseModel):
    id: str
    source: str
    target: str
    relation: str

class DecisionGraphData(BaseModel):
    nodes: List[EvidenceNode]
    edges: List[EvidenceEdge]

class GroundedCitation(BaseModel):
    source_file: str
    source_type: str  # csv_record, sales_note, inbound_email, transcript
    author_or_actor: str
    timestamp: str
    quote: str
    fact_checked: bool = True

class LeadRecommendation(BaseModel):
    rank: int
    lead_id: str
    lead_name: str
    company_name: str
    title: str
    stage: str
    deal_size: float
    composite_score: float
    est_effort_mins: int
    assigned_rep: str
    icp_fit: int
    why_this_lead: List[str]
    why_not_reasons: Optional[List[str]] = None
    what_changed: str
    grounded_evidence: List[GroundedCitation]
    suggested_action: Dict[str, Any]
    verification_status: Dict[str, Any]

class CounterfactualComparison(BaseModel):
    focus_lead: Dict[str, Any]
    alternative_lead: Dict[str, Any]
    tradeoff_summary: str
    key_differentiators: List[Dict[str, str]]

class DecisionResponse(BaseModel):
    decision_id: str
    query: str
    timestamp: str
    intent_summary: Dict[str, Any]
    recommendations: List[LeadRecommendation]
    counterfactual_analysis: Optional[CounterfactualComparison] = None
    delta_summary: Dict[str, Any]
    simulation_state: Dict[str, Any]
    evidence_graph: DecisionGraphData
    verification_report: Dict[str, Any]
    blast_radius: Optional[Dict[str, Any]] = None
    approval_status: str = "PENDING"
    approval_details: Optional[Dict[str, Any]] = None

class ApprovalActionRequest(BaseModel):
    decision_id: str
    action: str  # APPROVE, EDIT, REJECT
    approved_lead_ids: Optional[List[str]] = None
    manager_notes: Optional[str] = None
    dispatch_crm_tasks: bool = True
    generate_emails: bool = True

class ApprovalActionResponse(BaseModel):
    decision_id: str
    status: str
    audit_hash: str
    timestamp: str
    created_tasks: List[Dict[str, Any]]
    dispatched_emails: List[Dict[str, Any]]
    audit_entry: Dict[str, Any]
