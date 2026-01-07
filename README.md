# AIOps Evolution Platform

> **From Personal Knowledge Assistant to Autonomous DevOps Engineer**

An evolutionary AI platform designed to start as a "Second Brain" for developers and evolve into a proactive "AIOps Agent" that can diagnose and fix infrastructure issues.

## 🚀 Vision

This project follows a dual-phase evolution path:

1.  **Phase 1: The Brain (Current Focus)**
    *   **Goal**: Solve context switching and information silos.
    *   **Core**: A RAG-based assistant that understands your Code, Docs, and Preferences.
    *   **Key Feature**: **Passive Profiling** - The AI learns your tech stack and habits automatically from conversation.

2.  **Phase 2: The Nervous System (Future)**
    *   **Goal**: Autonomous Operations.
    *   **Core**: Integration with Prometheus, K8s, and Cloud APIs.
    *   **Key Feature**: **Self-Learning Loop** - Resolved incidents are automatically summarized into Post-Mortems and fed back into the Brain.

## ✨ Key Features

*   **Split-View Interface**: Chat on the left, Context/Artifacts on the right (Code previews, Docs).
*   **Active Tool Use**: The Agent doesn't just talk; it executes actions (with your permission).
*   **Hybrid Memory**:
    *   *Episodic*: Remembers past conversations (Vector DB).
    *   *Semantic*: Builds a structured profile of you (SQL).
*   **Git-Sync Knowledge Base**: Connects directly to your GitHub/GitLab repos to stay up-to-date.
*   **Human-in-the-Loop**: "Aggressive" autonomy mode, but sensitive actions always pop up an "Approve/Deny" card.

## 🛠 Tech Stack

*   **Backend**: Python 3.11+, FastAPI, LangGraph (Agent Orchestration)
*   **Frontend**: React, TailwindCSS, Vite
*   **Data**: ChromaDB (Vector), SQLite (Relational)
*   **Deployment**: Docker / K8s (Server-based architecture)

## 📂 Project Structure

```bash
.
├── backend/        # FastAPI Application & Agents
├── frontend/       # React SPA
├── docs/           # Architecture & Planning Documents
└── data/           # Persistent storage for DBs (Gitignored)
```

## 🚦 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Python 3.11+ (for local dev)
*   Node.js 18+ (for local dev)

### Quick Start (Local)

*(Coming Soon)*

## 📄 Documentation

*   [Implementation Plan](./docs/implementation_plan.md)
*   [Architecture Design](./docs/architecture_design.md)
*   [Product Requirements](./docs/requirements_prd.md)

## 🤝 Contributing

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/amazing-feature`)
3.  Commit your changes (`git commit -m 'Add some amazing feature'`)
4.  Push to the branch (`git push origin feature/amazing-feature`)
5.  Open a Pull Request

## 📜 License

[MIT](LICENSE)
