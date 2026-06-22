from typing import List, Dict, Any

class ContextBuilder:
    @staticmethod
    def build_context(retrieved_concepts: List[Dict[str, Any]]) -> str:
        """
        Formats retrieved concepts from ChromaDB into a structured string block.
        """
        if not retrieved_concepts:
            return "No relevant concepts retrieved."
            
        context_parts = []
        for item in retrieved_concepts:
            metadata = item["metadata"]
            term = metadata.get("term", item["id"])
            subdomain = metadata.get("subdomain", "")
            difficulty = metadata.get("difficulty", "")
            doc = item["document"]
            
            part = (
                f"- Concept: {term} (Subdomain: {subdomain}, Level: {difficulty})\n"
                f"  Details:\n"
                f"  {doc.strip()}\n"
            )
            context_parts.append(part)
            
        return "\n".join(context_parts)
