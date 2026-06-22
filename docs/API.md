# Corpus API Reference

This document provides a comprehensive REST API specification for **Corpus**, the domain-specific language learning platform.

*   **Interactive Swagger UI**: Start the server and navigate to [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
*   **Alternative ReDoc Interface**: Start the server and navigate to [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)
*   **Postman Collection**: Import [`docs/corpus_api.postman_collection.json`](./corpus_api.postman_collection.json) to quickly test endpoints.

---

## Base URL

| Environment | Base URL |
| :--- | :--- |
| **Local Development** | `http://localhost:8000` |
| **Docker Self-Hosted** | `http://localhost:8000` |
| **Production** | Deployed Domain |

---

## Router Module Structure

All backend route endpoints are defined in `backend/api/`:

```text
backend/api/
├── __init__.py       ← Aggregates routers and mounts under prefix /api
├── auth.py           ← Authentication stubs (register, login, me)
├── chat.py           ← LLM-backed simulator routes (message, personas)
├── health.py         ← Service health and liveness checks
├── projects.py       ← Workspace file parsing and uploads
└── vocabulary.py     ← Static and dynamic vocabulary query routes
```

---

## API Endpoints

### 1. Health & Status

#### `GET /api/health`
Performs service liveness and container health checks.

**Response (`200 OK`)**
```json
{
  "status": "ok",
  "service": "Corpus API",
  "version": "1.1.0"
}
```

---

### 2. File Analysis & Projects

#### `POST /api/projects/upload`
Upload a markdown files representing engineering context. Parses and extracts keywords, subdomains, and required competencies.

*   **Request Format**: `multipart/form-data`
*   **Parameters**:
    *   `file` (File, Required): A `.md` file to analyze.

**Response (`200 OK`)**
```json
{
  "status": "success",
  "filename": "my_system_design.md",
  "analysis": {
    "domain": "Artificial Intelligence",
    "subdomains": [
      "Retrieval-Augmented Generation (RAG)",
      "Natural Language Processing",
      "Vector Databases"
    ],
    "extracted_skills": ["Python", "FastAPI", "Prompt Engineering"],
    "content_length": 1420
  }
}
```

**Common Error Responses**:
*   `400 Bad Request`: If the file extension is not `.md`.
*   `500 Internal Server Error`: If file decoding fails.

---

### 3. Vocabulary Tracks

#### `GET /api/vocabulary/tracks`
Returns lists of available language/terminology tracks.

**Response (`200 OK`)**
```json
[
  {
    "id": "startup_pitching",
    "name": "Startup & Venture Capital",
    "accent_color": "#FF6B6B",
    "term_count": 8
  },
  {
    "id": "software_engineering",
    "name": "Software Engineering & Tech",
    "accent_color": "#4FC3F7",
    "term_count": 8
  },
  {
    "id": "business_product",
    "name": "Business & Product Management",
    "accent_color": "#AB6CFF",
    "term_count": 8
  },
  {
    "id": "ai_engineering",
    "name": "AI Engineering",
    "accent_color": "#10B981",
    "term_count": 8
  }
]
```

#### `GET /api/vocabulary/{track_id}`
Returns all terminology vocabulary details associated with a track ID.

*   **Path Parameters**:
    *   `track_id` (String, Required): `startup_pitching`, `software_engineering`, `business_product`, or `ai_engineering`.

**Response (`200 OK`)**
```json
{
  "id": "software_engineering",
  "name": "Software Engineering & Tech",
  "accent_color": "#4FC3F7",
  "terms": [
    {
      "term": "Latency",
      "definition": "The time delay between a client request and server response.",
      "category": "Performance"
    },
    {
      "term": "Scalability",
      "definition": "The ability of a system to handle increased load by adding resources.",
      "category": "Architecture"
    }
  ]
}
```

---

### 4. Chat & LLM Coach Roleplay

#### `GET /api/chat/personas`
Retrieves details of AI Coach identities and domains.

**Response (`200 OK`)**
```json
{
  "startup_pitching": {
    "name": "Alex Mercer",
    "title": "Partner, Apex Ventures"
  },
  "software_engineering": {
    "name": "Sarah Connor",
    "title": "Principal Tech Architect"
  },
  "business_product": {
    "name": "Michael Vance",
    "title": "Managing Director, Global Tech"
  },
  "ai_engineering": {
    "name": "Dr. Evelyn Vance",
    "title": "Lead AI Architect"
  }
}
```

#### `POST /api/chat/message`
Submit a message to the AI coach. Returns a tailored response using the configured LLM provider, matching key vocabulary terms.

*   **Request Body (`application/json`)**:
    *   `track_id` (String, Required): The track ID.
    *   `user_message` (String, Required): The user response.
    *   `history_length` (Integer, Optional): Number of previous exchanges to parse context.

**Example Request**
```json
{
  "track_id": "startup_pitching",
  "user_message": "Our burn rate is 50k and runway is 12 months.",
  "history_length": 1
}
```

**Response (`200 OK`)**
```json
{
  "reply": "Slowing down your burn rate seems like a priority. With 12 months of runway, when do you plan to raise your next round?",
  "coach_name": "Alex Mercer",
  "coach_title": "Partner, Apex Ventures",
  "highlighted_terms": ["Burn Rate", "Runway"]
}
```

---

### 5. Authentication (Under Active Development)

#### `POST /api/auth/register`
Create a new user account.

#### `POST /api/auth/login`
Authenticate email/password and obtain a secure JWT token.

#### `GET /api/auth/me`
Retrieve profile attributes of the authenticated user session.
