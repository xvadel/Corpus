from typing import List, Dict, Any

class DifficultyMapper:
    @staticmethod
    def group_by_difficulty(concepts_list: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Groups a list of concepts by their difficulty level.
        """
        grouped = {"Beginner": [], "Intermediate": [], "Advanced": []}
        for concept in concepts_list:
            diff = concept.get("difficulty", "Intermediate")
            if diff in grouped:
                grouped[diff].append(concept)
            else:
                grouped["Intermediate"].append(concept)
        return grouped

    @staticmethod
    def get_difficulty_weight(difficulty: str) -> int:
        mapping = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
        return mapping.get(difficulty, 2)
