"""
DEPRECATED — backend/api/routes.py
====================================
This file is kept only for backward compatibility.
All routes have been split into individual files:

  backend/api/health.py      → GET  /api/health
  backend/api/projects.py    → POST /api/projects/upload
  backend/api/vocabulary.py  → GET  /api/vocabulary/tracks
                               GET  /api/vocabulary/{track_id}
                               POST /api/vocabulary/custom
  backend/api/chat.py        → GET  /api/chat/personas
                               POST /api/chat/message
  backend/api/auth.py        → POST /api/auth/register
                               POST /api/auth/login
                               GET  /api/auth/me

The aggregated router lives in backend/api/__init__.py.
Do NOT add new routes here — add them to the appropriate file above.
"""

# Re-export the aggregated router for any code still importing from here
from backend.api import api_router as router  # noqa: F401
