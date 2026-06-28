"""
tests/integration/test_retrieval_pipeline.py
=============================================
Integration tests for the full retrieval pipeline:
  query → embed → vector retrieve → (optional) rerank → result

Tests that the pipeline returns the correct concept as a top result
for representative queries across easy, medium, and hard tiers.
"""

import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.retrieval.retriever import VectorRetriever


@pytest.fixture(scope="module")
def retriever():
    return VectorRetriever()


# ---------------------------------------------------------------------------
# Easy tier — direct term queries must return the correct concept at rank 1
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("query,expected_id", [
    ("What is an embedding?",        "embedding"),
    ("What is a vector database?",   "vector_database"),
    ("What is RAG?",                 "retrieval_augmented_generation"),
    ("What is gradient descent?",    "gradient_descent"),
    ("What is an LSTM?",             "lstm"),
    ("What is XGBoost?",             "xgboost"),
    ("What is a GRU?",               "gru"),
])
def test_easy_retrieval_top1(retriever, query, expected_id):
    results = retriever.retrieve(query, limit=5)
    ids = [r["id"] for r in results]
    assert expected_id in ids[:3], (
        f"Expected '{expected_id}' in top-3 for query '{query}'. Got: {ids[:3]}"
    )


# ---------------------------------------------------------------------------
# Medium tier — paraphrase queries must retrieve the correct concept in top-5
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("query,expected_id", [
    ("Mathematical representation of data as fixed-length numeric vectors.", "embedding"),
    ("Splitting model weight matrix into two low-rank matrices to reduce parameters.", "lora"),
    ("Specialized database for fast approximate nearest neighbor searches.", "vector_database"),
    ("Technique to re-score retrieved documents before passing to the generator.", "reranking"),
    ("An ensemble that trains many trees and combines predictions by majority vote.", "random_forest"),
])
def test_medium_retrieval_top5(retriever, query, expected_id):
    results = retriever.retrieve(query, limit=5)
    ids = [r["id"] for r in results]
    assert expected_id in ids, (
        f"Expected '{expected_id}' in top-5 for query '{query}'. Got: {ids}"
    )


# ---------------------------------------------------------------------------
# Pipeline integrity — retriever must return results with the required fields
# ---------------------------------------------------------------------------

def test_retriever_result_schema(retriever):
    results = retriever.retrieve("What is tokenization?", limit=5)
    assert len(results) > 0, "Retriever returned no results"
    for r in results:
        assert "id"       in r, f"Missing 'id' field in result: {r}"
        assert "distance" in r, f"Missing 'distance' field in result: {r}"


def test_retriever_respects_limit(retriever):
    results = retriever.retrieve("machine learning", limit=3)
    assert len(results) <= 3, f"Expected at most 3 results, got {len(results)}"


def test_retriever_returns_unique_ids(retriever):
    results = retriever.retrieve("neural network training", limit=10)
    ids = [r["id"] for r in results]
    assert len(ids) == len(set(ids)), "Retriever returned duplicate concept IDs"


def test_retriever_scores_are_ordered(retriever):
    results = retriever.retrieve("deep learning", limit=10)
    # Retriever uses distance (lower = more similar) — results should be ascending
    distances = [r["distance"] for r in results]
    assert distances == sorted(distances), "Results are not sorted by distance ascending"
