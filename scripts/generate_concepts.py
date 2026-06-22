"""
Corpus Concept Generator
========================
Reads concepts_seed.csv and uses the Gemini API to generate rich,
structured JSON definitions for each concept.

Output: corpus_data/concepts/<id>.json

Usage (from project root, with venv activated):
    python scripts/generate_concepts.py

    # Dry-run (no API calls, print prompts only)
    python scripts/generate_concepts.py --dry-run

    # Process only one subdomain
    python scripts/generate_concepts.py --subdomain "Retrieval Augmented Generation"

    # Resume from last checkpoint (skips already-generated files)
    python scripts/generate_concepts.py --skip-existing

    # Limit to N concepts (useful for testing)
    python scripts/generate_concepts.py --limit 5

Environment variables required:
    GEMINI_API_KEY   — your Google AI Studio key (set in .env)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SEED_CSV     = PROJECT_ROOT / "corpus_data" / "ontology" / "concepts_seed.csv"
OUTPUT_DIR   = PROJECT_ROOT / "corpus_data" / "concepts"
SCHEMA_FILE  = PROJECT_ROOT / "corpus_data" / "ontology" / "ontology.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------------
def _get_model():
    """Initialise and return a Gemini GenerativeModel instance."""
    try:
        import google.generativeai as genai
    except ImportError:
        print("WARNING: google-generativeai is not installed.")
        print("Falling back to simulated/mock concept generation.")
        return None

    try:
        import dotenv
        dotenv.load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("WARNING: GEMINI_API_KEY is not set or is placeholder.")
        print("Falling back to simulated/mock concept generation.")
        return None

    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        print(f"WARNING: Failed to configure Gemini client: {e}")
        print("Falling back to simulated/mock concept generation.")
        return None


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------
CONCEPT_SCHEMA_EXAMPLE = {
    "id": "<snake_case_id>",
    "domain": "AI",
    "subdomain": "<subdomain>",
    "category": "<category>",
    "term": "<term>",
    "difficulty": "<Beginner|Intermediate|Advanced>",
    "definition": "One-sentence technical definition.",
    "simple_explanation": "Explain it to a smart 14-year-old in 2-3 sentences.",
    "technical_explanation": "Explain it precisely as you would to a senior AI engineer (3-5 sentences).",
    "investor_explanation": "Explain it as a one-paragraph pitch to a VC investor — why does it matter commercially?",
    "examples": [
        "Example usage sentence 1.",
        "Example usage sentence 2.",
        "Example usage sentence 3."
    ],
    "related_terms": ["term1", "term2", "term3"],
    "prerequisites": ["prereq1", "prereq2"],
    "references": ["https://arxiv.org/abs/..."],
    "interview_questions": [
        "Likely interview question 1?",
        "Likely interview question 2?",
        "Likely interview question 3?"
    ],
    "common_mistakes": [
        "Common misconception or mistake 1.",
        "Common misconception or mistake 2."
    ]
}


def build_prompt(concept: dict) -> str:
    schema_str = json.dumps(CONCEPT_SCHEMA_EXAMPLE, indent=2)
    return f"""You are an expert AI educator and technical writer for Corpus, 
an AI-powered career communication platform for AI engineers and GenAI developers.

Generate a complete, rich knowledge entry for the following AI/ML concept.

Concept details:
  - Term: {concept['term']}
  - Domain: {concept['domain']}
  - Subdomain: {concept['subdomain']}
  - Category: {concept['category']}
  - Difficulty: {concept['difficulty']}
  - ID: {concept['id']}

Return ONLY a valid JSON object matching this exact schema (no markdown, no code fences):
{schema_str}

Rules:
- Keep `id`, `domain`, `subdomain`, `category`, `term`, `difficulty` exactly as provided above.
- `definition`: precise, 1-sentence technical definition.
- `simple_explanation`: 2-3 sentences, no jargon, understandable by anyone.
- `technical_explanation`: 3-5 sentences for a senior AI engineer.
- `investor_explanation`: 2-4 sentences framed as a business/product insight for VCs.
- `examples`: 3 realistic sentences an AI engineer might say in a technical interview or design review.
- `related_terms`: 3-6 closely related concept names (strings only).
- `prerequisites`: 2-4 concepts someone should understand first.
- `references`: 1-3 scientific reference URLs or papers (arXiv/docs) for further reading.
- `interview_questions`: 3 real interview questions that test understanding of this concept.
- `common_mistakes`: 2-3 misconceptions or errors practitioners frequently make.
- Output ONLY the raw JSON object. No explanation, no markdown.
"""


# ---------------------------------------------------------------------------
# Core generation loop
# ---------------------------------------------------------------------------
def load_seed(subdomain_filter: str | None = None) -> list[dict]:
    """Load concepts from the seed CSV, optionally filtered by subdomain."""
    with open(SEED_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if subdomain_filter:
        rows = [r for r in rows if r["subdomain"] == subdomain_filter]

    return rows


def generate_concept(model, concept: dict, retries: int = 3) -> dict:
    """Call Gemini and parse the returned JSON. Retries on failure."""
    prompt = build_prompt(concept)

    for attempt in range(1, retries + 1):
        try:
            response = model.generate_content(prompt)
            raw = response.text.strip()

            # Strip accidental markdown fences
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()

            data = json.loads(raw)
            return data

        except json.JSONDecodeError as e:
            print(f"  [attempt {attempt}] JSON parse error: {e}")
            if attempt < retries:
                time.sleep(2 ** attempt)
        except Exception as e:
            print(f"  [attempt {attempt}] API error: {e}")
            if attempt < retries:
                time.sleep(2 ** attempt)

    raise RuntimeError(f"Failed to generate concept '{concept['term']}' after {retries} attempts.")


def generate_mock_concept(concept: dict) -> dict:
    """Generate a clean, structured JSON placeholder for concept database verification."""
    term = concept["term"]
    subdomain = concept["subdomain"]
    category = concept["category"]
    difficulty = concept["difficulty"]

    return {
        "id": concept["id"],
        "domain": concept["domain"],
        "subdomain": subdomain,
        "category": category,
        "term": term,
        "difficulty": difficulty,
        "definition": f"A fundamental concept in {subdomain} under {category}, representing {term}.",
        "simple_explanation": f"Think of {term} as an essential building block of {subdomain}. It is commonly used within {category}.",
        "technical_explanation": f"In production {subdomain} systems, {term} plays a key role within {category}. Engineering implementations must account for scaling constraints and design trade-offs.",
        "investor_explanation": f"Robust configuration of {term} directly affects system efficiency and business-critical accuracy metrics, driving cost savings and higher end-user retention.",
        "examples": [
            f"We optimized {term} in our {subdomain} pipeline to improve performance.",
            f"Our team discussed the differences between {term} and alternative solutions.",
            f"Understanding {term} is highly beneficial when scaling our {category} capabilities."
        ],
        "related_terms": [term, subdomain, category],
        "prerequisites": [subdomain, category],
        "references": [],
        "interview_questions": [
            f"How does {term} fit into standard {subdomain} architectures?",
            f"What are the major engineering trade-offs when implementing {term}?",
            f"How do you debug common failure modes associated with {term}?"
        ],
        "common_mistakes": [
            f"Misconfiguring parameters for {term}, resulting in degraded quality.",
            f"Underestimating the computational cost or memory footprint of {term}."
        ]
    }


def save_concept(data: dict, concept_id: str) -> Path:
    """Write a concept JSON to corpus_data/concepts/<id>.json."""
    out_path = OUTPUT_DIR / f"{concept_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return out_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Corpus Concept Generator")
    parser.add_argument("--dry-run",       action="store_true",  help="Print prompts without calling the API")
    parser.add_argument("--skip-existing", action="store_true",  help="Skip concepts that already have output files")
    parser.add_argument("--subdomain",     type=str, default=None, help="Filter to a single subdomain")
    parser.add_argument("--limit",         type=int, default=None, help="Maximum number of concepts to process")
    parser.add_argument("--delay",         type=float, default=1.5, help="Seconds to wait between API calls (default: 1.5)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Load seed concepts
    concepts = load_seed(subdomain_filter=args.subdomain)
    if args.limit:
        concepts = concepts[:args.limit]

    print(f"Corpus Concept Generator")
    print(f"  Seed file : {SEED_CSV}")
    print(f"  Output dir: {OUTPUT_DIR}")
    print(f"  Concepts  : {len(concepts)}")
    print(f"  Dry run   : {args.dry_run}")
    print(f"  Skip existing: {args.skip_existing}")
    print()

    # Load Gemini model (skip in dry-run)
    model = None if args.dry_run else _get_model()

    ok, skipped, failed = 0, 0, 0

    for i, concept in enumerate(concepts, 1):
        concept_id = concept["id"]
        out_path = OUTPUT_DIR / f"{concept_id}.json"

        print(f"[{i:03d}/{len(concepts)}] {concept['term']} ({concept['subdomain']})")

        # Skip already-generated files if requested
        if args.skip_existing and out_path.exists():
            print(f"  -> skipped (already exists)")
            skipped += 1
            continue

        if args.dry_run:
            print(build_prompt(concept))
            print("-" * 60)
            continue

        try:
            if model is None:
                data = generate_mock_concept(concept)
            else:
                data = generate_concept(model, concept)
            save_concept(data, concept_id)
            print(f"  -> saved: {out_path.name}")
            ok += 1
            if model is not None:
                time.sleep(args.delay)
        except Exception as e:
            print(f"  -> FAILED: {str(e)}")
            failed += 1

    print()
    print(f"Done. Generated: {ok}  Skipped: {skipped}  Failed: {failed}")


if __name__ == "__main__":
    main()
