# Corpus 🗣️💼

> **Domain-specific language learning for high-stakes professional communication.**
> Master specialized vocabulary, pitch with confidence, and communicate like an expert in your field.

---

**Corpus** is an AI-powered, self-hostable learning platform designed to bridge the gap between technical mastery and professional communication. Unlike generic language platforms, Corpus targets the specialized vocabulary, architectural concepts, and conversational patterns needed in high-stakes professional environments—investor pitches, technical design reviews, system design interviews, and executive business alignment meetings.

---

## 🎯 Core Problem We Solve

*   **Terminology Gaps**: Technical practitioners often struggle to explain system design concepts or financial structures using correct, professional terms.
*   **High-Stakes Speaking Anxiety**: Learners lack sandbox environments to practice roleplaying critical, interactive scenarios with real-time domain vocabulary reinforcement.
*   **Generalist Scope**: Traditional language apps focus on standard conversational situations rather than domain-specific professional scenarios.

---

## ✨ Features & Architecture Highlights

### 1. Knowledge-First RAG Pipeline
Built on a deep, prerequisites-aware Ontology database of **108 concepts** across Deep Learning, NLP, RAG, Fine-Tuning, and AI Engineering. 
*   **Stage 1 Retrieval (Bi-Encoder Recall)**: Uses `BAAI/bge-small-en-v1.5` text embeddings (automatically query-prefixed for asymmetric search) to fetch the top candidate concepts from a local `ChromaDB` instance.
*   **Stage 2 Precision (Cross-Encoder Rerank)**: Reranks candidate vectors using the `BAAI/bge-reranker-base` model.

### 2. User Skill Tracking & Curriculum
*   **SQLite UserSkillModel**: Persists user interactions (success/failure) and calculates dynamic mastery levels via an **Exponential Moving Average (EMA)** algorithm.
*   **GapAnalyzer Curriculum Engine**: Performs topological sorting over prerequisite concepts to generate personalized learning paths based on the gaps in the user's active skill model.

### 3. AI Coach Simulator
Provides interactive domain-specific roleplay coaches:
*   **Alex Mercer** (Startup & VC Partner): Financial pitches, runway, and valuations.
*   **Sarah Connor** (Principal Software Architect): Low-latency designs, scaling, and technical debt.
*   **Dr. Evelyn Vance** (Lead AI Architect): Document chunking, embeddings, and RAG architectures.
*   **Michael Vance** (Product Management Director): KPI alignment, Q3 roadmap, and churn rate.

---

## 📊 Retrieval Performance Metrics

Our evaluation benchmark (evaluating 60 complex queries across Easy, Medium, and Hard tiers) shows a massive retrieval recall and precision uplift:

| Metric | Vector Only | Vector + Cross-Encoder Rerank | Delta |
| :--- | :---: | :---: | :---: |
| **Recall@1** | 56.7% | **70.0%** | **+13.3%** |
| **Recall@3** | 68.3% | **83.3%** | **+15.0%** |
| **Recall@5** | 75.0% | **86.7%** | **+11.7%** |
| **Mean Reciprocal Rank (MRR)** | 0.6411 | **0.7659** | **+0.1248** |

---

## 🏗️ Technical Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | Svelte 5 + TypeScript + Vite + Tailwind CSS |
| **Backend** | FastAPI (Python 3.11+) + Uvicorn |
| **Database** | SQLite + ChromaDB (Vector Store) |
| **AI Models** | Groq (Llama 3.3 70B), SentenceTransformers (`bge-small-en-v1.5` & `bge-reranker-base`) |
| **Testing** | Pytest |
| **Containerization** | Docker + Docker Compose |

---

## 📁 Repository Structure & Setup Guides

*   **[infrastructure/setup/CONTRIBUTING.md](file:///d:/Corpus/infrastructure/setup/CONTRIBUTING.md)**: Developer guide mapping python interpreter configurations, code standards, and PR workflows.
*   **[infrastructure/setup/dependencies.toml](file:///d:/Corpus/infrastructure/setup/dependencies.toml)**: System dependencies manifest for Python backend and Svelte frontend.
*   **[docs/API.md](file:///d:/Corpus/docs/API.md)**: Standard REST API specifications.
*   **[docs/concept_schema.md](file:///d:/Corpus/docs/concept_schema.md)**: Ontology JSON document schemas.

---

## 🚀 Quick Start

### Option A: Running via Docker (Recommended for Self-Hosting)
Requires only Docker and Docker Compose installed.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/Corpus.git
cd Corpus

# 2. Configure environment variables
cp .env.example .env
# Edit .env and supply your GROQ_API_KEY (and optionally GEMINI_API_KEY)

# 3. Spin up the containers
docker compose up --build
# Open http://localhost:8000
```

### Option B: Local Development (For Contributors)

#### 1. Backend Environment Setup
Create and configure an isolated virtual environment (`venv`) to resolve import pathways:

*   **Windows (PowerShell)**:
    ```powershell
    powershell -ExecutionPolicy Bypass -File infrastructure/setup/setup_venv.ps1
    ```
*   **macOS / Linux (Terminal)**:
    ```bash
    chmod +x infrastructure/setup/setup_venv.sh
    ./infrastructure/setup/setup_venv.sh
    ```

#### 2. Run the Servers
*   **Activate Environment and Start FastAPI Backend**:
    ```bash
    # Windows
    venv\Scripts\Activate.ps1
    # Unix
    source venv/bin/activate

    uvicorn backend.main:app --reload --port 8000
    ```
*   **Start the Frontend Svelte Dev Server**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
    Open [http://localhost:5173/](http://localhost:5173/) to see your hot-reloaded changes.

---

## 🔬 Testing & Validation

Run unit tests and verify code compliance:

```bash
# Run backend unit tests
venv\Scripts\pytest tests/

# Re-build and validate ontology graphs
python scripts/build_knowledge_graph.py

# Run retrieval benchmark metrics
python backend/evaluation/benchmark_runner.py
```

---

## 📄 License

Corpus is open-source software licensed under the [MIT License](LICENSE).
