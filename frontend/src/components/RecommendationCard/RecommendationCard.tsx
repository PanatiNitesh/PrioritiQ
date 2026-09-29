import React, { useState } from 'react';
import { LeadRecommendation } from '../../types';
import {
  Clock,
  ChevronDown,
  ChevronUp,
  Mail,
  CheckSquare,
  Sparkles,
  HelpCircle,
  ShieldCheck,
  Check,
  Copy
} from 'lucide-react';

interface Props {
  recommendation: LeadRecommendation;
  onAskWhyNot?: (leadId: string, companyName: string) => void;
  onSelectLead?: (lead: LeadRecommendation) => void;
  onOpenOutreach?: (lead: LeadRecommendation) => void;
  isSelected?: boolean;
}

export const RecommendationCard: React.FC<Props> = ({
  recommendation: r,
  onAskWhyNot,
  onSelectLead,
  onOpenOutreach,
  isSelected
}) => {
  const [expandedAction, setExpandedAction] = useState(false);
  const [expandedWhy, setExpandedWhy] = useState(false);
  const [copiedEmail, setCopiedEmail] = useState(false);
  const [isDispatched, setIsDispatched] = useState(false);

  const getScoreBadgeClass = (score: number) => {
    if (score >= 80) return 'badge-high';
    if (score >= 60) return 'badge-med';
    return 'badge-low';
  };

  const getStageColor = (stage: string) => {
    switch (stage.toLowerCase()) {
      case 'closing': return 'bg-emerald-50 text-emerald-800 border-emerald-200';
      case 'negotiation': return 'bg-teal-50 text-teal-800 border-teal-200';
      case 'proposal': return 'bg-sky-50 text-sky-800 border-sky-200';
      case 'demo': return 'bg-amber-50 text-amber-800 border-amber-200';
      default: return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  const copyEmailDraft = () => {
    const draftText = `Subject: ${r.suggested_action.email_draft.subject}\n\n${r.suggested_action.email_draft.body}`;
    navigator.clipboard.writeText(draftText);
    setCopiedEmail(true);
    setTimeout(() => setCopiedEmail(false), 2000);
  };

  const companyInitials = r.company_name
    ? r.company_name.split(' ').map(w => w[0]).slice(0, 2).join('')
    : 'CO';

  return (
    <div
      className={`pq-card p-5 transition-all duration-200 ${
        isSelected
          ? 'ring-2 ring-teal-600 bg-white shadow-md'
          : 'bg-white hover:border-[#CBD5E1] hover:shadow-xs'
      }`}
    >
      {/* Top Header: Rank, Avatar, Lead, Company, Score */}
      <div className="flex flex-wrap items-start justify-between gap-3 pb-3.5 border-b border-[#F4F4F0]">
        <div className="flex items-start gap-3.5">
          {/* Rank Badge */}
          <div className="w-8 h-8 rounded-lg bg-teal-800 text-white font-mono font-bold flex items-center justify-center text-sm shadow-xs shrink-0">
            #{r.rank}
          </div>

          {/* Company Avatar Initial */}
          <div className="w-10 h-10 rounded-xl bg-[#F4F4F0] border border-[#E5E5DF] flex items-center justify-center font-bold text-xs text-slate-700 font-mono shrink-0">
            {companyInitials}
          </div>

          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h3
                onClick={() => onSelectLead && onSelectLead(r)}
                className="text-base font-bold text-slate-900 hover:text-teal-700 cursor-pointer transition-colors"
              >
                {r.lead_name}
              </h3>
              <span className="text-xs px-2.5 py-0.5 rounded-full border border-[#E5E5DF] font-bold text-slate-700 bg-[#FBFBF9]">
                {r.company_name}
              </span>
              <span className={`text-[11px] px-2.5 py-0.5 rounded-full border font-mono font-bold uppercase ${getStageColor(r.stage)}`}>
                {r.stage}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              {r.title} • Assigned Rep: <strong className="text-slate-800">{r.assigned_rep}</strong>
            </p>
          </div>
        </div>

        {/* Score & Key Metrics */}
        <div className="flex items-center gap-3.5">
          <div className="text-right">
            <div className="text-[10px] uppercase font-mono text-slate-400 font-semibold">Priority Score</div>
            <span className={`badge-score-pill ${getScoreBadgeClass(r.composite_score)} text-sm`}>
              {r.composite_score}/100
            </span>
          </div>

          <div className="text-right pl-3 border-l border-[#E5E5DF]">
            <div className="text-[10px] uppercase font-mono text-slate-400 font-semibold">Deal Size</div>
            <span className="text-sm font-mono font-bold text-emerald-700">
              ${r.deal_size.toLocaleString()}
            </span>
          </div>

          <div className="text-right pl-3 border-l border-[#E5E5DF]">
            <div className="text-[10px] uppercase font-mono text-slate-400 font-semibold">Effort</div>
            <span className="text-xs font-mono text-slate-700 flex items-center gap-1 font-bold">
              <Clock size={11} className="text-slate-400" />
              {r.est_effort_mins}m
            </span>
          </div>
        </div>
      </div>

      {/* Delta Callout: What changed since yesterday? */}
      {r.what_changed && (
        <div className="my-3 px-3.5 py-2.5 rounded-xl bg-teal-50/60 border border-teal-100 flex items-center justify-between text-xs text-teal-950">
          <div className="flex items-center gap-2">
            <span className="relative flex h-2.5 w-2.5 shrink-0">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-teal-600"></span>
            </span>
            <span className="font-bold text-teal-900 shrink-0">What changed:</span>
            <span className="text-slate-700 font-medium truncate max-w-[500px]">{r.what_changed}</span>
          </div>
          <span className="text-[10px] font-mono font-bold text-teal-800 bg-white px-2 py-0.5 rounded-md border border-teal-200 shrink-0 ml-2">
            Today's Trigger
          </span>
        </div>
      )}

      {/* Grounded "Why this lead?" */}
      <div className="mt-2 text-xs">
        <div className="flex items-center justify-between text-slate-600 mb-1.5">
          <span className="font-bold text-slate-900 flex items-center gap-1.5">
            <Sparkles size={13} className="text-amber-500" />
            Why This Account Prioritized
          </span>
          <button
            onClick={() => setExpandedWhy(!expandedWhy)}
            className="text-[11px] text-teal-700 hover:text-teal-900 font-bold flex items-center gap-0.5"
          >
            {expandedWhy ? 'Collapse' : 'View all 3 signals'}
            {expandedWhy ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
          </button>
        </div>

        <div className="space-y-1.5 text-xs text-slate-700 leading-relaxed">
          <div className="flex items-start gap-2">
            <div className="w-4 h-4 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 mt-0.5">
              <Check size={10} strokeWidth={3} />
            </div>
            <span>{r.why_this_lead[0]}</span>
          </div>

          {expandedWhy && (
            <>
              {r.why_this_lead.slice(1).map((why, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <div className="w-4 h-4 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 mt-0.5">
                    <Check size={10} strokeWidth={3} />
                  </div>
                  <span>{why}</span>
                </div>
              ))}
            </>
          )}
        </div>
      </div>

      {/* Action Footer: Suggested Action & Email Draft */}
      <div className="mt-3.5 pt-3 border-t border-[#F4F4F0] flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setExpandedAction(!expandedAction)}
            className="px-3.5 py-1.5 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-900 border border-teal-200 text-xs font-bold flex items-center gap-1.5 transition-colors"
          >
            <Mail size={12} className="text-teal-700" />
            <span>{r.suggested_action.type}</span>
            {expandedAction ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
          </button>

          {onAskWhyNot && (
            <button
              onClick={() => onAskWhyNot(r.lead_id, r.company_name)}
              className="px-3.5 py-1.5 rounded-lg bg-white hover:bg-slate-50 text-slate-700 border border-[#D4D4D8] text-xs font-semibold flex items-center gap-1 transition-colors"
            >
              <HelpCircle size={12} className="text-slate-400" />
              Compare vs others
            </button>
          )}

          {onOpenOutreach && (
            <button
              onClick={() => onOpenOutreach(r)}
              className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-teal-50 to-emerald-50 hover:from-teal-100 hover:to-emerald-100 text-teal-800 border border-teal-200 text-xs font-bold flex items-center gap-1.5 transition-all shadow-xs"
              title="Launch Multi-Angle Executive Outreach Studio & Webhook Simulator"
            >
              <Sparkles size={12} className="text-teal-600 animate-pulse" />
              <span>Outreach Studio</span>
            </button>
          )}
        </div>

        <div className="flex items-center gap-2.5 text-[11px] text-slate-500 font-mono font-medium">
          <span>Enterprise ICP: <strong className="text-emerald-700 font-bold">{r.icp_fit}%</strong></span>
          <span>•</span>
          <span className="text-emerald-700 font-bold flex items-center gap-1">
            <ShieldCheck size={12} /> 100% Grounded
          </span>
        </div>
      </div>

      {/* Expanded Action & Email Preview Drawer */}
      {expandedAction && (
        <div className="mt-3.5 p-4 rounded-xl bg-[#FBFBF9] border border-[#E5E5DF] text-xs space-y-3">
          <div className="flex items-center justify-between border-b border-[#E5E5DF] pb-2.5">
            <div className="flex items-center gap-1.5 font-bold text-slate-900">
              <Mail size={13} className="text-teal-700" />
              <span>Personalized Outreach Briefing</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-mono text-slate-500">
                To: <strong className="text-slate-800">{r.suggested_action.email_draft.to}</strong>
              </span>
              <button
                onClick={copyEmailDraft}
                className="px-2 py-0.5 rounded bg-white border border-[#D4D4D8] text-slate-600 hover:text-slate-900 flex items-center gap-1 text-[10px] font-semibold"
              >
                {copiedEmail ? <Check size={10} className="text-emerald-600" /> : <Copy size={10} />}
                {copiedEmail ? 'Copied' : 'Copy Draft'}
              </button>
            </div>
          </div>

          <div>
            <div className="text-[11px] text-slate-600 font-mono mb-1.5">
              Subject: <strong className="text-slate-900 font-sans">{r.suggested_action.email_draft.subject}</strong>
            </div>
            <div className="p-3.5 rounded-xl bg-white border border-[#E5E5DF] text-slate-800 text-xs font-sans whitespace-pre-line leading-relaxed shadow-xs">
              {r.suggested_action.email_draft.body}
            </div>
          </div>

          <div className="flex items-center justify-between pt-1">
            <span className="text-[11px] text-slate-600 flex items-center gap-1.5 font-medium">
              <CheckSquare size={13} className="text-emerald-600" />
              Automates task creation for <strong className="text-slate-900">{r.assigned_rep}</strong>
            </span>
            {isDispatched ? (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-semibold">
                <Check size={12} className="text-emerald-600" /> Dispatched to CRM & Webhook
              </span>
            ) : (
              <button
                onClick={() => setIsDispatched(true)}
                className="btn-teal text-xs py-1.5 px-3.5"
              >
                Dispatch Task & Email
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
