"""
skill_runner.py
===============
Evaluates the gap analyzer against benchmark scenarios.

Dataset: corpus_data/benchmarks/skill_benchmark.json

Usage:
    python backend/evaluation/skill_runner.py
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

BENCHMARK_FILE = PROJECT_ROOT / "corpus_data" / "benchmarks" / "skill_benchmark.json"

from backend.curriculum.gap_analyzer import GapAnalyzer


def evaluate_scenario(scenario: dict, gap_analyzer: GapAnalyzer) -> dict:
    goal           = scenario["goal"]
    known          = set(scenario.get("known_concepts", []))
    expected_gaps  = set(scenario["expected_gaps"])

    detected_gaps  = set(gap_analyzer.find_gaps(goal, known_concepts=known))

    true_positives  = detected_gaps & expected_gaps
    false_positives = detected_gaps - expected_gaps
    false_negatives = expected_gaps - detected_gaps

    precision = len(true_positives) / len(detected_gaps)  if detected_gaps  else 0.0
    recall    = len(true_positives) / len(expected_gaps)  if expected_gaps  else 1.0
    f1        = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    return {
        "id":               scenario["id"],
        "goal":             goal,
        "precision":        precision,
        "recall":           recall,
        "f1":               f1,
        "true_positives":   sorted(true_positives),
        "false_positives":  sorted(false_positives),
        "false_negatives":  sorted(false_negatives),
    }


def run_skill_benchmark() -> None:
    print("=" * 65)
    print("USER SKILL GAP DETECTION BENCHMARK")
    print("=" * 65)

    with open(BENCHMARK_FILE, encoding="utf-8") as f:
        scenarios = json.load(f)

    gap_analyzer = GapAnalyzer()

    precision_sum = recall_sum = f1_sum = 0.0

    for scenario in scenarios:
        result = evaluate_scenario(scenario, gap_analyzer)

        status = "✓" if result["f1"] >= 0.70 else "✗"
        print(f"\n  [{status}] {result['id']}")
        print(f"       Goal:      {result['goal']}")
        print(f"       Precision: {result['precision']*100:.1f}%  "
              f"Recall: {result['recall']*100:.1f}%  "
              f"F1: {result['f1']*100:.1f}%")
        if result["false_negatives"]:
            print(f"       Missed:    {result['false_negatives']}")
        if result["false_positives"]:
            print(f"       Extra:     {result['false_positives']}")

        precision_sum += result["precision"]
        recall_sum    += result["recall"]
        f1_sum        += result["f1"]

    n = len(scenarios)
    print(f"\n{'=' * 65}")
    print(f"  Scenarios:      {n}")
    print(f"  Avg Precision:  {precision_sum/n*100:.1f}%")
    print(f"  Avg Recall:     {recall_sum/n*100:.1f}%")
    print(f"  Avg F1:         {f1_sum/n*100:.1f}%")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    run_skill_benchmark()
