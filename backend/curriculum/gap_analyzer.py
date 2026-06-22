from typing import List, Dict, Any, Set
from backend.curriculum.learning_path_builder import LearningPathBuilder

class GapAnalyzer:
    def __init__(self, path_builder: LearningPathBuilder):
        self.path_builder = path_builder

    def analyze_gaps(self, target_concept_id: str, known_concept_ids: List[str]) -> Dict[str, Any]:
        """
        Compares the target concept's required learning path against a user's known concepts.
        Identifies missing prerequisites and structural gaps.
        """
        required_path = self.path_builder.build_path_for_concept(target_concept_id)
        required_ids = [c["id"] for c in required_path]
        
        known_set = set(known_concept_ids)
        missing_ids = [cid for cid in required_ids if cid not in known_set]
        
        gaps = []
        for cid in missing_ids:
            concept_data = self.path_builder.concepts.get(cid, {})
            prereqs = concept_data.get("prerequisites", [])
            missing_prereqs = [p for p in prereqs if p not in known_set]
            
            gaps.append({
                "id": cid,
                "term": concept_data.get("term", cid),
                "difficulty": concept_data.get("difficulty", "Intermediate"),
                "missing_prerequisites": missing_prereqs
            })
            
        is_ready = target_concept_id in known_set or len(missing_ids) == 0
        
        return {
            "target_concept": target_concept_id,
            "is_ready": is_ready,
            "required_path_length": len(required_ids),
            "known_count_in_path": len(required_ids) - len(missing_ids),
            "missing_concepts": gaps
        }
