import os
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONCEPTS_DIR = PROJECT_ROOT / "corpus_data" / "concepts"

REQUIRED_KEYS = {
    "id": str,
    "term": str,
    "domain": str,
    "subdomain": str,
    "difficulty": str,
    "definition": str,
    "simple_explanation": str,
    "technical_explanation": str,
    "examples": list,
    "related_terms": list,
    "prerequisites": list,
    "references": list
}

def validate_concept_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 1. Check all required keys exist and have correct type
    for key, expected_type in REQUIRED_KEYS.items():
        if key not in data:
            raise KeyError(f"Missing required key: '{key}'")
        if not isinstance(data[key], expected_type):
            raise TypeError(f"Key '{key}' expected type {expected_type.__name__}, got {type(data[key]).__name__}")
            
    # 2. Check difficulty value
    if data["difficulty"] not in {"Beginner", "Intermediate", "Advanced"}:
        raise ValueError(f"Invalid difficulty '{data['difficulty']}', must be Beginner, Intermediate, or Advanced")
        
    # 3. Check list elements are strings
    for list_key in ["examples", "related_terms", "prerequisites", "references"]:
        for item in data[list_key]:
            if not isinstance(item, str):
                raise TypeError(f"Item in list '{list_key}' must be string, got {type(item).__name__}")
                
    # 4. Check ID matches filename (without .json extension)
    expected_id = file_path.stem
    if data["id"] != expected_id:
        raise ValueError(f"Concept ID '{data['id']}' does not match filename '{expected_id}'")

def test_all_concepts():
    assert CONCEPTS_DIR.exists(), f"Concepts directory {CONCEPTS_DIR} does not exist"
    concept_files = list(CONCEPTS_DIR.glob("*.json"))
    assert len(concept_files) > 0, "No concept files found"
    
    errors = []
    for file_path in concept_files:
        try:
            validate_concept_file(file_path)
        except Exception as e:
            errors.append(f"File {file_path.name} failed validation: {str(e)}")
            
    if errors:
        for err in errors:
            print(err)
        assert False, f"{len(errors)} concept files failed validation."

if __name__ == "__main__":
    test_all_concepts()
    print("All concept files validated successfully!")
