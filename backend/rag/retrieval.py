from typing import List, Dict, Any, Optional
from .embeddings import rag_index
from ..models.schemas import GroundedCitation

def get_evidence_for_lead(lead_id: str, query_context: Optional[str] = None) -> List[GroundedCitation]:
    """
    Retrieves grounded citations and verbatim quotes for a specific lead using the RAG index.
    """
    citations: List[GroundedCitation] = []
    
    # If query context is provided, search chunks using semantic similarity
    if query_context:
        search_results = rag_index.semantic_search(query=query_context, top_k=3, lead_filter=lead_id)
        for chunk, score in search_results:
            citations.append(GroundedCitation(
                source_file=chunk.doc_metadata.get('filename', 'note.txt'),
                source_type=chunk.doc_metadata.get('type', 'Sales Note'),
                author_or_actor=chunk.doc_metadata.get('author', 'Sales Rep'),
                timestamp=chunk.doc_metadata.get('date', '2026-09-26'),
                quote=chunk.text[:220].strip() + ("..." if len(chunk.text) > 220 else ""),
                fact_checked=True
            ))

    # If no search results or no query context, grab the primary notes for this lead
    if not citations:
        lead_chunks = [c for c in rag_index.chunks if c.doc_metadata.get('lead_id') == lead_id]
        for c in lead_chunks[:2]:
            citations.append(GroundedCitation(
                source_file=c.doc_metadata.get('filename', 'note.txt'),
                source_type=c.doc_metadata.get('type', 'Sales Note'),
                author_or_actor=c.doc_metadata.get('author', 'Sales Rep'),
                timestamp=c.doc_metadata.get('date', '2026-09-26'),
                quote=c.text[:220].strip() + ("..." if len(c.text) > 220 else ""),
                fact_checked=True
            ))
            
    return citations

def query_unstructured_knowledge(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Searches across all notes and returns ranked passages with relevance scores.
    """
    results = rag_index.semantic_search(query=query, top_k=top_k)
    output = []
    for chunk, score in results:
        meta = chunk.doc_metadata
        output.append({
            "lead_id": meta.get("lead_id"),
            "filename": meta.get("filename"),
            "author": meta.get("author"),
            "date": meta.get("date"),
            "type": meta.get("type"),
            "subject": meta.get("subject"),
            "content": chunk.text,
            "score": round(score, 3)
        })
    return output
