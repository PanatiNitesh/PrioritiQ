import React, { useEffect, useState } from 'react';
import { fetchLeads, fetchLeadDetail } from '../services/api';
import { Search, X } from 'lucide-react';

export const Leads: React.FC = () => {
  const [leads, setLeads] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedLeadId, setSelectedLeadId] = useState<string | null>(null);
  const [leadDetail, setLeadDetail] = useState<any>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [search, setSearch] = useState('');
  const [stageFilter, setStageFilter] = useState('');

  useEffect(() => {
    fetchLeads(stageFilter)
      .then(setLeads)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [stageFilter]);

  const handleSelectLead = async (id: string) => {
    setSelectedLeadId(id);
    setLoadingDetail(true);
    try {
      const detail = await fetchLeadDetail(id);
      setLeadDetail(detail);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingDetail(false);
    }
  };

  const filtered = leads.filter(l => {
    const q = search.toLowerCase();
    return (
      l.name?.toLowerCase().includes(q) ||
      l.company_name?.toLowerCase().includes(q) ||
      l.lead_id?.toLowerCase().includes(q) ||
      l.assigned_rep?.toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-indigo-700 font-mono text-xs font-semibold uppercase tracking-wider mb-1">
            CRM Structured Dataset
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900">Lead Intelligence & Pipeline</h1>
          <p className="text-xs text-slate-500 mt-1">
            Multi-signal deterministic scoring, firmographics, and engagement recency.
          </p>
        </div>

        {/* Search & Filter */}
        <div className="flex items-center gap-2.5">
          <div className="relative">
            <Search size={14} className="absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search leads, companies..."
              className="glass-input pl-9 pr-3 py-1.5 text-xs w-56 shadow-sm"
            />
          </div>

          <select
            value={stageFilter}
            onChange={(e) => setStageFilter(e.target.value)}
            className="glass-input px-3 py-1.5 text-xs bg-white text-slate-700 shadow-sm"
          >
            <option value="">All Stages</option>
            <option value="Closing">Closing</option>
            <option value="Negotiation">Negotiation</option>
            <option value="Proposal">Proposal</option>
            <option value="Demo">Demo</option>
            <option value="Discovery">Discovery</option>
          </select>
        </div>
      </div>

      {/* Main Grid: Table on Left, Inspect Drawer on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className={`${selectedLeadId ? 'lg:col-span-2' : 'lg:col-span-3'} glass-panel bg-white rounded-2xl overflow-hidden border border-slate-200 shadow-sm`}>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-mono uppercase text-[10px] border-b border-slate-200 font-bold">
                <tr>
                  <th className="p-3.5">Lead / Company</th>
                  <th className="p-3.5">Stage</th>
                  <th className="p-3.5">Deal Size</th>
                  <th className="p-3.5">Score</th>
                  <th className="p-3.5">ICP Fit</th>
                  <th className="p-3.5">Rep</th>
                  <th className="p-3.5">Delta Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-sans">
                {filtered.map((l) => (
                  <tr
                    key={l.lead_id}
                    onClick={() => handleSelectLead(l.lead_id)}
                    className={`cursor-pointer transition-colors ${
                      selectedLeadId === l.lead_id ? 'bg-indigo-50/60' : 'hover:bg-slate-50'
                    }`}
                  >
                    <td className="p-3.5">
                      <div className="font-bold text-slate-900">{l.name}</div>
                      <div className="text-[11px] text-slate-500">{l.company_name} • {l.title}</div>
                    </td>

                    <td className="p-3.5 font-mono">
                      <span className="px-2 py-0.5 rounded-full text-[10px] bg-slate-100 border border-slate-200 text-slate-700 font-semibold">
                        {l.stage}
                      </span>
                    </td>

                    <td className="p-3.5 font-mono text-emerald-700 font-bold">
                      ${Number(l.deal_size).toLocaleString()}
                    </td>

                    <td className="p-3.5 font-mono font-bold text-indigo-700">
                      {l.final_score}
                    </td>

                    <td className="p-3.5 font-mono text-slate-700 font-semibold">
                      {l.icp_fit}%
                    </td>

                    <td className="p-3.5 text-slate-600">
                      {l.assigned_rep}
                    </td>

                    <td className="p-3.5 max-w-[200px]">
                      <span className="text-[10px] font-mono font-semibold text-indigo-800 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded truncate block">
                        {l.delta_status?.replace(/_/g, ' ') || 'ACTIVE'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Lead Inspection Drawer */}
        {selectedLeadId && (
          <div className="glass-panel p-5 rounded-2xl bg-white border border-indigo-200 shadow-sm space-y-4">
            <div className="flex items-start justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="font-mono text-[10px] text-indigo-700 uppercase tracking-wider font-bold">
                  {leadDetail?.lead_id}
                </span>
                <h3 className="text-base font-bold text-slate-900 mt-0.5">{leadDetail?.name}</h3>
                <p className="text-xs text-slate-500">{leadDetail?.title} at {leadDetail?.company_name}</p>
              </div>
              <button
                onClick={() => setSelectedLeadId(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100"
              >
                <X size={16} />
              </button>
            </div>

            {loadingDetail ? (
              <p className="text-xs text-slate-400 py-4 text-center">Loading intelligence...</p>
            ) : leadDetail ? (
              <div className="space-y-4 text-xs">
                {/* Metric Summary */}
                <div className="grid grid-cols-2 gap-2">
                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                    <span className="text-[10px] font-mono text-slate-500 uppercase font-medium">Deal Size</span>
                    <p className="text-base font-bold font-mono text-emerald-700 mt-0.5">
                      ${Number(leadDetail.deal_size).toLocaleString()}
                    </p>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                    <span className="text-[10px] font-mono text-slate-500 uppercase font-medium">Composite Score</span>
                    <p className="text-base font-bold font-mono text-indigo-700 mt-0.5">
                      {leadDetail.final_score}/100
                    </p>
                  </div>
                </div>

                {/* Grounded Delta */}
                <div>
                  <h4 className="text-[11px] font-mono font-bold text-indigo-900 uppercase mb-1">
                    Delta Since Yesterday
                  </h4>
                  <div className="p-3 rounded-xl bg-indigo-50 border border-indigo-100 text-indigo-950 text-xs leading-relaxed">
                    {leadDetail.delta_info?.explanation}
                  </div>
                </div>

                {/* Grounded Unstructured Notes */}
                {leadDetail.grounded_citations && leadDetail.grounded_citations.length > 0 && (
                  <div>
                    <h4 className="text-[11px] font-mono font-bold text-purple-900 uppercase mb-1">
                      Verbatim RAG Citations ({leadDetail.grounded_citations.length})
                    </h4>
                    <div className="space-y-2">
                      {leadDetail.grounded_citations.map((c: any, i: number) => (
                        <div key={i} className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs">
                          <span className="font-mono text-purple-700 text-[10px] font-bold block mb-1">
                            {c.source_file} • {c.timestamp}
                          </span>
                          <p className="text-slate-800 italic leading-relaxed">"{c.quote}"</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : null}
          </div>
        )}
      </div>
    </div>
  );
};
