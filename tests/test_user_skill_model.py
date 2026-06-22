"""
Unit tests for backend.user_model.skill_model
"""
import sys
import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Redirect DB to a temporary location during testing
import backend.user_model.skill_model as sm_module
sm_module.DB_PATH = PROJECT_ROOT / "corpus_data" / "test_user_skills.db"

from backend.user_model.skill_model import UserSkillModel

USER = "test_user_001"
CONCEPT = "embedding"


@pytest.fixture(autouse=True)
def cleanup():
    """Reset test user before each test."""
    model = UserSkillModel()
    model.reset_user(USER)
    yield
    model.reset_user(USER)


class TestUserSkillModelReads:
    def test_get_score_unknown_concept_returns_zero(self):
        model = UserSkillModel()
        assert model.get_score(USER, "non_existent_concept") == 0.0

    def test_get_all_scores_empty_for_new_user(self):
        model = UserSkillModel()
        assert model.get_all_scores(USER) == {}

    def test_get_mastered_concepts_empty_initially(self):
        model = UserSkillModel()
        assert model.get_mastered_concepts(USER) == []

    def test_get_known_concept_ids_empty_initially(self):
        model = UserSkillModel()
        assert model.get_known_concept_ids(USER) == []


class TestUserSkillModelWrites:
    def test_first_interaction_seeds_score_directly(self):
        model = UserSkillModel()
        score = model.record_interaction(USER, CONCEPT, performance=0.8)
        assert score == pytest.approx(0.8)

    def test_second_interaction_uses_ema(self):
        model = UserSkillModel()
        model.record_interaction(USER, CONCEPT, performance=0.8)
        score = model.record_interaction(USER, CONCEPT, performance=0.5)
        expected = 0.4 * 0.5 + 0.6 * 0.8
        assert score == pytest.approx(expected, rel=1e-4)

    def test_score_persists_across_instances(self):
        model1 = UserSkillModel()
        model1.record_interaction(USER, CONCEPT, performance=1.0)
        model2 = UserSkillModel()
        assert model2.get_score(USER, CONCEPT) == pytest.approx(1.0)

    def test_invalid_performance_raises(self):
        model = UserSkillModel()
        with pytest.raises(ValueError):
            model.record_interaction(USER, CONCEPT, performance=1.5)

    def test_bulk_record(self):
        model = UserSkillModel()
        results = model.bulk_record(USER, [
            {"concept_id": "tokenization", "performance": 0.9},
            {"concept_id": "embedding",    "performance": 0.6},
        ])
        assert results["tokenization"] == pytest.approx(0.9)
        assert results["embedding"]    == pytest.approx(0.6)


class TestUserSkillModelQueries:
    def test_mastered_after_high_score(self):
        model = UserSkillModel()
        model.record_interaction(USER, CONCEPT, performance=1.0)
        assert CONCEPT in model.get_mastered_concepts(USER)

    def test_not_mastered_with_low_score(self):
        model = UserSkillModel()
        model.record_interaction(USER, CONCEPT, performance=0.3)
        assert CONCEPT not in model.get_mastered_concepts(USER)

    def test_known_concept_ids_threshold(self):
        model = UserSkillModel()
        model.record_interaction(USER, "embedding",    performance=0.9)
        model.record_interaction(USER, "chunking",     performance=0.2)  # below threshold
        known = model.get_known_concept_ids(USER, threshold=0.4)
        assert "embedding" in known
        assert "chunking" not in known

    def test_profile_summary_counts(self):
        model = UserSkillModel()
        model.record_interaction(USER, "embedding",    performance=1.0)   # mastered
        model.record_interaction(USER, "tokenization", performance=0.65)  # practiced
        model.record_interaction(USER, "chunking",     performance=0.45)  # introduced
        summary = model.get_profile_summary(USER)
        assert summary["mastered_count"]   == 1
        assert summary["practiced_count"]  == 1
        assert summary["introduced_count"] == 1
        assert summary["total_concepts"]   == 3

    def test_reset_user_clears_all_scores(self):
        model = UserSkillModel()
        model.record_interaction(USER, CONCEPT, performance=1.0)
        model.reset_user(USER)
        assert model.get_all_scores(USER) == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
