# Corpus 🗣️💼

An AI-powered, domain-specific language learning platform designed for professionals, entrepreneurs, and developers. 

Unlike general language learning tools (which focus on casual social scenarios), **Corpus** bridges the gap for professionals who need specialized vocabulary, career-specific grammar patterns, and communication confidence for high-stakes environments (e.g., pitching to venture capitalists, system design interviews, or client negotiations).

---

## 🎯 The Core Problem We Solve
Many non-native English speaking professionals possess exceptional technical skills, but face a career bottleneck due to:
* **Jargon & Terminology Gaps**: Inability to explain system architecture or financial models using standard industry jargon.
* **High-Stakes Speaking Anxiety**: Lack of practice communicating ideas in front of investors or board members.
* **Generalist Language Apps**: Existing platforms focus on ordering food or booking hotels rather than explaining market sizing, unit economics, or API design.

---

## 🚀 Key Features

* **Domain-Specific Tracks**: Tailored modules for Startup Pitching, Tech/Software Engineering, and Business Management.
* **Interactive AI Investor Roleplay**: Practice pitching your idea to simulated AI venture capitalists who ask tough questions and evaluate your responses.
* **Real-time Technical Feedback**: Instantly analyze grammar mistakes, suggest professional synonyms, and evaluate pronunciation quality.
* **Personalized Jargon Corpus**: A custom vocabulary bank where users can add their own industry-specific terms and practice them using Spaced Repetition (SRS).

---

## 📅 Roadmap & Implementation Phases

### 🛠️ Phase 1: Foundation & Setup (Current Phase)
* [x] Establish the project workspace (`d:\Lantest`).
* [x] Set up local Android SDK and Flutter SDK environments.
* [x] Draft initial dark-themed UI structure in Flutter.
* [x] Create configuration structure (`config.toml`) and root `.gitignore`.

### 📂 Phase 2: Track Selection & Vocabulary Engine
* [ ] Develop user profiling onboarding to select career paths (e.g., *Startup Pitching*).
* [ ] Build interactive dictionary & terminology flashcards.
* [ ] Implement local database (SQLite/Hive) to store the user's custom jargon corpus.

### 🤖 Phase 3: AI Language Coach & Pitch Simulator
* [ ] Integrate Google Gemini API / OpenAI API.
* [ ] Build interactive voice roleplay (Pitch Simulator) simulating Q&A with an investor.
* [ ] Create grammar evaluation engine to correct sentences in real time.

### 📊 Phase 4: Mastery Analytics & SRS
* [ ] Develop spaced repetition schedule algorithms.
* [ ] Create an analytics dashboard tracking speaking confidence, grammar accuracy, and vocabulary size.
* [ ] Generate performance reports and simulation certificates.

---

## 💻 Tech Stack
* **Framework**: Flutter (Dart) - for cross-platform Android, iOS, Windows, macOS, and Web support.
* **Environment**: Conda (`flutter_env`) for Python-based developer tooling.
* **AI Engine**: Gemini API & Local NLP models.
* **Configuration**: TOML for static app configurations.

---

## ⚙️ Development Setup

To set up the development environment locally:

### 1. Activate Environment Variables
We use Conda and local script wrappers to activate Flutter and Android SDK environment variables without polluting your global environment.

* **On Windows (PowerShell)**:
  ```powershell
  . .\activate_flutter.ps1
  ```
* **On Windows (CMD)**:
  ```cmd
  call activate_flutter.bat
  ```

### 2. Verify Installation
Run the following command to check if your Android tools and Flutter SDK are correctly configured:
```bash
flutter doctor
```

### 3. Run the App
Navigate into the `my_app` directory and launch the application:
```bash
cd my_app
flutter pub get
flutter run
```
