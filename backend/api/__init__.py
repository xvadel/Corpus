"""
Corpus API Router
=================
Aggregates all route modules into a single router that is registered
in `backend/main.py`.

Route modules:
  - health.py       →  GET  /api/health
  - projects.py     →  POST /api/projects/upload
  - vocabulary.py   →  GET  /api/vocabulary/{track_id}        (Phase 2)
  - chat.py         →  POST /api/chat/message                 (Phase 2)
  - auth.py         →  POST /api/auth/register, /api/auth/login  (Phase 2)

To add a new domain, create a new file in this directory, define an
`APIRouter`, and include it here.
"""

from fastapi import APIRouter

from backend.api.health import router as health_router
from backend.api.projects import router as projects_router
from backend.api.vocabulary import router as vocabulary_router
from backend.api.chat import router as chat_router
from backend.api.auth import router as auth_router

# Root API router — all child routers inherit the /api prefix
api_router = APIRouter(prefix="/api")

api_router.include_router(health_router)
api_router.include_router(projects_router)
api_router.include_router(vocabulary_router)
api_router.include_router(chat_router)
api_router.include_router(auth_router)
