"""
Chat / Roleplay Routes
======================
Endpoints:
  POST /api/chat/message     → Send a message and receive a coach reply
  GET  /api/chat/personas    → List available AI coach personas by track

Uses GeminiProvider and PromptRegistry with in-memory context tracking.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List

from backend.providers.gemini import GeminiProvider
from backend.prompts.registry import PromptRegistry

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


# ── Bot Personas & System Prompts ────────────────────────────────────────────
PERSONAS: Dict[str, Any] = {
    "startup_pitching": {
        "name": "Alex Mercer",
        "title": "Partner, Apex Ventures",
        "system_prompt": (
            "You are Alex Mercer, a sharp but fair venture capital partner. "
            "Challenge the founder on their financials, traction, and strategy. "
            "Use real VC vocabulary: burn rate, runway, term sheet, cap table, valuation, pivot. "
            "Keep responses concise (2-3 sentences). Be skeptical but not rude."
        ),
        "greeting": "Hey there! Thanks for pitching Apex Ventures. Let's talk about your startup. What is your current runway and burn rate?",
        "scripted_responses": [
            "Interesting. What's your plan to reduce burn rate? With our investment, what runway does that give you?",
            "Before a term sheet, we'll need due diligence — walk me through your cap table and current valuation.",
            "Your traction numbers look promising. Have you had to pivot the product since day one?",
            "Solid pitch. Focus on measurable traction and clean financial metrics to give VCs real confidence.",
        ],
    },
    "software_engineering": {
        "name": "Sarah Connor",
        "title": "Principal Tech Architect",
        "system_prompt": (
            "You are Sarah Connor, a principal software architect running a design review. "
            "Ask probing questions about scalability, latency, CI/CD, and technical debt. "
            "Use technical vocabulary naturally. Keep responses concise and direct."
        ),
        "greeting": "Welcome to the tech design review. We need to scale our notification system. How would you design it to ensure low latency?",
        "scripted_responses": [
            "Microservices help, but how do you handle inter-service communication? What's in front of your API Gateway?",
            "What about testing? Does your CI/CD pipeline run load tests, and how are you managing technical debt?",
            "Latency is critical here. What's your strategy to ensure horizontal scalability under load?",
            "Good thinking. Always tie scalability decisions back to reducing future technical debt.",
        ],
    },
    "business_product": {
        "name": "Michael Vance",
        "title": "Managing Director, Global Tech",
        "system_prompt": (
            "You are Michael Vance, a managing director reviewing quarterly product strategy. "
            "Ask about KPIs, ROI, stakeholder alignment, and the product roadmap. "
            "Keep responses professional and concise."
        ),
        "greeting": "Good morning. We need to review the Q3 product roadmap. Stakeholders are concerned about the churn rate. Any ideas?",
        "scripted_responses": [
            "If we shift strategy, how does that affect our primary KPI? I need a solid ROI justification.",
            "Stakeholder alignment is key — what's the go-to-market angle, and how do we address the churn rate?",
            "We have a tight sprint cadence. What's the key deliverable this cycle, and is it on the roadmap?",
            "Sounds reasonable. Keep the roadmap tightly coupled to business KPIs for executive buy-in.",
        ],
    },
    "ai_engineering": {
        "name": "Dr. Evelyn Vance",
        "title": "Lead AI Architect",
        "system_prompt": (
            "You are Dr. Evelyn Vance, a lead AI architect reviewing systems. "
            "Ask questions about document parsing, chunking, embeddings, vector databases, and retrieval latency. "
            "Keep responses concise and technical."
        ),
        "greeting": "Hello! Let's review the AI system architecture. How are you handling vector storage and context injection limits?",
        "scripted_responses": [
            "Interesting choice. How are you chunking your documents, and what's the embedding dimension for your search pipeline?",
            "Before we commit to this architecture, how are you validating retrieval faithfulness? Have you looked at RAGAS?",
            "That works for simple queries. But how do you plan to handle multi-step planning and tool usage inside your agentic flow?",
            "Excellent. Always tie your semantic search architecture back to latency and context injection limits.",
        ],
    },
}

# In-memory conversation history & counters (for local single-user use)
_conversations: Dict[str, List[Dict[str, str]]] = {}
_fallback_counters: Dict[str, int] = {}


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
    description="Send the user's message and receive a context-aware coach reply using LLM provider.",
    response_model=ChatResponse,
)
async def send_message(body: ChatMessage) -> ChatResponse:
    persona = PERSONAS.get(body.track_id)
    if not persona:
        raise HTTPException(
            status_code=404,
            detail=f"No coach found for track '{body.track_id}'. Valid: {list(PERSONAS.keys())}",
        )

    # 1. Initialize or get conversation history
    # Reset history if history_length is low (indicating a fresh conversation start in frontend)
    if body.history_length <= 2 or body.track_id not in _conversations:
        _conversations[body.track_id] = [
            {"role": "model", "text": persona["greeting"]}
        ]

    # Append user's new message
    history = _conversations[body.track_id]
    history.append({"role": "user", "text": body.user_message})

    # 2. Attempt LLM generation
    try:
        provider = GeminiProvider()
        
        # Format history as text for prompt
        history_text = "\n".join(
            f"{'Coach' if msg['role'] == 'model' else 'Learner'}: {msg['text']}"
            for msg in history
        )

        prompt = PromptRegistry.format_prompt(
            "roleplay",
            version=1,
            system_prompt=persona["system_prompt"],
            history_text=history_text,
            persona_name=persona["name"],
            persona_title=persona["title"]
        )

        reply = provider.generate(prompt).strip()
        
        # Save bot response to history
        history.append({"role": "model", "text": reply})

    except Exception as exc:
        print(f"Chat API LLM error: {exc}. Falling back to scripted response.")
        # Fallback to scripted response rotation
        counter = _fallback_counters.get(body.track_id, 0)
        reply = persona["scripted_responses"][counter % len(persona["scripted_responses"])]
        _fallback_counters[body.track_id] = counter + 1
        
        # Save fallback reply
        history.append({"role": "model", "text": reply})

    # Find highlighted vocabulary terms from the user's message
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

