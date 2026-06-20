"""
Vocabulary Routes
=================
Endpoints:
  GET  /api/vocabulary/tracks          → List all available learning tracks
  GET  /api/vocabulary/{track_id}      → Get vocabulary list for a specific track
  POST /api/vocabulary/custom          → Add a custom term (Phase 2 — requires auth)

Phase 1: Reads from the static tracks data embedded below.
Phase 2: Serve from database, support user-created custom terms.
"""

import os
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

router = APIRouter(prefix="/vocabulary", tags=["Vocabulary"])

# Helper function to dynamically load AI concepts from the generated JSON files
def load_ai_concepts() -> List[Dict[str, str]]:
    concepts_dir = Path("corpus_data/concepts")
    terms = []
    if concepts_dir.exists() and concepts_dir.is_dir():
        for file_path in sorted(concepts_dir.glob("*.json")):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Check first example, default to simple message if empty
                    example_list = data.get("examples", [])
                    example = example_list[0] if example_list else f"An example sentence using {data.get('term')}."
                    terms.append({
                        "term": data.get("term", ""),
                        "definition": data.get("definition", ""),
                        "example": example,
                        "category": data.get("category", "Core")
                      })
            except Exception:
                pass
    
    # Fallback to sample terms if directory is empty or not yet generated
    if not terms:
        terms = [
            {"term": "Embedding", "definition": "A mathematical representation of data in a high-dimensional vector space.", "example": "Cosine similarity of the embeddings is used to retrieve top-k results.", "category": "Embeddings"},
            {"term": "RAG", "definition": "An AI framework that improves the quality of LLM-generated responses by grounding the model on external sources of knowledge.", "example": "We built a customer support bot using a RAG architecture to query our internal wiki.", "category": "Retrieval"},
            {"term": "Vector Database", "definition": "A specialized database designed to store, manage, and query high-dimensional vectors.", "example": "We migrated to ChromaDB to serve search queries faster.", "category": "Vector Databases"}
        ]
    return terms

# Static vocabulary data (Phase 1/2 Unified)
TRACKS: Dict[str, Any] = {
    "startup_pitching": {
        "id": "startup_pitching",
        "name": "Startup & Venture Capital",
        "description": "Learn to pitch ideas to investors, negotiate term sheets, and handle tough Q&A sessions.",
        "icon": "rocket",
        "accentColor": "#FF6B6B",
        "focusAreas": ["Investor Pitching", "Financial Terminology", "Confidence & Delivery"],
        "terms": [
            {"term": "Burn Rate", "definition": "The rate at which a startup spends capital before positive cash flow.", "example": "\"Our current burn rate is $50K per month, giving us 14 months of runway.\"", "category": "Finance"},
            {"term": "Runway", "definition": "How long a company can operate before running out of money.", "example": "\"With the seed round, we extended our runway to 18 months.\"", "category": "Finance"},
            {"term": "Traction", "definition": "Measurable evidence of market demand — users, revenue, growth rate.", "example": "\"We have strong traction with 10K monthly active users growing 20% month-over-month.\"", "category": "Pitching"},
            {"term": "Valuation", "definition": "The estimated worth of a company during fundraising negotiations.", "example": "\"We are raising at a pre-money valuation of $5 million.\"", "category": "Finance"},
            {"term": "Cap Table", "definition": "A spreadsheet showing equity ownership and share value.", "example": "\"Let me walk you through our cap table to show the current ownership structure.\"", "category": "Legal"},
            {"term": "Term Sheet", "definition": "A non-binding document outlining the basic terms of an investment.", "example": "\"We received a term sheet from Sequoia with a $2M investment at 15% equity.\"", "category": "Legal"},
            {"term": "Due Diligence", "definition": "The investigation investors conduct before finalizing a deal.", "example": "\"The VC firm is currently in the due diligence phase, reviewing our financials.\"", "category": "Process"},
            {"term": "Pivot", "definition": "A fundamental change in a startup's business model or strategy.", "example": "\"After analyzing user feedback, we decided to pivot from B2C to B2B.\"", "category": "Strategy"},
        ],
    },
    "software_engineering": {
        "id": "software_engineering",
        "name": "Software Engineering & Tech",
        "description": "Master technical communication during system design, standups, code reviews, and interviews.",
        "icon": "code",
        "accentColor": "#4FC3F7",
        "focusAreas": ["System Design", "Agile Communication", "Explaining Technical Concepts"],
        "terms": [
            {"term": "Microservices", "definition": "An architecture where an app is composed of small, independent services.", "example": "\"We decomposed the monolith into microservices to improve scalability.\"", "category": "Architecture"},
            {"term": "API Gateway", "definition": "A single entry point server that routes to multiple microservices.", "example": "\"All client requests are routed through our API gateway for authentication.\"", "category": "Architecture"},
            {"term": "Load Balancer", "definition": "Software that distributes traffic across multiple servers.", "example": "\"We use a load balancer to distribute traffic evenly across three servers.\"", "category": "Infrastructure"},
            {"term": "CI/CD", "definition": "Continuous Integration / Deployment — automated build, test, and release.", "example": "\"Our CI/CD pipeline runs unit tests and deploys to staging on every pull request.\"", "category": "DevOps"},
            {"term": "Technical Debt", "definition": "The implied cost of rework from choosing quick over sustainable solutions.", "example": "\"We need to allocate two sprints to address the technical debt in the payment module.\"", "category": "Process"},
            {"term": "Latency", "definition": "The time delay between a request and its response.", "example": "\"We reduced API latency from 400ms to 120ms by implementing caching.\"", "category": "Performance"},
            {"term": "Scalability", "definition": "The ability to handle increasing workloads by adding resources.", "example": "\"The system is designed for horizontal scalability using Kubernetes.\"", "category": "Architecture"},
            {"term": "Refactoring", "definition": "Restructuring existing code without changing its external behavior.", "example": "\"I spent the sprint refactoring the authentication module to improve readability.\"", "category": "Process"},
        ],
    },
    "business_product": {
        "id": "business_product",
        "name": "Business & Product Management",
        "description": "Communicate effectively with cross-functional teams, stakeholders, and enterprise clients.",
        "icon": "briefcase",
        "accentColor": "#AB6CFF",
        "focusAreas": ["Stakeholder Alignment", "Product Discovery", "Metrics & KPI Reporting"],
        "terms": [
            {"term": "KPI", "definition": "Key Performance Indicator — a measurable value showing goal effectiveness.", "example": "\"Our primary KPI for Q3 is a 15% increase in user retention rate.\"", "category": "Metrics"},
            {"term": "ROI", "definition": "Return on Investment — the ratio of net profit to cost of investment.", "example": "\"The marketing campaign delivered a 3.5x ROI within the first quarter.\"", "category": "Finance"},
            {"term": "Stakeholder", "definition": "Any person with an interest or concern in a project.", "example": "\"We need to align with all stakeholders before proceeding with the redesign.\"", "category": "Communication"},
            {"term": "Go-to-Market", "definition": "A strategy for launching a product, including pricing and messaging.", "example": "\"Our go-to-market strategy focuses on enterprise clients in the healthcare sector.\"", "category": "Strategy"},
            {"term": "Churn Rate", "definition": "The percentage of customers who stop using a product over a period.", "example": "\"We reduced our monthly churn rate from 8% to 4.5% by improving onboarding.\"", "category": "Metrics"},
            {"term": "Sprint", "definition": "A fixed time period (1-2 weeks) for completing a set of tasks.", "example": "\"In this sprint, we are focusing on the checkout flow and payment integration.\"", "category": "Agile"},
            {"term": "Deliverable", "definition": "A tangible output produced as the result of a project.", "example": "\"The key deliverable for this milestone is a working prototype of the dashboard.\"", "category": "Project Management"},
            {"term": "Roadmap", "definition": "A strategic plan outlining the vision and milestones for a product.", "example": "\"According to our product roadmap, the mobile app launch is scheduled for Q2.\"", "category": "Strategy"},
        ],
    },
    "ai_engineering": {
        "id": "ai_engineering",
        "name": "AI & RAG Engineering",
        "description": "Master terminology of Large Language Models, Retrieval-Augmented Generation, and Agentic workflows.",
        "icon": "rocket",
        "accentColor": "#10B981",
        "focusAreas": ["LLMs & Prompting", "Vector Search & RAG", "Agentic Systems"],
        "terms": []  # Loaded dynamically below
    }
}

# Dynamically initialize AI terms
TRACKS["ai_engineering"]["terms"] = load_ai_concepts()

@router.get(
    "/tracks",
    summary="List all learning tracks",
    description="Returns a list of all available learning tracks with metadata (no vocabulary terms).",
    response_description="List of track summaries",
)
async def list_tracks() -> List[Dict[str, Any]]:
    return [
        {
            "id": t["id"], 
            "name": t["name"], 
            "description": t["description"],
            "icon": t["icon"],
            "accentColor": t["accentColor"], 
            "focusAreas": t["focusAreas"],
            "term_count": len(t["terms"])
        }
        for t in TRACKS.values()
    ]

@router.get(
    "/{track_id}",
    summary="Get vocabulary for a track",
    description="Returns the full vocabulary term list for the specified track ID.",
    response_description="Track metadata and vocabulary list",
)
async def get_vocabulary(track_id: str) -> Dict[str, Any]:
    track = TRACKS.get(track_id)
    if not track:
        raise HTTPException(
            status_code=404,
            detail=f"Track '{track_id}' not found. Valid IDs: {list(TRACKS.keys())}",
        )
    return track

@router.post(
    "/custom",
    summary="Add a custom vocabulary term (Phase 2)",
    description=(
        "Add a user-defined term to a personal vocabulary list. "
        "**Requires authentication (Phase 2).** Returns `501 Not Implemented` until auth is built."
    ),
    response_description="Created term",
    status_code=501,
)
async def add_custom_term() -> Dict[str, str]:
    raise HTTPException(
        status_code=501,
        detail="Custom vocabulary requires user authentication. Coming in Phase 2.",
    )
