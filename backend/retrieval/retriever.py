import os
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CHROMA_DIR = PROJECT_ROOT / "corpus_data" / "chromadb"

class VectorRetriever:
    def __init__(self, path: str = str(CHROMA_DIR), collection_name: str = "concepts"):
        # Import chromadb and sentence-transformers locally to keep FastAPI startup fast
        import chromadb
        from sentence_transformers import SentenceTransformer
        
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        self.model = SentenceTransformer('BAAI/bge-small-en-v1.5')

    def retrieve(self, query: str, limit: int = 5, where: dict = None) -> List[Dict[str, Any]]:
        """
        Embeds the query and retrieves similar concepts from ChromaDB.
        Optional metadata filtering can be passed via the `where` parameter.
        """
        query_vector = self.model.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=limit,
            where=where
        )
        
        retrieved = []
        if results and results.get("ids") and results["ids"][0]:
            ids = results["ids"][0]
            metadatas = results["metadatas"][0]
            documents = results["documents"][0]
            distances = results["distances"][0] if "distances" in results else [0.0] * len(ids)
            
            for i in range(len(ids)):
                retrieved.append({
                    "id": ids[i],
                    "metadata": metadatas[i],
                    "document": documents[i],
                    "distance": distances[i]
                })
        return retrieved
