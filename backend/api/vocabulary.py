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

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

router = APIRouter(prefix="/vocabulary", tags=["Vocabulary"])

# ── Static vocabulary data (Phase 1) ────────────────────────────────────────
# Phase 2: Replace this with a DB query via backend/database/session.py
TRACKS: Dict[str, Any] = {
    "startup_pitching": {
        "id": "startup_pitching",
        "name": "Startup & Venture Capital",
        "accent_color": "#FF6B6B",
        "terms": [
            {"term": "Burn Rate", "definition": "The rate at which a startup spends capital before positive cash flow.", "category": "Finance"},
            {"term": "Runway", "definition": "How long a company can operate before running out of money.", "category": "Finance"},
            {"term": "Traction", "definition": "Measurable evidence of market demand — users, revenue, growth rate.", "category": "Pitching"},
            {"term": "Valuation", "definition": "The estimated worth of a company during fundraising negotiations.", "category": "Finance"},
            {"term": "Cap Table", "definition": "A spreadsheet showing equity ownership and share value.", "category": "Legal"},
            {"term": "Term Sheet", "definition": "A non-binding document outlining the basic terms of an investment.", "category": "Legal"},
            {"term": "Due Diligence", "definition": "The investigation investors conduct before finalizing a deal.", "category": "Process"},
            {"term": "Pivot", "definition": "A fundamental change in a startup's business model or strategy.", "category": "Strategy"},
        ],
    },
    "software_engineering": {
        "id": "software_engineering",
        "name": "Software Engineering & Tech",
        "accent_color": "#4FC3F7",
        "terms": [
            {"term": "Microservices", "definition": "An architecture where an app is composed of small, independent services.", "category": "Architecture"},
            {"term": "API Gateway", "definition": "A single entry point server that routes to multiple microservices.", "category": "Architecture"},
            {"term": "Load Balancer", "definition": "Software that distributes traffic across multiple servers.", "category": "Infrastructure"},
            {"term": "CI/CD", "definition": "Continuous Integration / Deployment — automated build, test, and release.", "category": "DevOps"},
            {"term": "Technical Debt", "definition": "The implied cost of rework from choosing quick over sustainable solutions.", "category": "Process"},
            {"term": "Latency", "definition": "The time delay between a request and its response.", "category": "Performance"},
            {"term": "Scalability", "definition": "The ability to handle increasing workloads by adding resources.", "category": "Architecture"},
            {"term": "Refactoring", "definition": "Restructuring existing code without changing its external behavior.", "category": "Process"},
        ],
    },
    "business_product": {
        "id": "business_product",
        "name": "Business & Product Management",
        "accent_color": "#AB6CFF",
        "terms": [
            {"term": "KPI", "definition": "Key Performance Indicator — a measurable value showing goal effectiveness.", "category": "Metrics"},
            {"term": "ROI", "definition": "Return on Investment — the ratio of net profit to cost of investment.", "category": "Finance"},
            {"term": "Stakeholder", "definition": "Any person with an interest or concern in a project.", "category": "Communication"},
            {"term": "Go-to-Market", "definition": "A strategy for launching a product, including pricing and messaging.", "category": "Strategy"},
            {"term": "Churn Rate", "definition": "The percentage of customers who stop using a product over a period.", "category": "Metrics"},
            {"term": "Sprint", "definition": "A fixed time period (1-2 weeks) for completing a set of tasks.", "category": "Agile"},
            {"term": "Deliverable", "definition": "A tangible output produced as the result of a project.", "category": "Project Management"},
            {"term": "Roadmap", "definition": "A strategic plan outlining the vision and milestones for a product.", "category": "Strategy"},
        ],
    },
}


@router.get(
    "/tracks",
    summary="List all learning tracks",
    description="Returns a list of all available learning tracks with metadata (no vocabulary terms).",
    response_description="List of track summaries",
)
async def list_tracks() -> List[Dict[str, Any]]:
    return [
        {"id": t["id"], "name": t["name"], "accent_color": t["accent_color"], "term_count": len(t["terms"])}
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
