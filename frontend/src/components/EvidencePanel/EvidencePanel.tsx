import React from 'react';
import { GroundedCitation, VerificationStatus } from '../../types';
import { ShieldCheck, FileCheck, CheckCircle2, AlertCircle, Quote } from 'lucide-react';

interface Props {
  citations: GroundedCitation[];
  verificationStatus?: VerificationStatus;
  leadName?: string;
}

export const EvidencePanel: React.FC<Props> = ({ citations, verificationStatus, leadName }) => {
  return (
    <div className="pq-card p-5 border-[#E5E5DF] flex flex-col gap-3.5">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-[#F4F4F0] pb-3">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-teal-50 text-teal-800 border border-teal-200">
            <ShieldCheck size={16} />
          </div>
          <div>
            <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              Grounded Evidence & Provenance
            </h4>
            {leadName && <p className="text-[11px] text-slate-500 font-medium">Context for {leadName}</p>}
          </div>
        </div>

        {verificationStatus && (
          <div className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 font-mono text-[11px] font-bold">
            <CheckCircle2 size={12} className="text-emerald-600" />
            <span>{verificationStatus.grounding_score_pct}% Grounded</span>
          </div>
        )}
      </div>

      {/* Citations List */}
      <div className="flex flex-col gap-2.5 max-h-[300px] overflow-y-auto pr-1">
        {citations.length === 0 ? (
          <p className="text-xs text-slate-400 italic py-2">No direct unstructured notes attached.</p>
        ) : (
          citations.map((c, idx) => (
            <div key={idx} className="p-3.5 rounded-xl bg-[#FBFBF9] border border-[#E5E5DF] hover:border-teal-300 transition-all">
              <div className="flex items-center justify-between text-[11px] text-slate-500 mb-1.5">
                <span className="font-mono text-purple-700 flex items-center gap-1 font-bold">
                  <FileCheck size={12} />
                  {c.source_file}
                </span>
                <span className="text-[10px] text-slate-400 font-mono">{c.timestamp}</span>
              </div>

              <div className="flex items-start gap-2">
                <Quote size={13} className="text-purple-500 shrink-0 mt-0.5 opacity-70" />
                <p className="text-xs text-slate-800 leading-relaxed font-normal">
                  {c.quote}
                </p>
              </div>

              <div className="mt-2.5 pt-2 border-t border-[#E5E5DF] flex items-center justify-between text-[10px] text-slate-500 font-mono">
                <span>Author: <strong className="text-slate-800 font-sans">{c.author_or_actor}</strong></span>
                <span className="text-emerald-700 font-bold flex items-center gap-1">
                  <CheckCircle2 size={10} /> Fact Checked
                </span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Verification Agent Checks Breakdown */}
      {verificationStatus && verificationStatus.checks && (
        <div className="mt-1 pt-3 border-t border-[#F4F4F0]">
          <div className="text-[10px] uppercase font-mono text-slate-500 font-bold mb-2">
            Verification Checks ({verificationStatus.checks_passed}/{verificationStatus.checks_evaluated} Passed)
          </div>
          <div className="flex flex-col gap-1.5">
            {verificationStatus.checks.map((chk, i) => (
              <div key={i} className="flex items-center justify-between text-[11px] text-slate-700">
                <span className="flex items-center gap-1.5 font-medium">
                  {chk.passed ? (
                    <CheckCircle2 size={12} className="text-emerald-600 shrink-0" />
                  ) : (
                    <AlertCircle size={12} className="text-amber-600 shrink-0" />
                  )}
                  {chk.check.replace(/_/g, ' ')}
                </span>
                <span className="text-[10px] font-mono text-slate-500 truncate max-w-[180px]">{chk.evidence}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
