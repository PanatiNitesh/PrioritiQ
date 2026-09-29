import { DecisionResponse, AuditLogEntry } from '../types';

const isLocalDevVite = typeof window !== 'undefined' && window.location.hostname === 'localhost' && window.location.port === '5173';
const DEFAULT_API_BASE = isLocalDevVite ? 'http://127.0.0.1:8000/api' : '/api';
const API_BASE = (import.meta as any).env?.VITE_API_BASE || DEFAULT_API_BASE;

async function handleResponse(res: Response, defaultMessage: string) {
  if (!res.ok) {
    let msg = `${defaultMessage} (${res.status} ${res.statusText})`;
    try {
      const err = await res.json();
      if (err?.detail) msg = typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail);
    } catch (_) {}
    throw new Error(msg);
  }
  return res.json();
}

export async function fetchHealthCheck() {
  const rootBase = API_BASE.endsWith('/api') ? API_BASE.slice(0, -4) : API_BASE;
  const url = rootBase ? `${rootBase}/health` : '/health';
  const res = await fetch(url);
  return handleResponse(res, 'Health check failed');
}

export async function queryDecisionEngine(
  query: string,
  timeBudgetHours?: number,
  priorityWeight?: string,
  targetLeadId?: string
): Promise<DecisionResponse> {
  const res = await fetch(`${API_BASE}/decisions/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      time_budget_hours: timeBudgetHours,
      priority_weight: priorityWeight,
      target_lead_id: targetLeadId
    })
  });
  return handleResponse(res, 'Failed to process decision query');
}

export async function fetchDecisionById(decisionId: string): Promise<DecisionResponse> {
  const res = await fetch(`${API_BASE}/decisions/${encodeURIComponent(decisionId)}`);
  return handleResponse(res, `Failed to fetch decision ${decisionId}`);
}

export async function approveDecision(
  decisionId: string,
  action: 'APPROVE' | 'EDIT' | 'REJECT',
  approvedLeadIds?: string[],
  managerNotes?: string
) {
  const res = await fetch(`${API_BASE}/decisions/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      decision_id: decisionId,
      action,
      approved_lead_ids: approvedLeadIds,
      manager_notes: managerNotes,
      dispatch_crm_tasks: true,
      generate_emails: true
    })
  });
  return handleResponse(res, 'Failed to submit approval');
}

export async function fetchDecisionHistory(): Promise<AuditLogEntry[]> {
  const res = await fetch(`${API_BASE}/decisions/history`);
  return handleResponse(res, 'Failed to fetch decision history');
}

export async function verifyAuditChain() {
  const res = await fetch(`${API_BASE}/decisions/audit/verify`);
  return handleResponse(res, 'Failed to verify audit ledger');
}

export async function fetchScoringRules() {
  const res = await fetch(`${API_BASE}/decisions/config/rules`);
  return handleResponse(res, 'Failed to fetch scoring rules');
}

export async function updateScoringRules(rules: any) {
  const res = await fetch(`${API_BASE}/decisions/config/rules`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(rules)
  });
  return handleResponse(res, 'Failed to update scoring rules');
}

export async function fetchLeads(stage?: string) {
  const url = stage ? `${API_BASE}/leads?stage=${encodeURIComponent(stage)}` : `${API_BASE}/leads`;
  const res = await fetch(url);
  return handleResponse(res, 'Failed to fetch leads');
}

export async function fetchLeadDetail(leadId: string) {
  const res = await fetch(`${API_BASE}/leads/${leadId}`);
  return handleResponse(res, `Failed to fetch lead ${leadId}`);
}

export async function fetchDataSourcesSummary() {
  const res = await fetch(`${API_BASE}/sources/summary`);
  return handleResponse(res, 'Failed to fetch data sources summary');
}

export async function fetchAllNotes() {
  const res = await fetch(`${API_BASE}/sources/notes`);
  return handleResponse(res, 'Failed to fetch notes');
}

export async function runMonteCarloSimulation(params: {
  trials?: number;
  market_volatility?: number;
  priority_weight?: string;
  execution_efficiency?: number;
}) {
  const res = await fetch(`${API_BASE}/decisions/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  return handleResponse(res, 'Failed to run Monte Carlo simulation');
}

export async function previewScoringRulesImpact(prospectiveRules: any) {
  const res = await fetch(`${API_BASE}/decisions/config/rules/preview`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(prospectiveRules)
  });
  return handleResponse(res, 'Failed to preview scoring policy impact');
}
