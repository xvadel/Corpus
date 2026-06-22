# Concept Schema Specification

All concept files under `corpus_data/concepts/` must be structured JSON files conforming to this schema.

## Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Concept",
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique snake_case identifier matching the filename."
    },
    "term": {
      "type": "string",
      "description": "The concept term name (e.g., 'Embedding')."
    },
    "domain": {
      "type": "string",
      "description": "The parent domain name (e.g., 'AI')."
    },
    "subdomain": {
      "type": "string",
      "description": "The subdomain category from the ontology (e.g., 'Retrieval Augmented Generation')."
    },
    "category": {
      "type": "string",
      "description": "The classification category (e.g., 'Embeddings')."
    },
    "difficulty": {
      "type": "string",
      "enum": ["Beginner", "Intermediate", "Advanced"],
      "description": "Skill level classification."
    },
    "definition": {
      "type": "string",
      "description": "A single sentence technical definition."
    },
    "simple_explanation": {
      "type": "string",
      "description": "Explanation for a non-technical audience (e.g. 14-year-old) in 2-3 sentences."
    },
    "technical_explanation": {
      "type": "string",
      "description": "Detailed technical explanation for a senior engineer."
    },
    "investor_explanation": {
      "type": "string",
      "description": "Business or product pitch for venture investors."
    },
    "examples": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Realistic sentences illustrating how the term is used in industry context."
    },
    "related_terms": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "List of related concept term names."
    },
    "prerequisites": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Prerequisite concept term names that must be understood first."
    },
    "references": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Scientific papers, books, or documentation references."
    },
    "interview_questions": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Common interview questions testing knowledge of this concept."
    },
    "common_mistakes": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Frequent mistakes developers make when applying this concept."
    }
  },
  "required": [
    "id",
    "term",
    "domain",
    "subdomain",
    "difficulty",
    "definition",
    "simple_explanation",
    "technical_explanation",
    "examples",
    "related_terms",
    "prerequisites",
    "references"
  ]
}
```

## Field Breakdown

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | String | Yes | snake_case identifier matching filename (e.g. `vector_database.json`) |
| `term` | String | Yes | Professional name of the concept |
| `domain` | String | Yes | Broad domain name |
| `subdomain` | String | Yes | Specific subdomain under domain |
| `difficulty` | String | Yes | Beginner, Intermediate, or Advanced |
| `definition` | String | Yes | Clear 1-sentence technical definition |
| `simple_explanation` | String | Yes | Simple explanation without heavy jargon |
| `technical_explanation` | String | Yes | Full details for senior developers |
| `examples` | List[String] | Yes | Concrete sentences showing real usage |
| `related_terms` | List[String] | Yes | Connections to other concepts |
| `prerequisites` | List[String] | Yes | Dependency concepts |
| `references` | List[String] | Yes | Citations (defaults to empty list if none) |
