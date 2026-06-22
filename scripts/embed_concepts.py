import json
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONCEPTS_DIR = PROJECT_ROOT / "corpus_data" / "concepts"
CHROMA_DIR = PROJECT_ROOT / "corpus_data" / "chromadb"

def embed_all_concepts():
    print("Initializing Embedding Pipeline...")
    
    # 1. Imports inside function to avoid startup delays
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("ERROR: sentence-transformers is not installed. Run: pip install sentence-transformers")
        sys.exit(1)
        
    try:
        import chromadb
    except ImportError:
        print("ERROR: chromadb is not installed. Run: pip install chromadb")
        sys.exit(1)
        
    # 2. Load model
    print("Loading SentenceTransformer model BAAI/bge-small-en-v1.5...")
    # This will download/load the model
    model = SentenceTransformer('BAAI/bge-small-en-v1.5')
    
    # 3. Connect to ChromaDB
    print(f"Connecting to ChromaDB persistent storage at {CHROMA_DIR}...")
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    
    # Get or create collection
    # Note: We specify a default L2 distance space or cosine space. bge-small is typically cosine.
    collection = chroma_client.get_or_create_collection(
        name="concepts", 
        metadata={"hnsw:space": "cosine"}
    )
    
    # 4. Read all concept JSON files
    concept_files = list(CONCEPTS_DIR.glob("*.json"))
    if not concept_files:
        print("ERROR: No concept JSON files found. Run generate_concepts.py first.")
        sys.exit(1)
        
    documents = []
    ids = []
    metadatas = []
    
    for file_path in concept_files:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Skipping {file_path.name} due to parse error: {e}")
                continue
                
        # Construct the text representation to embed — lead with term name for BGE alignment
        term = data.get("term", "")
        definition = data.get("definition", "")
        simple_exp = data.get("simple_explanation", "")
        subdomain = data.get("subdomain", "")
        related = ", ".join(data.get("related_terms", [])[:4])  # top 4 related terms
        prereqs = ", ".join(data.get("prerequisites", [])[:4])
        
        # BGE passage-side text: term + subdomain + definition + simple explanation
        doc_text = (
            f"{term}. "
            f"Subdomain: {subdomain}. "
            f"Definition: {definition} "
            f"Explanation: {simple_exp}"
        )
        if prereqs:
            doc_text += f" Prerequisites: {prereqs}."
        if related:
            doc_text += f" Related concepts: {related}."
        
        # Serialize list metadata fields as comma-separated strings to avoid schema errors across ChromaDB versions
        prereqs = ",".join(data.get("prerequisites", []))
        related = ",".join(data.get("related_terms", []))
        
        metadata = {
            "term": term,
            "domain": data.get("domain", "AI"),
            "subdomain": data.get("subdomain", ""),
            "difficulty": data.get("difficulty", "Intermediate"),
            "prerequisites": prereqs,
            "related_terms": related
        }
        
        documents.append(doc_text)
        ids.append(data["id"])
        metadatas.append(metadata)
        
    # 5. Generate embeddings in batches with normalization
    print(f"Generating embeddings for {len(documents)} concepts...")
    embeddings = model.encode(documents, show_progress_bar=True, normalize_embeddings=True)
    
    # Convert embeddings from numpy array to list for ChromaDB
    embeddings_list = [emb.tolist() for emb in embeddings]
    
    # 6. Store in ChromaDB
    print("indexing into ChromaDB...")
    collection.upsert(
        ids=ids,
        embeddings=embeddings_list,
        metadatas=metadatas,
        documents=documents
    )
    
    print(f"Embedding pipeline completed successfully. Indexed {len(ids)} concepts.")

if __name__ == "__main__":
    embed_all_concepts()
