import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

BENCHMARK_FILE = PROJECT_ROOT / "backend" / "evaluation" / "benchmark_queries.json"

from backend.retrieval.retriever import VectorRetriever
from backend.evaluation.retrieval_metrics import evaluate_all_ks


def run_benchmark():
    print("=" * 70)
    print("CORPUS KNOWLEDGE ARCHITECTURE BENCHMARK RUNNER")
    print("=" * 70)

    with open(BENCHMARK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    all_queries = data["queries"]
    total = len(all_queries)
    easy_n   = sum(1 for q in all_queries if q["tier"] == "easy")
    medium_n = sum(1 for q in all_queries if q["tier"] == "medium")
    hard_n   = sum(1 for q in all_queries if q["tier"] == "hard")
    print(f"\nLoaded {total} queries  (Easy: {easy_n}  Medium: {medium_n}  Hard: {hard_n})")

    retriever = VectorRetriever()
    KS = [1, 3, 5]

    def run_pipeline(rerank: bool) -> dict:
        label = "VECTOR + CROSS-ENCODER RERANK" if rerank else "VECTOR ONLY"
        print(f"\n{'-'*70}")
        print(f"  Pipeline: {label}")
        print(f"{'-'*70}")

        easy   = [q for q in all_queries if q["tier"] == "easy"]
        medium = [q for q in all_queries if q["tier"] == "medium"]
        hard   = [q for q in all_queries if q["tier"] == "hard"]

        for tier_name, tier_qs in [("easy", easy), ("medium", medium), ("hard", hard)]:
            print(f"\n  [{tier_name.upper()} - {len(tier_qs)} queries]", flush=True)
            m = evaluate_all_ks(retriever, tier_qs, ks=KS, verbose=True, rerank=rerank)
            print(f"    Recall@1={m['recall@1']*100:.1f}%  "
                  f"Recall@3={m['recall@3']*100:.1f}%  "
                  f"Recall@5={m['recall@5']*100:.1f}%  "
                  f"MRR={m['mrr']:.4f}")

        print(f"\n  [OVERALL - {total} queries]", flush=True)
        m_all = evaluate_all_ks(retriever, all_queries, ks=KS, rerank=rerank)
        print(f"    Recall@1={m_all['recall@1']*100:.1f}%  "
              f"Recall@3={m_all['recall@3']*100:.1f}%  "
              f"Recall@5={m_all['recall@5']*100:.1f}%  "
              f"MRR={m_all['mrr']:.4f}")
        return m_all

    # Run both pipelines
    v = run_pipeline(rerank=False)
    r = run_pipeline(rerank=True)

    # Side-by-side uplift table
    print(f"\n{'='*70}")
    print("RECALL UPLIFT: VECTOR ONLY  ->  VECTOR + CROSS-ENCODER RERANK")
    print(f"{'='*70}")
    print(f"{'Metric':<12} | {'Vector Only':>12} | {'Reranked':>12} | {'Delta':>10}")
    print(f"{'-'*12}-+-{'-'*12}-+-{'-'*12}-+-{'-'*10}")
    for k in KS:
        v_val = v[f"recall@{k}"]
        r_val = r[f"recall@{k}"]
        delta = r_val - v_val
        d_str = f"+{delta*100:.1f}%" if delta >= 0 else f"{delta*100:.1f}%"
        print(f"{'Recall@'+str(k):<12} | {v_val*100:>11.1f}% | {r_val*100:>11.1f}% | {d_str:>10}")
    v_mrr, r_mrr = v["mrr"], r["mrr"]
    d_mrr = r_mrr - v_mrr
    d_str = f"+{d_mrr:.4f}" if d_mrr >= 0 else f"{d_mrr:.4f}"
    print(f"{'MRR':<12} | {v_mrr:>12.4f} | {r_mrr:>12.4f} | {d_str:>10}")
    print(f"{'='*70}")
    print("Benchmark completed!")


if __name__ == "__main__":
    run_benchmark()
