import uuid
from typing import List, Dict, Any
from ..models.schemas import DecisionGraphData, EvidenceNode, EvidenceEdge, LeadRecommendation

def construct_evidence_graph(
    decision_id: str,
    query: str,
    recommendations: List[LeadRecommendation],
    sim_state: Dict[str, Any]
) -> DecisionGraphData:
    nodes: List[EvidenceNode] = []
    edges: List[EvidenceEdge] = []

    # 1. Root Decision Node
    decision_node_id = f"decision_{decision_id[:8]}"
    nodes.append(EvidenceNode(
        id=decision_node_id,
        type="decision",
        label=f"Decision: {query[:45]}...",
        data={"query": query, "total_leads": len(recommendations)},
        confidence=1.0
    ))

    # 2. Constraint Node if present
    if sim_state.get("constrained"):
        constraint_id = f"constraint_{decision_id[:8]}"
        nodes.append(EvidenceNode(
            id=constraint_id,
            type="constraint",
            label=f"Constraint: {sim_state.get('time_budget_mins')} Mins Budget",
            data=sim_state,
            confidence=1.0
        ))
        edges.append(EvidenceEdge(
            id=str(uuid.uuid4())[:8],
            source=decision_node_id,
            target=constraint_id,
            relation="CONSTRAINED_BY"
        ))

    # 3. Add Lead Nodes and their respective Evidence & Action subtrees (top 4 in visual graph for clarity)
    for rec in recommendations[:5]:
        lead_node_id = f"lead_{rec.lead_id}"
        nodes.append(EvidenceNode(
            id=lead_node_id,
            type="lead",
            label=f"#{rec.rank} {rec.lead_name} ({rec.company_name})",
            data={
                "lead_id": rec.lead_id,
                "deal_size": rec.deal_size,
                "score": rec.composite_score,
                "stage": rec.stage,
                "effort_mins": rec.est_effort_mins
            },
            grounded_source=f"leads.csv:{rec.lead_id}",
            confidence=rec.composite_score / 100.0
        ))
        edges.append(EvidenceEdge(
            id=str(uuid.uuid4())[:8],
            source=decision_node_id,
            target=lead_node_id,
            relation="RECOMMENDS"
        ))

        # Metric Node
        metric_node_id = f"metric_{rec.lead_id}"
        nodes.append(EvidenceNode(
            id=metric_node_id,
            type="metric",
            label=f"Score: {rec.composite_score} | ${rec.deal_size:,.0f} | {rec.stage}",
            data={
                "score": rec.composite_score,
                "deal_size": rec.deal_size,
                "stage": rec.stage,
                "icp_fit": rec.icp_fit
            },
            grounded_source=f"leads.csv:{rec.lead_id}",
            confidence=1.0
        ))
        edges.append(EvidenceEdge(
            id=str(uuid.uuid4())[:8],
            source=lead_node_id,
            target=metric_node_id,
            relation="DERIVED_FROM"
        ))

        # RAG Qualitative Evidence Node
        if rec.grounded_evidence:
            ev = rec.grounded_evidence[0]
            rag_node_id = f"rag_{rec.lead_id}"
            nodes.append(EvidenceNode(
                id=rag_node_id,
                type="rag_evidence",
                label=f"Evidence: {ev.source_file}",
                data={
                    "quote": ev.quote,
                    "author": ev.author_or_actor,
                    "timestamp": ev.timestamp
                },
                grounded_source=f"notes/{ev.source_file}",
                confidence=0.98
            ))
            edges.append(EvidenceEdge(
                id=str(uuid.uuid4())[:8],
                source=lead_node_id,
                target=rag_node_id,
                relation="SUPPORTED_BY"
            ))

        # Suggested Action Node
        action_node_id = f"action_{rec.lead_id}"
        nodes.append(EvidenceNode(
            id=action_node_id,
            type="action",
            label=f"Action: {rec.suggested_action.get('type', 'Call')}",
            data=rec.suggested_action,
            confidence=1.0
        ))
        edges.append(EvidenceEdge(
            id=str(uuid.uuid4())[:8],
            source=lead_node_id,
            target=action_node_id,
            relation="TRIGGERS"
        ))

    return DecisionGraphData(nodes=nodes, edges=edges)
