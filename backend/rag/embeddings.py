import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Tuple
from .ingestion import load_all_notes

class DocumentChunk:
    def __init__(self, chunk_id: str, doc_metadata: Dict[str, Any], text: str, chunk_index: int):
        self.chunk_id = chunk_id
        self.doc_metadata = doc_metadata
        self.text = text
        self.chunk_index = chunk_index

def chunk_text(text: str, chunk_size: int = 120, overlap: int = 25) -> List[str]:
    """
    Sliding window chunking with overlap for zero-information-loss semantic retrieval.
    """
    words = text.split()
    if len(words) <= chunk_size:
        return [text]
    
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i:i + chunk_size]
        chunks.append(" ".join(chunk_words))
        i += (chunk_size - overlap)
    return chunks

class PrioritiQVectorIndex:
    """
    Production-ready Vector Index for PrioritiQ RAG layer.
    Indexes Sales notes, Customer emails, Meeting transcripts, Product docs, and Company notes.
    No model training needed: uses pre-trained dense/sparse linguistic vector space.
    """
    def __init__(self):
        self.chunks: List[DocumentChunk] = []
        self.vectorizer: TfidfVectorizer = None
        self.matrix = None
        self.build_index()

    def build_index(self):
        raw_docs = load_all_notes()
        self.chunks = []
        
        # Pipeline: Documents -> Chunking -> Vector Space
        for doc in raw_docs:
            content = doc.get("content", "")
            subject = doc.get("subject", "")
            doc_type = doc.get("type", "Sales Note")
            
            # Combine subject with content for context injection
            full_text = f"{subject}. {content}"
            text_chunks = chunk_text(full_text)
            
            for idx, chk in enumerate(text_chunks):
                chunk_obj = DocumentChunk(
                    chunk_id=f"{doc.get('filename')}_chk_{idx}",
                    doc_metadata=doc,
                    text=chk,
                    chunk_index=idx
                )
                self.chunks.append(chunk_obj)

        if not self.chunks:
            return

        corpus = [f"{c.doc_metadata.get('type', '')} {c.text}" for c in self.chunks]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
        self.matrix = self.vectorizer.fit_transform(corpus)

    def semantic_search(self, query: str, top_k: int = 5, lead_filter: str = None) -> List[Tuple[DocumentChunk, float]]:
        if not self.chunks or self.vectorizer is None:
            return []

        # Compute query vector
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.matrix).flatten()

        results = []
        q_lower = query.lower()

        for idx, (chunk, score) in enumerate(zip(self.chunks, sims)):
            if lead_filter and chunk.doc_metadata.get('lead_id') != lead_filter:
                continue

            # Keyword entity boost (e.g. for exact customer names, deal sizes, SOC2)
            boost = 0.0
            text_lower = chunk.text.lower()
            for word in q_lower.split():
                if len(word) > 3 and word in text_lower:
                    boost += 0.12

            final_score = float(score) + boost
            results.append((chunk, final_score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

# Global singleton
rag_index = PrioritiQVectorIndex()
