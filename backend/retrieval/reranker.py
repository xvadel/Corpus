"""
Corpus — CrossEncoder Reranker
================================
Re-scores candidate documents retrieved by VectorRetriever using a
cross-encoder model (BAAI/bge-reranker-base) for higher precision.

Architecture:
    VectorRetriever (bi-encoder recall)  →  CrossEncoderReranker (cross-encoder precision)

Usage:
    retriever = VectorRetriever()
    reranker  = CrossEncoderReranker()

    candidates = retriever.retrieve(query, limit=20)
    reranked   = reranker.rerank(query, candidates, top_k=5)
"""

from typing import List, Dict, Any


RERANKER_MODEL = "BAAI/bge-reranker-base"


class CrossEncoderReranker:
    """
    Re-scores retrieval candidates with a CrossEncoder.

    The bi-encoder (VectorRetriever) provides fast recall over the full corpus.
    This reranker then scores each (query, passage) pair jointly for precision.
    """

    def __init__(self, model_name: str = RERANKER_MODEL):
        from sentence_transformers import CrossEncoder
        print(f"[CrossEncoderReranker] Loading model: {model_name}")
        self.model = CrossEncoder(model_name)
        print("[CrossEncoderReranker] Model loaded.")

    def rerank(
        self,
        query: str,
        candidates: List[Dict[str, Any]],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Re-score a list of retrieval candidates and return the top-k results.

        Args:
            query:      The original user query string.
            candidates: List of retrieval dicts (each must have a 'document' key).
            top_k:      Number of results to return after reranking.

        Returns:
            Sorted list of dicts with an added 'rerank_score' field.
        """
        if not candidates:
            return []

        # Build (query, passage) pairs for the cross-encoder
        pairs = [(query, c["document"]) for c in candidates]

        # Score all pairs in one batch (CrossEncoder.predict is efficient)
        scores = self.model.predict(pairs)

        # Attach rerank score to each candidate
        for candidate, score in zip(candidates, scores):
            candidate["rerank_score"] = float(score)

        # Sort by cross-encoder score descending
        reranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
        return reranked[:top_k]
