"""
Project Analysis Prompt Template (Phase 2)
==========================================
Builds the Gemini prompt for extracting domain and skill data
from a user's project markdown description.

Usage:
    from backend.prompts.project_analysis import build_prompt
    prompt = build_prompt(markdown_text)
"""


def build_prompt(markdown_text: str) -> str:
    """
    Wraps the user's project markdown in a structured Gemini prompt.
    Returns JSON with: domain, subdomains[], extracted_skills[].
    """
    return f"""
You are an expert career coach and domain classifier.

Analyze the following project description and extract:
1. The primary professional domain (e.g., "Software Engineering", "Finance")
2. Up to 3 subdomains (e.g., "Machine Learning", "Cloud Infrastructure")
3. The top 5 technical or professional skills demonstrated

Return ONLY valid JSON in this exact format:
{{
  "domain": "...",
  "subdomains": ["...", "..."],
  "extracted_skills": ["...", "...", "..."]
}}

---
PROJECT DESCRIPTION:
{markdown_text}
---
""".strip()
