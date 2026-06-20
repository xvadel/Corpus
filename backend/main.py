"""
Corpus — FastAPI Application Entry Point
=========================================
Initializes the FastAPI app, registers middleware, mounts API routes,
and serves the pre-built Svelte SPA from backend/static/.

To run locally (with hot-reload):
    uvicorn backend.main:app --reload --port 8000

To run via Docker:
    docker compose up --build
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api import api_router

# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Corpus 🗣️💼",
    description=(
        "Domain-specific language learning for professionals. "
        "Practice vocabulary, roleplay industry conversations, and master "
        "the language of your field."
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Tighten this in production (e.g., your domain)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# API Routes  (/api/*)
# ---------------------------------------------------------------------------

app.include_router(api_router)

# ---------------------------------------------------------------------------
# Static Files — Svelte SPA
# Served last so /api/* routes take priority over the catch-all.
# ---------------------------------------------------------------------------

static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)   # Ensure dir exists even in dev mode

app.mount("/", StaticFiles(directory=static_dir, html=True), name="frontend")
