import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.retrieval.retriever import VectorRetriever
from backend.retrieval.context_builder import ContextBuilder

def test_vector_retriever():
    print("Testing VectorRetriever...")
    retriever = VectorRetriever()
    
    # Query for something relevant
    query = "What is Retrieval Augmented Generation?"
    results = retriever.retrieve(query, limit=3)
    
    assert len(results) > 0, "No results retrieved"
    
    print(f"Retrieved {len(results)} results for query: '{query}'")
    for r in results:
        print(f"  - {r['id']} (distance: {r['distance']:.4f})")
        assert "id" in r
        assert "metadata" in r
        assert "document" in r
        
    # Test context builder
    context = ContextBuilder.build_context(results)
    assert len(context) > 0
    print("\nFormatted Context:")
    print(context)
    
    # Test metadata filtering
    print("\nTesting metadata filtering (subdomain: Agentic AI)...")
    filtered_results = retriever.retrieve("agent planning", limit=3, where={"subdomain": "Agentic AI"})
    for r in filtered_results:
        print(f"  - {r['id']} (subdomain: {r['metadata']['subdomain']})")
        assert r["metadata"]["subdomain"] == "Agentic AI"

    # Test reranking
    print("\nTesting reranking...")
    reranked_results = retriever.retrieve("What is RAG?", limit=3, rerank=True)
    assert len(reranked_results) > 0
    print("Reranked results:")
    for r in reranked_results:
        print(f"  - {r['id']} (rerank score: {r.get('rerank_score'):.4f})")
        assert "rerank_score" in r

if __name__ == "__main__":
    test_vector_retriever()
    print("\nAll retriever tests passed!")

