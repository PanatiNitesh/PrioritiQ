import React, { useState, useEffect } from 'react';
import { fetchScoringRules, updateScoringRules, previewScoringRulesImpact } from '../services/api';
import {
  Sliders,
  Save,
  RotateCcw,
  CheckCircle2,
  TrendingUp,
  AlertCircle,
  ShieldAlert,
  ArrowUp,
  ArrowDown,
  Minus,
  Sparkles
} from 'lucide-react';

export const RevOpsStudio: React.FC = () => {
  const [rules, setRules] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [previewDiffs, setPreviewDiffs] = useState<any[]>([]);
  const [previewLoading, setPreviewLoading] = useState(false);

  useEffect(() => {
    fetchScoringRules()
      .then((data) => {
        setRules(data);
        handlePreview(data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handlePreview = async (currentRules: any) => {
    setPreviewLoading(true);
    try {
      const diffs = await previewScoringRulesImpact(currentRules);
      setPreviewDiffs(diffs);
    } catch (err) {
      console.error('Preview error:', err);
    } finally {
      setPreviewLoading(false);
    }
  };

  const handleWeightChange = (category: string, key: string, value: number) => {
    if (!rules) return;
    const updated = {
      ...rules,
      strategy_weights: {
        ...rules.strategy_weights,
        balanced: {
          ...rules.strategy_weights.balanced,
          [key]: value
        }
      }
    };
    setRules(updated);
    handlePreview(updated);
  };

  const handleStageWeightChange = (stage: string, value: number) => {
    if (!rules) return;
    const updated = {
      ...rules,
      stage_weights: {
        ...rules.stage_weights,
        [stage]: value
      }
    };
    setRules(updated);
    handlePreview(updated);
  };

  const handleChurnPenaltyChange = (tier: string, value: number) => {
    if (!rules) return;
    const updated = {
      ...rules,
      churn_penalties: {
        ...rules.churn_penalties,
        [tier]: value
      }
    };
    setRules(updated);
    handlePreview(updated);
  };

  const handleSavePolicy = async () => {
    if (!rules) return;
    setSaving(true);
    try {
      await updateScoringRules(rules);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      alert(`Failed to save policy: ${err}`);
    } finally {
      setSaving(false);
    }
  };

  const handleResetDefaults = () => {
    const defaults = {
      strategy_weights: {
        balanced: {
          deal_size: 0.40,
          intent_score: 0.25,
          icp_fit: 0.20,
          stage_weight: 0.15
        }
      },
      stage_weights: {
        Closing: 1.0,
        Negotiation: 0.88,
        Proposal: 0.72,
        Demo: 0.55,
        Discovery: 0.35
      },
      churn_penalties: {
        High: 0.20,
        Medium: 0.08,
        Low: 0.0
      },
      recency_decay_half_life_days: 4.0
    };
    setRules(defaults);
    handlePreview(defaults);
  };

  if (loading || !rules) {
    return (
      <div className="pq-card p-12 text-center text-slate-400">
        Loading RevOps Scoring Policy Studio...
      </div>
    );
  }

  const strat = rules.strategy_weights?.balanced || {};
  const stages = rules.stage_weights || {};
  const churn = rules.churn_penalties || {};

  return (
    <div className="space-y-6">
      {/* Studio Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-teal-800 font-mono text-xs font-semibold uppercase tracking-wider mb-1">
            <Sliders size={14} className="text-teal-700" />
            Revenue Operations Control Center
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Scoring Policy & Dynamic Weight Studio
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Fine-tune deterministic prioritization formulas, stage multipliers, and churn penalties with live pipeline impact previews.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={handleResetDefaults}
            className="px-3.5 py-2 rounded-xl bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all shadow-xs"
          >
            <RotateCcw size={13} className="text-slate-500" />
            <span>Reset to Standard</span>
          </button>

          <button
            onClick={handleSavePolicy}
            disabled={saving}
            className="btn-teal px-5 py-2 text-xs flex items-center gap-1.5 font-bold shadow-sm"
          >
            {saving ? (
              <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            ) : (
              <Save size={14} />
            )}
            <span>Publish Active Enterprise Policy</span>
          </button>
        </div>
      </div>

      {/* Confirmation Toast */}
      {saveSuccess && (
        <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 text-xs font-semibold flex items-center gap-2 animate-fadeIn shadow-xs">
          <CheckCircle2 size={16} className="text-emerald-600" />
          <span>Enterprise scoring policy updated and persisted successfully to SQLite database!</span>
        </div>
      )}

      {/* Main Grid: Policy Tuning on Left, Live Impact on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Sliders (5 cols) */}
        <div className="lg:col-span-5 space-y-5">
          {/* Strategy Dimension Weights */}
          <div className="pq-card p-5 border-[#E5E5DF] space-y-4 bg-white shadow-xs">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 font-mono">
                1. Core Strategic Dimension Weights
              </h3>
              <span className="text-[10px] font-mono bg-teal-50 text-teal-800 px-2 py-0.5 rounded font-bold border border-teal-200">
                Sum: {((strat.deal_size + strat.intent_score + strat.icp_fit + strat.stage_weight) * 100).toFixed(0)}%
              </span>
            </div>

            <div className="space-y-3.5 text-xs">
              <div>
                <div className="flex justify-between text-slate-700 font-semibold mb-1">
                  <span>Deal Size ($) Weight:</span>
                  <strong className="font-mono text-teal-800">{(strat.deal_size * 100).toFixed(0)}%</strong>
                </div>
                <input
                  type="range"
                  min="0.10"
                  max="0.70"
                  step="0.05"
                  value={strat.deal_size}
                  onChange={(e) => handleWeightChange('balanced', 'deal_size', parseFloat(e.target.value))}
                  className="w-full accent-teal-700 cursor-pointer h-1.5 bg-slate-200 rounded-lg"
                />
              </div>

              <div>
                <div className="flex justify-between text-slate-700 font-semibold mb-1">
                  <span>Inbound Intent & Velocity:</span>
                  <strong className="font-mono text-teal-800">{(strat.intent_score * 100).toFixed(0)}%</strong>
                </div>
                <input
                  type="range"
                  min="0.10"
                  max="0.60"
                  step="0.05"
                  value={strat.intent_score}
                  onChange={(e) => handleWeightChange('balanced', 'intent_score', parseFloat(e.target.value))}
                  className="w-full accent-teal-700 cursor-pointer h-1.5 bg-slate-200 rounded-lg"
                />
              </div>

              <div>
                <div className="flex justify-between text-slate-700 font-semibold mb-1">
                  <span>Enterprise ICP Alignment:</span>
                  <strong className="font-mono text-teal-800">{(strat.icp_fit * 100).toFixed(0)}%</strong>
                </div>
                <input
                  type="range"
                  min="0.05"
                  max="0.50"
                  step="0.05"
                  value={strat.icp_fit}
                  onChange={(e) => handleWeightChange('balanced', 'icp_fit', parseFloat(e.target.value))}
                  className="w-full accent-teal-700 cursor-pointer h-1.5 bg-slate-200 rounded-lg"
                />
              </div>

              <div>
                <div className="flex justify-between text-slate-700 font-semibold mb-1">
                  <span>Pipeline Milestone Weight:</span>
                  <strong className="font-mono text-teal-800">{(strat.stage_weight * 100).toFixed(0)}%</strong>
                </div>
                <input
                  type="range"
                  min="0.05"
                  max="0.40"
                  step="0.05"
                  value={strat.stage_weight}
                  onChange={(e) => handleWeightChange('balanced', 'stage_weight', parseFloat(e.target.value))}
                  className="w-full accent-teal-700 cursor-pointer h-1.5 bg-slate-200 rounded-lg"
                />
              </div>
            </div>
          </div>

          {/* Pipeline Stage Multipliers */}
          <div className="pq-card p-5 border-[#E5E5DF] space-y-4 bg-white shadow-xs">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 font-mono border-b border-slate-100 pb-2.5">
              2. Pipeline Stage Multipliers
            </h3>

            <div className="space-y-3 text-xs">
              {['Closing', 'Negotiation', 'Proposal', 'Demo', 'Discovery'].map((stg) => (
                <div key={stg} className="flex items-center justify-between gap-4">
                  <span className="font-semibold text-slate-700 w-24">{stg}:</span>
                  <input
                    type="range"
                    min="0.10"
                    max="1.0"
                    step="0.05"
                    value={stages[stg] || 0.5}
                    onChange={(e) => handleStageWeightChange(stg, parseFloat(e.target.value))}
                    className="flex-1 accent-teal-700 cursor-pointer h-1.5 bg-slate-200 rounded-lg"
                  />
                  <span className="font-mono text-slate-800 font-bold w-12 text-right">
                    {((stages[stg] || 0.5) * 100).toFixed(0)}%
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Churn Risk Penalties */}
          <div className="pq-card p-5 border-[#E5E5DF] space-y-4 bg-white shadow-xs">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 font-mono border-b border-slate-100 pb-2.5">
              3. Churn Risk Deduction Penalties
            </h3>

            <div className="space-y-3 text-xs">
              {['High', 'Medium', 'Low'].map((tier) => (
                <div key={tier} className="flex items-center justify-between gap-4">
                  <span className="font-semibold text-slate-700 w-24">{tier} Risk:</span>
                  <input
                    type="range"
                    min="0.0"
                    max="0.40"
                    step="0.02"
                    value={churn[tier] || 0.0}
                    onChange={(e) => handleChurnPenaltyChange(tier, parseFloat(e.target.value))}
                    className="flex-1 accent-rose-600 cursor-pointer h-1.5 bg-slate-200 rounded-lg"
                  />
                  <span className="font-mono text-rose-700 font-bold w-12 text-right">
                    -{((churn[tier] || 0.0) * 100).toFixed(0)} pts
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Live Pipeline Re-ranking Impact Preview (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="pq-card p-5 border-[#E5E5DF] bg-white shadow-xs space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <h3 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
                  <Sparkles size={16} className="text-teal-700" />
                  Live Pipeline Re-Ranking Preview
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Real-time simulation of rank movements and score differentials under modified rules
                </p>
              </div>

              {previewLoading && (
                <span className="text-xs font-mono text-teal-700 flex items-center gap-1.5 font-semibold">
                  <span className="w-3 h-3 border-2 border-teal-700 border-t-transparent rounded-full animate-spin"></span>
                  Calculating...
                </span>
              )}
            </div>

            {/* Impact Table */}
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-[#FBFBF9] text-slate-600 font-mono uppercase text-[10px] border-b border-[#E5E5DF]">
                  <tr>
                    <th className="p-3">New Rank</th>
                    <th className="p-3">Account & Stage</th>
                    <th className="p-3 text-right">Deal Size</th>
                    <th className="p-3 text-right">Baseline Score</th>
                    <th className="p-3 text-right">New Score</th>
                    <th className="p-3 text-right">Rank Shift</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-sans">
                  {previewDiffs.map((diff) => (
                    <tr key={diff.lead_id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="p-3 font-mono font-bold text-slate-900">
                        #{diff.new_rank}
                      </td>

                      <td className="p-3">
                        <span className="font-semibold text-slate-900 block">{diff.company_name}</span>
                        <span className="text-[10px] text-slate-400 font-mono">{diff.lead_name} • {diff.stage}</span>
                      </td>

                      <td className="p-3 text-right font-mono font-semibold text-slate-800">
                        ${diff.deal_size.toLocaleString()}
                      </td>

                      <td className="p-3 text-right font-mono text-slate-500">
                        {diff.old_score}
                      </td>

                      <td className="p-3 text-right font-mono font-bold text-teal-800">
                        {diff.new_score}
                        <span className={`text-[10px] ml-1.5 ${
                          diff.score_delta > 0 ? 'text-emerald-600' : diff.score_delta < 0 ? 'text-rose-600' : 'text-slate-400'
                        }`}>
                          ({diff.score_delta > 0 ? `+${diff.score_delta}` : diff.score_delta})
                        </span>
                      </td>

                      <td className="p-3 text-right font-mono">
                        {diff.rank_shift > 0 ? (
                          <span className="inline-flex items-center gap-0.5 px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
                            <ArrowUp size={10} /> +{diff.rank_shift}
                          </span>
                        ) : diff.rank_shift < 0 ? (
                          <span className="inline-flex items-center gap-0.5 px-2 py-0.5 rounded text-[10px] font-bold bg-rose-50 text-rose-800 border border-rose-200">
                            <ArrowDown size={10} /> {diff.rank_shift}
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-0.5 px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-500">
                            <Minus size={10} /> No shift
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
