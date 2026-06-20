# =============================================================================
# Corpus — Developer Makefile
# =============================================================================
# Quick commands for local development, building, and Docker deployment.
# Run `make help` to see all available commands.
# =============================================================================

.PHONY: help dev-frontend dev-backend install build docker-up docker-down clean lint

## ── Help ──────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  Corpus — Available Commands"
	@echo "  ──────────────────────────────────────────────────"
	@echo "  make install         Install all Python + Node dependencies"
	@echo "  make dev-frontend    Start the Svelte dev server (hot-reload)"
	@echo "  make dev-backend     Start the FastAPI backend (hot-reload)"
	@echo "  make build           Build frontend + copy into backend/static/"
	@echo "  make docker-up       Build image and start Docker container"
	@echo "  make docker-down     Stop and remove Docker containers"
	@echo "  make clean           Remove build artifacts and caches"
	@echo ""

## ── Installation ─────────────────────────────────────────────────────────────
install:
	@echo "→ Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "→ Installing Node dependencies..."
	cd frontend && npm install
	@echo "✓ All dependencies installed."

## ── Development ──────────────────────────────────────────────────────────────
dev-frontend:
	@echo "→ Starting Svelte dev server on http://localhost:5173"
	cd frontend && npm run dev

dev-backend:
	@echo "→ Starting FastAPI backend on http://localhost:8000"
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

## ── Production Build ─────────────────────────────────────────────────────────
build:
	@echo "→ Building Svelte frontend..."
	cd frontend && npm run build
	@echo "→ Copying dist/ into backend/static/..."
	rm -rf backend/static/*
	cp -r frontend/dist/. backend/static/
	@echo "✓ Build complete. Static files are in backend/static/"

## ── Docker ───────────────────────────────────────────────────────────────────
docker-up:
	@echo "→ Building and starting Docker container..."
	docker compose up --build -d
	@echo "✓ Corpus is running at http://localhost:8000"

docker-down:
	@echo "→ Stopping Docker containers..."
	docker compose down
	@echo "✓ Done."

## ── Cleanup ──────────────────────────────────────────────────────────────────
clean:
	@echo "→ Removing build artifacts..."
	rm -rf frontend/dist backend/static/__pycache__ backend/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
	@echo "✓ Cleaned."
