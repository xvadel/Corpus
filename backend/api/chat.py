"""
Chat / Roleplay Routes
======================
Endpoints:
  POST /api/chat/message     → Send a message and receive a coach reply
  GET  /api/chat/personas    → List available AI coach personas by track

Phase 1: Returns scripted bot responses based on the track.
Phase 2: Wire to `backend/services/gemini_service.py` → `generate_roleplay_reply()`.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List

router = APIRouter(prefix="/chat", tags=["Chat & Roleplay"])

# ── Request / Response Schemas ───────────────────────────────────────────────

class ChatMessage(BaseModel):
    track_id: str = Field(..., example="startup_pitching", description="The learning track ID")
    user_message: str = Field(..., example="Our burn rate is $50K/month.", description="The user's message text")
    history_length: int = Field(default=0, description="Number of previous turns (for context tracking in Phase 2)")


class ChatResponse(BaseModel):
    reply: str
    coach_name: str
    coach_title: str
    highlighted_terms: List[str]


# ── Scripted personas (Phase 1) ──────────────────────────────────────────────
PERSONAS: Dict[str, Any] = {
    "startup_pitching": {
        "name": "Alex Mercer",
        "title": "Partner, Apex Ventures",
        "responses": [
            "Interesting. What's your plan to reduce burn rate? With our investment, what runway does that give you?",
            "Before a term sheet, we'll need due diligence — walk me through your cap table and current valuation.",
            "Your traction numbers look promising. Have you had to pivot the product since day one?",
            "Solid pitch. Focus on measurable traction and clean financial metrics to give VCs real confidence.",
        ],
    },
    "software_engineering": {
        "name": "Sarah Connor",
        "title": "Principal Tech Architect",
        "responses": [
            "Microservices help, but how do you handle inter-service communication? What's in front of your API Gateway?",
            "What about testing? Does your CI/CD pipeline run load tests, and how are you managing technical debt?",
            "Latency is critical here. What's your strategy to ensure horizontal scalability under load?",
            "Good thinking. Always tie scalability decisions back to reducing future technical debt.",
        ],
    },
    "business_product": {
        "name": "Michael Vance",
        "title": "Managing Director, Global Tech",
        "responses": [
            "If we shift strategy, how does that affect our primary KPI? I need a solid ROI justification.",
            "Stakeholder alignment is key — what's the go-to-market angle, and how do we address the churn rate?",
            "We have a tight sprint cadence. What's the key deliverable this cycle, and is it on the roadmap?",
            "Sounds reasonable. Keep the roadmap tightly coupled to business KPIs for executive buy-in.",
        ],
    },
}

_response_counters: Dict[str, int] = {}


@router.get(
    "/personas",
    summary="List AI coach personas",
    description="Returns the available AI coach persona for each learning track.",
    response_description="Map of track_id → persona info",
)
async def list_personas() -> Dict[str, Any]:
    return {
        track_id: {"name": p["name"], "title": p["title"]}
        for track_id, p in PERSONAS.items()
    }


@router.post(
    "/message",
    summary="Send a message to the AI coach",
    description=(
        "Send the user's message and receive a coach reply. "
        "\n\n**Phase 1:** Returns scripted responses in sequence. "
        "\n\n**Phase 2:** Will call Gemini with full conversation history for context-aware replies."
    ),
    response_model=ChatResponse,
)
async def send_message(body: ChatMessage) -> ChatResponse:
    persona = PERSONAS.get(body.track_id)
    if not persona:
        raise HTTPException(
            status_code=404,
            detail=f"No coach found for track '{body.track_id}'. Valid: {list(PERSONAS.keys())}",
        )

    # ── Phase 1: Rotate scripted responses ───────────────────────────────────
    # TODO (Phase 2): Replace with:
    #   from backend.services.gemini_service import generate_roleplay_reply
    #   reply = await generate_roleplay_reply(body.track_id, conversation_history)
    counter = _response_counters.get(body.track_id, 0)
    reply = persona["responses"][counter % len(persona["responses"])]
    _response_counters[body.track_id] = counter + 1

    # Find any vocabulary terms in the user's message
    from backend.api.vocabulary import TRACKS
    track_data = TRACKS.get(body.track_id, {})
    terms = [t["term"] for t in track_data.get("terms", [])]
    highlighted = [t for t in terms if t.lower() in body.user_message.lower()]

    return ChatResponse(
        reply=reply,
        coach_name=persona["name"],
        coach_title=persona["title"],
        highlighted_terms=highlighted,
    )
