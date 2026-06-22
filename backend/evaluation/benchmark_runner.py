import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.retrieval.retriever import VectorRetriever
from backend.evaluation.retrieval_metrics import evaluate_retrieval_dataset
from backend.evaluation.generation_metrics import compute_relevancy
from backend.providers.gemini import GeminiProvider

# Phase 1 Evaluation Benchmark Dataset
BENCHMARK_DATASET = [
    {
        "query": "What is a mathematical representation of data in a high-dimensional space?",
        "ground_truth_id": "embedding",
        "reference_answer": "An embedding is a mathematical representation of data, like words or documents, as points in a high-dimensional vector space."
    },
    {
        "query": "AI framework that grounds LLM responses on external search sources to reduce hallucination.",
        "ground_truth_id": "retrieval_augmented_generation",
        "reference_answer": "Retrieval-Augmented Generation (RAG) is an AI framework that queries external databases to ground language models on verifiable sources."
    },
    {
        "query": "Specialized storage designed to perform fast similarity searches on high-dimensional vectors.",
        "ground_truth_id": "vector_database",
        "reference_answer": "A vector database is a specialized storage engine designed to run fast similarity searches (like cosine similarity) on multi-dimensional vectors."
    },
    {
        "query": "Splitting document text into smaller segments to fit within the context window.",
        "ground_truth_id": "chunking",
        "reference_answer": "Chunking is the process of breaking long documents into smaller segments to fit them within LLM context windows and keep retrieval precise."
    },
    {
        "query": "How can we direct-tune the preference model from human feedback without using RL agent training?",
        "ground_truth_id": "dpo",
        "reference_answer": "Direct Preference Optimization (DPO) directly optimizes the language model on binary human preferences without standard reinforcement learning actor-critic loops."
    },
    {
        "query": "Autonomous system that can plan tasks, use tools, and maintain state memory.",
        "ground_truth_id": "agent",
        "reference_answer": "An agent is an autonomous software system that can make decisions, use planning models, call APIs, and access context memory."
    }
]

def run_benchmark():
    print("=" * 60)
    print("CORPUS KNOWLEDGE ARCHITECTURE BENCHMARK RUNNER (PHASE 1)")
    print("=" * 60)
    
    # 1. Evaluate Retrieval
    print("\nRunning Retrieval Evaluation...")
    retriever = VectorRetriever()
    
    metrics_at_1 = evaluate_retrieval_dataset(retriever, BENCHMARK_DATASET, k=1)
    metrics_at_3 = evaluate_retrieval_dataset(retriever, BENCHMARK_DATASET, k=3)
    metrics_at_5 = evaluate_retrieval_dataset(retriever, BENCHMARK_DATASET, k=5)
    
    print("-" * 40)
    print(f"Recall@1: {metrics_at_1['recall_at_k'] * 100:.1f}%")
    print(f"Recall@3: {metrics_at_3['recall_at_k'] * 100:.1f}%")
    print(f"Recall@5: {metrics_at_5['recall_at_k'] * 100:.1f}%")
    print(f"MRR     : {metrics_at_5['mrr']:.4f}")
    print("-" * 40)
    
    # 2. Evaluate Generation Relevancy (if API Key is available)
    print("\nRunning Generation Relevancy Evaluation...")
    try:
        provider = GeminiProvider()
        
        relevancy_scores = []
        for i, item in enumerate(BENCHMARK_DATASET, 1):
            query = item["query"]
            ref_answer = item["reference_answer"]
            
            # Simple test answer to evaluate (we use reference answer itself as the test response)
            # You can also query the LLM to get a response, then score it
            test_response = provider.generate(f"Answer this query concisely: {query}")
            score = compute_relevancy(provider, query, test_response)
            relevancy_scores.append(score)
            
            print(f"  [{i}/{len(BENCHMARK_DATASET)}] Query: '{query[:40]}...'")
            print(f"      Response: '{test_response.strip()[:60]}...'")
            print(f"      Relevancy Score: {score:.2f}")
            
        avg_relevancy = sum(relevancy_scores) / len(relevancy_scores)
        print("-" * 40)
        print(f"Average Generation Relevancy: {avg_relevancy * 100:.1f}%")
        print("-" * 40)
        
    except Exception as e:
        print(f"Skipping Relevancy scoring: {e} (set GEMINI_API_KEY to run LLM-as-a-Judge evaluations)")
        
    print("\nBenchmark completed successfully!")

if __name__ == "__main__":
    run_benchmark()
