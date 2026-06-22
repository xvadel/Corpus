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

def evaluate_retrieval_dataset(retriever, dataset: List[Dict[str, str]], k: int = 5) -> Dict[str, float]:
    """
    Evaluates a list of {"query": str, "ground_truth_id": str} query pairs.
    Returns average Recall@K and average MRR.
    """
    total = len(dataset)
    if total == 0:
        return {"recall_at_k": 0.0, "mrr": 0.0}
        
    recall_sum = 0.0
    rr_sum = 0.0
    
    for item in dataset:
        query = item["query"]
        gt_id = item["ground_truth_id"]
        
        # Retrieve n_results up to k (or more to compute MRR beyond k)
        results = retriever.retrieve(query, limit=max(k, 10))
        retrieved_ids = [r["id"] for r in results]
        
        recall_sum += compute_recall_at_k(retrieved_ids, gt_id, k)
        rr_sum += compute_reciprocal_rank(retrieved_ids, gt_id)
        
    return {
        "recall_at_k": recall_sum / total,
        "mrr": rr_sum / total
    }
