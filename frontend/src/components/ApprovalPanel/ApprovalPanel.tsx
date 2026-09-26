import React, { useState } from 'react';
import { approveDecision } from '../../services/api';
import { CheckCircle2, XCircle, Edit3, Lock, Copy, Check } from 'lucide-react';

interface Props {
  decisionId: string;
  onApproved?: (res: any) => void;
  approvalStatus: string;
  selectedLeadCount: number;
}

export const ApprovalPanel: React.FC<Props> = ({
  decisionId,
  onApproved,
  approvalStatus: initialStatus,
  selectedLeadCount
}) => {
  const [status, setStatus] = useState(initialStatus);
  const [loading, setLoading] = useState(false);
  const [auditHash, setAuditHash] = useState<string | null>(null);
  const [copiedHash, setCopiedHash] = useState(false);
  const [notes, setNotes] = useState('');
  const [showNotesInput, setShowNotesInput] = useState(false);

  const handleAction = async (action: 'APPROVE' | 'EDIT' | 'REJECT') => {
    setLoading(true);
    try {
      const res = await approveDecision(decisionId, action, undefined, notes);
      setStatus(action);
      setAuditHash(res.audit_hash);
      if (onApproved) onApproved(res);
    } catch (err: any) {
      alert(`Approval error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedHash(true);
    setTimeout(() => setCopiedHash(false), 2000);
  };

  return (
    <div className="pq-card p-5 border-[#E5E5DF]">
      <div className="flex flex-wrap items-center justify-between gap-4">
        {/* Left Status info */}
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-xl bg-teal-50 border border-teal-200 text-teal-800 flex items-center justify-center shrink-0">
            <Lock size={18} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h4 className="text-sm font-bold text-slate-900">Human-in-the-Loop Governance</h4>
              <span className={`px-2.5 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider ${
                status === 'APPROVED' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' :
                status === 'REJECTED' ? 'bg-rose-50 text-rose-800 border border-rose-200' :
                'bg-amber-50 text-amber-800 border border-amber-200'
              }`}>
                {status}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Sales Manager sign-off required to dispatch rep tasks, trigger outreach, and commit cryptographic audit trail.
            </p>
          </div>
        </div>

        {/* Right Action Buttons */}
        <div className="flex items-center gap-2.5">
          {status === 'PENDING' ? (
            <>
              <button
                disabled={loading}
                onClick={() => setShowNotesInput(!showNotesInput)}
                className="btn-white text-xs py-2 px-3.5"
              >
                <Edit3 size={13} />
                {showNotesInput ? 'Hide Notes' : 'Add Rationale'}
              </button>

              <button
                disabled={loading}
                onClick={() => handleAction('REJECT')}
                className="btn-outline-danger text-xs py-2 px-3.5"
              >
                <XCircle size={13} />
                Reject
              </button>

              <button
                disabled={loading}
                onClick={() => handleAction('APPROVE')}
                className="btn-green text-xs py-2 px-4.5 shadow-sm"
              >
                <CheckCircle2 size={14} />
                {loading ? 'Dispatching...' : `Approve & Dispatch (${selectedLeadCount} Accounts)`}
              </button>
            </>
          ) : (
            <div className="flex items-center gap-3">
              <span className="text-xs text-emerald-800 flex items-center gap-1.5 font-bold bg-emerald-50 px-3.5 py-2 rounded-xl border border-emerald-200">
                <CheckCircle2 size={16} />
                Decision executed & logged to immutable audit ledger
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Optional Manager notes input */}
      {showNotesInput && status === 'PENDING' && (
        <div className="mt-3 pt-3 border-t border-[#F4F4F0]">
          <input
            type="text"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Optional supervisor notes: e.g. 'Approved with emphasis on ApexFin 2 PM deadline'..."
            className="w-full bg-[#FBFBF9] border border-[#E5E5DF] rounded-xl px-3.5 py-2 text-xs text-slate-900 focus:outline-none focus:border-teal-600"
          />
        </div>
      )}

      {/* Audit Hash Banner once approved */}
      {auditHash && (
        <div className="mt-3.5 pt-3 border-t border-[#F4F4F0] flex flex-wrap items-center justify-between text-xs text-slate-600 gap-2">
          <span className="flex items-center gap-1.5 font-mono text-[11px]">
            <Lock size={12} className="text-teal-700" />
            Audit Hash: <code className="text-teal-900 font-mono font-bold bg-[#F4F4F0] px-2 py-0.5 rounded border border-[#E5E5DF]">{auditHash.slice(0, 24)}...</code>
          </span>
          <button
            onClick={() => copyToClipboard(auditHash)}
            className="text-[11px] text-teal-800 hover:text-teal-950 flex items-center gap-1 font-mono font-bold"
          >
            {copiedHash ? <Check size={12} className="text-emerald-600" /> : <Copy size={12} />}
            {copiedHash ? 'Copied' : 'Copy Full Hash'}
          </button>
        </div>
      )}
    </div>
  );
};
