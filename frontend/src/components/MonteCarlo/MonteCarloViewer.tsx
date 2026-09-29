import React, { useState } from 'react';
import { MonteCarloSimulation } from '../../types';
import { runMonteCarloSimulation } from '../../services/api';
import {
  TrendingUp,
  BarChart3,
  Sliders,
  RefreshCw,
  ShieldAlert,
  ArrowUpRight,
  Sparkles,
  Percent
} from 'lucide-react';

interface Props {
  simulationData?: MonteCarloSimulation;
  priorityWeight?: string;
  onSimulationUpdated?: (newSim: MonteCarloSimulation) => void;
}

export const MonteCarloViewer: React.FC<Props> = ({
  simulationData,
  priorityWeight = 'balanced',
  onSimulationUpdated
}) => {
  const [data, setData] = useState<MonteCarloSimulation | undefined>(simulationData);
  const [volatility, setVolatility] = useState<number>(simulationData?.market_volatility || 0.12);
  const [running, setRunning] = useState(false);

  const handleRerun = async (newVol: number) => {
    setRunning(true);
    try {
      const res = await runMonteCarloSimulation({
        trials: 1000,
        market_volatility: newVol,
        priority_weight: priorityWeight
      });
      setData(res);
      if (onSimulationUpdated) onSimulationUpdated(res);
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setRunning(false);
    }
  };

  const sim = data || simulationData;
  if (!sim) return null;

  const maxDensity = Math.max(
    ...sim.distribution_buckets.map(b => Math.max(b.prioritiq_density, b.baseline_density)),
    1
  );

  return (
    <div className="pq-card p-6 bg-gradient-to-b from-white via-white to-[#F8FAF9] border border-teal-200/80 shadow-sm space-y-5">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-teal-50 border border-teal-200 text-teal-800 flex items-center justify-center shadow-xs">
            <TrendingUp size={16} className="text-teal-700" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-sm font-bold text-slate-900 tracking-tight">
                Monte Carlo Stochastic Pipeline Revenue Forecast
              </h3>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-teal-50 text-teal-800 border border-teal-200">
                1,000 Stochastic Iterations
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Simulating deal conversion variance, touchpoint acceleration & churn risk over 1,000 trials
            </p>
          </div>
        </div>

        {/* Expected Lift Badge */}
        <div className="flex items-center gap-2">
          <div className="px-3.5 py-1.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 font-mono text-xs flex items-center gap-1.5 shadow-xs">
            <ArrowUpRight size={14} className="text-emerald-600" />
            <span className="text-[11px] font-semibold text-emerald-700">Projected Lift:</span>
            <strong className="font-bold text-emerald-800 text-sm">
              +${sim.projected_revenue_lift.toLocaleString()} (+{sim.lift_percentage}%)
            </strong>
          </div>
        </div>
      </div>

      {/* Probability Summary Callout */}
      <div className="p-3.5 rounded-xl bg-teal-50/60 border border-teal-200/60 text-xs text-slate-700 flex items-start gap-2.5">
        <Sparkles size={16} className="text-teal-700 shrink-0 mt-0.5" />
        <p className="leading-relaxed font-sans">
          {sim.executive_summary}
        </p>
      </div>

      {/* Scenario Percentiles Comparison Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
        {/* PrioritiQ Schedule */}
        <div className="p-4 rounded-xl bg-white border-2 border-teal-600/30 shadow-xs space-y-3">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2">
            <span className="font-bold text-teal-900 flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-teal-600"></span>
              PrioritiQ Capacity Schedule
            </span>
            <span className="text-[11px] text-teal-700 font-bold bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
              EV: ${sim.expected_revenue_optimized.toLocaleString()}
            </span>
          </div>

          <div className="grid grid-cols-3 gap-2 text-center text-[11px]">
            <div className="bg-[#FBFBF9] p-2 rounded-lg border border-[#E5E5DF]">
              <span className="text-slate-400 block text-[10px]">P10 (Worst 10%)</span>
              <span className="font-bold text-slate-800">${(sim.prioritiq_schedule.p10_conservative / 1000).toFixed(0)}k</span>
            </div>
            <div className="bg-teal-50/50 p-2 rounded-lg border border-teal-200 text-teal-900">
              <span className="text-teal-600 block text-[10px] font-bold">P50 (Median)</span>
              <span className="font-bold text-teal-900">${(sim.prioritiq_schedule.p50_median / 1000).toFixed(0)}k</span>
            </div>
            <div className="bg-[#FBFBF9] p-2 rounded-lg border border-[#E5E5DF]">
              <span className="text-slate-400 block text-[10px]">P90 (Best 10%)</span>
              <span className="font-bold text-slate-800">${(sim.prioritiq_schedule.p90_optimistic / 1000).toFixed(0)}k</span>
            </div>
          </div>
          <div className="flex justify-between text-[11px] text-slate-500 pt-1">
            <span>Projected Closed Deals:</span>
            <strong className="text-slate-800">{sim.prioritiq_schedule.avg_deals_won} Deals</strong>
          </div>
        </div>

        {/* Legacy CRM Baseline */}
        <div className="p-4 rounded-xl bg-[#FBFBF9] border border-[#E5E5DF] shadow-xs space-y-3">
          <div className="flex items-center justify-between border-b border-slate-200 pb-2">
            <span className="font-bold text-slate-700 flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-slate-400"></span>
              Legacy Unprioritized CRM
            </span>
            <span className="text-[11px] text-slate-600 font-bold bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
              EV: ${sim.expected_revenue_baseline.toLocaleString()}
            </span>
          </div>

          <div className="grid grid-cols-3 gap-2 text-center text-[11px]">
            <div className="bg-white p-2 rounded-lg border border-[#E5E5DF]">
              <span className="text-slate-400 block text-[10px]">P10 (Worst 10%)</span>
              <span className="font-bold text-slate-600">${(sim.legacy_crm_baseline.p10_conservative / 1000).toFixed(0)}k</span>
            </div>
            <div className="bg-white p-2 rounded-lg border border-[#E5E5DF]">
              <span className="text-slate-400 block text-[10px]">P50 (Median)</span>
              <span className="font-bold text-slate-700">${(sim.legacy_crm_baseline.p50_median / 1000).toFixed(0)}k</span>
            </div>
            <div className="bg-white p-2 rounded-lg border border-[#E5E5DF]">
              <span className="text-slate-400 block text-[10px]">P90 (Best 10%)</span>
              <span className="font-bold text-slate-600">${(sim.legacy_crm_baseline.p90_optimistic / 1000).toFixed(0)}k</span>
            </div>
          </div>
          <div className="flex justify-between text-[11px] text-slate-500 pt-1">
            <span>Projected Closed Deals:</span>
            <strong className="text-slate-700">{sim.legacy_crm_baseline.avg_deals_won} Deals</strong>
          </div>
        </div>
      </div>

      {/* Probability Density Histogram */}
      <div className="space-y-2 pt-2">
        <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
          <span className="flex items-center gap-2">
            <BarChart3 size={14} className="text-teal-700" />
            Revenue Probability Density Distribution (1,000 Runs)
          </span>
          <div className="flex items-center gap-3 text-[11px] font-mono">
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded bg-teal-600"></span> PrioritiQ Schedule
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded bg-slate-300"></span> Baseline CRM
            </span>
          </div>
        </div>

        {/* Histogram Bars */}
        <div className="p-4 rounded-xl bg-white border border-[#E5E5DF] space-y-2">
          <div className="h-32 flex items-end gap-1.5 pt-4">
            {sim.distribution_buckets.map((bucket, idx) => {
              const optHeight = Math.round((bucket.prioritiq_density / maxDensity) * 100);
              const baseHeight = Math.round((bucket.baseline_density / maxDensity) * 100);
              return (
                <div key={idx} className="flex-1 flex flex-col justify-end items-center h-full group relative">
                  {/* Tooltip */}
                  <div className="absolute -top-10 bg-slate-900 text-white text-[10px] py-1 px-2 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-20 font-mono">
                    {bucket.label}: Opt {bucket.prioritiq_density} | Base {bucket.baseline_density}
                  </div>
                  <div className="w-full flex items-end justify-center gap-0.5 h-full">
                    {/* Baseline Bar */}
                    <div
                      style={{ height: `${baseHeight}%` }}
                      className="w-1/2 bg-slate-300 rounded-t transition-all group-hover:bg-slate-400"
                    ></div>
                    {/* PrioritiQ Bar */}
                    <div
                      style={{ height: `${optHeight}%` }}
                      className="w-1/2 bg-teal-600 rounded-t transition-all group-hover:bg-teal-500 shadow-xs"
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Histogram X Axis */}
          <div className="flex justify-between text-[10px] font-mono text-slate-400 border-t border-slate-100 pt-1.5">
            <span>${(sim.distribution_buckets[0]?.range_min / 1000).toFixed(0)}k</span>
            <span>Median Target (${(sim.prioritiq_schedule.p50_median / 1000).toFixed(0)}k)</span>
            <span>${(sim.distribution_buckets[sim.distribution_buckets.length - 1]?.range_max / 1000).toFixed(0)}k</span>
          </div>
        </div>
      </div>

      {/* Interactive Simulation Controls Slider */}
      <div className="pt-2 flex flex-wrap items-center justify-between gap-4 border-t border-slate-100 text-xs">
        <div className="flex items-center gap-3">
          <Sliders size={14} className="text-slate-500" />
          <span className="text-slate-600 font-semibold">Market Deal Volatility:</span>
          <input
            type="range"
            min="0.05"
            max="0.25"
            step="0.01"
            value={volatility}
            onChange={(e) => {
              const val = parseFloat(e.target.value);
              setVolatility(val);
              handleRerun(val);
            }}
            className="w-32 accent-teal-700 cursor-pointer h-1.5 bg-slate-200 rounded-lg"
          />
          <span className="font-mono text-slate-800 font-bold">±{(volatility * 100).toFixed(0)}%</span>
        </div>

        <button
          onClick={() => handleRerun(volatility)}
          disabled={running}
          className="px-3 py-1.5 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-800 font-bold border border-teal-200 flex items-center gap-1.5 transition-all text-xs shadow-xs"
        >
          <RefreshCw size={12} className={running ? 'animate-spin text-teal-700' : 'text-teal-700'} />
          <span>{running ? 'Simulating 1,000 Runs...' : 'Re-Run Simulation'}</span>
        </button>
      </div>
    </div>
  );
};
