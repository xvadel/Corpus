# Contributing to Corpus 🗣️💼

Welcome! We are excited that you want to help build **Corpus**, the AI-powered language platform for high-stakes professional communication. 

This document provides a comprehensive guide for developers, product managers, and UI designers to understand our clean architecture, set up their systems, configure their IDEs correctly, and follow standardized development workflows.

---

## 🗺️ System & Project Architecture

Corpus uses a simplified monorepo architecture designed for low-overhead self-hosting:

```
d:\Lantest
├── backend/               # FastAPI Python Server
│   ├── api/               # API Router and Endpoints (REST)
│   │   ├── __init__.py    # Central API Router Aggregator
│   │   ├── health.py      # Health Route
│   │   ├── projects.py    # Project upload/analysis routes
│   │   ├── vocabulary.py  # Terminology list tracks/custom routes
│   │   ├── chat.py        # Coach response & highlight routes
│   │   └── auth.py        # User authentication stub
│   ├── auth/              # JWT Handling and Security Utilities
│   ├── database/          # Connection Pools (SQLAlchemy models/engine)
│   ├── models/            # SQLAlchemy database tables
│   ├── prompts/           # LLM Prompt Templates
│   ├── services/          # External Integrations (Gemini API, RAG, etc.)
│   ├── static/            # Compiled static assets (created during build)
│   └── main.py            # FastAPI App initialization & route mounting
├── frontend/              # Svelte + Vite Client Application
│   ├── src/
│   │   ├── lib/           # UI Components (Splash, Onboarding, Chat, etc.)
│   │   │   └── tracks.js  # Static Track & Vocabulary configurations
│   │   ├── App.svelte     # State-based navigation router
│   │   ├── app.css        # Premium dark glassmorphic styling tokens
│   │   └── main.js        # Main Svelte mounting entry point
│   ├── package.json       # Node package configurations
│   └── vite.config.js     # Vite compiler configuration
├── corpus_data/           # Static terminology database files (.json)
├── config.toml            # Application settings and tracks configuration
├── setup/                 # Project installation, hosting, & contribution guides
│   ├── CONTRIBUTING.md    # Developer setup guide (This file)
│   ├── dependencies.toml  # Tech stack dependencies manifest
│   ├── setup_venv.ps1     # Windows automated virtual environment script
│   └── setup_venv.sh      # macOS/Linux automated virtual environment script
├── Dockerfile             # Multi-stage Docker deployment definition
├── docker-compose.yml     # Container services configuration
├── requirements.txt       # Python environment packages listing
└── Makefile               # Commands for local development and Docker
```

---

## ⚙️ Development Environment Setup

To keep your system clean and avoid version conflicts, **all python packages must be installed into an isolated local Python Virtual Environment (`venv`)**.

### Quick Automated Setup (Recommended)

We provide setup scripts to automate virtualenv creation, activation, and pip dependency installation.

**On Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File setup/setup_venv.ps1
```

**On macOS / Linux (Terminal):**
```bash
chmod +x setup/setup_venv.sh
./setup/setup_venv.sh
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
2. Go to **Project: Lantest** -> **Python Interpreter**.
3. Click the gear icon or **Add Interpreter** -> **Add Local Interpreter...**
4. Select **Existing Environment** and point the path to:
   - Windows: `venv/Scripts/python.exe`
   - macOS/Linux: `venv/bin/python`

---

## 🎨 Code & Design Standards

### 1. Frontend Styling & Theming
All UI components must adhere to the premium **dark glassmorphic** theme. Use the variables defined in `frontend/src/app.css`:
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

## 🚀 How to Extend the Application

### 1. Adding a New Language Track
To add a new professional path:
1. Update `config.toml` by appending a track dictionary:
   ```toml
   [[tracks]]
   id = "finance_analyst"
   name = "Investment Banking"
   description = "Pitch financial valuations, explain M&A models, and structure deals."
   focus_areas = ["Valuations", "Deal Structuring", "Market Reports"]
   ```
2. Update the static Javascript track configuration inside `frontend/src/lib/tracks.js` to append the corresponding visual details, icons, and vocabulary words.

### 2. Integrating a Real AI Coach (LLM Chat Integration)
Currently, the Pitch Simulator responses are simulated locally. To integrate a live LLM coach:
1. **Backend Route**: Define a chat endpoint in `backend/api/chat.py` utilizing the Google Gemini API (already installed via `google-generativeai`).
2. **Frontend Connection**: Modify `Chat.svelte` to make an async fetch call to `/api/chat/message` inside the message handler instead of relying on the local state-based responses.

---

## 🤝 Community & Contribution Workflow

1. **Issue Triaging**: Before writing code, open or assign yourself an issue on GitHub.
   - `good first issue`: Ideal for new contributors looking to get familiar with Svelte/FastAPI.
   - `bug`: Used for tracking syntax or runtime failures.
   - `feature request`: Reserved for Phase 2/3 roadmap tasks.
2. **Pull Requests**:
   - Create your branch off `develop` (e.g. `feature/live-chat-support`).
   - Run local lint checks and confirm your application compiles with `npm run build`.
   - Submit your PR with a clean title and describe what changed. Every PR requires at least one reviewer approval.
