"""
tests/integration/test_knowledge_graph_pipeline.py
===================================================
Integration tests for the knowledge graph pipeline:
  concept JSONs → ontology → graph → structural validation

Tests that the graph is well-formed: correct node count,
no cycles, no orphans, and that key concepts are reachable.
"""

import json
import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

GRAPH_FILE    = PROJECT_ROOT / "corpus_data" / "ontology" / "knowledge_graph.json"
CONCEPTS_DIR  = PROJECT_ROOT / "corpus_data" / "concepts"
EXPECTED_MIN_NODES = 140  # allow some tolerance below 149


@pytest.fixture(scope="module")
def graph():
    assert GRAPH_FILE.exists(), f"Knowledge graph not found at {GRAPH_FILE}"
    with open(GRAPH_FILE, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def concepts(graph):
    return graph["concepts"]


# ---------------------------------------------------------------------------
# Graph completeness
# ---------------------------------------------------------------------------

def test_graph_has_minimum_nodes(concepts):
    assert len(concepts) >= EXPECTED_MIN_NODES, (
        f"Expected at least {EXPECTED_MIN_NODES} nodes, got {len(concepts)}"
    )


def test_key_concepts_present(concepts):
    """Core concepts that must always exist in the graph."""
    required = [
        "embedding", "vector_database", "retrieval_augmented_generation",
        "transformer", "attention", "lora", "agent", "chunking",
        "gradient_descent", "backpropagation", "lstm", "convolution",
        "resnet", "yolo", "kubeflow", "drift_detection",
    ]
    for cid in required:
        assert cid in concepts, f"Required concept '{cid}' is missing from the graph"


# ---------------------------------------------------------------------------
# Graph structural integrity
# ---------------------------------------------------------------------------

def test_no_self_prerequisites(concepts):
    """No concept should list itself as a prerequisite."""
    for cid, node in concepts.items():
        assert cid not in node.get("prerequisites", []), (
            f"Concept '{cid}' lists itself as a prerequisite"
        )


def test_all_prerequisite_ids_exist(concepts):
    """Every prerequisite ID referenced must correspond to an actual concept."""
    for cid, node in concepts.items():
        for prereq in node.get("prerequisites", []):
            assert prereq in concepts, (
                f"Concept '{cid}' references unknown prerequisite '{prereq}'"
            )


def test_no_cycles(concepts):
    """Prerequisite graph must be a DAG (no circular dependencies)."""
    visited = {}  # 0=unvisited, 1=visiting, 2=done

    def has_cycle(node_id: str) -> bool:
        state = visited.get(node_id, 0)
        if state == 1:
            return True  # back-edge → cycle
        if state == 2:
            return False
        visited[node_id] = 1
        for prereq in concepts.get(node_id, {}).get("prerequisites", []):
            if has_cycle(prereq):
                return True
        visited[node_id] = 2
        return False

    for cid in concepts:
        assert not has_cycle(cid), f"Cycle detected involving concept '{cid}'"


def test_no_isolated_orphans(concepts):
    """
    Every concept must either have prerequisites or be a prerequisite of something.
    Pure leaf concepts with no connections at all indicate a data problem.
    We allow at most 10 orphans (some beginner concepts have no prereqs by design).
    """
    all_prereq_targets = set()
    for node in concepts.values():
        all_prereq_targets.update(node.get("prerequisites", []))

    orphans = [
        cid for cid, node in concepts.items()
        if not node.get("prerequisites") and cid not in all_prereq_targets
    ]
    assert len(orphans) <= 10, (
        f"Too many orphan concepts ({len(orphans)}): {orphans[:10]}"
    )


# ---------------------------------------------------------------------------
# Node schema
# ---------------------------------------------------------------------------

def test_all_nodes_have_required_fields(concepts):
    """Every graph node must have term, difficulty, subdomain."""
    for cid, node in concepts.items():
        assert "term"       in node, f"Node '{cid}' missing 'term'"
        assert "difficulty" in node, f"Node '{cid}' missing 'difficulty'"
        assert "subdomain"  in node, f"Node '{cid}' missing 'subdomain'"


def test_difficulty_values_are_valid(concepts):
    valid = {"Beginner", "Intermediate", "Advanced"}
    for cid, node in concepts.items():
        d = node.get("difficulty", "")
        assert d in valid, f"Node '{cid}' has invalid difficulty '{d}'"
