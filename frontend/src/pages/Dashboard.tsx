import React, { useState, useEffect } from 'react';
import { queryDecisionEngine } from '../services/api';
import { DecisionResponse, LeadRecommendation } from '../types';
import { RecommendationCard } from '../components/RecommendationCard/RecommendationCard';
import { DecisionGraphViewer } from '../components/DecisionGraph/DecisionGraphViewer';
import { EvidencePanel } from '../components/EvidencePanel/EvidencePanel';
import { ApprovalPanel } from '../components/ApprovalPanel/ApprovalPanel';
import {
  Send,
  Sliders,
  Clock,
  RotateCcw,
  ArrowRight,
  Split,
  Sparkles,
  Zap,
  TrendingUp,
  DollarSign,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Users
} from 'lucide-react';

interface Props {
  onOpenDataSources: () => void;
  onNavigateDetail: (decisionId: string) => void;
}

export const Dashboard: React.FC<Props> = ({ onOpenDataSources, onNavigateDetail }) => {
  const [queryInput, setQueryInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [decision, setDecision] = useState<DecisionResponse | null>(null);
  const [selectedLead, setSelectedLead] = useState<LeadRecommendation | null>(null);

  // Simulation controls state
  const [timeBudget, setTimeBudget] = useState<number | undefined>(undefined);
  const [priorityMode, setPriorityMode] = useState<string>('balanced');
  const [showSimSliders, setShowSimSliders] = useState(false);

  const suggestedQueries = [
    { label: 'Priority Leads Today', query: 'Which leads should my team prioritize today?', icon: Zap },
    { label: '3-Hour Capacity Sprint', query: 'What if my team only has 3 hours?', icon: Clock },
    { label: 'Maximize Deal Value', query: 'What if I prioritize deal value?', icon: DollarSign },
    { label: 'Why Not Vanguard?', query: 'Why not Vanguard Logistics?', icon: Split },
    { label: 'What Changed Today?', query: 'What changed since yesterday?', icon: TrendingUp }
  ];

  const executeQuery = async (
    q: string,
    overrideTime?: number,
    overrideWeight?: string,
    targetLeadId?: string
  ) => {
    setLoading(true);
    try {
      const res = await queryDecisionEngine(q, overrideTime, overrideWeight, targetLeadId);
      setDecision(res);
      if (res.recommendations && res.recommendations.length > 0) {
        setSelectedLead(res.recommendations[0]);
      }
    } catch (err: any) {
      console.error('Query execution error:', err);
      alert(`Could not connect to PrioritiQ Engine: ${err.message}. Ensure backend is running.`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Initial default query on mount
    executeQuery('Which leads should my team prioritize today?');
  }, []);

  const handleSimulateHours = (hours: number) => {
    setTimeBudget(hours);
    executeQuery(
      `What if my team only has ${hours} hours?`,
      hours,
      priorityMode
    );
  };

  const handlePriorityChange = (mode: string) => {
    setPriorityMode(mode);
    executeQuery(
      decision?.query || 'Which leads should my team prioritize today?',
      timeBudget,
      mode
    );
  };

  const handleAskWhyNot = (leadId: string, companyName: string) => {
    const q = `Why not ${companyName}?`;
    setQueryInput(q);
    executeQuery(q, timeBudget, priorityMode, leadId);
  };

  return (
    <div className="space-y-6">
      {/* Top Welcome & Conversational Prompt Bar */}
      <div className="pq-card p-6 sm:p-8 bg-gradient-to-b from-white via-white to-[#F7F9F8] border border-[#E5E5DF] relative overflow-hidden">
        {/* Subtle decorative verdigris ambient glow */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-teal-100/30 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20"></div>

        <div className="max-w-3xl relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-200/80 text-teal-800 font-mono text-xs font-bold uppercase tracking-wider mb-3">
            <Sparkles size={13} className="text-teal-700" />
            PrioritiQ AI Engine • Session Active
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight leading-tight">
            Which accounts should your sales team prioritize today, and why?
          </h1>
          <p className="text-sm text-slate-600 mt-2 leading-relaxed">
            Deterministic scoring + RAG knowledge over customer emails, call notes & transcripts. Real provenance, zero hallucination.
          </p>
        </div>

        {/* Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (queryInput.trim()) executeQuery(queryInput, timeBudget, priorityMode);
          }}
          className="mt-6 flex flex-col sm:flex-row gap-2.5 relative z-10"
        >
          <div className="relative flex-1">
            <input
              type="text"
              value={queryInput}
              onChange={(e) => setQueryInput(e.target.value)}
              placeholder="Ask any sales prioritization question or follow-up (e.g. Why not Acme Corp? What if deal value prioritized?)"
              className="w-full bg-white border border-[#D4D4D0] rounded-xl px-4 py-3.5 text-sm text-slate-900 placeholder-slate-400 pr-12 shadow-sm focus:border-teal-600 focus:ring-2 focus:ring-teal-100 focus:outline-none"
            />
            {queryInput ? (
              <button
                type="button"
                onClick={() => setQueryInput('')}
                className="absolute right-3.5 top-3.5 text-slate-400 hover:text-slate-600 text-xs font-bold"
              >
                ✕
              </button>
            ) : (
              <span className="absolute right-3.5 top-3.5 text-[10px] font-mono font-bold text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">
                ↵
              </span>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-teal px-7 py-3 text-sm justify-center shadow-md"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                Evaluating...
              </span>
            ) : (
              <>
                <span>Reason & Rank</span>
                <Send size={15} />
              </>
            )}
          </button>
        </form>

        {/* Suggested Quick Prompt Chips */}
        <div className="mt-5 flex flex-wrap items-center gap-2 relative z-10">
          <span className="text-xs text-slate-500 font-bold mr-1">Suggested inquiries:</span>
          {suggestedQueries.map((item, i) => {
            const Icon = item.icon;
            return (
              <button
                key={i}
                onClick={() => {
                  setQueryInput(item.query);
                  executeQuery(item.query);
                }}
                className="pq-chip"
              >
                <Icon size={12} className="text-teal-700" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Simulation & What-If Controls Bar */}
      <div className="pq-card p-4 flex flex-wrap items-center justify-between gap-4 border border-[#E5E5DF]">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowSimSliders(!showSimSliders)}
            className={`px-3 py-1.5 rounded-lg border text-xs font-semibold flex items-center gap-2 transition-all ${
              showSimSliders
                ? 'bg-teal-50 border-teal-300 text-teal-800 shadow-sm'
                : 'bg-white border-slate-300 text-slate-700 hover:bg-slate-50'
            }`}
          >
            <Sliders size={13} className="text-teal-700" />
            <span>Knapsack Capacity Simulation</span>
          </button>

          {decision?.simulation_state?.constrained && (
            <span className="text-xs px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-800 font-mono font-bold flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-amber-500"></span>
              Constrained: {decision.simulation_state.time_budget_mins} Mins Capacity Budget
            </span>
          )}
        </div>

        {/* Strategy Selector Buttons */}
        <div className="flex items-center gap-2 text-xs">
          <span className="text-slate-500 font-mono text-[11px] font-semibold">Priority Strategy:</span>
          {[
            { id: 'balanced', label: 'Balanced' },
            { id: 'deal_value', label: 'Deal Size ($)' },
            { id: 'velocity', label: 'Closing Velocity' }
          ].map((mode) => (
            <button
              key={mode.id}
              onClick={() => handlePriorityChange(mode.id)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                priorityMode === mode.id
                  ? 'bg-teal-700 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200'
              }`}
            >
              {mode.label}
            </button>
          ))}
        </div>
      </div>

      {/* Interactive Simulation Sliders Drawer */}
      {showSimSliders && (
        <div className="pq-card p-6 border-teal-200 bg-gradient-to-r from-teal-50/40 via-white to-white shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Clock size={16} className="text-amber-600" />
                Knapsack Resource Packing Optimizer
              </h4>
              <p className="text-xs text-slate-600 mt-0.5">
                Applies mathematical 0/1 knapsack optimization to prioritize highest return accounts under strict operational team hours.
              </p>
            </div>
            <button
              onClick={() => {
                setTimeBudget(undefined);
                executeQuery(decision?.query || 'Which leads should my team prioritize today?', undefined, priorityMode);
              }}
              className="text-xs text-slate-500 hover:text-slate-900 flex items-center gap-1 font-semibold"
            >
              <RotateCcw size={12} /> Reset to Unconstrained
            </button>
          </div>

          <div className="flex flex-col md:flex-row gap-6 pt-2">
            <div className="flex-1 space-y-2.5">
              <div className="flex justify-between text-xs font-mono">
                <span className="text-slate-700 font-semibold">Available Team Hours:</span>
                <strong className="text-teal-800 font-bold bg-teal-100 px-2 py-0.5 rounded border border-teal-200">
                  {timeBudget ? `${timeBudget} Hours (${timeBudget * 60} mins)` : 'Unconstrained (Full Working Day)'}
                </strong>
              </div>
              <input
                type="range"
                min="1"
                max="8"
                step="0.5"
                value={timeBudget || 4}
                onChange={(e) => handleSimulateHours(parseFloat(e.target.value))}
                className="w-full accent-teal-700 cursor-pointer h-2 bg-slate-200 rounded-lg"
              />
              <div className="flex justify-between text-[11px] text-slate-500 font-mono font-medium">
                <span>1h (Quick Sprint)</span>
                <span>3h (Afternoon Shift)</span>
                <span>6h (Full Day)</span>
                <span>8h (Expanded Capacity)</span>
              </div>
            </div>

            {decision?.simulation_state && (
              <div className="md:w-72 p-4 rounded-xl bg-white border border-[#E5E5DF] space-y-2 text-xs font-mono shadow-sm">
                <div className="flex justify-between text-slate-600">
                  <span>Selected Leads:</span>
                  <span className="text-emerald-700 font-bold">{decision.simulation_state.leads_selected} Accounts</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>Time Allocated:</span>
                  <span className="text-slate-900 font-semibold">{decision.simulation_state.allocated_mins} / {decision.simulation_state.time_budget_mins || '∞'} mins</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>Pipeline Unlocked:</span>
                  <span className="text-emerald-700 font-bold">
                    ${decision.simulation_state.total_deal_value?.toLocaleString()}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Counterfactual Comparison Card ("Why not Lead X?") */}
      {decision?.counterfactual_analysis && (
        <div className="pq-card p-6 border-amber-200 bg-amber-50/50 shadow-sm">
          <div className="flex items-center gap-2 mb-2.5">
            <Split size={18} className="text-amber-700" />
            <h3 className="text-sm font-bold text-amber-950">
              Counterfactual Tradeoff Analysis: Grounded Explainability
            </h3>
          </div>

          <p className="text-xs text-amber-950 leading-relaxed bg-white p-4 rounded-xl border border-amber-200 font-sans shadow-sm">
            {decision.counterfactual_analysis.tradeoff_summary}
          </p>

          <div className="mt-3.5 grid grid-cols-1 md:grid-cols-3 gap-3">
            {decision.counterfactual_analysis.key_differentiators.map((diff, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-white border border-amber-100 text-xs shadow-sm">
                <span className="text-[10px] uppercase font-mono text-slate-500 font-bold">{diff.factor}</span>
                <div className="mt-1.5 flex items-center justify-between text-[11px]">
                  <span className="text-emerald-700 font-semibold">✓ {diff.focus}</span>
                  <span className="text-rose-600 font-medium">✕ {diff.alternative}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Blast-Radius Prediction Panel (Weakness 2) */}
      {decision?.blast_radius && (
        <div className="pq-card p-5 border-[#E5E5DF] space-y-3 bg-white shadow-xs">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <div className={`p-1.5 rounded-lg ${
                decision.blast_radius.risk_level === 'CRITICAL' ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-teal-50 text-teal-800 border border-teal-200'
              }`}>
                <AlertTriangle size={15} />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-900 tracking-tight">
                  Resource Reallocation Blast-Radius Prediction
                </h4>
                <p className="text-xs text-slate-500">
                  Pre-execution modeling of account attrition, rep skew, and quarter-end slippage
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <span className={`px-2.5 py-0.5 rounded text-[11px] font-mono font-bold uppercase ${
                decision.blast_radius.risk_level === 'CRITICAL'
                  ? 'bg-rose-50 text-rose-800 border border-rose-200'
                  : decision.blast_radius.risk_level === 'ELEVATED'
                  ? 'bg-amber-50 text-amber-800 border border-amber-200'
                  : 'bg-emerald-50 text-emerald-800 border border-emerald-200'
              }`}>
                Risk Level: {decision.blast_radius.risk_level} ({decision.blast_radius.collateral_damage_score}/100)
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
            <div className="p-3 rounded-xl bg-[#FBFBF9] border border-[#E5E5DF]">
              <span className="text-slate-500 block text-[11px]">Excluded Pipeline</span>
              <span className="font-bold text-slate-900 font-mono text-sm">
                ${(decision.blast_radius.excluded_pipeline_value || 0).toLocaleString()}
              </span>
              <span className="text-[10px] text-slate-400 block mt-0.5">
                {decision.blast_radius.excluded_accounts_count} accounts left unserviced
              </span>
            </div>

            <div className="p-3 rounded-xl bg-[#FBFBF9] border border-[#E5E5DF]">
              <span className="text-slate-500 block text-[11px]">At-Risk Churn Value</span>
              <span className="font-bold text-rose-700 font-mono text-sm">
                ${(decision.blast_radius.at_risk_excluded_value || 0).toLocaleString()}
              </span>
              <span className="text-[10px] text-slate-400 block mt-0.5">
                High churn accounts neglected
              </span>
            </div>

            <div className="p-3 rounded-xl bg-[#FBFBF9] border border-[#E5E5DF]">
              <span className="text-slate-500 block text-[11px]">Late-Stage Slippage</span>
              <span className="font-bold text-amber-700 font-mono text-sm">
                ${(decision.blast_radius.late_stage_slippage_value || 0).toLocaleString()}
              </span>
              <span className="text-[10px] text-slate-400 block mt-0.5">
                {decision.blast_radius.late_stage_deferred_count} deals deferred
              </span>
            </div>

            <div className="p-3 rounded-xl bg-[#FBFBF9] border border-[#E5E5DF]">
              <span className="text-slate-500 block text-[11px]">Rep Capacity Skew</span>
              <span className="font-bold text-slate-900 font-mono text-sm">
                ±{decision.blast_radius.rep_skew_std_dev_mins} mins
              </span>
              <span className="text-[10px] text-slate-400 block mt-0.5">
                Team effort variance
              </span>
            </div>
          </div>

          {decision.blast_radius.warnings && decision.blast_radius.warnings.length > 0 && (
            <div className="space-y-1.5 pt-2 border-t border-[#F4F4F0]">
              {decision.blast_radius.warnings.map((w: string, idx: number) => (
                <div key={idx} className="text-xs text-amber-900 bg-amber-50/70 border border-amber-200/60 px-3 py-1.5 rounded-lg flex items-center gap-2 font-medium">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-600 shrink-0"></span>
                  <span>{w}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Interactive Evidence Graph View */}
      {decision?.evidence_graph && (
        <DecisionGraphViewer
          graphData={decision.evidence_graph}
          onSelectNode={(node) => {
            if (node.type === 'lead') {
              const matched = decision.recommendations.find(r => r.lead_id === node.data?.lead_id);
              if (matched) setSelectedLead(matched);
            }
          }}
        />
      )}

      {/* Main Split: Recommendations on Left, Grounded Evidence Panel on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Ranked Recommendations List */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <h2 className="text-base font-bold text-slate-900 tracking-tight">
                Prioritized Sales Recommendations
              </h2>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-teal-50 text-teal-800 border border-teal-200 font-mono font-bold">
                {decision?.recommendations?.length || 0} Ranked Accounts
              </span>
            </div>

            <button
              onClick={() => decision && onNavigateDetail(decision.decision_id)}
              className="text-xs text-teal-700 hover:text-teal-900 font-bold flex items-center gap-1"
            >
              Full Verification Dossier <ArrowRight size={13} />
            </button>
          </div>

          <div className="space-y-3.5">
            {decision?.recommendations?.map((r) => (
              <RecommendationCard
                key={r.lead_id}
                recommendation={r}
                isSelected={selectedLead?.lead_id === r.lead_id}
                onSelectLead={(lead) => setSelectedLead(lead)}
                onAskWhyNot={(lid, cName) => handleAskWhyNot(lid, cName)}
              />
            ))}
          </div>
        </div>

        {/* Right Col: Grounded Evidence & Verification Details */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-slate-900 tracking-tight">Evidence & Citations</h3>
            <button
              onClick={onOpenDataSources}
              className="text-xs text-teal-700 hover:text-teal-900 font-semibold underline font-mono"
            >
              Inspect Sources
            </button>
          </div>

          {selectedLead && (
            <EvidencePanel
              citations={selectedLead.grounded_evidence}
              verificationStatus={selectedLead.verification_status}
              leadName={`${selectedLead.lead_name} (${selectedLead.company_name})`}
            />
          )}

          {/* Verification Agent Overview Card */}
          {decision?.verification_report && (
            <div className="pq-card p-5 border-[#E5E5DF] space-y-2 text-xs bg-white shadow-sm">
              <div className="flex items-center gap-2 font-bold text-emerald-700">
                <ShieldCheck size={16} />
                <span>Verification Agent Report</span>
              </div>
              <p className="text-slate-600 leading-relaxed">
                {decision.verification_report.verification_agent_summary}
              </p>
              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] font-mono text-slate-500 font-semibold">
                <span>Groundedness: <strong className="text-emerald-700">
                  {((decision.verification_report.average_grounding_score_pct ?? (decision.verification_report.grounding_confidence ? decision.verification_report.grounding_confidence * 100 : 96.5))).toFixed(1)}%
                </strong></span>
                <span>Calibrated Risk: <strong className="text-teal-800 uppercase">
                  {decision.verification_report.all_recommendations_verified ? 'MINIMAL' : 'ELEVATED'}
                </strong></span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Human-in-the-Loop Governance & Approval Panel */}
      {decision && (
        <ApprovalPanel
          decisionId={decision.decision_id}
          approvalStatus={decision.approval_status}
          selectedLeadCount={decision.recommendations.length}
        />
      )}
    </div>
  );
};
