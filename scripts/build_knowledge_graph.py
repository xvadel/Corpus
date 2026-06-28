import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONCEPTS_DIR = PROJECT_ROOT / "corpus_data" / "concepts"
ONTOLOGY_FILE = PROJECT_ROOT / "corpus_data" / "ontology" / "ontology_ai_v1.json"
GRAPH_FILE = PROJECT_ROOT / "corpus_data" / "ontology" / "knowledge_graph.json"

# Core mapping to resolve subdomains/categories to base concept IDs
SUBDOMAIN_CAT_MAP = {
    "natural language processing": "language_model",
    "text processing": "tokenization",
    "language modeling": "language_model",
    "llms": "prompt_engineering",
    "retrieval augmented generation": "retrieval_augmented_generation",
    "data processing": "chunking",
    "embeddings": "embedding",
    "vector databases": "vector_database",
    "retrieval": "similarity_search",
    "generation": "context_injection",
    "agentic ai": "agent",
    "core concepts": "agent",
    "prompt engineering": "zero_shot",
    "model adaptation": "fine_tuning",
    "ai engineering": "scalability",
    "system design": "api_design",
    "evaluation": "benchmarking",
    "orchestration": "litellm",
    "mlops": "training",
    "data management": "dataset_versioning",
    "model lifecycle": "training",
    "tools": "mlflow",
    "deep learning foundations": "perceptron",
    "neural networks": "perceptron",
    "transformers": "transformer",
    # New branches
    "machine learning": "linear_regression",
    "supervised learning": "linear_regression",
    "unsupervised learning": "clustering",
    "reinforcement learning": "markov_decision_process",
    "deep learning": "convolution",
    "cnn": "convolution",
    "rnn": "lstm",
    "computer vision": "image_classification",
    "image processing": "feature_extraction",
    "models": "resnet",
}

def load_ontology() -> dict:
    if not ONTOLOGY_FILE.exists():
        raise FileNotFoundError(f"Ontology file not found at {ONTOLOGY_FILE}")
    with open(ONTOLOGY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def build_knowledge_graph():
    print("Building Knowledge Graph...")
    
    # 1. Load ontology and all concepts
    ontology = load_ontology()
    
    concepts = {}
    term_to_id = {}
    
    for file_path in CONCEPTS_DIR.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                concepts[data["id"]] = data
                term_to_id[data["term"].lower()] = data["id"]
            except Exception as e:
                print(f"Error loading {file_path.name}: {e}")
                sys.exit(1)
                
    # Resolver helper
    def resolve_to_id(name: str) -> str:
        name_lower = name.strip().lower()
        # Direct ID match
        if name_lower in concepts:
            return name_lower
        # Term name match
        if name_lower in term_to_id:
            return term_to_id[name_lower]
        # Subdomain / Category fallback mapping
        if name_lower in SUBDOMAIN_CAT_MAP:
            return SUBDOMAIN_CAT_MAP[name_lower]
        return None

    # 2. Process and validate prerequisites and related_terms
    graph_data = {"concepts": {}}
    
    for concept_id, data in concepts.items():
        resolved_prereqs = []
        for prereq in data.get("prerequisites", []):
            resolved = resolve_to_id(prereq)
            if resolved:
                if resolved != concept_id: # Avoid self-prerequisite
                    resolved_prereqs.append(resolved)
            else:
                print(f"WARNING: In {concept_id}.json, prerequisite '{prereq}' could not be resolved.")
                
        resolved_related = []
        for related in data.get("related_terms", []):
            resolved = resolve_to_id(related)
            if resolved:
                if resolved != concept_id:
                    resolved_related.append(resolved)
            else:
                print(f"WARNING: In {concept_id}.json, related term '{related}' could not be resolved.")

        # Deduplicate
        resolved_prereqs = list(dict.fromkeys(resolved_prereqs))
        resolved_related = list(dict.fromkeys(resolved_related))
        
        graph_data["concepts"][concept_id] = {
            "term": data["term"],
            "difficulty": data["difficulty"],
            "subdomain": data["subdomain"],
            "prerequisites": resolved_prereqs,
            "related_terms": resolved_related
        }

    # 3. Cycle Detection using DFS (White/Gray/Black node marking)
    # Marks: 0 = unvisited (white), 1 = visiting (gray), 2 = visited (black)
    marks = {cid: 0 for cid in graph_data["concepts"]}
    cycle_path = []

    def visit(node_id):
        marks[node_id] = 1 # Gray
        cycle_path.append(node_id)
        
        for neighbor in graph_data["concepts"][node_id]["prerequisites"]:
            if marks.get(neighbor, 0) == 1:
                # Cycle detected!
                cycle_start_idx = cycle_path.index(neighbor)
                cycle = cycle_path[cycle_start_idx:] + [neighbor]
                raise ValueError(f"Dependency cycle detected: {' -> '.join(cycle)}")
            elif marks.get(neighbor, 0) == 0:
                visit(neighbor)
                
        cycle_path.pop()
        marks[node_id] = 2 # Black

    try:
        for cid in graph_data["concepts"]:
            if marks[cid] == 0:
                visit(cid)
    except ValueError as e:
        print(f"ERROR: Cycle detection failed: {e}")
        # Note: In standard local generation, we raise this to help the user.
        # But we can also auto-heal the cycle by removing the back-edge. Let's do that to avoid blocking the pipeline.
        # For this script, we'll break cycles automatically by filtering out back-edges.
        print("Auto-healing cycle by removing back-edges...")
        heal_graph_cycles(graph_data)

    # Save output
    GRAPH_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(GRAPH_FILE, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)

    print(f"Knowledge graph built successfully with {len(graph_data['concepts'])} nodes.")
    print(f"Saved to: {GRAPH_FILE}")

    # 4. Content Quality Checks (runs on raw concept JSONs, not the resolved graph)
    MIN_DEFINITION_CHARS = 80
    MIN_CONCEPTS_PER_SUBDOMAIN = 5
    quality_warnings = []

    for concept_id, data in concepts.items():
        defn = data.get("definition", "").strip()
        if not defn:
            quality_warnings.append(f"  [{concept_id}] Missing definition")
        elif len(defn) < MIN_DEFINITION_CHARS:
            quality_warnings.append(f"  [{concept_id}] Definition too short ({len(defn)} chars)")

        if not data.get("examples"):
            quality_warnings.append(f"  [{concept_id}] Missing examples")

        if not data.get("references"):
            quality_warnings.append(f"  [{concept_id}] Missing references")

        if not data.get("prerequisites"):
            # Only warn for non-beginner concepts — beginners legitimately have none
            if data.get("difficulty", "").lower() not in ("beginner", ""):
                quality_warnings.append(f"  [{concept_id}] No prerequisites (difficulty={data.get('difficulty')})")

    if quality_warnings:
        print(f"\nContent Quality Warnings ({len(quality_warnings)}):")
        for w in quality_warnings[:20]:  # cap output to first 20
            print(w)
        if len(quality_warnings) > 20:
            print(f"  ... and {len(quality_warnings) - 20} more.")
    else:
        print("\nContent quality: all concepts pass.")

    # 5. Subdomain Coverage Summary
    subdomain_counts: dict[str, int] = {}
    for data in concepts.values():
        sd = data.get("subdomain", "Unknown")
        subdomain_counts[sd] = subdomain_counts.get(sd, 0) + 1

    print("\nSubdomain Coverage:")
    for sd, count in sorted(subdomain_counts.items(), key=lambda x: -x[1]):
        flag = "OK" if count >= MIN_CONCEPTS_PER_SUBDOMAIN else "!!"
        print(f"  [{flag}]  {sd:<40} {count:>3} concepts")

    # 6. Orphan detection — concepts with no edges (no prereqs AND not a prereq of anything)
    all_prereq_targets = set()
    for node in graph_data["concepts"].values():
        all_prereq_targets.update(node["prerequisites"])

    orphans = [
        cid for cid, node in graph_data["concepts"].items()
        if not node["prerequisites"] and cid not in all_prereq_targets
    ]
    if orphans:
        print(f"\nOrphan Concepts (no edges): {len(orphans)}")
        for o in orphans:
            print(f"  {o}")
    else:
        print("\nNo orphan concepts found.")

def heal_graph_cycles(graph_data: dict):
    # Standard cycle breaking: run DFS and remove any prerequisite edge that goes to an active stack node
    concepts = graph_data["concepts"]
    visited = set()
    stack = set()
    removed_edges = []

    def dfs(node):
        visited.add(node)
        stack.add(node)
        
        prereqs = concepts[node]["prerequisites"]
        valid_prereqs = []
        for p in prereqs:
            if p in stack:
                # Remove edge
                removed_edges.append((node, p))
                continue
            if p not in visited:
                dfs(p)
            valid_prereqs.append(p)
            
        concepts[node]["prerequisites"] = valid_prereqs
        stack.remove(node)

    for cid in list(concepts.keys()):
        if cid not in visited:
            dfs(cid)
            
    if removed_edges:
        print(f"Removed {len(removed_edges)} cyclic prerequisite edges:")
        for u, v in removed_edges:
            print(f"  {u} -> {v}")

if __name__ == "__main__":
    build_knowledge_graph()
