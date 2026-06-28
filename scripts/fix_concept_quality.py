"""
Corpus — Concept Quality Fixer
================================
Deterministic (no LLM) cleanup pass over all concept JSON files in corpus_data/concepts/.

Fixes:
  1. Removes self-referencing entries from related_terms (concept lists itself)
  2. Removes subdomain/category strings from related_terms (should be concept names only)
  3. Removes subdomain/category strings from prerequisites (should be concept names only)
  4. Populates empty references[] with curated academic references for key concepts
  5. Ensures category field is present (backfills from seed CSV if missing)

Usage:
    python scripts/fix_concept_quality.py [--dry-run] [--concept-id ID]
"""

import json
import csv
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONCEPTS_DIR = PROJECT_ROOT / "corpus_data" / "concepts"
SEED_CSV     = PROJECT_ROOT / "corpus_data" / "ontology" / "concepts_seed.csv"

# ---------------------------------------------------------------------------
# Curated references for landmark concepts (arXiv / official docs / papers)
# ---------------------------------------------------------------------------
CURATED_REFERENCES = {
    "attention":                ["https://arxiv.org/abs/1706.03762"],
    "self_attention":           ["https://arxiv.org/abs/1706.03762"],
    "multi_head_attention":     ["https://arxiv.org/abs/1706.03762"],
    "transformer":              ["https://arxiv.org/abs/1706.03762"],
    "encoder":                  ["https://arxiv.org/abs/1706.03762"],
    "decoder":                  ["https://arxiv.org/abs/1706.03762"],
    "positional_encoding":      ["https://arxiv.org/abs/1706.03762"],
    "bert":                     ["https://arxiv.org/abs/1810.04805"],
    "masked_language_model":    ["https://arxiv.org/abs/1810.04805"],
    "gpt":                      ["https://openai.com/research/language-unsupervised"],
    "autoregressive_model":     ["https://arxiv.org/abs/2005.14165"],
    "language_model":           ["https://arxiv.org/abs/2005.14165"],
    "embedding":                ["https://arxiv.org/abs/1301.3666", "https://arxiv.org/abs/1706.03762"],
    "word_embedding":           ["https://arxiv.org/abs/1301.3666"],
    "retrieval_augmented_generation": ["https://arxiv.org/abs/2005.11401"],
    "lora":                     ["https://arxiv.org/abs/2106.09685"],
    "qlora":                    ["https://arxiv.org/abs/2305.14314"],
    "rlhf":                     ["https://arxiv.org/abs/2203.02155"],
    "dpo":                      ["https://arxiv.org/abs/2305.18290"],
    "ppo":                      ["https://arxiv.org/abs/1707.06347"],
    "rlaif":                    ["https://arxiv.org/abs/2309.00267"],
    "peft":                     ["https://arxiv.org/abs/2106.09685", "https://github.com/huggingface/peft"],
    "instruction_tuning":       ["https://arxiv.org/abs/2109.01652"],
    "fine_tuning":              ["https://arxiv.org/abs/1801.06146"],
    "transfer_learning":        ["https://arxiv.org/abs/1411.1792"],
    "backpropagation":          ["https://www.nature.com/articles/323533a0"],
    "gradient_descent":         ["https://arxiv.org/abs/1412.6980"],
    "batch_normalization":      ["https://arxiv.org/abs/1502.03167"],
    "dropout":                  ["https://jmlr.org/papers/v15/srivastava14a.html"],
    "chromadb":                 ["https://docs.trychroma.com/"],
    "faiss":                    ["https://arxiv.org/abs/1702.08734"],
    "pinecone":                 ["https://docs.pinecone.io/"],
    "milvus":                   ["https://milvus.io/docs"],
    "weaviate":                 ["https://weaviate.io/developers/weaviate"],
    "bm25":                     ["https://dl.acm.org/doi/10.1561/1500000019"],
    "approximate_nearest_neighbor": ["https://arxiv.org/abs/1702.08734"],
    "cosine_similarity":        ["https://en.wikipedia.org/wiki/Cosine_similarity"],
    "byte_pair_encoding":       ["https://arxiv.org/abs/1508.07909"],
    "tokenization":             ["https://arxiv.org/abs/1508.07909"],
    "chain_of_thought":         ["https://arxiv.org/abs/2201.11903"],
    "few_shot_learning":        ["https://arxiv.org/abs/2005.14165"],
    "react_pattern":            ["https://arxiv.org/abs/2210.03629"],
    "ragas":                    ["https://arxiv.org/abs/2309.15217"],
    "deepeval":                 ["https://github.com/confident-ai/deepeval"],
    "langchain":                ["https://python.langchain.com/docs/get_started/introduction"],
    "llamaindex":               ["https://docs.llamaindex.ai/"],
    "langgraph":                ["https://langchain-ai.github.io/langgraph/"],
    "crewai":                   ["https://docs.crewai.com/"],
    "litellm":                  ["https://docs.litellm.ai/"],
    "mlflow":                   ["https://mlflow.org/docs/latest/index.html"],
    "weights_and_biases":       ["https://docs.wandb.ai/"],
    "kubeflow":                 ["https://www.kubeflow.org/docs/"],
    "airflow":                  ["https://airflow.apache.org/docs/"],
    "linear_regression":        ["https://en.wikipedia.org/wiki/Linear_regression"],
    "logistic_regression":      ["https://en.wikipedia.org/wiki/Logistic_regression"],
    "decision_trees":           ["https://en.wikipedia.org/wiki/Decision_tree_learning"],
    "random_forest":            ["https://link.springer.com/article/10.1023/A:1010933404324"],
    "gradient_boosting":        ["https://arxiv.org/abs/1603.02754"],
    "xgboost":                  ["https://arxiv.org/abs/1603.02754"],
    "support_vector_machine":   ["https://link.springer.com/article/10.1007/BF00994018"],
    "pca":                      ["https://royalsocietypublishing.org/doi/10.1098/rsta.1933.0009"],
    "t_sne":                    ["https://jmlr.org/papers/v9/vandermaaten08a.html"],
    "umap":                     ["https://arxiv.org/abs/1802.03426"],
    "k_means":                  ["https://en.wikipedia.org/wiki/K-means_clustering"],
    "dbscan":                   ["https://dl.acm.org/doi/10.1145/3299869.3319876"],
    "markov_decision_process":  ["https://en.wikipedia.org/wiki/Markov_decision_process"],
    "q_learning":               ["https://link.springer.com/article/10.1007/BF00992698"],
    "deep_q_networks":          ["https://arxiv.org/abs/1312.5602"],
    "policy_gradient":          ["https://papers.nips.cc/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html"],
    "actor_critic":             ["https://arxiv.org/abs/1602.01783"],
    "convolution":              ["https://arxiv.org/abs/1998.01448"],
    "resnet":                   ["https://arxiv.org/abs/1512.03385"],
    "yolo":                     ["https://arxiv.org/abs/1506.02640"],
    "efficientnet":             ["https://arxiv.org/abs/1905.11946"],
    "vision_transformer":       ["https://arxiv.org/abs/2010.11929"],
    "lstm":                     ["https://www.bioinf.jku.at/publications/older/2604.pdf"],
    "gru":                      ["https://arxiv.org/abs/1412.3555"],
    "bi_encoder":               ["https://arxiv.org/abs/1908.10084"],
    "cross_encoder":            ["https://arxiv.org/abs/1910.14424"],
    "reciprocal_rank_fusion":   ["https://dl.acm.org/doi/10.1145/1571941.1572114"],
    "hybrid_search":            ["https://arxiv.org/abs/2210.07316"],
    "reranking":                ["https://arxiv.org/abs/1910.14424"],
    "semantic_similarity":      ["https://arxiv.org/abs/1908.10084"],
    "vector_representation":    ["https://arxiv.org/abs/1301.3666"],
    "grounding":                ["https://arxiv.org/abs/2005.11401"],
    "hallucination":            ["https://arxiv.org/abs/2202.03629"],
    "context_window":           ["https://arxiv.org/abs/2307.03172"],
    "function_calling":         ["https://platform.openai.com/docs/guides/function-calling"],
    "multi_agent_system":       ["https://arxiv.org/abs/2308.08155"],
    "agent":                    ["https://arxiv.org/abs/2210.03629"],
    "workflow_orchestration":   ["https://arxiv.org/abs/2308.08155"],
    "model_serving":            ["https://arxiv.org/abs/1712.09355"],
    "drift_detection":          ["https://arxiv.org/abs/2204.09882"],
    "sentence_window_retrieval":["https://arxiv.org/abs/2312.10997"],
    "auto_merging_retrieval":   ["https://arxiv.org/abs/2312.10997"],
    "overfitting":              ["https://en.wikipedia.org/wiki/Overfitting"],
    "regularization":           ["https://en.wikipedia.org/wiki/Regularization_(mathematics)"],
    "dimensionality_reduction": ["https://en.wikipedia.org/wiki/Dimensionality_reduction"],
    "sequence_modeling":        ["https://arxiv.org/abs/1409.3215"],
    "image_segmentation":       ["https://arxiv.org/abs/1505.04597"],
    "feature_extraction":       ["https://en.wikipedia.org/wiki/Feature_extraction"],
    "knowledge_base":           ["https://arxiv.org/abs/2005.11401"],
    "chunking":                 ["https://arxiv.org/abs/2312.10997"],
    "document_parsing":         ["https://arxiv.org/abs/2408.09869"],
    "metadata_extraction":      ["https://arxiv.org/abs/2408.09869"],
    "answer_synthesis":         ["https://arxiv.org/abs/2005.11401"],
    "context_injection":        ["https://arxiv.org/abs/2005.11401"],
    "model_evaluation":         ["https://arxiv.org/abs/2009.03300"],
    "benchmarking":             ["https://arxiv.org/abs/2009.03300"],
    "accuracy":                 ["https://en.wikipedia.org/wiki/Accuracy_and_precision"],
    "faithfulness":             ["https://arxiv.org/abs/2309.15217"],
    "latency":                  ["https://en.wikipedia.org/wiki/Latency_(engineering)"],
    "scalability":              ["https://en.wikipedia.org/wiki/Scalability"],
    "caching":                  ["https://en.wikipedia.org/wiki/Cache_(computing)"],
    "load_balancing":           ["https://en.wikipedia.org/wiki/Load_balancing_(computing)"],
    "api_design":               ["https://swagger.io/specification/"],
    "semantic_router":          ["https://github.com/aurelio-labs/semantic-router"],
    "guardrails":               ["https://github.com/guardrails-ai/guardrails"],
    "data_pipeline":            ["https://en.wikipedia.org/wiki/Pipeline_(computing)"],
    "data_validation":          ["https://greatexpectations.io/"],
    "dataset_versioning":       ["https://dvc.org/doc/start"],
    "deployment":               ["https://en.wikipedia.org/wiki/Software_deployment"],
    "monitoring":               ["https://en.wikipedia.org/wiki/Application_performance_management"],
    "training":                 ["https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets"],
    "loss_function":            ["https://en.wikipedia.org/wiki/Loss_function"],
    "activation_function":      ["https://en.wikipedia.org/wiki/Activation_function"],
    "perceptron":               ["https://en.wikipedia.org/wiki/Perceptron"],
    "feed_forward_network":     ["https://en.wikipedia.org/wiki/Feedforward_neural_network"],
    "next_token_prediction":    ["https://arxiv.org/abs/2005.14165"],
    "prompt_engineering":       ["https://arxiv.org/abs/2302.11382"],
    "zero_shot":                ["https://arxiv.org/abs/2005.14165"],
    "one_shot":                 ["https://arxiv.org/abs/2005.14165"],
    "few_shot":                 ["https://arxiv.org/abs/2005.14165"],
    "role_prompting":           ["https://arxiv.org/abs/2302.11382"],
    "structured_prompting":     ["https://arxiv.org/abs/2302.11382"],
    "tool_calling":             ["https://platform.openai.com/docs/guides/function-calling"],
    "tool_use":                 ["https://arxiv.org/abs/2210.03629"],
    "memory":                   ["https://arxiv.org/abs/2304.01373"],
    "planner":                  ["https://arxiv.org/abs/2210.03629"],
    "similarity_search":        ["https://arxiv.org/abs/1702.08734"],
    "top_k_retrieval":          ["https://arxiv.org/abs/2005.11401"],
    "stop_words":               ["https://en.wikipedia.org/wiki/Stop_word"],
    "stemming":                 ["https://en.wikipedia.org/wiki/Stemming"],
    "lemmatization":            ["https://en.wikipedia.org/wiki/Lemmatisation"],
    "named_entity_recognition": ["https://arxiv.org/abs/1810.04805"],
    "vector_database":          ["https://arxiv.org/abs/2309.07990"],
    "image_classification":     ["https://arxiv.org/abs/1512.03385"],
    "object_detection":         ["https://arxiv.org/abs/1506.02640"],
    "pooling":                  ["https://arxiv.org/abs/1512.03385"],
    "feature_maps":             ["https://arxiv.org/abs/1512.03385"],
    "hierarchical_clustering":  ["https://en.wikipedia.org/wiki/Hierarchical_clustering"],
    "clustering":               ["https://en.wikipedia.org/wiki/Cluster_analysis"],
    "k_nearest_neighbors":      ["https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm"],
    "reward_function":          ["https://en.wikipedia.org/wiki/Reinforcement_learning"],
    "policy_gradient":          ["https://papers.nips.cc/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html"],
}

# Terms that should NOT appear as related_terms or prerequisites (subdomains/categories)
INVALID_RELATION_TERMS = {
    # Subdomains
    "natural language processing", "retrieval augmented generation", "agentic ai",
    "ai engineering", "mlops", "deep learning foundations", "machine learning",
    "computer vision", "deep learning",
    # Categories
    "text processing", "language modeling", "llms", "data processing", "embeddings",
    "vector databases", "retrieval", "generation", "core concepts", "prompt engineering",
    "model adaptation", "system design", "evaluation", "orchestration", "data management",
    "model lifecycle", "tools", "neural networks", "transformers", "cnn", "rnn",
    "supervised learning", "unsupervised learning", "reinforcement learning",
    "image processing", "models",
    # Domain
    "ai", "artificial intelligence",
}


def load_seed_category_map() -> dict:
    """Return {concept_id: category} from the seed CSV."""
    mapping = {}
    try:
        with open(SEED_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                mapping[row["id"]] = row.get("category", "")
    except FileNotFoundError:
        pass
    return mapping


def clean_relation_list(items: list, concept_term: str) -> list:
    """Remove self-references and subdomain/category strings from a list."""
    seen = set()
    cleaned = []
    for item in items:
        item_lower = item.strip().lower()
        if item_lower == concept_term.lower():
            continue  # self-reference
        if item_lower in INVALID_RELATION_TERMS:
            continue  # subdomain/category string
        if item_lower in seen:
            continue  # duplicate
        seen.add(item_lower)
        cleaned.append(item)
    return cleaned


def fix_concept(file_path: Path, seed_map: dict, dry_run: bool = False) -> bool:
    """Apply all quality fixes to a single concept file. Returns True if changed."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    changed = False
    concept_id = data.get("id", file_path.stem)
    term = data.get("term", concept_id)

    # 1 & 2. Clean related_terms
    old_related = data.get("related_terms", [])
    new_related = clean_relation_list(old_related, term)
    if new_related != old_related:
        data["related_terms"] = new_related
        changed = True
        print(f"  [related_terms] {term}: {len(old_related)} -> {len(new_related)} entries")

    # 3. Clean prerequisites
    old_prereqs = data.get("prerequisites", [])
    new_prereqs = clean_relation_list(old_prereqs, term)
    if new_prereqs != old_prereqs:
        data["prerequisites"] = new_prereqs
        changed = True
        print(f"  [prerequisites] {term}: {len(old_prereqs)} -> {len(new_prereqs)} entries")

    # 4. Populate empty references
    if not data.get("references"):
        refs = CURATED_REFERENCES.get(concept_id, [])
        if refs:
            data["references"] = refs
            changed = True
            print(f"  [references]    {term}: added {len(refs)} reference(s)")

    # 5. Backfill missing category from seed CSV
    if not data.get("category") and concept_id in seed_map:
        data["category"] = seed_map[concept_id]
        changed = True
        print(f"  [category]      {term}: backfilled from seed")

    if changed and not dry_run:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return changed


def main():
    parser = argparse.ArgumentParser(description="Fix concept quality issues deterministically.")
    parser.add_argument("--dry-run",    action="store_true", help="Show changes without writing.")
    parser.add_argument("--concept-id", type=str, default=None, help="Fix a single concept by ID.")
    args = parser.parse_args()

    seed_map = load_seed_category_map()

    if args.concept_id:
        files = [CONCEPTS_DIR / f"{args.concept_id}.json"]
    else:
        files = sorted(CONCEPTS_DIR.glob("*.json"))

    fixed = 0
    unchanged = 0

    print(f"Quality fix pass — {'DRY RUN' if args.dry_run else 'WRITING'}")
    print(f"Processing {len(files)} concept files...\n")

    for fp in files:
        if not fp.exists():
            print(f"  WARNING: {fp.name} not found")
            continue
        if fix_concept(fp, seed_map, dry_run=args.dry_run):
            fixed += 1
        else:
            unchanged += 1

    print(f"\nDone. Fixed: {fixed}  Unchanged: {unchanged}")
    if args.dry_run:
        print("(Dry run — no files were written)")


if __name__ == "__main__":
    main()
