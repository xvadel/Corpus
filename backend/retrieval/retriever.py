import re
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CHROMA_DIR = PROJECT_ROOT / "corpus_data" / "chromadb"

# BGE instruction prefix for asymmetric search queries (required for bge-small-en-v1.5)
BGE_QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "

def _normalize_query(query: str) -> str:
    """Normalize query text: strip punctuation, lowercase, remove extra spaces."""
    query = query.strip()
    query = re.sub(r'[^\w\s\-]', '', query)  # strip non-word chars except hyphens
    query = re.sub(r'\s+', ' ', query)
    return query.lower()

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

    def retrieve(
        self,
        query: str,
        limit: int = 5,
        where: dict = None,
        rerank: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Embeds the query (with BGE instruction prefix) and retrieves similar concepts from ChromaDB.
        Optional metadata filtering can be passed via the `where` parameter.
        If `rerank` is True, performs a two-stage retrieval using a Cross-Encoder to re-score
        a larger pool of candidates.
        """
        if rerank:
            # Stage 1: Fetch a larger candidate set using vector retrieval
            candidate_limit = max(limit * 3, 15)
            candidates = self.retrieve(query, limit=candidate_limit, where=where, rerank=False)
            
            # Stage 2: Rerank the candidates
            if not hasattr(self, "_reranker") or self._reranker is None:
                from backend.retrieval.reranker import CrossEncoderReranker
                self._reranker = CrossEncoderReranker()
            
            return self._reranker.rerank(query, candidates, top_k=limit)

        # Apply instruction prefix required by BAAI/bge-small-en-v1.5 for query encoding
        normalized = _normalize_query(query)
        prefixed_query = BGE_QUERY_INSTRUCTION + normalized
        query_vector = self.model.encode(prefixed_query, normalize_embeddings=True).tolist()
        
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

