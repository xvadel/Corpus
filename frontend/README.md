# Corpus — Svelte Frontend Client

This directory contains the Svelte client application for **Corpus**, the domain-specific language learning platform.

It is built using **Svelte 5**, **TypeScript**, **Tailwind CSS**, and **Vite** for rapid hot-module-reloading (HMR) during development. The output compiles down to zero-dependency static assets (`index.html`, `index.js`, `index.css`) which are served directly by the FastAPI backend.

---

## 🛠️ Project Tech Stack

*   **UI Framework**: Svelte 5 (using runes for reactive state management)
*   **Compiler/Bundler**: Vite + Svelte Plugin
*   **Styling**: Vanilla CSS (Tailwind CSS 4.0 configuration)
*   **Icons**: Lucide Svelte
*   **Typography**: Google Fonts — *Outfit* (headers) and *Inter* (content)
*   **Design Language**: Glassmorphic dark UI

---

## 🚀 Getting Started

### Prerequisites

*   **Node.js**: `>= 20.0.0`
*   **npm**: `>= 9.0.0`

### 1. Install Dependencies

Navigate into the `frontend` directory and install JavaScript packages:

```bash
cd frontend
npm install
```

### 2. Launch Local Development Server

Run the Vite development server with hot-module-reloading:

```bash
npm run dev
```

The app will be available at [http://localhost:5173/](http://localhost:5173/).

> **Note**: During local development, API requests are proxied from the Svelte client to the FastAPI backend running on port `8000`.

### 3. Compile Static Production Build

To compile the application into static files:

```bash
npm run build
```

This compiles your code into the `dist/` directory.

### 4. Syncing Assets with the Backend

FastAPI serves the Svelte single-page application (SPA) from the `backend/static/` folder. Sync compiled files after running a build:

```bash
# Windows PowerShell
Copy-Item -Path .\dist\* -Destination ..\backend\static -Recurse -Force

# Linux / macOS
cp -r ./dist/* ../backend/static/
```

---

## 📁 Directory Structure

```text
frontend/
├── src/
│   ├── lib/              # UI Components (Splash, Onboarding, Chat, etc.)
│   │   ├── components/   # Sub-components (Cards, Buttons, Inputs)
│   │   └── tracks.js     # Static visual tracks configuration
│   ├── App.svelte        # State-based UI router & main layout
│   ├── app.css           # Global CSS variables, fonts, and Tailwind directives
│   └── main.ts           # Svelte mount entry point
├── package.json          # Dependency definition
├── tsconfig.json         # TypeScript compiler configurations
└── vite.config.ts        # Vite configuration (assets routing, server proxy)
```

---

## 💻 Recommended Developer Setup

1.  **IDE**: VS Code or Cursor.
2.  **Extensions**:
    *   `svelte.svelte-vscode` — Official Svelte support.
    *   `dbaeumer.vscode-eslint` — Linting configuration.
    *   `bradlc.vscode-tailwindcss` — Tailwind CSS autocomplete.
