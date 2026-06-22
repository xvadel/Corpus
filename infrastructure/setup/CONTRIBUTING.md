# Contributing to Corpus 🗣️💼

Welcome! We are excited that you want to help build **Corpus**, the AI-powered language platform for high-stakes professional communication. 

This document provides a comprehensive guide for developers, AI engineers, and UI designers to understand our clean architecture, set up their systems, configure their IDEs correctly, and follow standardized development workflows.

---

## 🗺️ System & Project Architecture

Corpus uses a simplified monorepo architecture designed for low-overhead self-hosting:

```text
d:\Corpus
├── backend/               # FastAPI Python Server
│   ├── api/               # API Router and Endpoints (REST)
│   │   ├── __init__.py    # Central API Router Aggregator
│   │   ├── health.py      # Health Route
│   │   ├── projects.py    # Project upload/analysis routes
│   │   ├── vocabulary.py  # Terminology list tracks/custom routes
│   │   └── chat.py        # Coach response & highlight routes
│   ├── auth/              # JWT Handling and Security Utilities
│   ├── curriculum/        # Curriculum Engine (GapAnalyzer, topological sorting)
│   ├── database/          # Connection Pools (SQLAlchemy models/engine)
│   ├── evaluation/        # Benchmark Runner, queries, and metrics
│   ├── models/            # SQLAlchemy database tables
│   ├── prompts/           # Prompt templates and PromptRegistry
│   ├── providers/         # LLM Provider Abstractions (Gemini, Groq, OpenAI)
│   ├── retrieval/         # VectorRetriever & CrossEncoderReranker
│   ├── static/            # Compiled static assets (created during build)
│   ├── user_model/        # SQLite UserSkillModel with EMA mastery tracking
│   └── main.py            # FastAPI App initialization & route mounting
├── frontend/              # Svelte + Vite Client Application (TS + Tailwind)
│   ├── src/
│   │   ├── lib/           # UI Components (Splash, Onboarding, Chat, etc.)
│   │   │   └── tracks.js  # Static Track & Vocabulary configurations
│   │   ├── App.svelte     # State-based navigation router
│   │   ├── app.css        # Premium dark glassmorphic styling tokens
│   │   └── main.ts        # Main Svelte mounting entry point
│   ├── package.json       # Node package configurations
│   ├── tsconfig.json      # TypeScript compiler configuration
│   └── vite.config.ts     # Vite compiler configuration with Tailwind plugin
├── corpus_data/           # Static terminology & concepts database files (.json)
├── config.toml            # Application settings and tracks configuration
├── infrastructure/        # Project installation, hosting, & contribution guides
│   └── setup/
│       ├── CONTRIBUTING.md    # Developer setup guide (This file)
│       ├── dependencies.toml  # Tech stack dependencies manifest
│       ├── setup_venv.ps1     # Windows automated virtual environment script
│       └── setup_venv.sh      # macOS/Linux automated virtual environment script
├── Dockerfile             # Multi-stage Docker deployment definition
├── docker-compose.yml     # Container services configuration
├── requirements.txt       # Python environment packages listing
├── Makefile               # Commands for local development and Docker
├── tests/                 # Full unit and integration test suite
└── scripts/               # Utility scripts (indexing, ontology graph, enrichment)
```

---

## ⚙️ Development Environment Setup

To keep your system clean and avoid version conflicts, **all python packages must be installed into an isolated local Python Virtual Environment (`venv`)**.

### Quick Automated Setup (Recommended)

We provide setup scripts to automate virtualenv creation, activation, and pip dependency installation.

**On Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File infrastructure/setup/setup_venv.ps1
```

**On macOS / Linux (Terminal):**
```bash
chmod +x infrastructure/setup/setup_venv.sh
./infrastructure/setup/setup_venv.sh
```

---

### Manual Setup Instructions

If you prefer to configure the environment manually, run the following steps:

#### 1. Setup the Backend Environment
Create a virtual environment, activate it, and install python libraries:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
venv\Scripts\Activate.ps1

# Activate (Windows Command Prompt)
venv\Scripts\activate.bat

# Activate (Linux/macOS Terminal)
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2. Setup the Frontend
Start a separate terminal session for Svelte development:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` to see hot-reloading code changes in your browser.

#### 3. Compile static production build
When you are ready to prepare files for FastAPI serving:
```bash
# Inside frontend directory
npm run build

# Copy build outputs to backend/static (Windows PowerShell Example)
Copy-Item -Path .\dist\* -Destination ..\backend\static -Recurse -Force
```

---

## 🔧 Solving IDE Import & Linter Issues (e.g. `Cannot find module backend...`)

If your IDE shows errors or red squiggly lines like `Cannot find module backend.api...` or `Could not find name...`, this means your IDE is running on a global Python interpreter (like Miniconda or system python) instead of your activated `venv`.

Follow these quick steps to register the virtual environment inside your IDE:

### 1. VS Code / Cursor
1. Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS) to open the Command Palette.
2. Search for and select: **`Python: Select Interpreter`**
3. Select **`Enter interpreter path...`** -> **`Find...`**
4. Browse to the project folder, locate the virtual environment executable, and click select:
   - Windows: `venv/Scripts/python.exe`
   - macOS/Linux: `venv/bin/python`
5. Restart your terminal session within the IDE so it loads the active venv.

### 2. PyCharm
1. Open **Settings** (`Ctrl + Alt + S` or `Cmd + ,` on macOS).
2. Go to **Project: Corpus** -> **Python Interpreter**.
3. Click the gear icon or **Add Interpreter** -> **Add Local Interpreter...**
4. Select **Existing Environment** and point the path to:
   - Windows: `venv/Scripts/python.exe`
   - macOS/Linux: `venv/bin/python`

---

## 🔬 Core RAG & Knowledge Layer Architecture

Corpus is an evaluation-driven platform built on a strict, modular knowledge-first structure:

### 1. The Concepts Database
All 108 concepts in Deep Learning, RAG, NLP, Fine-Tuning, and AI Engineering reside in `corpus_data/concepts/*.json`. Each file contains details like prereqs, related terms, definitions, and explanations.

### 2. Two-Stage Retrieval
*   **Stage 1: Bi-Encoder Recall**: Under `backend/retrieval/retriever.py`, `VectorRetriever` queries a local `ChromaDB` instance using `BAAI/bge-small-en-v1.5` embeddings (which are query-prefixed with search instructions).
*   **Stage 2: Cross-Encoder Precision**: Candidates are reranked using `CrossEncoderReranker` running `BAAI/bge-reranker-base`.

### 3. User Skill & Curriculum Engine
*   **UserSkillModel**: Stores concept interaction outcomes (success/fail) in a SQLite database and computes an Exponential Moving Average (EMA) mastery score (mastery threshold = `0.80`).
*   **Curriculum Engine**: Uses topological sorting to recommend learning paths, comparing concepts the user has already mastered (`GapAnalyzer`) with overall prerequisites.

---

## 🧪 Testing and CI

Always run local validation before creating a pull request:

### 1. Run Unit Tests
Use Pytest to assert correctness of retrieval, curriculum, schemas, and user skill model tracking:
```bash
venv\Scripts\pytest tests/
```

### 2. Re-Build Knowledge Graph
Ensure that dependencies don't form a cyclic loop:
```bash
venv\Scripts\python.exe scripts/build_knowledge_graph.py
```

### 3. Run Benchmark Runner
Run standard precision and recall evaluations on your retrieval changes:
```bash
venv\Scripts\python.exe backend/evaluation/benchmark_runner.py
```

---

## 🎨 Code & Design Standards

### 1. Frontend Styling & Theming
All UI components must adhere to the premium **dark glassmorphic** theme. Use the variables defined in `frontend/src/app.css` and incorporate Tailwind CSS utility classes.
- **Main Background**: `#0A0E21` (Dark Navy)
- **Secondary Card Background**: `#1C2043`
- **Glass Utility class**:
  ```css
  .glass {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
  }
  ```
- **Typography**: Always use Google Font `Outfit` for headers and `Inter` for content and inputs.

### 2. Backend Coding Standards
- **REST Endpoints**: All API paths must begin with `/api/` (e.g. `/api/projects/upload`) to separate them from static frontend routes.
- **Type Hinting**: All python function signatures must contain complete type definitions.
  ```python
  async def upload_project(file: UploadFile = File(...)) -> Dict[str, Any]:
  ```
- **Pydantic Validation**: Use Pydantic schemas in `backend/models` for request validation and response formatting.

---

## 🤝 Community & Contribution Workflow

1. **Pull Requests**:
   - Create your branch off `main`/`master` (e.g., `feature/live-chat-support`).
   - Run local unit tests and confirm your application compiles with `npm run build`.
   - Submit your PR with a clean title and describe what changed. Every PR triggers the GitHub Actions CI pipeline in `.github/workflows/ci.yml`.
