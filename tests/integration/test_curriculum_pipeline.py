"""
tests/integration/test_curriculum_pipeline.py
=============================================
Integration tests for the full curriculum pipeline:
  known skills + goal → GapAnalyzer → LearningPathBuilder → ordered path

Tests that the pipeline identifies correct gaps and generates paths
that respect dependency ordering.
"""

import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.curriculum.gap_analyzer import GapAnalyzer
from backend.curriculum.learning_path_builder import LearningPathBuilder


@pytest.fixture(scope="module")
def path_builder():
    return LearningPathBuilder()


@pytest.fixture(scope="module")
def gap_analyzer(path_builder):
    return GapAnalyzer(path_builder=path_builder)


# ---------------------------------------------------------------------------
# Gap detection correctness
# ---------------------------------------------------------------------------

def test_gap_detection_no_known_concepts(gap_analyzer):
    """With no prior knowledge, all prerequisites of RAG should be identified as gaps."""
    result = gap_analyzer.analyze_gaps("retrieval_augmented_generation", known_concept_ids=[])
    missing_ids = [g["id"] for g in result["missing_concepts"]]
    assert "embedding" in missing_ids, "embedding should be a gap when starting from scratch"
    assert "vector_database" in missing_ids, "vector_database should be a gap"
    assert result["is_ready"] is False


def test_gap_detection_with_known_concepts(gap_analyzer):
    """With embedding and vector_database known, fewer gaps should remain for RAG."""
    result_empty = gap_analyzer.analyze_gaps("retrieval_augmented_generation", known_concept_ids=[])
    result_partial = gap_analyzer.analyze_gaps(
        "retrieval_augmented_generation",
        known_concept_ids=["embedding", "vector_database"]
    )
    assert len(result_partial["missing_concepts"]) < len(result_empty["missing_concepts"]), (
        "Knowing prerequisites should reduce the number of detected gaps"
    )


def test_gap_detection_already_known(gap_analyzer):
    """If the target concept is already known, is_ready should be True."""
    result = gap_analyzer.analyze_gaps(
        "embedding",
        known_concept_ids=["embedding"]
    )
    assert result["is_ready"] is True


# ---------------------------------------------------------------------------
# Learning path ordering
# ---------------------------------------------------------------------------

def test_path_respects_dependency_order(path_builder):
    """embedding must appear before retrieval_augmented_generation in the path."""
    path = path_builder.build_path_for_concept("retrieval_augmented_generation")
    ids = [c["id"] for c in path]
    if "embedding" in ids and "retrieval_augmented_generation" in ids:
        assert ids.index("embedding") < ids.index("retrieval_augmented_generation"), (
            "embedding must be taught before retrieval_augmented_generation"
        )


def test_path_contains_goal(path_builder):
    """The generated path must include the target concept itself."""
    path = path_builder.build_path_for_concept("lora")
    ids = [c["id"] for c in path]
    assert "lora" in ids, "Goal concept must appear in the learning path"


def test_path_not_empty(path_builder):
    """A valid goal always produces a non-empty path."""
    path = path_builder.build_path_for_concept("transformer")
    assert len(path) > 0, "Learning path should not be empty for a known concept"


def test_path_concepts_have_required_fields(path_builder):
    """Each step in the path must have id, term, and difficulty."""
    path = path_builder.build_path_for_concept("deep_q_networks")
    for step in path:
        assert "id" in step,         f"Missing 'id' in path step: {step}"
        assert "term" in step,       f"Missing 'term' in path step: {step}"
        assert "difficulty" in step, f"Missing 'difficulty' in path step: {step}"
