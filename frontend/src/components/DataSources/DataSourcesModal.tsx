import React, { useEffect, useState } from 'react';
import { fetchDataSourcesSummary, fetchAllNotes } from '../../services/api';
import { Database, X, CheckCircle2, Layers } from 'lucide-react';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const DataSourcesModal: React.FC<Props> = ({ isOpen, onClose }) => {
  const [summary, setSummary] = useState<any>(null);
  const [notes, setNotes] = useState<any[]>([]);
  const [selectedNote, setSelectedNote] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'sources' | 'notes'>('sources');

  useEffect(() => {
    if (isOpen) {
      fetchDataSourcesSummary().then(setSummary).catch(console.error);
      fetchAllNotes().then(n => {
        setNotes(n);
        if (n.length > 0) setSelectedNote(n[0]);
      }).catch(console.error);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="glass-panel w-full max-w-4xl max-h-[90vh] flex flex-col rounded-2xl border border-slate-200 shadow-2xl overflow-hidden bg-white">
        {/* Header */}
        <div className="p-5 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-indigo-50 text-indigo-700 border border-indigo-200">
              <Database size={18} />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-900">Underlying Business Data Sources</h3>
              <p className="text-xs text-slate-500">Structured CRM records & Unstructured Sales Knowledge</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex rounded-lg bg-slate-200/70 p-0.5 text-xs font-semibold">
              <button
                onClick={() => setActiveTab('sources')}
                className={`px-3 py-1 rounded-md transition-all ${activeTab === 'sources' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
              >
                Data Catalog
              </button>
              <button
                onClick={() => setActiveTab('notes')}
                className={`px-3 py-1 rounded-md transition-all ${activeTab === 'notes' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
              >
                Sales Notes ({notes.length})
              </button>
            </div>

            <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-slate-200 text-slate-400 hover:text-slate-700">
              <X size={18} />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto flex-1">
          {activeTab === 'sources' ? (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {summary?.sources?.map((s: any, idx: number) => (
                  <div key={idx} className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-mono text-sm font-bold text-slate-900 flex items-center gap-2">
                        <Layers size={14} className="text-indigo-600" />
                        {s.name}
                      </span>
                      <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 flex items-center gap-1">
                        <CheckCircle2 size={10} /> {s.status}
                      </span>
                    </div>
                    <div className="text-xs text-slate-600 mb-2">{s.type}</div>
                    <div className="text-xs text-slate-800 font-mono">
                      Records: <strong className="text-indigo-700">{s.records_count}</strong>
                    </div>
                    {s.columns && (
                      <div className="mt-2 text-[10px] text-slate-500 truncate font-mono">
                        Schema: {s.columns.slice(0, 5).join(', ')}...
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <div className="p-4 rounded-xl bg-indigo-50 border border-indigo-200 text-xs text-indigo-950">
                <span className="font-bold text-indigo-900">Architecture Guarantee:</span> Zero simulated data or hallucinations.
                The DecisionGraph Orchestrator reads directly from these mounted files, generating verifiable citations and exact deterministic formulas for every lead priority.
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 min-h-[400px]">
              {/* Notes List */}
              <div className="space-y-2 max-h-[420px] overflow-y-auto pr-2 border-r border-slate-200">
                {notes.map((n, idx) => (
                  <div
                    key={idx}
                    onClick={() => setSelectedNote(n)}
                    className={`p-3 rounded-xl border text-xs cursor-pointer transition-all ${
                      selectedNote?.filename === n.filename
                        ? 'bg-indigo-50 border-indigo-300 text-indigo-950 font-semibold'
                        : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    <div className="font-mono font-bold text-[11px] text-indigo-700 truncate">{n.filename}</div>
                    <div className="text-[11px] text-slate-800 truncate mt-0.5">{n.subject || n.type}</div>
                    <div className="text-[10px] text-slate-500 mt-1 flex justify-between font-mono">
                      <span>{n.lead_id}</span>
                      <span>{n.date}</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Note Content View */}
              <div className="md:col-span-2 p-5 rounded-xl bg-slate-50 border border-slate-200 flex flex-col">
                {selectedNote ? (
                  <>
                    <div className="border-b border-slate-200 pb-3 mb-3">
                      <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                        <span className="font-mono text-purple-700 font-bold">{selectedNote.filename}</span>
                        <span className="font-mono text-[10px]">{selectedNote.date}</span>
                      </div>
                      <h4 className="text-sm font-bold text-slate-900">{selectedNote.subject}</h4>
                      <p className="text-xs text-slate-600 mt-1 font-mono">
                        Lead: <strong className="text-slate-900">{selectedNote.lead_id}</strong> • Author: <strong className="text-slate-900">{selectedNote.author}</strong>
                      </p>
                    </div>

                    <div className="flex-1 overflow-y-auto p-4 rounded-xl bg-white border border-slate-200 text-xs text-slate-800 whitespace-pre-wrap font-mono leading-relaxed shadow-inner">
                      {selectedNote.content}
                    </div>
                  </>
                ) : (
                  <div className="flex items-center justify-center h-full text-xs text-slate-400">
                    Select a note to inspect raw RAG text
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
