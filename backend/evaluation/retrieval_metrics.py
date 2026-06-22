from typing import List, Dict, Any

def compute_recall_at_k(retrieved_ids: List[str], ground_truth_id: str, k: int) -> float:
    """
    Calculates Recall@K. Returns 1.0 if ground_truth_id is within the top k retrieved_ids, else 0.0.
    """
    top_k = retrieved_ids[:k]
    return 1.0 if ground_truth_id in top_k else 0.0

def compute_reciprocal_rank(retrieved_ids: List[str], ground_truth_id: str) -> float:
    """
    Calculates Reciprocal Rank. Returns 1 / rank of the ground_truth_id in retrieved_ids (1-indexed).
    Returns 0.0 if not found.
    """
    if ground_truth_id in retrieved_ids:
        rank = retrieved_ids.index(ground_truth_id) + 1
        return 1.0 / rank
    return 0.0

def evaluate_retrieval_dataset(
    retriever,
    dataset: List[Dict[str, str]],
    k: int = 5,
    verbose: bool = False,
    **kwargs
) -> Dict[str, float]:
    """
    Evaluates a list of {"query": str, "ground_truth_id": str} query pairs.

    Performs a SINGLE retrieval call per query (at limit=max(k,10)) and
    computes Recall@k and MRR from the same result list — avoids redundant
    ChromaDB round-trips.

    Returns average Recall@K and average MRR.
    """
    total = len(dataset)
    if total == 0:
        return {"recall_at_k": 0.0, "mrr": 0.0}

    recall_sum = 0.0
    rr_sum = 0.0

    for i, item in enumerate(dataset):
        query = item["query"]
        gt_id = item["ground_truth_id"]

        # Single retrieval pass — fetch enough results for MRR denominator
        results = retriever.retrieve(query, limit=max(k, 10), **kwargs)
        retrieved_ids = [r["id"] for r in results]

        recall_sum += compute_recall_at_k(retrieved_ids, gt_id, k)
        rr_sum     += compute_reciprocal_rank(retrieved_ids, gt_id)

        if verbose:
            hit = "[HIT]" if gt_id in retrieved_ids[:k] else "[---]"
            print(f"  [{i+1:>3}/{total}] {hit}  gt={gt_id:<35} top1={retrieved_ids[0] if retrieved_ids else 'none'}", flush=True)

    return {
        "recall_at_k": recall_sum / total,
        "mrr":         rr_sum / total
    }

def evaluate_all_ks(
    retriever,
    dataset: List[Dict[str, str]],
    ks: List[int] = (1, 3, 5),
    verbose: bool = False,
    **kwargs
) -> Dict[str, float]:
    """
    Evaluate multiple k values in a single retrieval pass per query.
    Returns {f"recall@{k}": float, ..., "mrr": float}.
    """
    total = len(dataset)
    if total == 0:
        return {f"recall@{k}": 0.0 for k in ks} | {"mrr": 0.0}

    max_k = max(ks)
    recall_sums = {k: 0.0 for k in ks}
    rr_sum = 0.0

    for i, item in enumerate(dataset):
        query = item["query"]
        gt_id = item["ground_truth_id"]

        results = retriever.retrieve(query, limit=max(max_k, 10), **kwargs)
        retrieved_ids = [r["id"] for r in results]

        for k in ks:
            recall_sums[k] += compute_recall_at_k(retrieved_ids, gt_id, k)
        rr_sum += compute_reciprocal_rank(retrieved_ids, gt_id)

        if verbose:
            hit = "[HIT]" if gt_id in retrieved_ids[:max_k] else "[---]"
            print(f"  [{i+1:>3}/{total}] {hit}  gt={gt_id:<35} top1={retrieved_ids[0] if retrieved_ids else 'none'}", flush=True)

    result = {f"recall@{k}": recall_sums[k] / total for k in ks}
    result["mrr"] = rr_sum / total
    return result
