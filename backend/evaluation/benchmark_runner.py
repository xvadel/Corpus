import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

BENCHMARK_FILE = PROJECT_ROOT / "backend" / "evaluation" / "benchmark_queries.json"

from backend.retrieval.retriever import VectorRetriever
from backend.evaluation.retrieval_metrics import evaluate_retrieval_dataset

def run_benchmark():
    print("=" * 70)
    print("CORPUS KNOWLEDGE ARCHITECTURE BENCHMARK RUNNER")
    print("=" * 70)

    # Load benchmark dataset
    with open(BENCHMARK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    all_queries = data["queries"]
    total = len(all_queries)
    print(f"\nLoaded {total} benchmark queries from benchmark_queries.json")
    print(f"  Easy  : {sum(1 for q in all_queries if q['tier'] == 'easy')}")
    print(f"  Medium: {sum(1 for q in all_queries if q['tier'] == 'medium')}")
    print(f"  Hard  : {sum(1 for q in all_queries if q['tier'] == 'hard')}")

    retriever = VectorRetriever()

    def print_metrics(metrics_1, metrics_3, metrics_5):
        print(f"    Recall@1 : {metrics_1['recall_at_k'] * 100:.1f}%")
        print(f"    Recall@3 : {metrics_3['recall_at_k'] * 100:.1f}%")
        print(f"    Recall@5 : {metrics_5['recall_at_k'] * 100:.1f}%")
        print(f"    MRR      : {metrics_5['mrr']:.4f}")

    def eval_pipeline(rerank: bool):
        pipeline_name = "VECTOR + CROSS-ENCODER RERANK" if rerank else "VECTOR RETRIEVAL ONLY"
        print(f"\nEvaluating: {pipeline_name}")
        print("-" * 50)

        easy   = [q for q in all_queries if q["tier"] == "easy"]
        medium = [q for q in all_queries if q["tier"] == "medium"]
        hard   = [q for q in all_queries if q["tier"] == "hard"]

        # Run tiers
        for tier_name, tier_queries in [("easy", easy), ("medium", medium), ("hard", hard)]:
            if not tier_queries:
                continue
            m1 = evaluate_retrieval_dataset(retriever, tier_queries, k=1, rerank=rerank)
            m3 = evaluate_retrieval_dataset(retriever, tier_queries, k=3, rerank=rerank)
            m5 = evaluate_retrieval_dataset(retriever, tier_queries, k=5, rerank=rerank)
            print(f"  [{tier_name.upper()} — {len(tier_queries)} queries]")
            print_metrics(m1, m3, m5)

        # Run overall
        m1_all = evaluate_retrieval_dataset(retriever, all_queries, k=1, rerank=rerank)
        m3_all = evaluate_retrieval_dataset(retriever, all_queries, k=3, rerank=rerank)
        m5_all = evaluate_retrieval_dataset(retriever, all_queries, k=5, rerank=rerank)
        print("\n  [OVERALL — all tiers combined]")
        print_metrics(m1_all, m3_all, m5_all)
        print("-" * 50)
        return {"m1": m1_all, "m3": m3_all, "m5": m5_all}

    # 1. Run Vector Retrieval Only
    v_results = eval_pipeline(rerank=False)

    # 2. Run Vector + Reranking
    r_results = eval_pipeline(rerank=True)

    # 3. Side-by-Side Summary
    print("\n" + "=" * 70)
    print("RECALL UPLIFT COMPARISON")
    print("=" * 70)
    print(f"{'Metric':<15} | {'Vector Only':<15} | {'Reranked':<15} | {'Delta':<10}")
    print("-" * 65)
    
    def print_delta(metric_name, v_val, r_val, is_pct=True):
        delta = r_val - v_val
        if is_pct:
            v_str = f"{v_val * 100:.1f}%"
            r_str = f"{r_val * 100:.1f}%"
            d_str = f"+{delta * 100:.1f}%" if delta >= 0 else f"{delta * 100:.1f}%"
        else:
            v_str = f"{v_val:.4f}"
            r_str = f"{r_val:.4f}"
            d_str = f"+{delta:.4f}" if delta >= 0 else f"{delta:.4f}"
        print(f"{metric_name:<15} | {v_str:<15} | {r_str:<15} | {d_str:<10}")

    print_delta("Recall@1", v_results["m1"]["recall_at_k"], r_results["m1"]["recall_at_k"])
    print_delta("Recall@3", v_results["m3"]["recall_at_k"], r_results["m3"]["recall_at_k"])
    print_delta("Recall@5", v_results["m5"]["recall_at_k"], r_results["m5"]["recall_at_k"])
    print_delta("MRR", v_results["m5"]["mrr"], r_results["m5"]["mrr"], is_pct=False)
    print("=" * 70)
    print("Benchmark completed!")

if __name__ == "__main__":
    run_benchmark()

