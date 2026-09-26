import React, { useEffect, useState } from 'react';
import { fetchDecisionHistory } from '../services/api';
import { AuditLogEntry } from '../types';
import { Lock, CheckCircle2, ArrowRight, Download } from 'lucide-react';

interface Props {
  onSelectDecision?: (decisionId: string) => void;
}

export const Decisions: React.FC<Props> = ({ onSelectDecision }) => {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDecisionHistory()
      .then(setLogs)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const exportAuditLog = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(logs, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute("href", dataStr);
    dlAnchor.setAttribute("download", `decisiongraph_audit_ledger_${new Date().toISOString().slice(0, 10)}.json`);
    dlAnchor.click();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-indigo-700 font-mono text-xs font-semibold uppercase tracking-wider mb-1">
            <Lock size={14} />
            Governance & Audit Trail
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900">Decision Audit Ledger</h1>
          <p className="text-xs text-slate-500 mt-1">
            Tamper-evident record of all AI orchestrator runs, user follow-ups, and sales manager approvals.
          </p>
        </div>

        <button onClick={exportAuditLog} className="btn-secondary text-xs flex items-center gap-1.5 font-semibold">
          <Download size={14} />
          Export JSON Audit Log
        </button>
      </div>

      {/* Ledger Table */}
      <div className="glass-panel bg-white rounded-2xl overflow-hidden border border-slate-200 shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 font-mono uppercase text-[10px] border-b border-slate-200 font-bold">
              <tr>
                <th className="p-4">Event & ID</th>
                <th className="p-4">Decision Query</th>
                <th className="p-4">Role & Action</th>
                <th className="p-4">Timestamp</th>
                <th className="p-4">Audit Hash (SHA-256)</th>
                <th className="p-4 text-right">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-sans">
              {loading ? (
                <tr>
                  <td colSpan={6} className="p-8 text-center text-slate-400">
                    Loading decision logs...
                  </td>
                </tr>
              ) : logs.length === 0 ? (
                <tr>
                  <td colSpan={6} className="p-8 text-center text-slate-400">
                    No decisions logged yet. Run a query on the dashboard to create decisions.
                  </td>
                </tr>
              ) : (
                logs.map((log) => (
                  <tr key={log.event_id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-4 font-mono">
                      <span className="font-bold text-slate-900">{log.event_id}</span>
                      <div className="text-[10px] text-slate-400">{log.decision_id}</div>
                    </td>

                    <td className="p-4 max-w-xs">
                      <p className="font-semibold text-slate-800 truncate">{log.query}</p>
                    </td>

                    <td className="p-4 font-mono">
                      <span
                        className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                          log.action === 'APPROVED'
                            ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                            : log.action === 'REJECTED'
                            ? 'bg-rose-50 text-rose-800 border border-rose-200'
                            : 'bg-indigo-50 text-indigo-800 border border-indigo-200'
                        }`}
                      >
                        {log.action === 'APPROVED' ? <CheckCircle2 size={10} /> : null}
                        {log.action}
                      </span>
                      <div className="text-[10px] text-slate-500 mt-0.5">{log.user_role}</div>
                    </td>

                    <td className="p-4 text-slate-600 font-mono text-[11px]">
                      {new Date(log.timestamp).toLocaleString()}
                    </td>

                    <td className="p-4 font-mono text-[11px] text-slate-600 max-w-[140px] truncate">
                      <code className="text-indigo-700 bg-slate-100 px-1.5 py-0.5 rounded">{log.audit_hash.slice(0, 16)}...</code>
                    </td>

                    <td className="p-4 text-right">
                      {onSelectDecision && (
                        <button
                          onClick={() => onSelectDecision(log.decision_id)}
                          className="px-2.5 py-1 rounded bg-slate-100 hover:bg-indigo-50 text-slate-700 hover:text-indigo-700 border border-slate-200 transition-colors inline-flex items-center gap-1 font-semibold"
                        >
                          <span>Inspect</span>
                          <ArrowRight size={11} />
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
