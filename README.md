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
*   **Long-Term Memory Governance**: write triggers, recall priority, lifecycle, and approval workflow.
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

## ✅ Test Flow (MVP)

1) Start backend: `uvicorn app.main:app --reload`  
2) Ingest text:
```
curl -X POST http://localhost:8000/api/v1/ingest/text ^
  -H "Content-Type: application/json" ^
  -d "{\"source\":\"docs/demo.md\",\"content\":\"AIOps is about monitoring and automation.\"}"
```
3) Hybrid retrieval:
```
curl -X POST http://localhost:8000/api/v1/retrieve/hybrid ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"monitoring automation\",\"top_k\":5}"
```
Note: the current embedding is a lightweight placeholder for pipeline validation only.
4) Memory record/recall:
```
curl -X POST http://localhost:8000/api/v1/memory/record ^
  -H "Content-Type: application/json" ^
  -d "{\"type\":\"semantic\",\"key\":\"preferred_language\",\"value\":\"Python\"}"

curl -X POST http://localhost:8000/api/v1/memory/recall ^
  -H "Content-Type: application/json" ^
  -d "{\"type\":\"semantic\",\"query\":\"preferred\",\"limit\":5}"
```
5) Retrieval evaluation:
```
curl -X POST http://localhost:8000/api/v1/evaluate/retrieval ^
  -H "Content-Type: application/json" ^
  -d "{\"items\":[{\"query\":\"monitoring\",\"expected\":\"automation\"}],\"top_k\":5}"
```
6) LangGraph Agent run:
```
curl -X POST http://localhost:8000/api/v1/agent/run ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"What is the core of AIOps?\",\"top_k\":5}"
```

## 🧪 UI Integration (Local test page)

```
cd frontend
python -m http.server 5173
```
Open `http://localhost:5173` in your browser to test ingest/retrieve/memory/evaluation.

## 📄 Documentation

*   [Implementation Plan](./docs/实施计划.md)
*   [Architecture Design](./docs/架构设计.md)
*   [Product Requirements](./docs/产品需求.md)
*   [Context Memory Engineering](./docs/形成上下文记忆工程.md)
*   [AIOps Ops Template](./docs/AIOps运维模板.md)

## 🤝 Contributing

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/amazing-feature`)
3.  Commit your changes (`git commit -m 'Add some amazing feature'`)
4.  Push to the branch (`git push origin feature/amazing-feature`)
5.  Open a Pull Request

## 📜 License

[MIT](LICENSE)
