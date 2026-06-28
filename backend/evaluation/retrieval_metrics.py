"""
retrieval_metrics.py
====================
Evaluation metrics for vector retrieval.

Supports both the legacy schema  {"ground_truth_id": str}
and the v2.0 schema              {"primary": str, "ground_truth": [str, ...]}

Metrics:
    Recall@K     — is the primary answer in the top-K results?
    Precision@K  — what fraction of top-K results are in ground_truth?
    nDCG@K       — primary answer ranked higher earns a higher score
    MRR          — reciprocal rank of the primary answer
"""

from __future__ import annotations
import math
from typing import List, Dict, Any


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _primary(item: Dict) -> str:
    """Return the single canonical answer for a query (v1 and v2 schemas)."""
    return item.get("primary") or item.get("ground_truth_id", "")


def _ground_truth(item: Dict) -> List[str]:
    """Return the full set of acceptable answers (v1 and v2 schemas)."""
    gt = item.get("ground_truth")
    if gt:
        return gt
    primary = item.get("ground_truth_id", "")
    return [primary] if primary else []


# ---------------------------------------------------------------------------
# Per-query metric functions
# ---------------------------------------------------------------------------

def compute_recall_at_k(retrieved_ids: List[str], item: Dict, k: int) -> float:
    """1.0 if the *primary* answer appears in the top-K results, else 0.0."""
    return 1.0 if _primary(item) in retrieved_ids[:k] else 0.0


def compute_precision_at_k(retrieved_ids: List[str], item: Dict, k: int) -> float:
    """Fraction of top-K retrieved results that belong to ground_truth."""
    top_k = retrieved_ids[:k]
    if not top_k:
        return 0.0
    gt = set(_ground_truth(item))
    hits = sum(1 for r in top_k if r in gt)
    return hits / k


def compute_ndcg_at_k(retrieved_ids: List[str], item: Dict, k: int) -> float:
    """
    nDCG@K using binary relevance.
    Primary answer has relevance 2; other ground_truth members have relevance 1.
    Ideal DCG assumes primary is at rank 1 and all others follow.
    """
    gt = set(_ground_truth(item))
    primary = _primary(item)

    def relevance(doc_id: str) -> int:
        if doc_id == primary:
            return 2
        if doc_id in gt:
            return 1
        return 0

    top_k = retrieved_ids[:k]
    dcg = sum(relevance(doc) / math.log2(i + 2) for i, doc in enumerate(top_k))

    # Ideal DCG: primary at rank 1, then remaining gt members
    ideal_order = [primary] + [g for g in _ground_truth(item) if g != primary]
    ideal_top_k = ideal_order[:k]
    idcg = sum(relevance(doc) / math.log2(i + 2) for i, doc in enumerate(ideal_top_k))

    return dcg / idcg if idcg > 0 else 0.0


def compute_reciprocal_rank(retrieved_ids: List[str], item: Dict) -> float:
    """1 / rank of the *primary* answer (1-indexed). 0.0 if not found."""
    primary = _primary(item)
    if primary in retrieved_ids:
        return 1.0 / (retrieved_ids.index(primary) + 1)
    return 0.0


# ---------------------------------------------------------------------------
# Dataset-level evaluation
# ---------------------------------------------------------------------------

def evaluate_all_ks(
    retriever,
    dataset: List[Dict],
    ks: List[int] = (1, 3, 5),
    verbose: bool = False,
    **kwargs,
) -> Dict[str, float]:
    """
    Single retrieval pass per query. Returns:
        recall@K, precision@K, ndcg@K  (for each k)
        mrr
    """
    total = len(dataset)
    if total == 0:
        result = {}
        for k in ks:
            result[f"recall@{k}"] = 0.0
            result[f"precision@{k}"] = 0.0
            result[f"ndcg@{k}"] = 0.0
        result["mrr"] = 0.0
        return result

    max_k = max(ks)
    recall_sums    = {k: 0.0 for k in ks}
    precision_sums = {k: 0.0 for k in ks}
    ndcg_sums      = {k: 0.0 for k in ks}
    rr_sum = 0.0

    for i, item in enumerate(dataset):
        results = retriever.retrieve(item["query"], limit=max(max_k, 10), **kwargs)
        retrieved_ids = [r["id"] for r in results]

        for k in ks:
            recall_sums[k]    += compute_recall_at_k(retrieved_ids, item, k)
            precision_sums[k] += compute_precision_at_k(retrieved_ids, item, k)
            ndcg_sums[k]      += compute_ndcg_at_k(retrieved_ids, item, k)
        rr_sum += compute_reciprocal_rank(retrieved_ids, item)

        if verbose:
            primary = _primary(item)
            hit = "[HIT]" if primary in retrieved_ids[:max_k] else "[---]"
            top1 = retrieved_ids[0] if retrieved_ids else "none"
            print(
                f"  [{i+1:>3}/{total}] {hit}  "
                f"gt={primary:<35} top1={top1}",
                flush=True,
            )

    result = {}
    for k in ks:
        result[f"recall@{k}"]    = recall_sums[k] / total
        result[f"precision@{k}"] = precision_sums[k] / total
        result[f"ndcg@{k}"]      = ndcg_sums[k] / total
    result["mrr"] = rr_sum / total
    return result
