import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONCEPTS_DIR = PROJECT_ROOT / "corpus_data" / "concepts"

def add_references():
    count = 0
    for file_path in CONCEPTS_DIR.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error loading {file_path.name}: {e}")
                continue
        
        # Add references if not present
        if "references" not in data:
            data["references"] = []
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            count += 1
            
    print(f"Successfully added 'references' key to {count} concept files.")

if __name__ == "__main__":
    add_references()
