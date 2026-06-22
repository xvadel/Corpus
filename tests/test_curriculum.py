import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.curriculum.learning_path_builder import LearningPathBuilder
from backend.curriculum.difficulty_mapper import DifficultyMapper
from backend.curriculum.gap_analyzer import GapAnalyzer

def test_curriculum_engine():
    print("Testing Curriculum Engine...")
    
    path_builder = LearningPathBuilder()
    
    # Generate learning path for a deep concept like 'retrieval_augmented_generation'
    target = "retrieval_augmented_generation"
    path = path_builder.build_path_for_concept(target)
    
    assert len(path) > 0, "Learning path should contain at least the target concept"
    print(f"\nLearning Path to master '{target}':")
    for i, c in enumerate(path, 1):
        print(f"  {i}. {c['term']} ({c['subdomain']}, {c['difficulty']})")
        
    # Check that 'retrieval_augmented_generation' is the last item (or at least in the path)
    assert path[-1]["id"] == target, f"Target '{target}' should be at the end of the topological path"
    
    # Test Difficulty Mapping
    grouped = DifficultyMapper.group_by_difficulty(path)
    print("\nGrouped by Difficulty Tiers:")
    for tier, items in grouped.items():
        print(f"  {tier}: {', '.join([c['term'] for c in items]) if items else 'None'}")
        
    # Test Gap Analysis
    analyzer = GapAnalyzer(path_builder)
    
    # Suppose user knows 'embedding' and 'vector_database'
    known_concepts = ["embedding", "vector_database"]
    analysis = analyzer.analyze_gaps(target, known_concepts)
    
    print("\nGap Analysis:")
    print(f"  Target: {analysis['target_concept']}")
    print(f"  Is User Ready? {analysis['is_ready']}")
    print(f"  Required concepts count: {analysis['required_path_length']}")
    print(f"  Known concepts in path count: {analysis['known_count_in_path']}")
    print("  Missing concepts:")
    for mc in analysis["missing_concepts"]:
        print(f"    - {mc['term']} (missing prerequisites: {mc['missing_prerequisites']})")
        
    assert len(analysis["missing_concepts"]) > 0, "Should have missing concepts if user only knows 2"
    assert "retrieval_augmented_generation" in [mc["id"] for mc in analysis["missing_concepts"]], "Target concept should be missing"

if __name__ == "__main__":
    test_curriculum_engine()
    print("\nAll curriculum engine tests passed!")
