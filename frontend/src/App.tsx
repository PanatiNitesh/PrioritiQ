import React, { useState } from 'react';
import { Dashboard } from './pages/Dashboard';
import { Decisions } from './pages/Decisions';
import { Leads } from './pages/Leads';
import { DecisionDetail } from './pages/DecisionDetail';
import { DataSourcesModal } from './components/DataSources/DataSourcesModal';
import {
  Compass,
  FileCheck2,
  Users2,
  Database,
  Sparkles,
  Layers,
  ShieldCheck
} from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'decisions' | 'leads' | 'detail'>('dashboard');
  const [selectedDecisionId, setSelectedDecisionId] = useState<string | null>(null);
  const [showDataSources, setShowDataSources] = useState(false);

  const navigateToDetail = (id: string) => {
    setSelectedDecisionId(id);
    setActiveTab('detail');
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#FBFBF9] text-[#18181B]">
      {/* Top PrioritiQ Command Navigation */}
      <header className="sticky top-0 z-40 bg-[#FFFFFF]/95 backdrop-blur-md border-b border-[#E5E5DF] px-6 py-3 shadow-[0_1px_4px_rgba(0,0,0,0.02)]">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo & Product Monogram */}
          <div
            onClick={() => setActiveTab('dashboard')}
            className="flex items-center gap-3.5 cursor-pointer group"
          >
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-teal-700 via-teal-600 to-emerald-600 flex items-center justify-center shadow-md shadow-teal-900/10 group-hover:scale-105 transition-all">
              <span className="font-mono font-black text-white text-sm tracking-tighter">PQ</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-base tracking-tight text-slate-900 group-hover:text-teal-700 transition-colors">
                  PrioritiQ
                </span>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono uppercase bg-teal-50 text-teal-800 border border-teal-200 font-bold">
                  Decision Engine
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium hidden sm:block">
                Evidence-Grounded AI Sales Prioritization
              </p>
            </div>
          </div>

          {/* Center Navigation Tabs */}
          <nav className="flex items-center p-1 bg-[#F4F4F0] rounded-xl border border-[#E5E5DF] text-xs">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`px-3.5 py-1.5 rounded-lg font-semibold flex items-center gap-1.5 transition-all ${
                activeTab === 'dashboard'
                  ? 'bg-white text-teal-800 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Compass size={14} className={activeTab === 'dashboard' ? 'text-teal-700' : 'text-slate-400'} />
              <span>Workspace</span>
            </button>

            <button
              onClick={() => setActiveTab('decisions')}
              className={`px-3.5 py-1.5 rounded-lg font-semibold flex items-center gap-1.5 transition-all ${
                activeTab === 'decisions'
                  ? 'bg-white text-teal-800 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <FileCheck2 size={14} className={activeTab === 'decisions' ? 'text-teal-700' : 'text-slate-400'} />
              <span>Audit Ledger</span>
            </button>

            <button
              onClick={() => setActiveTab('leads')}
              className={`px-3.5 py-1.5 rounded-lg font-semibold flex items-center gap-1.5 transition-all ${
                activeTab === 'leads'
                  ? 'bg-white text-teal-800 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Users2 size={14} className={activeTab === 'leads' ? 'text-teal-700' : 'text-slate-400'} />
              <span>Pipeline & Leads</span>
            </button>

            <button
              onClick={() => setShowDataSources(true)}
              className="px-3.5 py-1.5 rounded-lg font-semibold text-slate-600 hover:text-slate-900 flex items-center gap-1.5 transition-all"
            >
              <Database size={14} className="text-slate-400" />
              <span className="hidden sm:inline">Data & RAG Docs</span>
            </button>
          </nav>

          {/* Right Status & Persona */}
          <div className="flex items-center gap-3">
            <div className="hidden md:flex flex-col text-right">
              <span className="text-xs font-bold text-slate-900">Sales Manager</span>
              <span className="text-[10px] font-mono text-emerald-700 flex items-center justify-end gap-1 font-semibold">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                RAG Vector DB Active
              </span>
            </div>
            <div className="w-8 h-8 rounded-full bg-teal-50 border border-teal-200 text-teal-800 flex items-center justify-center text-xs font-bold shadow-inner">
              SM
            </div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        {activeTab === 'dashboard' && (
          <Dashboard
            onOpenDataSources={() => setShowDataSources(true)}
            onNavigateDetail={navigateToDetail}
          />
        )}
        {activeTab === 'decisions' && (
          <Decisions onSelectDecision={navigateToDetail} />
        )}
        {activeTab === 'leads' && <Leads />}
        {activeTab === 'detail' && selectedDecisionId && (
          <DecisionDetail
            decisionId={selectedDecisionId}
            onBack={() => setActiveTab('dashboard')}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-[#E5E5DF] bg-white/70 py-4 text-center text-xs text-slate-500 font-mono">
        <p>PrioritiQ • Deterministic Analytics + RAG Knowledge Vector Layer + Multi-Agent Orchestration + Human Governance</p>
      </footer>

      {/* Data Sources Inspector Modal */}
      <DataSourcesModal
        isOpen={showDataSources}
        onClose={() => setShowDataSources(false)}
      />
    </div>
  );
};
