import pytest
from backend.rag.retrieval import query_unstructured_knowledge
from backend.rag.embeddings import rag_index

def test_rag_semantic_retrieval_accuracy():
    """
    RAG Benchmark evaluation:
    Tests semantic retrieval against ground-truth queries to measure Recall@K and MRR.
    """
    assert len(rag_index.chunks) > 0, "RAG index must contain indexed chunks"

    benchmark_queries = [
        {"query": "indemnification clause section 9.2 mutual liability", "expected_keyword": "indemnif"},
        {"query": "SOC2 clearance Type II executive briefing", "expected_keyword": "soc2"},
        {"query": "HIPAA BAA hospital network clinical compliance", "expected_keyword": "hipaa"},
        {"query": "CapEx surplus deadline Friday procurement", "expected_keyword": "capex"}
    ]

    hits = 0
    reciprocal_ranks = []

    for item in benchmark_queries:
        results = query_unstructured_knowledge(item["query"], top_k=4)
        found_rank = None
        for rank, res in enumerate(results, start=1):
            if item["expected_keyword"].lower() in res["content"].lower():
                found_rank = rank
                break

        if found_rank is not None:
            hits += 1
            reciprocal_ranks.append(1.0 / found_rank)
        else:
            reciprocal_ranks.append(0.0)

    recall_at_4 = hits / len(benchmark_queries)
    mrr = sum(reciprocal_ranks) / len(benchmark_queries)

    assert recall_at_4 >= 0.75, f"Recall@4 {recall_at_4} is below threshold 0.75"
    assert mrr >= 0.70, f"MRR {mrr} is below threshold 0.70"
