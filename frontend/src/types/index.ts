export interface EvidenceNode {
  id: string;
  type: 'decision' | 'lead' | 'metric' | 'rag_evidence' | 'constraint' | 'action';
  label: string;
  data: Record<string, any>;
  grounded_source?: string;
  confidence: number;
}

export interface EvidenceEdge {
  id: string;
  source: string;
  target: string;
  relation: string;
}

export interface DecisionGraphData {
  nodes: EvidenceNode[];
  edges: EvidenceEdge[];
}

export interface GroundedCitation {
  source_file: string;
  source_type: string;
  author_or_actor: string;
  timestamp: string;
  quote: string;
  fact_checked: boolean;
}

export interface SuggestedAction {
  type: string;
  title: string;
  assigned_rep: string;
  due_date: string;
  email_draft: {
    to: string;
    subject: string;
    body: string;
  };
}

export interface VerificationCheck {
  check: string;
  passed: boolean;
  evidence: string;
}

export interface VerificationStatus {
  is_verified: boolean;
  grounding_score_pct: number;
  checks_evaluated: number;
  checks_passed: number;
  hallucination_risk: string;
  checks: VerificationCheck[];
}

export interface LeadRecommendation {
  rank: number;
  lead_id: string;
  lead_name: string;
  company_name: string;
  title: string;
  stage: string;
  deal_size: number;
  composite_score: number;
  est_effort_mins: number;
  assigned_rep: string;
  icp_fit: number;
  why_this_lead: string[];
  why_not_reasons?: string[];
  what_changed: string;
  grounded_evidence: GroundedCitation[];
  suggested_action: SuggestedAction;
  verification_status: VerificationStatus;
}

export interface CounterfactualComparison {
  focus_lead: {
    lead_id: string;
    name: string;
    company: string;
    score: number;
    stage: string;
    deal_size: number;
  };
  alternative_lead: {
    lead_id: string;
    name: string;
    company: string;
    score: number;
    stage: string;
    deal_size: number;
    churn_risk?: string;
  };
  tradeoff_summary: string;
  key_differentiators: Array<{
    factor: string;
    focus: string;
    alternative: string;
  }>;
}

export interface SimulationState {
  constrained: boolean;
  time_budget_mins?: number;
  allocated_mins: number;
  slack_mins?: number;
  total_deal_value: number;
  priority_weight: string;
  leads_evaluated: number;
  leads_selected: number;
  excluded_count?: number;
  constraint_explanation: string;
}

export interface BlastRadiusReport {
  collateral_damage_score: number;
  risk_level: string;
  excluded_accounts_count: number;
  excluded_pipeline_value: number;
  at_risk_excluded_value: number;
  estimated_daily_attrition_cost: number;
  late_stage_slippage_value: number;
  late_stage_deferred_count: number;
  rep_skew_std_dev_mins: number;
  rep_utilizations: Array<{
    rep_name: string;
    deals_count: number;
    total_effort_mins: number;
    deal_value_allocated: number;
    bottleneck_risk: boolean;
    utilization_pct: number;
  }>;
  warnings: string[];
}

export interface MonteCarloSimulation {
  simulation_trials: number;
  market_volatility: number;
  expected_revenue_optimized: number;
  expected_revenue_baseline: number;
  projected_revenue_lift: number;
  lift_percentage: number;
  probability_outperforming_baseline_pct: number;
  prioritiq_schedule: {
    p10_conservative: number;
    p50_median: number;
    p90_optimistic: number;
    avg_deals_won: number;
  };
  legacy_crm_baseline: {
    p10_conservative: number;
    p50_median: number;
    p90_optimistic: number;
    avg_deals_won: number;
  };
  distribution_buckets: Array<{
    range_min: number;
    range_max: number;
    label: string;
    prioritiq_density: number;
    baseline_density: number;
  }>;
  executive_summary: string;
}

export interface DecisionResponse {
  decision_id: string;
  query: string;
  timestamp: string;
  intent_summary: {
    intent_type: string;
    time_budget_hours?: number;
    priority_weight: string;
    target_lead_ref?: string;
    query_plan: Record<string, boolean>;
  };
  recommendations: LeadRecommendation[];
  counterfactual_analysis?: CounterfactualComparison;
  delta_summary: Record<string, any>;
  simulation_state: SimulationState;
  evidence_graph: DecisionGraphData;
  verification_report: {
    pipeline_grounded: boolean;
    all_recommendations_verified: boolean;
    crm_source?: string;
    db_source?: string;
    rag_source: string;
    grounding_confidence: number;
    average_grounding_score_pct?: number;
    verification_agent_summary: string;
  };
  blast_radius?: BlastRadiusReport;
  monte_carlo_simulation?: MonteCarloSimulation;
  approval_status: string;
  approval_details?: Record<string, any>;
}

export interface AuditLogEntry {
  event_id: string;
  decision_id: string;
  query: string;
  timestamp: string;
  action: string;
  user_role: string;
  audit_hash: string;
  details: Record<string, any>;
}
