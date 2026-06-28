"""
benchmark_runner.py
===================
Runs the Corpus retrieval benchmark against both the vector-only and
vector + cross-encoder reranked pipelines.

Benchmark data: corpus_data/benchmarks/retrieval_queries.json  (v2.0 schema)
Thresholds:     backend/evaluation/thresholds.json

Usage:
    python backend/evaluation/benchmark_runner.py
    python backend/evaluation/benchmark_runner.py --no-rerank
    python backend/evaluation/benchmark_runner.py --negatives
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

BENCHMARK_FILE  = PROJECT_ROOT / "corpus_data" / "benchmarks" / "retrieval_queries.json"
NEGATIVE_FILE   = PROJECT_ROOT / "corpus_data" / "benchmarks" / "negative_queries.json"
THRESHOLDS_FILE = PROJECT_ROOT / "backend" / "evaluation" / "thresholds.json"

from backend.retrieval.retriever import VectorRetriever
from backend.evaluation.retrieval_metrics import evaluate_all_ks

KS = [1, 3, 5]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_thresholds() -> dict:
    if THRESHOLDS_FILE.exists():
        with open(THRESHOLDS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _print_tier(tier_name: str, metrics: dict) -> None:
    r1  = metrics.get("recall@1",    0) * 100
    r3  = metrics.get("recall@3",    0) * 100
    r5  = metrics.get("recall@5",    0) * 100
    p5  = metrics.get("precision@5", 0) * 100
    n5  = metrics.get("ndcg@5",      0)
    mrr = metrics.get("mrr",         0)
    print(
        f"    Recall@1={r1:.1f}%  Recall@3={r3:.1f}%  Recall@5={r5:.1f}%  "
        f"Prec@5={p5:.1f}%  nDCG@5={n5:.4f}  MRR={mrr:.4f}"
    )


def _check_thresholds(metrics: dict, tier: str, thresholds: dict) -> list[str]:
    """Return list of failed threshold strings."""
    failures = []
    tier_t = thresholds.get(tier, {})
    mapping = {
        "recall_at_1": "recall@1",
        "recall_at_3": "recall@3",
        "recall_at_5": "recall@5",
        "mrr":         "mrr",
        "ndcg_at_5":   "ndcg@5",
    }
    for t_key, m_key in mapping.items():
        if t_key in tier_t and m_key in metrics:
            if metrics[m_key] < tier_t[t_key]:
                failures.append(
                    f"  [{tier.upper()}] {m_key}: {metrics[m_key]:.4f} < threshold {tier_t[t_key]:.4f}"
                )
    return failures


# ---------------------------------------------------------------------------
# Negative query pass
# ---------------------------------------------------------------------------

def run_negatives(retriever: VectorRetriever, confidence_threshold: float = 0.60) -> None:
    """
    Runs negative (out-of-domain) queries and reports rejection accuracy.
    A query is 'rejected' when the top-1 distance is ABOVE the threshold
    (high distance = low similarity = the system doesn't recognise the query).
    """
    if not NEGATIVE_FILE.exists():
        print("\n[NEGATIVES] negative_queries.json not found — skipping.")
        return

    with open(NEGATIVE_FILE, encoding="utf-8") as f:
        negatives = json.load(f)

    total = len(negatives)
    rejected = 0
    print(f"\n{'-'*70}")
    print(f"  Negative Queries — rejection threshold: distance > {confidence_threshold}")
    print(f"{'-'*70}")

    for item in negatives:
        query    = item["query"]
        expected = item.get("expected_behavior", "reject")
        results  = retriever.retrieve(query, limit=1)

        distance = results[0].get("distance", 0.0) if results else 1.0
        rejected_flag = distance > confidence_threshold
        if rejected_flag:
            rejected += 1

        status = "REJECTED" if rejected_flag else "RETRIEVED"
        print(f"  [{status:<9}]  dist={distance:.3f}  [{expected}]  {query[:55]}")

    accuracy = rejected / total * 100
    print(f"\n  Rejection accuracy: {rejected}/{total} = {accuracy:.1f}%")


# ---------------------------------------------------------------------------
# Main benchmark
# ---------------------------------------------------------------------------

def run_pipeline(retriever: VectorRetriever, all_queries: list, rerank: bool) -> dict:
    label = "VECTOR + CROSS-ENCODER RERANK" if rerank else "VECTOR ONLY"
    total = len(all_queries)
    print(f"\n{'-'*70}")
    print(f"  Pipeline: {label}")
    print(f"{'-'*70}")

    tier_metrics = {}
    for tier_name in ("easy", "medium", "hard"):
        tier_qs = [q for q in all_queries if q["tier"] == tier_name]
        print(f"\n  [{tier_name.upper()} - {len(tier_qs)} queries]", flush=True)
        m = evaluate_all_ks(retriever, tier_qs, ks=KS, verbose=True, rerank=rerank)
        _print_tier(tier_name, m)
        tier_metrics[tier_name] = m

    print(f"\n  [OVERALL - {total} queries]", flush=True)
    m_all = evaluate_all_ks(retriever, all_queries, ks=KS, rerank=rerank)
    _print_tier("overall", m_all)

    return {"overall": m_all, "tiers": tier_metrics}


def run_benchmark(no_rerank: bool = False, run_neg: bool = False) -> None:
    print("=" * 70)
    print("CORPUS KNOWLEDGE ARCHITECTURE BENCHMARK RUNNER")
    print("=" * 70)

    with open(BENCHMARK_FILE, encoding="utf-8") as f:
        data = json.load(f)
    all_queries = data["queries"]
    meta = data.get("metadata", {})
    print(f"\nDataset v{meta.get('version','?')} — {len(all_queries)} queries")
    counts = {t: sum(1 for q in all_queries if q["tier"] == t) for t in ("easy","medium","hard")}
    print(f"  Easy: {counts['easy']}  Medium: {counts['medium']}  Hard: {counts['hard']}")

    thresholds = _load_thresholds()
    retriever  = VectorRetriever()

    # --- Vector-only pass ---
    v_result = run_pipeline(retriever, all_queries, rerank=False)

    # --- Reranked pass (optional) ---
    r_result = None
    if not no_rerank:
        r_result = run_pipeline(retriever, all_queries, rerank=True)

    # --- Negative queries ---
    if run_neg:
        run_negatives(retriever)

    # --- Uplift table ---
    if r_result:
        v, r = v_result["overall"], r_result["overall"]
        print(f"\n{'='*70}")
        print("UPLIFT: VECTOR ONLY  →  VECTOR + CROSS-ENCODER RERANK")
        print(f"{'='*70}")
        print(f"{'Metric':<14} | {'Vector Only':>11} | {'Reranked':>10} | {'Delta':>10}")
        print(f"{'-'*14}-+-{'-'*11}-+-{'-'*10}-+-{'-'*10}")
        for k in KS:
            key = f"recall@{k}"
            delta = r[key] - v[key]
            sign  = "+" if delta >= 0 else ""
            print(f"{'Recall@'+str(k):<14} | {v[key]*100:>10.1f}% | {r[key]*100:>9.1f}% | {sign}{delta*100:.1f}%")
        for key, label in [("precision@5","Precision@5"), ("ndcg@5","nDCG@5"), ("mrr","MRR")]:
            delta = r[key] - v[key]
            sign  = "+" if delta >= 0 else ""
            print(f"{label:<14} | {v[key]:>11.4f} | {r[key]:>10.4f} | {sign}{delta:.4f}")
        print(f"{'='*70}")

    # --- Threshold check ---
    if thresholds and r_result:
        failures = []
        for tier in ("easy", "medium", "hard"):
            failures += _check_thresholds(r_result["tiers"][tier], tier, thresholds)
        failures += _check_thresholds(r_result["overall"], "overall", thresholds)
        if failures:
            print("\n⚠  THRESHOLD FAILURES:")
            for f in failures:
                print(f)
        else:
            print("\n✓  All thresholds passed.")

    print("\nBenchmark completed!")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-rerank",  action="store_true", help="Skip the cross-encoder rerank pass")
    parser.add_argument("--negatives",  action="store_true", help="Also run negative (out-of-domain) queries")
    args = parser.parse_args()
    run_benchmark(no_rerank=args.no_rerank, run_neg=args.negatives)
