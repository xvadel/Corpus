"""
Project Routes
==============
Endpoints:
  POST /api/projects/upload   → Upload a Markdown project file for domain analysis

Phase 1: Simulated response (no LLM call).
Phase 2: Wire to `backend/services/gemini_service.py` → `analyze_project_markdown()`.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "/upload",
    summary="Upload a project for domain analysis",
    description=(
        "Upload a Markdown (`.md`) file describing your project. "
        "The backend extracts your professional domain, subdomains, and key skills. "
        "\n\n**Phase 1:** Returns a simulated analysis response. "
        "\n\n**Phase 2:** Will call Gemini API for real extraction."
    ),
    response_description="Domain analysis result",
)
async def upload_project(file: UploadFile = File(...)) -> Dict[str, Any]:
    if not file.filename.endswith(".md"):
        raise HTTPException(
            status_code=400,
            detail="Only Markdown (.md) files are supported.",
        )

    try:
        content = await file.read()
        markdown_text = content.decode("utf-8")

        # ── Phase 1 MVP: Simulated Gemini response ───────────────────────────
        # TODO (Phase 2): Replace with:
        #   from backend.services.gemini_service import analyze_project_markdown
        #   return await analyze_project_markdown(markdown_text)
        return {
            "status": "success",
            "filename": file.filename,
            "analysis": {
                "domain": "Artificial Intelligence",
                "subdomains": [
                    "Retrieval-Augmented Generation (RAG)",
                    "Natural Language Processing",
                    "Vector Databases",
                ],
                "extracted_skills": ["Python", "FastAPI", "Prompt Engineering"],
                "content_length": len(markdown_text),
            },
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing file: {exc}",
        )
