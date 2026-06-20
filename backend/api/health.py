"""
Health Routes
=============
Endpoint: GET /api/health

Used by Docker healthcheck, monitoring tools, and load balancers
to verify the backend is alive and responding.
"""

from fastapi import APIRouter
from typing import Dict

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Returns `200 OK` when the backend is live. Used by Docker and monitoring tools.",
    response_description="Service status string",
)
async def health_check() -> Dict[str, str]:
    return {"status": "ok", "service": "Corpus API", "version": "1.0.0"}
