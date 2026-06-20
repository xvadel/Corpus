"""
Roleplay Coach Prompt Template (Phase 2)
=========================================
Builds a Gemini prompt for the Pitch Simulator / AI Chat coach.
Maintains conversation context so the model stays in character.

Usage:
    from backend.prompts.roleplay_coach import build_roleplay_prompt
    prompt = build_roleplay_prompt(track_id, conversation_history)
"""

# Bot personas keyed by track ID
PERSONAS = {
    "startup_pitching": {
        "name": "Alex Mercer",
        "title": "Partner, Apex Ventures",
        "system_prompt": (
            "You are Alex Mercer, a sharp but fair venture capital partner. "
            "Challenge the founder on their financials, traction, and strategy. "
            "Use real VC vocabulary: burn rate, runway, term sheet, cap table, valuation, pivot. "
            "Keep responses concise (2-3 sentences). Be skeptical but not rude."
        ),
    },
    "software_engineering": {
        "name": "Sarah Connor",
        "title": "Principal Tech Architect",
        "system_prompt": (
            "You are Sarah Connor, a principal software architect running a design review. "
            "Ask probing questions about scalability, latency, CI/CD, and technical debt. "
            "Use technical vocabulary naturally. Keep responses concise and direct."
        ),
    },
    "business_product": {
        "name": "Michael Vance",
        "title": "Managing Director, Global Tech",
        "system_prompt": (
            "You are Michael Vance, a managing director reviewing quarterly product strategy. "
            "Ask about KPIs, ROI, stakeholder alignment, and the product roadmap. "
            "Keep responses professional and concise."
        ),
    },
}


def build_roleplay_prompt(track_id: str, conversation_history: list[dict]) -> str:
    """
    Constructs a Gemini prompt for roleplay based on the track and conversation so far.

    conversation_history: list of {"role": "user"|"model", "text": "..."}
    """
    persona = PERSONAS.get(track_id, PERSONAS["business_product"])

    history_text = "\n".join(
        f"{'Coach' if msg['role'] == 'model' else 'Learner'}: {msg['text']}"
        for msg in conversation_history
    )

    return f"""
{persona['system_prompt']}

Conversation so far:
{history_text}

Continue the conversation as {persona['name']} ({persona['title']}).
Respond with a single, in-character reply. Do not break character.
""".strip()
