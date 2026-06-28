"""
scripts/enrich_concepts.py
===========================
Idempotent script to add new schema fields to all concept JSON files in corpus_data/concepts/.

New fields added (default to empty lists):
  - aliases
  - abbreviations
  - keywords
  - counter_examples
  - applications
  - not_to_confuse_with
  - commonly_confused_with
  - common_misconceptions
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONCEPTS_DIR = PROJECT_ROOT / "corpus_data" / "concepts"

NEW_FIELDS = {
    "aliases": [],
    "abbreviations": [],
    "keywords": [],
    "counter_examples": [],
    "applications": [],
    "not_to_confuse_with": [],
    "commonly_confused_with": [],
    "common_misconceptions": []
}

def enrich_concept_files():
    count = 0
    for file_path in CONCEPTS_DIR.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error reading {file_path.name}: {e}")
                continue
        
        modified = False
        for field, default in NEW_FIELDS.items():
            if field not in data:
                data[field] = default
                modified = True
        
        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            count += 1
            
    print(f"Enriched {count} concept files with missing schema fields.")

if __name__ == "__main__":
    enrich_concept_files()
