"""
Corpus — Concept Dependency Enrichment
========================================
Writes precise, concept-to-concept prerequisite relationships into
corpus_data/concepts/*.json files.

Run ONCE after initial concept generation and BEFORE build_knowledge_graph.py.

Usage:
    python scripts/enrich_concept_dependencies.py
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONCEPTS_DIR = PROJECT_ROOT / "corpus_data" / "concepts"

# ---------------------------------------------------------------------------
# Curated prerequisite dependency map: { concept_id: [prerequisite_ids] }
# These are CONCEPT-TO-CONCEPT links (not subdomain strings).
# ---------------------------------------------------------------------------
DEPENDENCIES = {
    # ── Deep Learning Foundations ──────────────────────────────────────────
    "perceptron":          [],
    "activation_function": ["perceptron"],
    "loss_function":       ["perceptron"],
    "gradient_descent":    ["loss_function"],
    "backpropagation":     ["gradient_descent", "activation_function"],
    "feed_forward_network":["perceptron", "activation_function", "loss_function"],
    "attention":           ["feed_forward_network"],
    "self_attention":      ["attention"],
    "multi_head_attention":["self_attention"],
    "positional_encoding": ["attention"],
    "encoder":             ["multi_head_attention", "positional_encoding"],
    "decoder":             ["multi_head_attention", "positional_encoding"],
    "transformer":         ["encoder", "decoder"],
    "transfer_learning":   ["feed_forward_network", "training"],
    "training":            ["loss_function", "gradient_descent"],

    # ── Natural Language Processing ────────────────────────────────────────
    "tokenization":            [],
    "stemming":                ["tokenization"],
    "lemmatization":           ["tokenization"],
    "stop_words":              ["tokenization"],
    "byte_pair_encoding":      ["tokenization"],
    "named_entity_recognition":["tokenization", "language_model"],
    "language_model":          ["tokenization", "transformer"],
    "masked_language_model":   ["language_model", "transformer"],
    "autoregressive_model":    ["language_model", "transformer"],
    "next_token_prediction":   ["autoregressive_model", "tokenization"],

    # ── LLMs ──────────────────────────────────────────────────────────────
    "context_window":     ["language_model"],
    "hallucination":      ["language_model"],
    "prompt_engineering": ["language_model"],
    "chain_of_thought":   ["prompt_engineering"],
    "few_shot_learning":  ["prompt_engineering"],
    "few_shot":           ["prompt_engineering"],
    "one_shot":           ["prompt_engineering"],
    "zero_shot":          ["prompt_engineering"],
    "role_prompting":     ["prompt_engineering"],
    "structured_prompting":["prompt_engineering"],
    "function_calling":   ["language_model", "tool_calling"],
    "tool_calling":       ["language_model"],

    # ── Embeddings ────────────────────────────────────────────────────────
    "vector_representation":  ["feed_forward_network"],
    "embedding":              ["vector_representation", "transformer"],
    "cosine_similarity":      ["embedding"],
    "semantic_similarity":    ["cosine_similarity", "embedding"],

    # ── Vector Databases ──────────────────────────────────────────────────
    "approximate_nearest_neighbor": ["embedding", "cosine_similarity"],
    "vector_database":        ["embedding", "approximate_nearest_neighbor"],
    "chromadb":               ["vector_database"],
    "faiss":                  ["vector_database", "approximate_nearest_neighbor"],
    "pinecone":               ["vector_database"],
    "milvus":                 ["vector_database"],
    "weaviate":               ["vector_database"],

    # ── Retrieval ─────────────────────────────────────────────────────────
    "similarity_search":           ["embedding", "vector_database"],
    "top_k_retrieval":             ["similarity_search"],
    "bm25":                        ["tokenization", "stop_words"],
    "hybrid_search":               ["similarity_search", "bm25"],
    "bi_encoder":                  ["embedding", "similarity_search"],
    "cross_encoder":               ["bi_encoder", "embedding"],
    "reranking":                   ["similarity_search", "cross_encoder"],
    "reciprocal_rank_fusion":      ["hybrid_search", "reranking"],
    "approximate_nearest_neighbor":["embedding", "cosine_similarity"],

    # ── RAG Data Processing ───────────────────────────────────────────────
    "chunking":              ["tokenization"],
    "document_parsing":      ["tokenization"],
    "metadata_extraction":   ["document_parsing"],
    "knowledge_base":        ["document_parsing", "embedding"],
    "sentence_window_retrieval": ["chunking", "top_k_retrieval"],
    "auto_merging_retrieval":    ["chunking", "top_k_retrieval", "reranking"],

    # ── RAG Generation ────────────────────────────────────────────────────
    "context_injection":      ["prompt_engineering", "top_k_retrieval"],
    "grounding":              ["context_injection", "hallucination"],
    "answer_synthesis":       ["grounding", "language_model"],

    # ── Core RAG Concept ──────────────────────────────────────────────────
    "retrieval_augmented_generation": [
        "embedding", "vector_database", "chunking",
        "similarity_search", "context_injection", "language_model"
    ],

    # ── Agentic AI ────────────────────────────────────────────────────────
    "memory":               ["language_model"],
    "tool_use":             ["function_calling"],
    "planner":              ["chain_of_thought", "language_model"],
    "react_pattern":        ["planner", "tool_use"],
    "agent":                ["planner", "memory", "tool_use"],
    "multi_agent_system":   ["agent"],
    "workflow_orchestration":["multi_agent_system"],

    # ── Model Adaptation ──────────────────────────────────────────────────
    "fine_tuning":           ["training", "language_model"],
    "instruction_tuning":    ["fine_tuning"],
    "lora":                  ["fine_tuning"],
    "qlora":                 ["lora"],
    "rlhf":                  ["fine_tuning", "training"],
    "peft":                  ["fine_tuning", "lora"],
    "dpo":                   ["rlhf", "fine_tuning"],
    "ppo":                   ["rlhf"],
    "rlaif":                 ["rlhf", "dpo"],

    # ── AI Engineering / System Design ────────────────────────────────────
    "api_design":            [],
    "latency":               ["api_design"],
    "caching":               ["api_design", "latency"],
    "load_balancing":        ["api_design", "scalability"],
    "scalability":           ["api_design"],
    "model_serving":         ["api_design", "scalability", "latency"],
    "semantic_router":       ["embedding", "similarity_search"],
    "guardrails":            ["language_model", "prompt_engineering"],

    # ── Evaluation ────────────────────────────────────────────────────────
    "accuracy":              [],
    "faithfulness":          ["retrieval_augmented_generation", "grounding"],
    "benchmarking":          ["accuracy"],
    "ragas":                 ["faithfulness", "retrieval_augmented_generation"],
    "deepeval":              ["faithfulness", "benchmarking"],

    # ── Orchestration Tools ───────────────────────────────────────────────
    "litellm":               ["api_design", "model_serving"],
    "langchain":             ["retrieval_augmented_generation", "agent"],
    "llamaindex":            ["retrieval_augmented_generation", "embedding"],
    "langgraph":             ["langchain", "workflow_orchestration"],
    "crewai":                ["multi_agent_system"],

    # ── MLOps ─────────────────────────────────────────────────────────────
    "dataset_versioning":    [],
    "data_pipeline":         ["dataset_versioning"],
    "data_validation":       ["data_pipeline"],
    "deployment":            ["model_serving"],
    "monitoring":            ["deployment"],
    "drift_detection":       ["monitoring"],
    "mlflow":                ["training", "deployment"],
    "weights_and_biases":    ["training"],
}

def enrich_dependencies():
    updated = 0
    missing = 0
    for concept_id, prereq_ids in DEPENDENCIES.items():
        path = CONCEPTS_DIR / f"{concept_id}.json"
        if not path.exists():
            print(f"  MISSING file: {concept_id}.json")
            missing += 1
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Convert concept IDs to human-readable term names for the prerequisites list
        term_names = []
        for pid in prereq_ids:
            prereq_path = CONCEPTS_DIR / f"{pid}.json"
            if prereq_path.exists():
                with open(prereq_path, "r", encoding="utf-8") as pf:
                    pdata = json.load(pf)
                    term_names.append(pdata["term"])
            else:
                print(f"  WARNING: prerequisite '{pid}' not found for '{concept_id}'")

        data["prerequisites"] = term_names
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        updated += 1

    print(f"\nDependency enrichment complete.")
    print(f"  Updated : {updated} concept files")
    print(f"  Missing : {missing} concept files not found")

if __name__ == "__main__":
    enrich_dependencies()
