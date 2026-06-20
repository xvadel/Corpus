# Corpus API Reference

> **Interactive docs:** Run the server and visit [`http://localhost:8000/api/docs`](http://localhost:8000/api/docs) for the live Swagger UI, or [`http://localhost:8000/api/redoc`](http://localhost:8000/api/redoc) for ReDoc.
>
> **Postman:** Import [`docs/corpus_api.postman_collection.json`](./corpus_api.postman_collection.json) into Postman to test all endpoints instantly.

---

## Base URL

| Environment | URL |
|---|---|
| Local development | `http://localhost:8000` |
| Docker self-hosted | `http://localhost:8000` |
| Production | Your deployed domain |

---

## Route File Structure

Each domain has its own file inside `backend/api/`:

```
backend/api/
├── __init__.py       ← Aggregates all routers → imported by main.py
├── health.py         ← GET  /api/health
├── projects.py       ← POST /api/projects/upload
├── vocabulary.py     ← GET  /api/vocabulary/tracks
│                        GET  /api/vocabulary/{track_id}
│                        POST /api/vocabulary/custom       [Phase 2]
├── chat.py           ← GET  /api/chat/personas
│                        POST /api/chat/message
├── auth.py           ← POST /api/auth/register            [Phase 2]
│                        POST /api/auth/login              [Phase 2]
│                        GET  /api/auth/me                 [Phase 2]
└── routes.py         ← DEPRECATED shim (do not add routes here)
```

---

## Endpoints

### 🏥 Health

#### `GET /api/health`
Liveness check used by Docker healthcheck, load balancers, and uptime monitors.

**Response `200 OK`**
```json
{
  "status": "ok",
  "service": "Corpus API",
  "version": "1.0.0"
}
```

---

### 📂 Projects

#### `POST /api/projects/upload`
Upload a Markdown file describing your project. Returns extracted domain, subdomains, and skills.

> **Phase 1:** Returns a simulated response. **Phase 2:** Calls Gemini API.

**Request** — `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | `File` | ✅ | A `.md` Markdown file |

**Response `200 OK`**
```json
{
  "status": "success",
  "filename": "my_project.md",
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

**Error Responses**

| Code | Reason |
|---|---|
| `400` | File is not a `.md` file |
| `500` | File could not be read or decoded |

---

### 📚 Vocabulary

#### `GET /api/vocabulary/tracks`
Returns a summary list of all available learning tracks (without vocabulary terms).

**Response `200 OK`**
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
  }
]
```

---

#### `GET /api/vocabulary/{track_id}`
Returns the full vocabulary term list for a specific track.

**Path Parameters**

| Parameter | Type | Valid Values |
|---|---|---|
| `track_id` | `string` | `startup_pitching`, `software_engineering`, `business_product` |

**Response `200 OK`**
```json
{
  "id": "startup_pitching",
  "name": "Startup & Venture Capital",
  "accent_color": "#FF6B6B",
  "terms": [
    {
      "term": "Burn Rate",
      "definition": "The rate at which a startup spends capital before positive cash flow.",
      "category": "Finance"
    },
    {
      "term": "Runway",
      "definition": "How long a company can operate before running out of money.",
      "category": "Finance"
    }
  ]
}
```

**Error Responses**

| Code | Reason |
|---|---|
| `404` | `track_id` does not exist |

---

#### `POST /api/vocabulary/custom` ⚠️ Phase 2
Add a user-defined term to a personal vocabulary list. Requires authentication.

**Returns `501 Not Implemented` until Phase 2.**

---

### 💬 Chat & Roleplay

#### `GET /api/chat/personas`
Returns the AI coach persona name and title for each available track.

**Response `200 OK`**
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
  }
}
```

---

#### `POST /api/chat/message`
Send a user message and receive an AI coach reply with vocabulary term highlighting.

> **Phase 1:** Returns scripted responses in sequence. **Phase 2:** Calls Gemini API with full conversation context.

**Request Body** — `application/json`

| Field | Type | Required | Description |
|---|---|---|---|
| `track_id` | `string` | ✅ | One of the valid track IDs |
| `user_message` | `string` | ✅ | The learner's message text |
| `history_length` | `integer` | ❌ | Number of previous turns (used in Phase 2) |

**Example Request**
```json
{
  "track_id": "startup_pitching",
  "user_message": "Our burn rate is $50K/month and we have 18 months of runway.",
  "history_length": 0
}
```

**Response `200 OK`**
```json
{
  "reply": "Interesting. What's your plan to reduce burn rate? With our investment, what runway does that give you?",
  "coach_name": "Alex Mercer",
  "coach_title": "Partner, Apex Ventures",
  "highlighted_terms": ["Burn Rate", "Runway"]
}
```

**Error Responses**

| Code | Reason |
|---|---|
| `404` | `track_id` does not match any known persona |
| `422` | Request body failed validation |

---

### 🔐 Authentication — Phase 2

> All auth endpoints currently return `501 Not Implemented`.
> See `backend/api/auth.py` for the full implementation plan and TODOs.

#### `POST /api/auth/register` ⚠️ Phase 2

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "Jane Doe"
}
```

---

#### `POST /api/auth/login` ⚠️ Phase 2

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Expected Response (Phase 2)**
```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

---

#### `GET /api/auth/me` ⚠️ Phase 2

**Headers**
```
Authorization: Bearer <access_token>
```

---

## Error Format

All errors follow FastAPI's standard error schema:

```json
{
  "detail": "Human-readable error message here."
}
```

---

## Testing with Swagger UI

1. Start the backend:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

2. Open [http://localhost:8000/api/docs](http://localhost:8000/api/docs) in your browser.

3. Click any endpoint → **Try it out** → **Execute**.

4. For file upload endpoints, use the file picker to select a `.md` file.

---

## Testing with Postman

1. Open Postman → **Import** → select `docs/corpus_api.postman_collection.json`.
2. The collection sets `{{baseUrl}}` to `http://localhost:8000` automatically.
3. For Phase 2 auth endpoints, set the `{{authToken}}` variable after a successful login.
