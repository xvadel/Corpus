"""
curriculum_runner.py
====================
Evaluates the curriculum engine against a set of benchmark scenarios.

Dataset: corpus_data/benchmarks/curriculum_benchmark.json

Usage:
    python backend/evaluation/curriculum_runner.py
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

BENCHMARK_FILE = PROJECT_ROOT / "corpus_data" / "benchmarks" / "curriculum_benchmark.json"

from backend.curriculum.gap_analyzer import GapAnalyzer
from backend.curriculum.learning_path_builder import LearningPathBuilder


def evaluate_scenario(scenario: dict, gap_analyzer: GapAnalyzer, path_builder: LearningPathBuilder) -> dict:
    """Run one benchmark scenario and return per-scenario metrics."""
    goal          = scenario["goal"]
    known         = set(scenario.get("known_concepts", []))
    expected_path = [step["id"] for step in scenario["expected_path"]]
    expected_diffs = {step["id"]: step["difficulty"] for step in scenario["expected_path"]}

    # Run the pipeline
    gaps = gap_analyzer.find_gaps(goal, known_concepts=known)
    path = path_builder.build_path(goal, known_concepts=known)
    path_ids = [step["id"] if isinstance(step, dict) else step for step in path]

    # Metric 1: Path Completeness — fraction of expected concepts present in generated path
    expected_set = set(expected_path)
    generated_set = set(path_ids)
    completeness = len(expected_set & generated_set) / len(expected_set) if expected_set else 1.0

    # Metric 2: Dependency Satisfaction — for each consecutive pair in generated path,
    # check that no concept appears before its expected prerequisite
    violations = 0
    for i, concept in enumerate(path_ids):
        if concept in expected_path:
            exp_idx = expected_path.index(concept)
            # All expected prerequisites should appear earlier in path_ids
            for prereq in expected_path[:exp_idx]:
                if prereq in path_ids and path_ids.index(prereq) > i:
                    violations += 1

    dep_satisfaction = 1.0 - (violations / max(len(path_ids), 1))

    # Metric 3: Missing Prerequisites — concepts in expected_path not generated at all
    missing = [c for c in expected_path if c not in generated_set]

    # Metric 4: Difficulty Progression — check no higher-difficulty concept precedes a lower one
    difficulty_order = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
    progression_ok = True
    prev_level = -1
    for pid in path_ids:
        diff = expected_diffs.get(pid, "")
        level = difficulty_order.get(diff, 1)
        if level < prev_level - 1:  # allow same or one step back
            progression_ok = False
            break
        prev_level = max(prev_level, level)

    return {
        "id":               scenario["id"],
        "goal":             goal,
        "completeness":     completeness,
        "dep_satisfaction": dep_satisfaction,
        "missing":          missing,
        "progression_ok":   progression_ok,
        "generated_path":   path_ids,
        "expected_path":    expected_path,
    }


def run_curriculum_benchmark() -> None:
    print("=" * 65)
    print("CURRICULUM ENGINE BENCHMARK")
    print("=" * 65)

    with open(BENCHMARK_FILE, encoding="utf-8") as f:
        scenarios = json.load(f)

    gap_analyzer  = GapAnalyzer()
    path_builder  = LearningPathBuilder()

    completeness_sum    = 0.0
    dep_satisfaction_sum = 0.0
    progression_ok_count = 0
    total_missing = 0

    for scenario in scenarios:
        result = evaluate_scenario(scenario, gap_analyzer, path_builder)

        status = "✓" if result["completeness"] >= 0.8 and result["dep_satisfaction"] >= 0.8 else "✗"
        print(f"\n  [{status}] {result['id']}")
        print(f"       Goal:           {result['goal']}")
        print(f"       Completeness:   {result['completeness']*100:.1f}%")
        print(f"       Dep.Satisf.:    {result['dep_satisfaction']*100:.1f}%")
        print(f"       Progression:    {'OK' if result['progression_ok'] else 'FAIL'}")
        if result["missing"]:
            print(f"       Missing:        {result['missing']}")
        print(f"       Generated path: {result['generated_path']}")
        print(f"       Expected path:  {result['expected_path']}")

        completeness_sum     += result["completeness"]
        dep_satisfaction_sum += result["dep_satisfaction"]
        total_missing        += len(result["missing"])
        if result["progression_ok"]:
            progression_ok_count += 1

    n = len(scenarios)
    print(f"\n{'=' * 65}")
    print(f"  Scenarios:             {n}")
    print(f"  Avg Completeness:      {completeness_sum/n*100:.1f}%")
    print(f"  Avg Dep. Satisfaction: {dep_satisfaction_sum/n*100:.1f}%")
    print(f"  Progression OK:        {progression_ok_count}/{n}")
    print(f"  Total missing prereqs: {total_missing}")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    run_curriculum_benchmark()
