from typing import List, Dict, Any, Optional
from ..rag.retrieval import get_evidence_for_lead, query_unstructured_knowledge
from ..models.schemas import GroundedCitation

class RetrievalAgent:
    """
    RAG Agent responsible for extracting grounded qualitative evidence,
    verbatim quotes, and contextual caveats from emails, transcripts, and notes.
    """
    def __init__(self):
        pass

    def retrieve_lead_evidence(self, lead_id: str, query_context: Optional[str] = None) -> List[GroundedCitation]:
        return get_evidence_for_lead(lead_id=lead_id, query_context=query_context)

    def search_unstructured_signals(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        return query_unstructured_knowledge(query=query, top_k=top_k)
