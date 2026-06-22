"""
Corpus — Concept Content Enrichment
======================================
Regenerates the definition, simple_explanation, and technical_explanation fields
for all concepts in corpus_data/concepts/ using the LLM provider.

Template-generated content like "A fundamental concept in X under Y, representing Z."
is replaced with real semantic definitions that improve embedding quality.

Usage:
    python scripts/enrich_concept_content.py [--limit N] [--dry-run] [--concept-id ID]

Options:
    --limit N       Process only the first N concepts (for testing).
    --dry-run       Show what would be generated without writing files.
    --concept-id    Process a single concept by ID.
"""

import json
import sys
import time
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

CONCEPTS_DIR = PROJECT_ROOT / "corpus_data" / "concepts"

# Detection heuristic: template content always contains this pattern
TEMPLATE_MARKERS = [
    "A fundamental concept in",
    "Think of {term} as an essential building block",
    "plays a key role within",
    "Robust configuration of"
]

ENRICHMENT_PROMPT = """You are an expert AI/ML educator writing a knowledge base for software engineers learning AI Engineering concepts.

Write a rich, accurate, semantically dense description for the concept: **{term}**

Requirements:
- definition (1-2 sentences): precise technical definition. Include alternative names or acronyms if applicable.
- simple_explanation (2-3 sentences): an analogy or plain-english explanation a junior engineer can understand. Be concrete and specific.
- technical_explanation (2-3 sentences): how it works under the hood, key mechanisms, and engineering trade-offs.

Respond ONLY with valid JSON in this exact format:
{{
  "definition": "...",
  "simple_explanation": "...",
  "technical_explanation": "..."
}}

Context:
- Subdomain: {subdomain}
- Category: {category}
- Prerequisites: {prerequisites}
- Related terms: {related_terms}
"""


def is_template_content(data: dict) -> bool:
    """Return True if the concept still has auto-generated template content."""
    definition = data.get("definition", "")
    for marker in TEMPLATE_MARKERS:
        term = data.get("term", "TERM")
        marker_filled = marker.replace("{term}", term)
        if marker_filled in definition:
            return True
        if "A fundamental concept in" in definition:
            return True
    return False


def enrich_concept(provider, data: dict) -> dict:
    """Use LLM to generate real definitions for a concept. Returns updated fields."""
    term        = data.get("term", "")
    subdomain   = data.get("subdomain", "")
    category    = data.get("category", "")
    prerequisites = ", ".join(data.get("prerequisites", [])) or "None"
    related     = ", ".join(data.get("related_terms", [])[:5]) or "None"

    prompt = ENRICHMENT_PROMPT.format(
        term=term,
        subdomain=subdomain,
        category=category,
        prerequisites=prerequisites,
        related_terms=related
    )

    response = provider.generate(prompt)

    # Extract JSON from the response
    text = response.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    enriched = json.loads(text)
    return {
        "definition":           enriched["definition"],
        "simple_explanation":   enriched["simple_explanation"],
        "technical_explanation":enriched["technical_explanation"],
    }


def main():
    parser = argparse.ArgumentParser(description="Enrich concept content with real definitions.")
    parser.add_argument("--limit",      type=int, default=None,  help="Process only first N concepts.")
    parser.add_argument("--dry-run",    action="store_true",     help="Print output without writing files.")
    parser.add_argument("--concept-id", type=str, default=None,  help="Enrich a single concept by ID.")
    parser.add_argument("--force",      action="store_true",     help="Re-enrich even non-template concepts.")
    parser.add_argument("--provider",   type=str, default="groq", choices=["gemini", "groq"], help="LLM provider (default: groq)")
    args = parser.parse_args()

    # Load LLM provider
    provider_name = args.provider.lower()
    if provider_name == "gemini":
        try:
            from backend.providers.gemini import GeminiProvider
            provider = GeminiProvider()
            print("Using GeminiProvider.")
        except Exception as e:
            print(f"ERROR: Could not load GeminiProvider: {e}")
            sys.exit(1)
    elif provider_name == "groq":
        try:
            from backend.providers.groq_provider import GroqProvider
            provider = GroqProvider()
            print("Using GroqProvider.")
        except Exception as e:
            print(f"ERROR: Could not load GroqProvider: {e}")
            sys.exit(1)
    else:
        print(f"ERROR: Unknown provider {provider_name}")
        sys.exit(1)

    # Gather target files
    if args.concept_id:
        files = [CONCEPTS_DIR / f"{args.concept_id}.json"]
    else:
        files = sorted(CONCEPTS_DIR.glob("*.json"))

    if args.limit:
        files = files[:args.limit]

    enriched_count = 0
    skipped_count  = 0
    error_count    = 0

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        term = data.get("term", file_path.stem)

        if not args.force and not is_template_content(data):
            print(f"  SKIP  {term} (already has real content)")
            skipped_count += 1
            continue

        print(f"  ENRICH {term} ...", end="", flush=True)
        try:
            updates = enrich_concept(provider, data)

            if args.dry_run:
                print(f"\n    definition: {updates['definition'][:80]}...")
                print(f"    simple_exp: {updates['simple_explanation'][:80]}...")
            else:
                data.update(updates)
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(" done")

            enriched_count += 1
            # Small delay to avoid rate limiting
            time.sleep(0.5)

        except Exception as e:
            print(f" ERROR: {e}")
            error_count += 1
            time.sleep(1)

    print(f"\nContent enrichment complete.")
    print(f"  Enriched : {enriched_count}")
    print(f"  Skipped  : {skipped_count} (already had real content)")
    print(f"  Errors   : {error_count}")

    if not args.dry_run and enriched_count > 0:
        print("\nNext step: re-run scripts/embed_concepts.py to re-index with improved content.")


if __name__ == "__main__":
    main()
