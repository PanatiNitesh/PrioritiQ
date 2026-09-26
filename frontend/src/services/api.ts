import { DecisionResponse, AuditLogEntry } from '../types';

const API_BASE = 'http://127.0.0.1:8000/api';

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
  if (!res.ok) {
    throw new Error(`API error: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchDecisionById(decisionId: string): Promise<DecisionResponse> {
  const res = await fetch(`${API_BASE}/decisions/${encodeURIComponent(decisionId)}`);
  if (!res.ok) {
    throw new Error(`Decision ${decisionId} fetch error: ${res.statusText}`);
  }
  return res.json();
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
  if (!res.ok) {
    throw new Error(`Approval error: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchDecisionHistory(): Promise<AuditLogEntry[]> {
  const res = await fetch(`${API_BASE}/decisions/history`);
  if (!res.ok) {
    throw new Error(`History error: ${res.statusText}`);
  }
  return res.json();
}

export async function verifyAuditChain() {
  const res = await fetch(`${API_BASE}/decisions/audit/verify`);
  if (!res.ok) {
    throw new Error(`Audit verification error: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchScoringRules() {
  const res = await fetch(`${API_BASE}/decisions/config/rules`);
  if (!res.ok) {
    throw new Error(`Rules error: ${res.statusText}`);
  }
  return res.json();
}

export async function updateScoringRules(rules: any) {
  const res = await fetch(`${API_BASE}/decisions/config/rules`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(rules)
  });
  if (!res.ok) {
    throw new Error(`Update rules error: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchLeads(stage?: string) {
  const url = stage ? `${API_BASE}/leads?stage=${encodeURIComponent(stage)}` : `${API_BASE}/leads`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Leads error: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchLeadDetail(leadId: string) {
  const res = await fetch(`${API_BASE}/leads/${leadId}`);
  if (!res.ok) {
    throw new Error(`Lead detail error: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchDataSourcesSummary() {
  const res = await fetch(`${API_BASE}/sources/summary`);
  if (!res.ok) {
    throw new Error(`Sources error: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchAllNotes() {
  const res = await fetch(`${API_BASE}/sources/notes`);
  if (!res.ok) {
    throw new Error(`Notes error: ${res.statusText}`);
  }
  return res.json();
}
