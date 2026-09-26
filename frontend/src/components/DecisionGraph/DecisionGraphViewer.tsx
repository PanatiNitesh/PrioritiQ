import React, { useState, useEffect, useRef, useMemo } from 'react';
import { DecisionGraphData, EvidenceNode, EvidenceEdge } from '../../types';
import { Network, ShieldCheck, Database, FileText, CheckCircle2, Sliders, ChevronDown, ChevronUp, Eye } from 'lucide-react';

interface Props {
  graphData: DecisionGraphData;
  onSelectNode?: (node: EvidenceNode) => void;
}

interface EdgeCoordinate {
  id: string;
  source: string;
  target: string;
  relation: string;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export const DecisionGraphViewer: React.FC<Props> = ({ graphData, onSelectNode }) => {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);
  const [showAllNodes, setShowAllNodes] = useState<boolean>(false);
  const [activeEdgeFilter, setActiveEdgeFilter] = useState<string | null>(null);

  const containerRef = useRef<HTMLDivElement>(null);
  const nodeRefs = useRef<Map<string, HTMLDivElement>>(new Map());
  const [edgeCoords, setEdgeCoords] = useState<EdgeCoordinate[]>([]);

  const nodes = graphData.nodes || [];
  const edges = graphData.edges || [];

  // Group nodes by columns
  const decisionNodes = useMemo(() => nodes.filter(n => n.type === 'decision' || n.type === 'constraint'), [nodes]);
  const leadNodes = useMemo(() => nodes.filter(n => n.type === 'lead'), [nodes]);
  const ragNodes = useMemo(() => nodes.filter(n => n.type === 'rag_evidence'), [nodes]);
  const actionNodes = useMemo(() => nodes.filter(n => n.type === 'action'), [nodes]);

  const displayedLeads = showAllNodes ? leadNodes : leadNodes.slice(0, 5);
  const displayedRags = showAllNodes ? ragNodes : ragNodes.slice(0, 5);
  const displayedActions = showAllNodes ? actionNodes : actionNodes.slice(0, 5);

  // Recalculate SVG edge coordinates when nodes mount or window resizes
  const updateEdgeCoordinates = () => {
    if (!containerRef.current) return;
    const containerRect = containerRef.current.getBoundingClientRect();
    const coords: EdgeCoordinate[] = [];

    edges.forEach((edge) => {
      const srcEl = nodeRefs.current.get(edge.source);
      const tgtEl = nodeRefs.current.get(edge.target);

      if (srcEl && tgtEl) {
        const srcRect = srcEl.getBoundingClientRect();
        const tgtRect = tgtEl.getBoundingClientRect();

        // Source right-center anchor
        const x1 = srcRect.right - containerRect.left;
        const y1 = srcRect.top + srcRect.height / 2 - containerRect.top;

        // Target left-center anchor
        const x2 = tgtRect.left - containerRect.left;
        const y2 = tgtRect.top + tgtRect.height / 2 - containerRect.top;

        coords.push({
          id: edge.id || `${edge.source}->${edge.target}`,
          source: edge.source,
          target: edge.target,
          relation: edge.relation,
          x1,
          y1,
          x2,
          y2
        });
      }
    });

    setEdgeCoords(coords);
  };

  useEffect(() => {
    // Delay slightly to let DOM layout settle
    const timer = setTimeout(updateEdgeCoordinates, 80);
    window.addEventListener('resize', updateEdgeCoordinates);
    return () => {
      clearTimeout(timer);
      window.removeEventListener('resize', updateEdgeCoordinates);
    };
  }, [graphData, showAllNodes, hoveredNodeId, selectedNodeId]);

  const handleNodeClick = (node: EvidenceNode) => {
    setSelectedNodeId(node.id === selectedNodeId ? null : node.id);
    if (onSelectNode) onSelectNode(node);
  };

  const selectedNode = nodes.find(n => n.id === selectedNodeId);

  // Helper to check if an edge is active
  const isEdgeActive = (edge: EdgeCoordinate) => {
    const activeNode = hoveredNodeId || selectedNodeId;
    if (!activeNode && !activeEdgeFilter) return true;
    if (activeEdgeFilter && edge.relation !== activeEdgeFilter) return false;
    if (activeNode) {
      return edge.source === activeNode || edge.target === activeNode;
    }
    return true;
  };

  const isEdgeHighlighted = (edge: EdgeCoordinate) => {
    const activeNode = hoveredNodeId || selectedNodeId;
    if (!activeNode) return false;
    return edge.source === activeNode || edge.target === activeNode;
  };

  const getNodeIcon = (type: string) => {
    switch (type) {
      case 'decision': return <Network size={14} className="text-teal-700" />;
      case 'constraint': return <Sliders size={14} className="text-amber-600" />;
      case 'lead': return <ShieldCheck size={14} className="text-emerald-700" />;
      case 'metric': return <Database size={14} className="text-sky-600" />;
      case 'rag_evidence': return <FileText size={14} className="text-purple-600" />;
      case 'action': return <CheckCircle2 size={14} className="text-amber-700" />;
      default: return <Network size={14} />;
    }
  };

  const getNodeStyle = (type: string, nodeId: string) => {
    const isSelected = selectedNodeId === nodeId;
    const isHovered = hoveredNodeId === nodeId;
    const isConnected = hoveredNodeId
      ? edges.some(e => (e.source === hoveredNodeId && e.target === nodeId) || (e.target === hoveredNodeId && e.source === nodeId))
      : false;

    if (isSelected) return 'ring-2 ring-teal-700 bg-white border-teal-700 shadow-md scale-[1.02] z-20';
    if (isHovered) return 'ring-2 ring-teal-600 bg-white border-teal-600 shadow-sm scale-[1.01] z-20';
    if (isConnected) return 'ring-1.5 ring-emerald-500 bg-emerald-50/40 border-emerald-400 z-10';

    switch (type) {
      case 'decision': return 'bg-white border-l-4 border-l-teal-700 border-[#E5E5DF] text-slate-900 hover:border-slate-300';
      case 'constraint': return 'bg-white border-l-4 border-l-amber-600 border-[#E5E5DF] text-slate-900 hover:border-slate-300';
      case 'lead': return 'bg-white border-l-4 border-l-emerald-600 border-[#E5E5DF] text-slate-900 hover:border-slate-300';
      case 'metric': return 'bg-white border-l-4 border-l-sky-500 border-[#E5E5DF] text-slate-900 hover:border-slate-300';
      case 'rag_evidence': return 'bg-white border-l-4 border-l-purple-600 border-[#E5E5DF] text-slate-900 hover:border-slate-300';
      case 'action': return 'bg-white border-l-4 border-l-amber-600 border-[#E5E5DF] text-slate-900 hover:border-slate-300';
      default: return 'bg-white border-[#E5E5DF] text-slate-900';
    }
  };

  const relationCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    edges.forEach(e => {
      counts[e.relation] = (counts[e.relation] || 0) + 1;
    });
    return counts;
  }, [edges]);

  return (
    <div className="pq-card p-6 border-[#E5E5DF] space-y-4">
      {/* Header bar */}
      <div className="flex flex-wrap items-center justify-between pb-4 border-b border-[#F4F4F0] gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-teal-50 text-teal-800 border border-teal-200">
            <Network size={18} />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">Interactive Explainability DAG</h3>
            <p className="text-xs text-slate-500">
              {nodes.length} Nodes • {edges.length} Directed Grounded Edges (Hover to trace lineage)
            </p>
          </div>
        </div>

        {/* Edge Relation Filters / Legend */}
        <div className="flex flex-wrap items-center gap-2 text-xs font-semibold">
          <button
            onClick={() => setActiveEdgeFilter(null)}
            className={`px-2 py-0.5 rounded text-[11px] font-mono transition-colors ${
              !activeEdgeFilter ? 'bg-teal-700 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            All ({edges.length})
          </button>
          {Object.entries(relationCounts).map(([rel, count]) => (
            <button
              key={rel}
              onClick={() => setActiveEdgeFilter(activeEdgeFilter === rel ? null : rel)}
              className={`px-2 py-0.5 rounded text-[10px] font-mono transition-colors ${
                activeEdgeFilter === rel
                  ? 'bg-teal-700 text-white'
                  : 'bg-white text-slate-600 border border-[#E5E5DF] hover:border-slate-300'
              }`}
            >
              {rel} ({count})
            </button>
          ))}
          <button
            onClick={() => setShowAllNodes(!showAllNodes)}
            className="ml-2 px-2 py-0.5 rounded text-[11px] font-semibold text-teal-800 bg-teal-50 border border-teal-200 hover:bg-teal-100 flex items-center gap-1"
          >
            <Eye size={12} />
            {showAllNodes ? 'Compact View' : `Show All (${nodes.length})`}
          </button>
        </div>
      </div>

      {/* Relative Canvas Container with SVG Connectors */}
      <div ref={containerRef} className="relative min-h-[300px] py-2">
        {/* SVG Directed Edge Layer (Weakness 11) */}
        <svg
          className="absolute inset-0 w-full h-full pointer-events-none z-0"
          style={{ minHeight: '100%' }}
        >
          <defs>
            <marker
              id="arrow-teal"
              viewBox="0 0 10 10"
              refX="8"
              refY="5"
              markerWidth="6"
              markerHeight="6"
              orient="auto-start-reverse"
            >
              <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0F766E" />
            </marker>
            <marker
              id="arrow-muted"
              viewBox="0 0 10 10"
              refX="8"
              refY="5"
              markerWidth="5"
              markerHeight="5"
              orient="auto-start-reverse"
            >
              <path d="M 0 2 L 6 5 L 0 8 z" fill="#CBD5E1" />
            </marker>
            <marker
              id="arrow-amber"
              viewBox="0 0 10 10"
              refX="8"
              refY="5"
              markerWidth="6"
              markerHeight="6"
              orient="auto-start-reverse"
            >
              <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#D97706" />
            </marker>
          </defs>

          {edgeCoords.map((edge) => {
            const isHighlighted = isEdgeHighlighted(edge);
            const isActive = isEdgeActive(edge);
            if (!isActive && !isHighlighted) return null;

            const dx = Math.abs(edge.x2 - edge.x1) * 0.45;
            const pathD = `M ${edge.x1} ${edge.y1} C ${edge.x1 + dx} ${edge.y1}, ${edge.x2 - dx} ${edge.y2}, ${edge.x2} ${edge.y2}`;

            const strokeColor = isHighlighted
              ? edge.relation === 'TRIGGERS' ? '#D97706' : '#0F766E'
              : '#E2E8F0';
            const strokeWidth = isHighlighted ? 2.5 : 1.2;
            const marker = isHighlighted
              ? edge.relation === 'TRIGGERS' ? 'url(#arrow-amber)' : 'url(#arrow-teal)'
              : 'url(#arrow-muted)';
            const opacity = isHighlighted ? 1.0 : (hoveredNodeId || selectedNodeId ? 0.2 : 0.65);

            return (
              <g key={edge.id}>
                <path
                  d={pathD}
                  stroke={strokeColor}
                  strokeWidth={strokeWidth}
                  fill="none"
                  markerEnd={marker}
                  strokeDasharray={edge.relation === 'CONSTRAINED_BY' ? '4,3' : 'none'}
                  opacity={opacity}
                  className="transition-all duration-200"
                />
              </g>
            );
          })}
        </svg>

        {/* 4 Columns Node Layout */}
        <div className="relative z-10 grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Column 1: Policy / Decision */}
          <div className="flex flex-col gap-3 justify-center">
            <span className="text-[10px] uppercase font-mono tracking-wider text-teal-800 font-bold px-1 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-teal-700"></span> Policy & Goals
            </span>
            {decisionNodes.map((node) => (
              <div
                key={node.id}
                ref={(el) => { if (el) nodeRefs.current.set(node.id, el); }}
                onClick={() => handleNodeClick(node)}
                onMouseEnter={() => setHoveredNodeId(node.id)}
                onMouseLeave={() => setHoveredNodeId(null)}
                className={`p-3.5 rounded-xl border cursor-pointer transition-all shadow-xs ${getNodeStyle(node.type, node.id)}`}
              >
                <div className="flex items-center gap-2 mb-1.5">
                  {getNodeIcon(node.type)}
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-700">{node.type}</span>
                </div>
                <p className="text-xs font-bold text-slate-900 line-clamp-2">{node.label}</p>
              </div>
            ))}
          </div>

          {/* Column 2: Selected Accounts */}
          <div className="flex flex-col gap-2.5">
            <span className="text-[10px] uppercase font-mono tracking-wider text-emerald-800 font-bold px-1 flex items-center justify-between">
              <span className="flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span> Selected Accounts
              </span>
              <span className="font-mono text-[9px] text-slate-400">{displayedLeads.length} of {leadNodes.length}</span>
            </span>
            {displayedLeads.map((node) => (
              <div
                key={node.id}
                ref={(el) => { if (el) nodeRefs.current.set(node.id, el); }}
                onClick={() => handleNodeClick(node)}
                onMouseEnter={() => setHoveredNodeId(node.id)}
                onMouseLeave={() => setHoveredNodeId(null)}
                className={`p-3 rounded-xl border cursor-pointer transition-all shadow-xs ${getNodeStyle(node.type, node.id)}`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold text-slate-900 truncate">{node.label}</span>
                  <span className="text-[10px] font-mono font-bold text-emerald-800 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
                    ${(node.data?.deal_size || 0).toLocaleString()}
                  </span>
                </div>
                <div className="flex items-center justify-between text-[11px] text-slate-600">
                  <span>Stage: <strong className="text-slate-800">{node.data?.stage}</strong></span>
                  <span className="font-mono font-bold text-teal-700">Score: {node.data?.score}</span>
                </div>
              </div>
            ))}
          </div>

          {/* Column 3: Grounded Evidence */}
          <div className="flex flex-col gap-2.5">
            <span className="text-[10px] uppercase font-mono tracking-wider text-purple-800 font-bold px-1 flex items-center justify-between">
              <span className="flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-purple-600"></span> Grounded Evidence
              </span>
              <span className="font-mono text-[9px] text-slate-400">{displayedRags.length} of {ragNodes.length}</span>
            </span>
            {displayedRags.map((node) => (
              <div
                key={node.id}
                ref={(el) => { if (el) nodeRefs.current.set(node.id, el); }}
                onClick={() => handleNodeClick(node)}
                onMouseEnter={() => setHoveredNodeId(node.id)}
                onMouseLeave={() => setHoveredNodeId(null)}
                className={`p-3 rounded-xl border cursor-pointer transition-all shadow-xs ${getNodeStyle(node.type, node.id)}`}
              >
                <div className="flex items-center gap-1.5 text-xs text-purple-900 font-bold mb-1">
                  <FileText size={12} className="text-purple-600" />
                  <span className="truncate">{node.label}</span>
                </div>
                <p className="text-[11px] text-slate-700 italic line-clamp-2">
                  "{node.data?.quote || 'Verified evidence from call transcripts and email redlines.'}"
                </p>
                <div className="mt-1 text-[10px] font-mono text-slate-500">
                  {node.data?.author || 'Sales Team'} • {node.data?.timestamp || 'Today'}
                </div>
              </div>
            ))}
          </div>

          {/* Column 4: Dispatched Actions */}
          <div className="flex flex-col gap-2.5">
            <span className="text-[10px] uppercase font-mono tracking-wider text-amber-800 font-bold px-1 flex items-center justify-between">
              <span className="flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-600"></span> Dispatched Actions
              </span>
              <span className="font-mono text-[9px] text-slate-400">{displayedActions.length} of {actionNodes.length}</span>
            </span>
            {displayedActions.map((node) => (
              <div
                key={node.id}
                ref={(el) => { if (el) nodeRefs.current.set(node.id, el); }}
                onClick={() => handleNodeClick(node)}
                onMouseEnter={() => setHoveredNodeId(node.id)}
                onMouseLeave={() => setHoveredNodeId(null)}
                className={`p-3 rounded-xl border cursor-pointer transition-all shadow-xs ${getNodeStyle(node.type, node.id)}`}
              >
                <div className="flex items-center gap-1.5 text-xs text-amber-950 font-bold mb-1">
                  <CheckCircle2 size={12} className="text-amber-700" />
                  <span className="truncate">{node.data?.type || 'Execution'}</span>
                </div>
                <p className="text-[11px] text-slate-800 line-clamp-2 font-medium">
                  {node.data?.title || 'Dispatch CRM task and follow-up'}
                </p>
                <span className="inline-block mt-1 text-[10px] font-mono bg-amber-50 text-amber-800 font-bold px-1.5 py-0.5 rounded border border-amber-200">
                  Due: {node.data?.due_date || 'Today 17:00'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Selected Node Inspector Drawer */}
      {selectedNode && (
        <div className="p-4 rounded-xl bg-[#FBFBF9] border border-teal-200 flex flex-wrap items-center justify-between gap-3 text-xs shadow-xs animate-in fade-in duration-150">
          <div className="flex items-center gap-2.5">
            <span className="px-2.5 py-0.5 rounded-md text-[10px] font-mono uppercase bg-teal-100 text-teal-800 font-bold">
              {selectedNode.type}
            </span>
            <span className="font-bold text-slate-900">{selectedNode.label}</span>
            {selectedNode.grounded_source && (
              <span className="text-slate-500 font-mono text-[11px]">
                Proven Source: <span className="text-teal-800 font-bold">{selectedNode.grounded_source}</span>
              </span>
            )}
          </div>
          <div className="flex items-center gap-3">
            <span className="text-slate-600 font-medium">
              Grounding: <strong className="text-emerald-700 font-mono font-bold">{(selectedNode.confidence * 100).toFixed(0)}% Fact-Checked</strong>
            </span>
            <button
              onClick={() => setSelectedNodeId(null)}
              className="text-slate-600 hover:text-slate-900 px-2.5 py-0.5 rounded bg-white border border-[#D4D4D8] shadow-xs font-semibold"
            >
              Close Inspector
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
