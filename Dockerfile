# Multi-stage build for self-hosted Corpus application
# Stage 1: Build the Svelte static frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

# Copy dependencies first for caching
COPY frontend/package*.json ./
RUN npm install

# Copy source and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the FastAPI runner
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies (e.g. for database connectors)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files and static assets
COPY backend/ ./backend/
COPY config.toml ./config.toml
COPY corpus_data/ ./corpus_data/

# Copy built static files from Stage 1 into backend/static
COPY --from=frontend-builder /app/frontend/dist ./backend/static

EXPOSE 8000

# Run uvicorn server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
