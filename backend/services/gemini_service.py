"""
Gemini AI Service (Phase 2)
===========================
Wraps the Google Generative AI SDK to provide project analysis,
vocabulary generation, and roleplay coaching via Gemini.

Prerequisites:
  1. Set GEMINI_API_KEY in your .env file.
  2. Uncomment the implementation below.
  3. Install: pip install google-generativeai

Usage:
    from backend.services.gemini_service import analyze_project_markdown
    result = await analyze_project_markdown(markdown_text)
"""

import os

# ---------------------------------------------------------------------------
# Phase 2 — Uncomment when integrating Gemini
# ---------------------------------------------------------------------------
# import google.generativeai as genai
#
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise RuntimeError("GEMINI_API_KEY is not set. Check your .env file.")
#
# genai.configure(api_key=GEMINI_API_KEY)
# model = genai.GenerativeModel("gemini-1.5-flash")
#
#
# async def analyze_project_markdown(markdown_text: str) -> dict:
#     """
#     Sends a project markdown to Gemini and returns extracted domain data.
#     """
#     from backend.prompts.project_analysis import build_prompt
#     prompt = build_prompt(markdown_text)
#     response = model.generate_content(prompt)
#     # TODO: Parse structured JSON from response.text
#     return {"raw": response.text}
#
#
# async def generate_roleplay_reply(track_id: str, conversation_history: list) -> str:
#     """
#     Continues a roleplay conversation with context-aware Gemini responses.
#     """
#     from backend.prompts.roleplay_coach import build_roleplay_prompt
#     prompt = build_roleplay_prompt(track_id, conversation_history)
#     response = model.generate_content(prompt)
#     return response.text
