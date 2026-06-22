import json
from pathlib import Path
from typing import List, Dict, Any, Set

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
GRAPH_FILE = PROJECT_ROOT / "corpus_data" / "ontology" / "knowledge_graph.json"

class LearningPathBuilder:
    def __init__(self, graph_path: str = str(GRAPH_FILE)):
        self.graph_path = Path(graph_path)
        self.concepts = {}
        self.load_graph()

    def load_graph(self):
        if self.graph_path.exists():
            with open(self.graph_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.concepts = data.get("concepts", {})
        else:
            self.concepts = {}

    def get_all_prerequisites_recursive(self, concept_id: str, visited: Set[str] = None) -> Set[str]:
        """
        Recursively finds all prerequisite concept IDs (ancestors) for a given concept.
        """
        if visited is None:
            visited = set()
            
        if concept_id not in self.concepts:
            return visited
            
        prereqs = self.concepts[concept_id].get("prerequisites", [])
        for p in prereqs:
            if p not in visited:
                visited.add(p)
                self.get_all_prerequisites_recursive(p, visited)
        return visited

    def build_path_for_concept(self, target_concept_id: str) -> List[Dict[str, Any]]:
        """
        Generates an ordered list of concepts to learn in order to master the target concept.
        Uses topological sort on the dependencies.
        """
        if target_concept_id not in self.concepts:
            return []
            
        # Get all required nodes (target + its ancestors)
        required_nodes = self.get_all_prerequisites_recursive(target_concept_id)
        required_nodes.add(target_concept_id)
        
        # Build dependency subgraph
        dependencies = {node: list(self.concepts[node].get("prerequisites", [])) for node in required_nodes}
        # Filter dependencies to only include nodes in our required set
        for node in dependencies:
            dependencies[node] = [p for p in dependencies[node] if p in required_nodes]
            
        # Topological Sort using DFS post-order traversal
        visited = set()
        stack = []
        
        def dfs(node):
            visited.add(node)
            for neighbor in dependencies.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(node)
            
        for node in required_nodes:
            if node not in visited:
                dfs(node)
                
        # Stack now contains nodes sorted topologically ( leaf dependencies first )
        path = []
        for cid in stack:
            cdata = self.concepts[cid]
            path.append({
                "id": cid,
                "term": cdata["term"],
                "difficulty": cdata["difficulty"],
                "subdomain": cdata["subdomain"]
            })
        return path
