import chromadb
from pathlib import Path

CHROMA_DIR = Path("d:/Corpus/corpus_data/chromadb")
client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_collection("concepts")

print(f"Total documents in collection: {collection.count()}")
all_data = collection.get()
print("All IDs:")
print(all_data["ids"])

print("\nAll Subdomains in database:")
subdomains = set(m.get("subdomain") for m in all_data["metadatas"] if m)
print(subdomains)

print("\nLet's test query directly with where filter:")
res = collection.query(
    query_embeddings=[[0.1] * 384],
    n_results=5,
    where={"subdomain": "Agentic AI"}
)
print("Query results with filter:")
print(res)
