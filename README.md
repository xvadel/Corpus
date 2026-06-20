# Corpus 🗣️💼

> **Domain-specific language learning for professionals.**
> Master the vocabulary, pitch confidently, and communicate like an expert in your field.

An AI-powered, self-hostable platform that bridges the gap between technical skill and professional communication. Unlike general language apps (Duolingo, Babbel), **Corpus** targets the specialized vocabulary and conversational patterns required in high-stakes professional environments — investor pitches, system design interviews, and executive stakeholder meetings.

---

## 🎯 The Problem We Solve

Many skilled professionals face a career bottleneck due to:

- **Jargon & Terminology Gaps** — Can't explain system architecture or financial models using standard industry language.
- **High-Stakes Speaking Anxiety** — No structured practice for pitching to investors or presenting to boards.
- **Generalist Language Apps** — Existing tools teach ordering food, not explaining burn rate or API design.

---

## ✨ Features

| Feature | Status |
|---|---|
| Domain-specific learning tracks (Startup, Tech, Business) | ✅ Live |
| Interactive flashcard vocabulary deck | ✅ Live |
| AI coach roleplay / pitch simulator | ✅ Live (scripted) |
| Vocabulary term highlighting in chat | ✅ Live |
| REST API with Swagger UI | ✅ Live |
| Gemini AI-powered chat responses | 🔜 Phase 2 |
| User accounts & saved progress | 🔜 Phase 2 |
| Custom vocabulary bank | 🔜 Phase 2 |
| Grammar evaluation engine | 🔜 Phase 3 |
| Spaced Repetition (SRS) analytics | 🔜 Phase 4 |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Svelte + Vite → compiled to static files (`index.html` + minimal JS/CSS) |
| **Backend** | FastAPI (Python 3.11) |
| **AI Engine** | Google Gemini API (Phase 2) |
| **Database** | SQLite (dev) / PostgreSQL (production) via SQLAlchemy |
| **Container** | Docker + Docker Compose (multi-stage build) |
| **Docs** | Swagger UI (`/api/docs`), ReDoc (`/api/redoc`), Postman collection |

---

## 🗂️ Project Structure & Setup Index

Corpus groups all contributing, developer setup, and self-hosting documentation/scripts into the [setup/](file:///d:/Lantest/setup) folder to keep the root directory clean and highly organized.

### ⚙️ Setup & Contributing Folder Index

Each of these files is located inside the [setup/](file:///d:/Lantest/setup) directory:

1. **[CONTRIBUTING.md](file:///d:/Lantest/setup/CONTRIBUTING.md)**
   - Detailed guide for setting up local python environment, frontend svelte dev server, IDE python interpreter path integration (VS Code, Cursor, PyCharm), code standards, and database structure.
2. **[dependencies.toml](file:///d:/Lantest/setup/dependencies.toml)**
   - Modernized developer manifest defining backend Python dependencies (FastAPI, SQLAlchemy, etc.) and frontend packages (Svelte, Vite, Lucide icons) along with target IDE tools.
3. **[setup_venv.ps1](file:///d:/Lantest/setup/setup_venv.ps1)**
   - PowerShell script that automates creating an isolated virtual environment (`venv`), upgrading pip, and installing all package requirements on **Windows**.
4. **[setup_venv.sh](file:///d:/Lantest/setup/setup_venv.sh)**
   - Bash script that automates creating an isolated virtual environment (`venv`), upgrading pip, and installing all package requirements on **macOS/Linux**.

### 🐳 Self-Hosting & Root Assets

These files reside in the root directory for standard operations:

1. **[Dockerfile](file:///d:/Lantest/Dockerfile)**
   - Multi-stage image build instructions compiling the Svelte frontend into static assets and packaging them into the Python runtime container.
2. **[docker-compose.yml](file:///d:/Lantest/docker-compose.yml)**
   - Container orchestration config managing environment variables, volumes, ports, and healthchecks.
3. **[.env.example](file:///d:/Lantest/.env.example)**
   - Configuration template mapping database URL, secrets, and AI keys. Copy to `.env` to configure.
4. **[Makefile](file:///d:/Lantest/Makefile)**
   - Developer helper commands for building, starting services, and lint checks.
5. **[requirements.txt](file:///d:/Lantest/requirements.txt)**
   - Lockfile containing python packages list.

---

## 🚀 Quick Start

### Option A — Docker (Recommended for Self-Hosting)
Requires only Docker installed. No Node.js or Python environments required locally.

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/Corpus.git
cd Corpus

# 2. Copy and configure environment
cp .env.example .env
# Edit .env and set your GEMINI_API_KEY and SECRET_KEY

# 3. Build and run
docker compose up --build

# 4. Open http://localhost:8000
```

### Option B — Local Development & Contributors
To resolve any import warning or path detection issue, **always run within an isolated and activated Python virtual environment**.

#### 1. Automated Setup (Recommended)
Run the setup script corresponding to your operating system to automatically initialize, activate, and configure your virtual environment:

- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy Bypass -File setup/setup_venv.ps1
  ```
- **macOS / Linux (Bash):**
  ```bash
  chmod +x setup/setup_venv.sh
  ./setup/setup_venv.sh
  ```

#### 2. Manual Setup
If you prefer configuring packages step-by-step:
```bash
# Create and activate python virtual environment
python -m venv venv
venv\Scripts\Activate.ps1       # Windows PowerShell
source venv/bin/activate        # Linux / macOS

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start backend server
uvicorn backend.main:app --reload

# Start Svelte frontend (in a separate terminal)
cd frontend
npm install
npm run dev
```

> [!IMPORTANT]
> **IDE Setup**: After setting up your virtual environment, verify that your IDE (VS Code, Cursor, PyCharm) is set to use the environment's Python interpreter path (`venv/Scripts/python.exe` on Windows or `venv/bin/python` on Unix). This resolves any "Cannot find module" linter and path configuration warnings. See the **[CONTRIBUTING.md](file:///d:/Lantest/setup/CONTRIBUTING.md)** instructions for full IDE screenshots and details.

---

## 📡 API Documentation

The backend exposes a fully documented REST API.

| Method | Endpoint | Description | Status |
|---|---|---|---|
| `GET` | `/api/health` | Service liveness check | ✅ Live |
| `POST` | `/api/projects/upload` | Upload `.md` file for domain analysis | ✅ Live |
| `GET` | `/api/vocabulary/tracks` | List all learning tracks | ✅ Live |
| `GET` | `/api/vocabulary/{track_id}` | Get vocabulary for a track | ✅ Live |
| `POST` | `/api/vocabulary/custom` | Add a custom term | 🔜 Phase 2 |
| `GET` | `/api/chat/personas` | List AI coach personas | ✅ Live |
| `POST` | `/api/chat/message` | Send message, get coach reply | ✅ Live |
| `POST` | `/api/auth/register` | Create an account | 🔜 Phase 2 |
| `POST` | `/api/auth/login` | Log in, get JWT token | 🔜 Phase 2 |
| `GET` | `/api/auth/me` | Get current user profile | 🔜 Phase 2 |

### Interactive Testing
- **Swagger UI**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- **ReDoc**: [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)
- **Postman**: Import `docs/corpus_api.postman_collection.json`
- **Full Reference**: See [`docs/API.md`](./docs/API.md)

---

## 🐳 Self-Hosting

The multi-stage Dockerfile builds the Svelte frontend (Node) and bundles it directly into the Python image — users only need Docker, **no Node.js required at runtime**.

```bash
docker compose up --build -d
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./corpus_dev.db` | DB connection string |
| `SECRET_KEY` | *(change this!)* | JWT signing secret |
| `GEMINI_API_KEY` | *(empty)* | Google Gemini API key ([get one free](https://aistudio.google.com/app/apikey)) |

### Cloud Deployment

Works on any host that supports Python or Docker:
- **Railway / Render** — connect repo, set env vars, deploy
- **DigitalOcean App Platform** — Docker-based deploy
- **AWS / GCP / Azure** — use the `Dockerfile` directly

Ensure port `8000` is exposed and `DATABASE_URL` points to your production PostgreSQL instance.

---

## 🍴 Contributing

We welcome all contributions! Detailed workflows are documented in **[setup/CONTRIBUTING.md](file:///d:/Lantest/setup/CONTRIBUTING.md)**:
- Local setup guide
- Code architecture deep-dive
- How to add a new learning track
- Phase 2 implementation checklist
- PR and commit guidelines

---

## 📅 Roadmap

### ✅ Phase 1 — Foundation (Current)
- [x] Svelte + Vite static frontend with glassmorphic dark UI
- [x] FastAPI backend serving SPA + REST API
- [x] Flashcard vocabulary deck (Startup, Tech, Business)
- [x] AI coach roleplay simulator (scripted responses)
- [x] Swagger UI + ReDoc + Postman collection
- [x] Docker multi-stage self-hosting build
- [x] Modular backend route structure

### 🔜 Phase 2 — AI & Auth
- [ ] Gemini API integration for real chat replies
- [ ] JWT-based user authentication
- [ ] User progress persistence in database
- [ ] Custom vocabulary bank

### 🔜 Phase 3 — Grammar Coach
- [ ] Real-time grammar evaluation engine
- [ ] Writing correction and synonym suggestions

### 🔜 Phase 4 — Analytics & SRS
- [ ] Spaced Repetition Schedule (SRS) algorithm
- [ ] Speaking confidence analytics dashboard
- [ ] Performance reports and certificates

---

## 📄 License

MIT — free to use, fork, and self-host.
